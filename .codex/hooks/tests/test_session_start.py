import importlib.util
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
        patch.object(HOOK, "get_git_info", return_value=("main", False, "latest commit")),
        patch.object(HOOK, "read_text", return_value=instructions),
    ):
        HOOK.main()

    output = capsys.readouterr().out
    assert "Current Git Branch" in output
    assert "Git Worktree Status" in output
    assert "Context Clue (Last Commit)" in output
    assert instructions in output
    assert list(tmp_path.iterdir()) == []


def test_get_git_info_returns_unknown_on_failure(tmp_path: Path) -> None:
    with patch.object(HOOK.subprocess, "check_output", side_effect=OSError("git not found")):
        branch, is_worktree, last_msg = HOOK.get_git_info(tmp_path)

    assert branch.startswith("unknown (error:")
    assert is_worktree is False
    assert last_msg == "No history found"


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
        side_effect=["main\n", ".git\n", "commit message\n"],
    ):
        branch, is_worktree, last_msg = HOOK.get_git_info(root)

    assert branch == "main"
    assert is_worktree is False
    assert last_msg == "commit message"
