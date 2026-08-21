import importlib.util
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

import pytest

ROOT = Path(__file__).parents[2]


def load_hook() -> ModuleType:
    path = ROOT / ".agent" / "hooks" / "session_start.py"
    spec = importlib.util.spec_from_file_location("antigravity_session_start", path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


HOOK = load_hook()


def test_main_outputs_branch_context_without_writing_files(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    with (
        patch.object(HOOK, "repo_root", return_value=tmp_path),
        patch.object(HOOK, "git_context", return_value=("main", False)),
    ):
        assert HOOK.main() == 0

    output = capsys.readouterr().out
    assert "Antigravity Session Context" in output
    assert "Branch: `main`" in output
    assert "Workspace: main repository" in output
    assert list(tmp_path.iterdir()) == []


def test_git_context_returns_unknown_on_failure(tmp_path: Path) -> None:
    with patch.object(HOOK.subprocess, "check_output", side_effect=OSError("git not found")):
        branch, is_worktree = HOOK.git_context(tmp_path)

    assert branch == "unknown"
    assert is_worktree is False


def test_git_context_resolves_relative_common_dir_from_repo_root(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    nested = root / "scripts"
    nested.mkdir(parents=True)
    monkeypatch.chdir(nested)

    with patch.object(HOOK.subprocess, "check_output", side_effect=["main\n", ".git\n"]):
        branch, is_worktree = HOOK.git_context(root)

    assert branch == "main"
    assert is_worktree is False
