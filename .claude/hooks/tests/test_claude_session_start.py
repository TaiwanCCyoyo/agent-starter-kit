import importlib.util
import json
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

import pytest

ROOT = Path(__file__).parents[3]


def load_hook() -> ModuleType:
    path = ROOT / ".claude" / "hooks" / "session_start.py"
    spec = importlib.util.spec_from_file_location("claude_session_start", path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


HOOK = load_hook()


def test_repo_root_prefers_claude_project_dir_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))

    with patch.object(HOOK.subprocess, "check_output") as mock_check_output:
        result = HOOK.repo_root()

    assert result == tmp_path.resolve()
    mock_check_output.assert_not_called()


def test_repo_root_ignores_nonexistent_claude_project_dir_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path / "does-not-exist"))

    with patch.object(HOOK.subprocess, "check_output", return_value=f"{tmp_path}\n") as mock_check_output:
        result = HOOK.repo_root()

    assert result == tmp_path
    mock_check_output.assert_called_once()


def test_repo_root_falls_back_to_git_when_env_unset(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("CLAUDE_PROJECT_DIR", raising=False)

    with patch.object(HOOK.subprocess, "check_output", return_value=f"{tmp_path}\n") as mock_check_output:
        result = HOOK.repo_root()

    assert result == tmp_path
    mock_check_output.assert_called_once()


def test_get_git_info_runs_git_commands_in_given_cwd(tmp_path: Path) -> None:
    calls: list[tuple[str, Path | None]] = []

    def fake_check_output(command: str, shell: bool, cwd: Path | None = None, text: bool = True, encoding: str = "utf-8") -> str:
        calls.append((command, cwd))
        if "branch" in command:
            return "feat/example\n"
        if "worktree list" in command:
            return f"{tmp_path} abc [feat/example]\n"
        return "commit message\n"

    with patch.object(HOOK.subprocess, "check_output", side_effect=fake_check_output):
        branch, is_worktree, last_msg = HOOK.get_git_info(tmp_path)

    assert branch == "feat/example"
    assert is_worktree is False
    assert last_msg == "commit message"
    assert calls
    assert all(cwd == tmp_path for _command, cwd in calls)


def test_get_git_info_returns_unknown_on_failure(tmp_path: Path) -> None:
    with patch.object(HOOK.subprocess, "check_output", side_effect=OSError("git not found")):
        branch, is_worktree, last_msg = HOOK.get_git_info(tmp_path)

    assert branch.startswith("unknown (error:")
    assert is_worktree is False
    assert last_msg == "No history found"


def test_sync_memory_if_needed_runs_git_common_dir_in_current_root(tmp_path: Path) -> None:
    current_root = tmp_path / "worktree"
    current_root.mkdir()

    with patch.object(HOOK.subprocess, "check_output", return_value=f"{current_root / '.git'}\n") as mock_check_output:
        status = HOOK.sync_memory_if_needed(current_root)

    assert status == "Main repository (no memory copy needed)"
    mock_check_output.assert_called_once()
    _args, kwargs = mock_check_output.call_args
    assert kwargs["cwd"] == current_root


def test_sync_memory_if_needed_copies_missing_items_from_main_repo(tmp_path: Path) -> None:
    main_root = tmp_path / "main"
    worktree_root = tmp_path / "worktree"
    main_root.mkdir()
    worktree_root.mkdir()

    source_memories = main_root / HOOK.MEMORY_ROOT_REL_DIR
    source_memories.mkdir(parents=True)
    (source_memories / "MEMORY.md").write_text("shared memory\n", encoding="utf-8")

    with patch.object(HOOK.subprocess, "check_output", return_value=f"{main_root / '.git'}\n"):
        status = HOOK.sync_memory_if_needed(worktree_root)

    assert "Copied memory from main repo" in status
    copied_file = worktree_root / HOOK.MEMORY_ROOT_REL_DIR / "MEMORY.md"
    assert copied_file.read_text(encoding="utf-8") == "shared memory\n"


def test_main_output_does_not_inject_memory_content(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))

    def fake_check_output(command: str, shell: bool, cwd: Path | None = None, text: bool = True, encoding: str = "utf-8") -> str:
        if "branch" in command:
            return "main\n"
        if "worktree list" in command:
            return f"{tmp_path} abc [main]\n"
        return "commit message\n"

    with patch.object(HOOK.subprocess, "check_output", side_effect=fake_check_output):
        HOOK.main()

    output = capsys.readouterr().out
    memory_dir = tmp_path / HOOK.MEMORY_REL_DIR
    assert (memory_dir / "MEMORY.md").exists()
    assert "[MISSION REQUIRED]" not in output
    assert "### [Project Context: MEMORY.md]" not in output
    assert "### [User Context: USER.md]" not in output
    assert "System: Session Auto-Initialization" in output


def test_claude_hooks_use_exec_form_with_project_dir_placeholder() -> None:
    config = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
    for event in ("SessionStart", "PostToolUse"):
        hook = config["hooks"][event][0]["hooks"][0]
        assert hook["command"] == "uv"
        assert any("${CLAUDE_PROJECT_DIR}" in arg for arg in hook["args"])
