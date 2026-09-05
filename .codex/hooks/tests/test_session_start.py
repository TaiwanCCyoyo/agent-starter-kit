import importlib.util
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

import pytest

ROOT = Path(__file__).parents[3]


def load_hook() -> ModuleType:
    path = ROOT / ".codex" / "hooks" / "session_start.py"
    spec = importlib.util.spec_from_file_location("codex_session_start", path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


HOOK = load_hook()


def test_main_outputs_repository_context_without_writing_files(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    instructions = "## Operating Contract\n\n- Keep changes scoped.\n"

    with (
        patch.object(HOOK, "repo_root", return_value=tmp_path),
        patch.object(HOOK, "get_git_info", return_value=("main", False)),
        patch.object(HOOK, "read_text", return_value=instructions),
    ):
        HOOK.main()

    output = capsys.readouterr().out
    assert "Current Git Branch" in output
    assert "Git Worktree Status" in output
    assert "Goal Alignment" not in output
    assert "Last Commit" not in output
    assert instructions in output
    assert list(tmp_path.iterdir()) == []


def test_get_git_info_returns_unknown_on_failure(tmp_path: Path) -> None:
    with patch.object(HOOK.subprocess, "check_output", side_effect=OSError("git not found")):
        branch, is_worktree = HOOK.get_git_info(tmp_path)

    assert branch.startswith("unknown (error:")
    assert is_worktree is False


def test_get_git_info_resolves_relative_common_dir_from_repo_root(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    nested = root / "scripts"
    nested.mkdir(parents=True)
    monkeypatch.chdir(nested)

    with patch.object(
        HOOK.subprocess,
        "check_output",
        side_effect=["main\n", ".git\n"],
    ):
        branch, is_worktree = HOOK.get_git_info(root)

    assert branch == "main"
    assert is_worktree is False


def test_entrypoint_loads_instructions_in_repository_without_commits(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "--initial-branch=main", str(tmp_path)], check=True, capture_output=True)
    instruction_dir = tmp_path / ".codex"
    instruction_dir.mkdir()
    (instruction_dir / "AGENTS.md").write_text("- Preserve source artifacts.\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(ROOT / ".codex/hooks/session_start.py")],
        cwd=tmp_path,
        input='{"hook_event_name":"SessionStart","source":"startup"}',
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )

    assert "`main`" in result.stdout
    assert "Preserve source artifacts." in result.stdout
    assert "unknown" not in result.stdout
    assert result.stderr == ""


def test_instruction_reader_rejects_external_target(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    outside = tmp_path / "outside.md"
    outside.write_text("outside content must not enter context", encoding="utf-8")

    with patch.object(Path, "resolve", side_effect=[outside, root]):
        result = HOOK.read_text(root / ".codex/AGENTS.md", "unavailable", root=root)

    assert result == "unavailable"


def test_instruction_reader_rejects_oversized_content(tmp_path: Path) -> None:
    instructions = tmp_path / "AGENTS.md"
    instructions.write_text("x" * 32769, encoding="utf-8")

    result = HOOK.read_text(instructions, root=tmp_path)

    assert "exceed" in result
    assert "x" * 100 not in result
