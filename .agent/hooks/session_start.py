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


def git_context(root: Path) -> tuple[str, bool]:
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
    except Exception:
        return "unknown", False


def main() -> int:
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")

    root = repo_root()
    branch, is_worktree = git_context(root)
    sys.stdout.write(f"## Antigravity Session Context\n- Branch: `{branch}`\n- Workspace: {'worktree' if is_worktree else 'main repository'}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
