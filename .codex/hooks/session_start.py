import io
import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    try:
        root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            text=True,
            encoding="utf-8",
        ).strip()
        return Path(root)
    except Exception:
        return Path.cwd().resolve()


def get_git_info(root: Path) -> tuple[str, bool, str]:
    try:
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            cwd=root,
            text=True,
            encoding="utf-8",
        ).strip()
        common_dir = subprocess.check_output(
            ["git", "rev-parse", "--git-common-dir"],
            cwd=root,
            text=True,
            encoding="utf-8",
        ).strip()
        last_commit_msg = subprocess.check_output(
            ["git", "log", "-1", "--pretty=%B"],
            cwd=root,
            text=True,
            encoding="utf-8",
        ).strip()
        common_path = Path(common_dir)
        if not common_path.is_absolute():
            common_path = root / common_path
        main_root = common_path.resolve().parent
        return branch or "detached", main_root != root.resolve(), last_commit_msg
    except Exception as exc:
        return f"unknown (error: {exc})", False, "No history found"


def read_text(path: Path, missing: str = "") -> str:
    if not path.exists():
        return missing
    try:
        return path.read_text(encoding="utf-8").strip()
    except Exception as exc:
        return f"Error reading {path.name}: {exc}"


def get_branch_purpose(branch: str) -> str:
    if branch.startswith("feat/") or "feature" in branch:
        return "New Feature Development"
    if branch.startswith("fix/") or "bugfix" in branch:
        return "Bug Fixing & Maintenance"
    if branch.startswith("docs/"):
        return "Documentation Update"
    if branch in {"main", "master", "develop"}:
        return "Production/Stable Branch"
    return "General Development"


def main() -> int:
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")

    root = repo_root()
    branch, is_worktree, last_msg = get_git_info(root)
    purpose = get_branch_purpose(branch)
    codex_instructions = read_text(
        root / ".codex" / "AGENTS.md",
        "Codex instructions not found at `.codex/AGENTS.md`.",
    )
    sys.stdout.write(
        "## [System: Session Auto-Initialization]\n"
        f"- **Current Git Branch**: `{branch}` ({purpose})\n"
        f"- **Git Worktree Status**: {'Active Worktree' if is_worktree else 'Main Workspace'}\n\n"
        "### [Goal Alignment Suggestion]\n"
        f"Focus on: **{purpose}**.\n"
        f"**Context Clue (Last Commit)**: `{last_msg}`\n\n"
        "### [Codex Repository Instructions: .codex/AGENTS.md]\n"
        f"{codex_instructions}\n\n"
        "---\n"
        "*This context was automatically injected by the Codex SessionStart hook.*\n"
    )
    return 0


if __name__ == "__main__":
    main()
