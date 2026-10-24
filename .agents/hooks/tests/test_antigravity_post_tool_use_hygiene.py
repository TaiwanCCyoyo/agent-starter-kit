import importlib.util
import io
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

import pytest

ROOT = Path(__file__).parents[3]


def load_hook() -> ModuleType:
    path = ROOT / ".agents" / "hooks" / "antigravity_post_tool_use_hygiene.py"
    spec = importlib.util.spec_from_file_location("antigravity_post_tool_use_hygiene", path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


HOOK = load_hook()


def invoke_main(payload: object, root: Path, run_results: list[tuple[int, str, str]]) -> tuple[int, str, str, list[list[str]]]:
    stdin = io.StringIO(json.dumps(payload))
    stdout = io.StringIO()
    stderr = io.StringIO()
    commands: list[list[str]] = []
    results = iter(run_results)

    def fake_run(_root: Path, args: list[str]) -> tuple[int, str, str]:
        commands.append(args)
        return next(results)

    def fake_repo_root(cwd: str) -> Path:
        candidate = Path(cwd)
        if candidate.is_dir():
            return candidate.resolve()
        return root

    with (
        patch.object(HOOK.sys, "stdin", stdin),
        patch.object(HOOK.sys, "stdout", stdout),
        patch.object(HOOK.sys, "stderr", stderr),
        patch.object(HOOK, "repo_root", side_effect=fake_repo_root),
        patch.object(HOOK, "run", side_effect=fake_run),
    ):
        exit_code = HOOK.main()

    return exit_code, stdout.getvalue(), stderr.getvalue(), commands


def expected_command(root: Path, rel_path: str) -> list[str]:
    return [
        "uv",
        "run",
        "--no-sync",
        "--project",
        str(root),
        "ruff",
        "check",
        "--no-fix",
        "--select",
        "F",
        "--ignore",
        "F401,F841,F842",
        "--output-format",
        "concise",
        "--",
        rel_path,
    ]


def test_edit_file_python_target_runs_read_only_ruff_check(tmp_path: Path) -> None:
    target = tmp_path / "src" / "sample.py"
    target.parent.mkdir()
    target.write_text("value = 1\n", encoding="utf-8")
    payload = {
        "workspacePaths": [str(tmp_path)],
        "toolCall": {"name": "edit_file", "args": {"Path": str(target)}},
    }

    exit_code, stdout, stderr, commands = invoke_main(payload, tmp_path, [(0, "", "")])

    assert exit_code == 0
    assert json.loads(stdout) == {}
    assert stderr == ""
    assert commands == [expected_command(tmp_path, "src/sample.py")]


def test_ruff_failure_logs_diagnostics_and_emits_empty_json_stdout(tmp_path: Path) -> None:
    target = tmp_path / "src" / "sample.py"
    target.parent.mkdir()
    target.write_text("value = missing_name\n", encoding="utf-8")
    payload = {
        "workspacePaths": [str(tmp_path)],
        "toolCall": {"name": "write_file", "args": {"Path": str(target)}},
    }

    exit_code, stdout, stderr, _commands = invoke_main(payload, tmp_path, [(1, "F821 undefined name", "")])

    assert exit_code == 0
    assert json.loads(stdout) == {}
    assert "Post-edit Ruff diagnostics; fix relevant issues before completion." in stderr
    assert "F821 undefined name" in stderr


def test_non_python_edit_is_ignored(tmp_path: Path) -> None:
    target = tmp_path / "docs" / "sample.md"
    target.parent.mkdir()
    target.write_text("content\n", encoding="utf-8")
    payload = {
        "workspacePaths": [str(tmp_path)],
        "toolCall": {"name": "write_file", "args": {"Path": str(target)}},
    }

    exit_code, stdout, stderr, commands = invoke_main(payload, tmp_path, [])

    assert exit_code == 0
    assert json.loads(stdout) == {}
    assert stderr == ""
    assert commands == []


def test_multi_file_args_runs_one_check_on_only_existing_in_repo_python_files(tmp_path: Path) -> None:
    for name in ("one.py", "two.py", "notes.md"):
        (tmp_path / name).write_text("", encoding="utf-8")
    outside = tmp_path.parent / "outside.py"
    outside.write_text("", encoding="utf-8")
    payload = {
        "workspacePaths": [str(tmp_path)],
        "toolCall": {
            "name": "edit_file",
            "args": {
                "Paths": [
                    str(tmp_path / "one.py"),
                    str(tmp_path / "two.py"),
                    str(tmp_path / "one.py"),
                    str(tmp_path / "notes.md"),
                    str(tmp_path / "gone.py"),
                    str(outside),
                ]
            },
        },
    }

    _code, stdout, stderr, commands = invoke_main(payload, tmp_path, [(0, "", "")])

    assert json.loads(stdout) == {}
    assert stderr == ""
    assert commands == [expected_command(tmp_path, "one.py") + ["two.py"]]


def test_entrypoint_reports_real_ruff_failure_without_applying_configured_fixes(tmp_path: Path) -> None:
    subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
    (tmp_path / "ruff.toml").write_text("fix = true\nunsafe-fixes = true\n", encoding="utf-8")
    target = tmp_path / "sample.py"
    source = 'value = missing_name\ndata = {"key": 1, "key": 2}\n'
    target.write_text(source, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(ROOT / ".agents/hooks/antigravity_post_tool_use_hygiene.py")],
        cwd=ROOT,
        input=json.dumps({
            "workspacePaths": [str(tmp_path)],
            "toolCall": {"name": "edit_file", "args": {"Path": str(target)}},
        }),
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )

    assert json.loads(result.stdout) == {}
    assert "F821" in result.stderr
    assert target.read_text(encoding="utf-8") == source


def test_linter_timeout_returns_actionable_diagnostic(tmp_path: Path) -> None:
    with patch.object(HOOK.subprocess, "run", side_effect=subprocess.TimeoutExpired("ruff", 15)) as run:
        code, stdout, stderr = HOOK.run(tmp_path, ["ruff", "check", "sample.py"])

    assert code == 124
    assert stdout == ""
    assert "exceeded 15 seconds" in stderr
    assert run.call_args.kwargs["timeout"] == 15


@pytest.mark.parametrize("raw_input", ["", "{not-json"])
def test_invalid_json_is_ignored(raw_input: str) -> None:
    stdin = io.StringIO(raw_input)
    stdout = io.StringIO()

    with patch.object(HOOK.sys, "stdin", stdin), patch.object(HOOK.sys, "stdout", stdout):
        exit_code = HOOK.main()

    assert exit_code == 0
    assert stdout.getvalue() == ""


@pytest.mark.parametrize("path_style", ["backslash", "forward-slash", "quoted-backslash"])
def test_windows_path_input_becomes_repo_relative_argument(tmp_path: Path, path_style: str) -> None:
    target = tmp_path / "src" / "windows.py"
    target.parent.mkdir()
    target.write_text("value = 1\n", encoding="utf-8")
    if path_style == "backslash":
        file_path = str(target).replace("/", "\\")
    elif path_style == "quoted-backslash":
        file_path = json.dumps(str(target).replace("/", "\\"))
    else:
        file_path = target.as_posix()
    payload = {
        "workspacePaths": [str(tmp_path)],
        "toolCall": {"name": "edit_file", "args": {"Path": file_path}},
    }

    _exit_code, _stdout, _stderr, commands = invoke_main(payload, tmp_path, [(0, "", "")])

    assert commands == [expected_command(tmp_path, "src/windows.py")]


def test_second_workspace_python_target_runs_ruff_in_matching_workspace(tmp_path: Path) -> None:
    first_ws = tmp_path / "ws-one"
    second_ws = tmp_path / "ws-two"
    first_ws.mkdir()
    target = second_ws / "pkg" / "module.py"
    target.parent.mkdir(parents=True)
    target.write_text("value = missing_symbol\n", encoding="utf-8")
    payload = {
        "workspacePaths": [str(first_ws), str(second_ws)],
        "toolCall": {"name": "edit_file", "args": {"Path": str(target)}},
    }

    exit_code, stdout, stderr, commands = invoke_main(payload, first_ws, [(1, "F821 undefined name `missing_symbol`", "")])

    assert exit_code == 0
    assert json.loads(stdout) == {}
    assert "F821 undefined name `missing_symbol`" in stderr
    assert commands == [expected_command(second_ws.resolve(), "pkg/module.py")]


def test_nested_workspace_prefers_most_specific_workspace_root(tmp_path: Path) -> None:
    outer_ws = tmp_path / "outer"
    inner_ws = outer_ws / "inner"
    target = inner_ws / "src" / "nested.py"
    target.parent.mkdir(parents=True)
    target.write_text("value = 1\n", encoding="utf-8")
    payload = {
        "workspacePaths": [str(outer_ws), str(inner_ws)],
        "toolCall": {"name": "edit_file", "args": {"Path": str(target)}},
    }

    exit_code, stdout, stderr, commands = invoke_main(payload, outer_ws, [(0, "", "")])

    assert exit_code == 0
    assert json.loads(stdout) == {}
    assert stderr == ""
    assert commands == [expected_command(inner_ws.resolve(), "src/nested.py")]


def test_unknown_payload_does_not_scan_unrelated_dirty_files(tmp_path: Path) -> None:
    dirty = tmp_path / "src" / "unrelated.py"
    dirty.parent.mkdir()
    dirty.write_text("value = 1\n", encoding="utf-8")
    payload = {
        "workspacePaths": [str(tmp_path)],
        "toolCall": {"name": "run_command", "args": {"CommandLine": "echo hi"}},
    }

    exit_code, stdout, stderr, commands = invoke_main(payload, tmp_path, [])

    assert exit_code == 0
    assert json.loads(stdout) == {}
    assert stderr == ""
    assert commands == []
