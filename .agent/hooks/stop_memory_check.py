import subprocess
import sys
from pathlib import Path

MEMORY_CHAR_LIMIT = 2200
MEMORY_LINE_LIMIT = 100
USER_CHAR_LIMIT = 500
MEMORY_ROOT = Path(".memories")
MEMORY_DIR = MEMORY_ROOT / "memories"
APPROVED_ROOT_FILES = {"memory_store.db"}
APPROVED_ROOT_DIRS = {"memories"}
APPROVED_MEMORY_FILES = {"MEMORY.md", "USER.md"}


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


def size_message(path: Path, char_limit: int, line_limit: int | None = None) -> str:
    if not path.exists():
        return f"Missing required memory file: `{path.as_posix()}`."
    content = path.read_text(encoding="utf-8")
    chars = len(content)
    lines = len(content.splitlines())
    if chars <= char_limit and (line_limit is None or lines <= line_limit):
        return ""
    limits = f"{char_limit} chars"
    if line_limit is not None:
        limits += f" / {line_limit} lines"
    return f"`{path.name}` is too large ({chars} chars, {lines} lines; limit {limits})."


def taxonomy_message(root: Path) -> str:
    memory_root = root / MEMORY_ROOT
    if not memory_root.exists():
        return "Missing `.memories/`."

    unexpected: list[str] = []
    for child in memory_root.iterdir():
        if child.name.startswith("."):
            continue
        if child.is_dir() and child.name not in APPROVED_ROOT_DIRS:
            unexpected.append(child.name + "/")
        elif child.is_file() and child.name not in APPROVED_ROOT_FILES:
            unexpected.append(child.name)

    memory_dir = memory_root / "memories"
    if memory_dir.exists():
        for child in memory_dir.iterdir():
            if child.is_dir() or child.name not in APPROVED_MEMORY_FILES:
                suffix = "/" if child.is_dir() else ""
                unexpected.append(f"memories/{child.name}{suffix}")
    if not unexpected:
        return ""
    return "Unexpected memory items: " + ", ".join(sorted(unexpected)) + "."


def main() -> int:
    try:
        import datetime

        root = repo_root()
        log_path = root / "hook_debug.log"
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now()}] stop_memory_check.py executed\n")
    except Exception:
        pass

    root = repo_root()
    messages = [
        size_message(
            root / MEMORY_DIR / "MEMORY.md",
            MEMORY_CHAR_LIMIT,
            MEMORY_LINE_LIMIT,
        ),
        size_message(root / MEMORY_DIR / "USER.md", USER_CHAR_LIMIT),
        taxonomy_message(root),
    ]
    messages = [message for message in messages if message]
    if messages:
        sys.stdout.write("\n".join(messages) + "\nUse `memory-manager` and `memory-sql` to curate bounded files and SQLite facts.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
