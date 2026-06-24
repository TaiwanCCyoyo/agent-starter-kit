import importlib.util
import io
import json
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

import pytest

ROOT = Path(__file__).parents[3]


def load_hook() -> ModuleType:
    path = ROOT / ".claude" / "hooks" / "post_tool_use_hygiene.py"
    spec = importlib.util.spec_from_file_location("claude_post_tool_use_hygiene", path)
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
    payload = {"cwd": str(tmp_path), "tool_name": "Write", "tool_input": {"file_path": str(target)}}

    exit_code, output, commands = invoke_main(payload, tmp_path, [(0, "", "")])

    assert exit_code == 0
    assert output == ""
    assert commands == [["uv", "run", "python", "scripts/file_hygiene.py", "--file", "docs/sample.md"]]


def test_failed_check_returns_claude_blocking_json(tmp_path: Path) -> None:
    target = tmp_path / "docs" / "sample.md"
    target.parent.mkdir()
    target.write_text("bad\n", encoding="utf-8")
    payload = {"cwd": str(tmp_path), "tool_name": "Write", "tool_input": {"file_path": str(target)}}

    exit_code, output, _commands = invoke_main(payload, tmp_path, [(1, "", "invalid content")])

    assert exit_code == 0
    assert json.loads(output) == {
        "decision": "block",
        "reason": "`file_hygiene` failed on `docs/sample.md`.\ninvalid content",
    }


def test_python_print_failure_returns_blocking_json(tmp_path: Path) -> None:
    target = tmp_path / "src" / "sample.py"
    target.parent.mkdir()
    target.write_text("print('hello')\n", encoding="utf-8")
    payload = {"cwd": str(tmp_path), "tool_name": "Edit", "tool_input": {"file_path": str(target)}}
    run_results = [
        (0, "", ""),  # ruff format
        (1, "T201 `print` found", ""),  # ruff check --fix
        (0, "", ""),  # file_hygiene
    ]

    exit_code, output, commands = invoke_main(payload, tmp_path, run_results)

    assert exit_code == 0
    assert json.loads(output) == {
        "decision": "block",
        "reason": "`ruff check --fix` failed on `src/sample.py`.\nT201 `print` found",
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


@pytest.mark.parametrize("raw_input", ["", "{not-json"])
def test_invalid_json_is_ignored_without_output(raw_input: str) -> None:
    stdin = io.StringIO(raw_input)
    stdout = io.StringIO()

    with patch.object(HOOK.sys, "stdin", stdin), patch.object(HOOK.sys, "stdout", stdout):
        exit_code = HOOK.main()

    assert exit_code == 0
    assert stdout.getvalue() == ""
