import importlib.util
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

import pytest

ROOT = Path(__file__).parents[3]


def load_hook() -> ModuleType:
    path = ROOT / ".codex" / "hooks" / "codex_session_start.py"
    spec = importlib.util.spec_from_file_location("codex_session_start", path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


HOOK = load_hook()


def test_main_outputs_repository_context_without_writing_files(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    with (
        patch.object(HOOK, "repo_root", return_value=tmp_path),
        patch.object(HOOK, "get_git_info", return_value=("main", False)),
    ):
        HOOK.main()

    output = capsys.readouterr().out
    assert "Current Git Branch" in output
    assert "Git Worktree Status" in output
    assert "Goal Alignment" not in output
    assert "Last Commit" not in output
    assert list(tmp_path.iterdir()) == []


def test_main_does_not_inject_repository_instructions(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Codex discovers the root AGENTS.md natively; the hook must not inject it."""
    with (
        patch.object(HOOK, "repo_root", return_value=tmp_path),
        patch.object(HOOK, "get_git_info", return_value=("main", False)),
    ):
        HOOK.main()

    output = capsys.readouterr().out
    assert "AGENTS.md" not in output
    assert "Repository Instructions" not in output
    assert not hasattr(HOOK, "read_text")


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


def test_entrypoint_reports_branch_in_repository_without_commits(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "--initial-branch=main", str(tmp_path)], check=True, capture_output=True)
    (tmp_path / "AGENTS.md").write_text("- Preserve source artifacts.\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(ROOT / ".codex/hooks/codex_session_start.py")],
        cwd=tmp_path,
        input='{"hook_event_name":"SessionStart","source":"startup"}',
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )

    assert "`main`" in result.stdout
    assert "Preserve source artifacts." not in result.stdout
    assert "unknown" not in result.stdout
    assert result.stderr == ""
