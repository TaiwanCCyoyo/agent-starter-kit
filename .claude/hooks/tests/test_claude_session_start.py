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


def test_repo_root_prefers_existing_claude_project_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))

    with patch.object(HOOK.subprocess, "check_output") as mock_check_output:
        result = HOOK.repo_root()

    assert result == tmp_path.resolve()
    mock_check_output.assert_not_called()


def test_repo_root_falls_back_to_git_for_missing_env_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path / "does-not-exist"))

    with patch.object(HOOK.subprocess, "check_output", return_value=f"{tmp_path}\n") as mock_check_output:
        result = HOOK.repo_root()

    assert result == tmp_path
    mock_check_output.assert_called_once()


def test_get_git_info_runs_commands_in_given_cwd(tmp_path: Path) -> None:
    calls: list[tuple[list[str], Path | None]] = []

    def fake_check_output(
        command: list[str],
        cwd: Path | None = None,
        text: bool = True,
        encoding: str = "utf-8",
    ) -> str:
        calls.append((command, cwd))
        if "--show-current" in command:
            return "feat/example\n"
        if "--git-common-dir" in command:
            return f"{tmp_path / '.git'}\n"
        return "commit message\n"

    with patch.object(HOOK.subprocess, "check_output", side_effect=fake_check_output):
        branch, is_worktree, last_msg = HOOK.get_git_info(tmp_path)

    assert branch == "feat/example"
    assert is_worktree is False
    assert last_msg == "commit message"
    assert calls
    assert all(cwd == tmp_path for _command, cwd in calls)


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


def test_main_outputs_only_project_context(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))

    def fake_check_output(
        command: list[str],
        cwd: Path | None = None,
        text: bool = True,
        encoding: str = "utf-8",
    ) -> str:
        if "--show-current" in command:
            return "main\n"
        if "--git-common-dir" in command:
            return f"{tmp_path / '.git'}\n"
        return "commit message\n"

    with patch.object(HOOK.subprocess, "check_output", side_effect=fake_check_output):
        HOOK.main()

    output = capsys.readouterr().out
    assert "System: Session Auto-Initialization" in output
    assert "Current Git Branch" in output
    assert "Context Clue (Last Commit)" in output
    assert list(tmp_path.iterdir()) == []


def test_claude_hooks_use_exec_form_with_project_dir_placeholder() -> None:
    config = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
    for event in ("SessionStart", "PostToolUse"):
        hook = config["hooks"][event][0]["hooks"][0]
        assert hook["command"] == "uv"
        assert any("${CLAUDE_PROJECT_DIR}" in arg for arg in hook["args"])
