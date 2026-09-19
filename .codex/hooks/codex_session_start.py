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


def get_git_info(root: Path) -> tuple[str, bool]:
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
        common_path = Path(common_dir)
        if not common_path.is_absolute():
            common_path = root / common_path
        main_root = common_path.resolve().parent
        return branch or "detached", main_root != root.resolve()
    except Exception as exc:
        return f"unknown (error: {exc})", False


def main() -> int:
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")

    root = repo_root()
    branch, is_worktree = get_git_info(root)
    sys.stdout.write(
        "## Codex Repository Context\n"
        f"- **Current Git Branch**: `{branch}`\n"
        f"- **Git Worktree Status**: {'Active Worktree' if is_worktree else 'Main Workspace'}\n\n"
        "Branch metadata describes the checkout, not the user's task.\n"
    )
    return 0


if __name__ == "__main__":
    main()
