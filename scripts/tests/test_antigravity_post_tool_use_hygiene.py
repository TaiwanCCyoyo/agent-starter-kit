import importlib.util
import io
import json
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

import pytest

ROOT = Path(__file__).parents[2]


def load_hook() -> ModuleType:
    path = ROOT / ".agent" / "hooks" / "post_tool_use_hygiene.py"
    spec = importlib.util.spec_from_file_location("antigravity_post_tool_use_hygiene", path)
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


def expected_command(root: Path, rel_path: str) -> list[str]:
    return [
        "uv",
        "run",
        "--project",
        str(root),
        "ruff",
        "check",
        "--no-fix",
        "--select",
        "E722,F601,F602,F634",
        "--output-format",
        "concise",
        rel_path,
    ]


def test_clean_python_edit_runs_only_read_only_ruff_check(tmp_path: Path) -> None:
    target = tmp_path / "src" / "sample.py"
    target.parent.mkdir()
    target.write_text("value = 1\n", encoding="utf-8")
    payload = {
        "cwd": str(tmp_path),
        "toolCall": {"name": "replace_file_content", "args": {"TargetFile": str(target)}},
    }

    exit_code, output, commands = invoke_main(payload, tmp_path, [(0, "", "")])

    assert exit_code == 0
    assert json.loads(output) == {}
    assert commands == [expected_command(tmp_path, "src/sample.py")]


def test_ruff_failure_returns_diagnostics(tmp_path: Path) -> None:
    target = tmp_path / "src" / "sample.py"
    target.parent.mkdir()
    target.write_text('{"a": 1, "a": 2}\n', encoding="utf-8")
    payload = {
        "cwd": str(tmp_path),
        "toolCall": {"name": "replace_file_content", "args": {"TargetFile": str(target)}},
    }

    exit_code, output, _commands = invoke_main(payload, tmp_path, [(1, "F601 duplicate key", "")])

    assert exit_code == 0
    assert json.loads(output) == {
        "error": "`ruff check` failed on `src/sample.py`.\nF601 duplicate key",
    }


def test_non_python_edit_is_ignored(tmp_path: Path) -> None:
    target = tmp_path / "docs" / "sample.md"
    target.parent.mkdir()
    target.write_text("content\n", encoding="utf-8")
    payload = {
        "cwd": str(tmp_path),
        "toolCall": {"name": "write_to_file", "args": {"TargetFile": str(target)}},
    }

    exit_code, output, commands = invoke_main(payload, tmp_path, [])

    assert exit_code == 0
    assert json.loads(output) == {}
    assert commands == []


@pytest.mark.parametrize("raw_input", ["", "{not-json"])
def test_invalid_json_is_ignored(raw_input: str) -> None:
    stdin = io.StringIO(raw_input)
    stdout = io.StringIO()

    with patch.object(HOOK.sys, "stdin", stdin), patch.object(HOOK.sys, "stdout", stdout):
        exit_code = HOOK.main()

    assert exit_code == 0
    assert stdout.getvalue() == ""
