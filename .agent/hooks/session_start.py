import shutil
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.memory_store import initialize_memory_store  # noqa: E402

MEMORY_ROOT_REL_DIR = Path(".memories")
MEMORY_REL_DIR = MEMORY_ROOT_REL_DIR / "memories"
MEMORY_STORE_REL_PATH = MEMORY_ROOT_REL_DIR / "memory_store.db"
MEMORY_FILE_TEMPLATES = {
    "MEMORY.md": (
        "[MISSION REQUIRED] Define the durable project mission and constraints.\n\u79ae\nStore only stable facts that should influence most future sessions.\n"
    ),
    "USER.md": ("Stable user preferences belong here as atomic entries separated by the standard memory delimiter.\n"),
}


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
        main_root = Path(common_dir).resolve().parent
        return branch or "detached", main_root != root.resolve()
    except Exception:
        return "unknown", False


def copy_memory_if_needed(root: Path) -> str:
    try:
        common_dir = subprocess.check_output(
            ["git", "rev-parse", "--git-common-dir"],
            cwd=root,
            text=True,
            encoding="utf-8",
        ).strip()
        main_root = Path(common_dir).resolve().parent
        if main_root == root.resolve():
            return "Main repository (no memory copy needed)"

        source = main_root / MEMORY_ROOT_REL_DIR
        target = root / MEMORY_ROOT_REL_DIR
        if not source.exists():
            return "No source memory directory found"

        copied: list[str] = []
        for source_path in source.rglob("*"):
            relative = source_path.relative_to(source)
            if any(part.startswith(".") or part == "__pycache__" for part in relative.parts):
                continue
            target_path = target / relative
            if target_path.exists():
                continue
            if source_path.is_dir():
                target_path.mkdir(parents=True, exist_ok=True)
            else:
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_path, target_path)
                copied.append(relative.as_posix())
        if copied:
            return "Copied memory from main repository: " + ", ".join(copied)
        return "Worktree memory already exists"
    except Exception as exc:
        return f"Memory copy check failed: {exc}"


def initialize_memory(root: Path) -> str:
    memory_dir = root / MEMORY_REL_DIR
    store_path = root / MEMORY_STORE_REL_PATH
    created: list[str] = []
    try:
        memory_dir.mkdir(parents=True, exist_ok=True)
        for name, template in MEMORY_FILE_TEMPLATES.items():
            path = memory_dir / name
            if not path.exists():
                path.write_text(template, encoding="utf-8")
                created.append(name)

        store_existed = store_path.exists()
        initialize_memory_store(store_path)
        if not store_existed:
            created.append("memory_store.db")
    except Exception as exc:
        return f"Memory initialization failed: {exc}"
    if created:
        return "Initialized: " + ", ".join(created)
    return "Memory skeleton exists"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()
    except Exception as exc:
        return f"Unable to read {path.name}: {exc}"


def main() -> int:
    try:
        import datetime

        root = repo_root()
        log_path = root / "hook_debug.log"
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now()}] session_start.py executed\n")
    except Exception:
        pass

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    root = repo_root()
    branch, is_worktree = git_context(root)
    sync_status = copy_memory_if_needed(root)
    init_status = initialize_memory(root)
    memory = read_text(root / MEMORY_REL_DIR / "MEMORY.md")
    user = read_text(root / MEMORY_REL_DIR / "USER.md")

    sys.stdout.write(
        "## Antigravity Session Context\n"
        f"- Branch: `{branch}`\n"
        f"- Workspace: {'worktree' if is_worktree else 'main repository'}\n"
        f"- Memory sync: {sync_status}\n"
        f"- Memory initialization: {init_status}\n\n"
        "### Project Memory\n"
        f"{memory}\n\n"
        "### User Preferences\n"
        f"{user}\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
