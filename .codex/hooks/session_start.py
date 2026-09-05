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


def read_text(path: Path, missing: str = "", *, root: Path) -> str:
    """Read bounded repository instructions without following an external target."""
    try:
        resolved = path.resolve()
        if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
            return missing
        with resolved.open("r", encoding="utf-8") as stream:
            content = stream.read(32769)
        if len(content) > 32768:
            return "Repository instructions exceed the 32768-character hook limit; read the file directly."
        return content.strip()
    except (OSError, UnicodeError, ValueError):
        return f"Unable to read repository instructions at {path.name}."


def main() -> int:
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")

    root = repo_root()
    branch, is_worktree = get_git_info(root)
    codex_instructions = read_text(
        root / ".codex" / "AGENTS.md",
        "Codex instructions not found at `.codex/AGENTS.md`.",
        root=root,
    )
    sys.stdout.write(
        "## Codex Repository Context\n"
        f"- **Current Git Branch**: `{branch}`\n"
        f"- **Git Worktree Status**: {'Active Worktree' if is_worktree else 'Main Workspace'}\n\n"
        "Branch metadata describes the checkout, not the user's task.\n\n"
        "### [Codex Repository Instructions: .codex/AGENTS.md]\n"
        f"{codex_instructions}\n\n"
        "---\n"
        "*This context was automatically injected by the Codex SessionStart hook.*\n"
    )
    return 0


if __name__ == "__main__":
    main()
