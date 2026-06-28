import importlib.util
import io
import json
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

import pytest

ROOT = Path(__file__).parents[3]


def load_hook() -> ModuleType:
    path = ROOT / ".codex" / "hooks" / "post_tool_use_hygiene.py"
    spec = importlib.util.spec_from_file_location("codex_post_tool_use_hygiene", path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


HOOK = load_hook()


def invoke_main(payload: object, root: Path, run_results: list[tuple[int, str, str]]) -> tuple[int, str, list[list[str]]]:
    stdin = io.StringIO(json.dumps(payload))
    stdout = io.StringIO()
    commands: list[list[str]] = []
    results = iter(run_results)

    def fake_run(_root: Path, args: list[str]) -> tuple[int, str, str]:
        commands.append(args)
        return next(results)

    with (
        patch.object(HOOK.sys, "stdin", stdin),
        patch.object(HOOK.sys, "stdout", stdout),
        patch.object(HOOK, "repo_root", return_value=root),
        patch.object(HOOK, "run", side_effect=fake_run),
    ):
        exit_code = HOOK.main()

    return exit_code, stdout.getvalue(), commands


def test_valid_json_with_clean_markdown_produces_no_output(tmp_path: Path) -> None:
    target = tmp_path / "docs" / "sample.md"
    target.parent.mkdir()
    target.write_text("clean\n", encoding="utf-8")
    payload = {"cwd": str(tmp_path), "tool_name": "apply_patch", "tool_input": {"file_path": str(target)}}

    exit_code, output, commands = invoke_main(payload, tmp_path, [(0, "", "")])

    assert exit_code == 0
    assert output == ""
    assert commands == [["uv", "run", "python", "scripts/file_hygiene.py", "--file", "docs/sample.md"]]


def test_apply_patch_uses_patch_paths_instead_of_dirty_worktree(tmp_path: Path) -> None:
    target = tmp_path / "docs" / "target.md"
    dirty = tmp_path / "docs" / "dirty.md"
    target.parent.mkdir()
    target.write_text("clean\n", encoding="utf-8")
    dirty.write_text("unrelated\n", encoding="utf-8")
    patch_text = """*** Begin Patch
*** Update File: docs/target.md
@@
-old
+clean
*** End Patch
"""
    payload = {"cwd": str(tmp_path), "tool_name": "apply_patch", "tool_input": {"cmd": patch_text}}

    exit_code, output, commands = invoke_main(payload, tmp_path, [(0, "", "")])

    assert exit_code == 0
    assert output == ""
    assert commands == [["uv", "run", "python", "scripts/file_hygiene.py", "--file", "docs/target.md"]]


def test_failed_check_returns_codex_blocking_json(tmp_path: Path) -> None:
    target = tmp_path / "docs" / "sample.md"
    target.parent.mkdir()
    target.write_text("bad\n", encoding="utf-8")
    payload = {"cwd": str(tmp_path), "tool_name": "Write", "tool_input": {"file_path": str(target)}}

    exit_code, output, _commands = invoke_main(payload, tmp_path, [(1, "", "invalid content")])

    assert exit_code == 0
    assert json.loads(output) == {
        "systemMessage": "`file_hygiene` failed on `docs/sample.md`.\ninvalid content",
        "continue": False,
        "stopReason": "Codex post-edit hygiene check failed.",
    }


def test_python_print_failure_returns_blocking_json(tmp_path: Path) -> None:
    target = tmp_path / "src" / "sample.py"
    target.parent.mkdir()
    target.write_text("print('hello')\n", encoding="utf-8")
    payload = {"cwd": str(tmp_path), "tool_name": "Edit", "tool_input": {"file_path": str(target)}}
    run_results = [
        (0, "", ""),
        (1, "T201 `print` found", ""),
        (0, "", ""),
    ]

    exit_code, output, commands = invoke_main(payload, tmp_path, run_results)

    assert exit_code == 0
    assert json.loads(output) == {
        "systemMessage": "`ruff check --fix` failed on `src/sample.py`.\nT201 `print` found",
        "continue": False,
        "stopReason": "Codex post-edit hygiene check failed.",
    }
    assert commands == [
        ["uv", "run", "ruff", "format", "src/sample.py"],
        ["uv", "run", "ruff", "check", "--fix", "src/sample.py"],
        ["uv", "run", "python", "scripts/file_hygiene.py", "--file", "src/sample.py"],
    ]


@pytest.mark.parametrize("path_style", ["backslash", "forward-slash"])
def test_windows_path_input_becomes_repo_relative_cli_argument(tmp_path: Path, path_style: str) -> None:
    target = tmp_path / "docs" / "windows.md"
    target.parent.mkdir()
    target.write_text("clean\n", encoding="utf-8")
    windows_path = str(target).replace("/", "\\") if path_style == "backslash" else target.as_posix()
    payload = {"cwd": str(tmp_path), "tool_input": {"file_path": windows_path}}

    _exit_code, _output, commands = invoke_main(payload, tmp_path, [(0, "", "")])

    assert commands[-1][-1] == "docs/windows.md"


def test_tool_without_file_path_falls_back_to_changed_files(tmp_path: Path) -> None:
    # When no file_path or patch header is found, the hook falls back to
    # changed_files() so hygiene still runs if the JSON format is unexpected.
    dirty = tmp_path / "docs" / "unrelated.md"
    dirty.parent.mkdir()
    dirty.write_text("unrelated\n", encoding="utf-8")
    payload = {"cwd": str(tmp_path), "tool_name": "shell", "tool_input": {"command": "echo hi"}}

    with patch.object(HOOK, "changed_files", return_value=["docs/unrelated.md"]):
        exit_code, output, commands = invoke_main(payload, tmp_path, [(0, "", "")])

    assert exit_code == 0
    assert output == ""
    assert commands == [["uv", "run", "python", "scripts/file_hygiene.py", "--file", "docs/unrelated.md"]]


@pytest.mark.parametrize("raw_input", ["", "{not-json"])
def test_invalid_json_is_ignored_without_output(raw_input: str) -> None:
    stdin = io.StringIO(raw_input)
    stdout = io.StringIO()

    with patch.object(HOOK.sys, "stdin", stdin), patch.object(HOOK.sys, "stdout", stdout):
        exit_code = HOOK.main()

    assert exit_code == 0
    assert stdout.getvalue() == ""
