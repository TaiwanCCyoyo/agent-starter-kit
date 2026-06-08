import shutil
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.memory_store import initialize_memory_store

MEMORY_ROOT_REL_DIR = Path(".memories")
MEMORY_REL_DIR = MEMORY_ROOT_REL_DIR / "memories"
MEMORY_STORE_REL_PATH = MEMORY_ROOT_REL_DIR / "memory_store.db"
MEMORY_FILE_TEMPLATES = {
    "USER.md": "Stable user preferences belong here as atomic entries separated by §.\n",
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


def get_git_info() -> tuple[str, bool, str]:
    try:
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            text=True,
            encoding="utf-8",
        ).strip()
        worktree_list = subprocess.check_output(
            ["git", "worktree", "list"],
            text=True,
            encoding="utf-8",
        ).strip()
        last_commit_msg = subprocess.check_output(
            ["git", "log", "-1", "--pretty=%B"],
            text=True,
            encoding="utf-8",
        ).strip()
        return branch or "detached", len(worktree_list.splitlines()) > 1, last_commit_msg
    except Exception as exc:
        return f"unknown (error: {exc})", False, "No history found"


DEFAULT_MEMORY_TEMPLATE = """[MISSION REQUIRED] Define the durable project mission and constraints for branch `{branch}`.
§
Store only stable project, environment, tool, decision, lesson, or workflow facts that should influence most future sessions.
§
Use memory_store.db for searchable structured facts, recurring problem occurrences, root causes, and verified resolutions.
"""


def branch_mission_prompt(branch: str) -> str:
    return f"""- **[MISSION REQUIRED]**: This is a new session on branch `{branch}`.
  - **Short-term Goal**: [What are we doing right now?]
  - **Mid-term Goal**: [What does this branch achieve?]
  - **Long-term Impact**: [How does this benefit the project?]
  - **Definition of Done**: [2-3 concrete criteria]"""


def memory_template_for_branch(branch: str) -> str:
    return DEFAULT_MEMORY_TEMPLATE.format(branch=branch)


def initialize_memory_taxonomy(root_dir: Path, branch: str) -> str:
    memory_dir = root_dir / MEMORY_REL_DIR
    store_path = root_dir / MEMORY_STORE_REL_PATH
    created: list[str] = []

    try:
        memory_dir.mkdir(parents=True, exist_ok=True)
        memory_path = memory_dir / "MEMORY.md"
        if not memory_path.exists():
            memory_path.write_text(memory_template_for_branch(branch), encoding="utf-8")
            created.append("MEMORY.md")

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
        return f"Taxonomy initialization failed: {exc}"

    return "Initialized memory skeleton: " + ", ".join(created) if created else "Memory skeleton exists"


def read_text(path: Path, missing: str = "") -> str:
    if not path.exists():
        return missing
    try:
        return path.read_text(encoding="utf-8").strip()
    except Exception as exc:
        return f"Error reading {path.name}: {exc}"


def sync_memory_if_needed(current_root: Path) -> str:
    target_dir = current_root / MEMORY_ROOT_REL_DIR
    try:
        common_dir = subprocess.check_output(
            ["git", "rev-parse", "--git-common-dir"],
            text=True,
            encoding="utf-8",
        ).strip()
        main_root = Path(common_dir).resolve().parent
        if main_root == current_root:
            return "Main repository (no memory copy needed)"
        source_dir = main_root / MEMORY_ROOT_REL_DIR
        if not source_dir.exists():
            return "No source memory directory found"
        copied = copy_memory_tree(source_dir, target_dir)
        return f"Copied memory from main repo ({main_root.name}): " + ", ".join(copied) if copied else "Worktree memory already exists"
    except Exception as exc:
        return f"Memory copy check failed: {exc}"


def should_copy_memory_item(path: Path) -> bool:
    return not path.name.startswith((".codex_", ".claude_")) and path.name != "__pycache__"


def copy_memory_tree(source_dir: Path, target_dir: Path) -> list[str]:
    copied: list[str] = []
    target_dir.mkdir(parents=True, exist_ok=True)
    for source_path in source_dir.rglob("*"):
        relative = source_path.relative_to(source_dir)
        if not should_copy_memory_item(source_path):
            continue
        if any(part.startswith((".codex_", ".claude_")) or part == "__pycache__" for part in relative.parts):
            continue
        target_path = target_dir / relative
        if target_path.exists():
            continue
        if source_path.is_dir():
            target_path.mkdir(parents=True, exist_ok=True)
            copied.append(relative.as_posix() + "/")
        elif source_path.is_file():
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)
            copied.append(relative.as_posix())
    return copied


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


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    root_dir = repo_root()
    branch, is_worktree, last_msg = get_git_info()
    sync_status = sync_memory_if_needed(root_dir)
    taxonomy_status = initialize_memory_taxonomy(root_dir, branch)
    memory_content = read_text(root_dir / MEMORY_REL_DIR / "MEMORY.md")
    user_content = read_text(root_dir / MEMORY_REL_DIR / "USER.md")
    codex_instructions = read_text(
        root_dir / ".codex" / "AGENTS.md",
        "Codex instructions not found at `.codex/AGENTS.md`.",
    )

    mission_alert = ""
    if "[MISSION REQUIRED]" in memory_content:
        mission_alert = f"""
> [!IMPORTANT]
> **UNINITIALIZED BRANCH MISSION DETECTED**
> Define the branch goal and definition of done for `{branch}` in `MEMORY.md` before implementation.
"""

    worktree_alert = ""
    if is_worktree:
        worktree_alert = """
> [!NOTE]
> **WORKTREE MEMORY INITIALIZATION**
> Ignored memory is copied from the main repository without overwriting local memory.
> Review `MEMORY.md`, `USER.md`, and relevant facts or problem history in `memory_store.db`.
"""

    user_section = f"\n### [User Context: USER.md]\n{user_content}\n" if user_content else ""
    additional_context = f"""
## [System: Session Auto-Initialization]
- **Current Git Branch**: `{branch}` ({get_branch_purpose(branch)})
- **Git Worktree Status**: {"Active Worktree" if is_worktree else "Main Workspace"}
- **Memory Sync Status**: {sync_status}
- **Memory Initialization Status**: {taxonomy_status}
{mission_alert}
{worktree_alert}

### [Goal Alignment Suggestion]
Focus on: **{get_branch_purpose(branch)}**.
**Context Clue (Last Commit)**: `{last_msg}`

### [Codex Repository Instructions: .codex/AGENTS.md]
{codex_instructions}

### [Project Context: MEMORY.md]
{memory_content}
{user_section}

---
*This context was automatically injected by the Codex SessionStart hook.*
"""
    sys.stdout.write(additional_context + "\n")


if __name__ == "__main__":
    main()
