import shutil
import subprocess
import sys
from pathlib import Path

MEMORY_REL_DIR = Path(".agents") / "memory"
MEMORY_FILE_TEMPLATES = {
    "USER.md": """# User

Stable cross-agent user context: communication language, review style, working preferences, and collaboration conventions. Keep under ~500 chars so all agents can load it cheaply.
""",
    "decisions.md": """# Decisions

Record durable architectural decisions here. Graduate old entries to `memory.db` via `/memory-sql` when this file grows.
""",
    "lessons.md": """# Lessons

Keep this file concise. Session start auto-loads only the last 50 lines. Graduate stale lessons to `memory.db` rather than accumulating here.
""",
}
MEMORY_DIRS = [
    Path("changes"),
    Path("archive"),
]


def repo_root() -> Path:
    try:
        root = subprocess.check_output("git rev-parse --show-toplevel", shell=True, text=True, encoding="utf-8").strip()
        return Path(root)
    except Exception:
        return Path.cwd().resolve()


def get_git_info():
    try:
        branch = subprocess.check_output("git branch --show-current", shell=True, text=True, encoding="utf-8").strip()
        worktree_list = subprocess.check_output("git worktree list", shell=True, text=True, encoding="utf-8").strip()
        is_worktree = len(worktree_list.splitlines()) > 1
        last_commit_msg = subprocess.check_output("git log -1 --pretty=%B", shell=True, text=True, encoding="utf-8").strip()
        return branch or "detached", is_worktree, last_commit_msg
    except Exception as e:
        return f"unknown (error: {str(e)})", False, "No history found"


DEFAULT_MEMORY_TEMPLATE = """# Long-term Project Memory & State

*(Agent Note: Session-start project context. Keep MEMORY.md under ~2,200 chars. All files in `.agents/memory/` are git-ignored instantiated project memory.)*

## 1. Project Mission & Long-term Goals
[Define the ultimate goal of this project and architectural rules here]

## 2. Current State
[What is happening right now? Keep compact — one paragraph max. Detail goes in active `changes/` plans.]

## 3. Memory Map
- **Session-start context**: `MEMORY.md` (mission, current state), `USER.md` (user preferences), and the recent lesson tail.
- **Read on demand**: `decisions.md`, the full `lessons.md`, and active `changes/<id>/`.
- **Search or inspect when needed**: `memory.db` (SQLite FTS5 through Claude Code MCP) and `archive/`.
- **Policy**: Keep MEMORY.md under ~2,200 chars. Graduate lessons/decisions to `memory.db` instead of accumulating files.

## 4. Active Work

| Feature | Status | Evidence/Notes |
| :--- | :--- | :--- |
| **Initial Setup** | [ ] | Base project structure |

### Doing
- **[Session Name]**: [MISSION REQUIRED] Define the 'Branch Goal' and 'Definition of Done' here.

### Done
- [Record completed tasks here]
"""


def branch_mission_prompt(branch: str) -> str:
    return f"""- **[MISSION REQUIRED]**: This is a new session on branch `{branch}`.
  - **Short-term Goal**: [What are we doing right now?]
  - **Mid-term Goal**: [What does this branch achieve?]
  - **Long-term Impact**: [How does this benefit the project?]
  - **Definition of Done**: [2-3 concrete criteria]"""


def memory_template_for_branch(branch: str) -> str:
    return DEFAULT_MEMORY_TEMPLATE.replace(
        "- **[Session Name]**: [MISSION REQUIRED] Define the 'Branch Goal' and 'Definition of Done' here.",
        branch_mission_prompt(branch),
    )


def initialize_memory_taxonomy(root_dir: Path, branch: str) -> str:
    memory_dir = root_dir / MEMORY_REL_DIR
    created: list[str] = []

    try:
        memory_dir.mkdir(parents=True, exist_ok=True)
        memory_path = memory_dir / "MEMORY.md"
        if not memory_path.exists():
            memory_path.write_text(memory_template_for_branch(branch), encoding="utf-8")
            created.append("MEMORY.md")

        for name, template in MEMORY_FILE_TEMPLATES.items():
            path = memory_dir / name
            if path.exists():
                continue
            path.write_text(template, encoding="utf-8")
            created.append(name)

        for relative_dir in MEMORY_DIRS:
            path = memory_dir / relative_dir
            if path.exists():
                continue
            path.mkdir(parents=True, exist_ok=True)
            created.append(str(relative_dir).replace("\\", "/") + "/")
    except Exception as e:
        return f"Taxonomy initialization failed: {str(e)}"

    if created:
        return "Initialized memory skeleton: " + ", ".join(created)
    return "Memory skeleton exists"


def read_lessons_tail(root_dir: Path, line_limit: int = 50):
    lessons_path = root_dir / ".agents" / "memory" / "lessons.md"
    if not lessons_path.exists():
        return "No `.agents/memory/lessons.md` found."

    try:
        lines = lessons_path.read_text(encoding="utf-8").splitlines()
    except Exception as e:
        return f"Error reading lessons tail: {str(e)}"

    if not lines:
        return "`lessons.md` exists but is empty."

    tail = lines[-line_limit:]
    prefix = ""
    if len(lines) > line_limit:
        prefix = f"*(Showing last {line_limit} of {len(lines)} lines. Keep the bottom of `lessons.md` recent, repeated, and high-signal.)*\n\n"
    return prefix + "\n".join(tail)


def read_user_md(root_dir: Path) -> str:
    user_path = root_dir / ".agents" / "memory" / "USER.md"
    if not user_path.exists():
        return ""
    try:
        content = user_path.read_text(encoding="utf-8").strip()
        return content if content else ""
    except Exception:
        return ""


def read_memory(root_dir: Path, branch: str):
    memory_dir = root_dir / MEMORY_REL_DIR
    memory_path = memory_dir / "MEMORY.md"

    try:
        return memory_path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading memory: {str(e)}"


def read_claude_instructions(root_dir: Path):
    instructions_path = root_dir / "CLAUDE.md"
    if not instructions_path.exists():
        return "Claude instructions not found at `CLAUDE.md`."

    try:
        return instructions_path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading Claude instructions: {str(e)}"


def sync_memory_if_needed(current_root: Path):
    target_dir = current_root / MEMORY_REL_DIR

    try:
        common_dir = subprocess.check_output("git rev-parse --git-common-dir", shell=True, text=True, encoding="utf-8").strip()
        main_root = Path(common_dir).resolve().parent

        if main_root == current_root:
            return "Main repository (no memory copy needed)"

        source_dir = main_root / MEMORY_REL_DIR
        if not source_dir.exists():
            return "No source memory directory found"

        copied = copy_memory_tree(source_dir, target_dir)
        if copied:
            return f"Copied memory from main repo ({main_root.name}): " + ", ".join(copied)
        return "Worktree memory already exists"
    except Exception as e:
        return f"Memory copy check failed: {str(e)}"


def should_copy_memory_item(path: Path) -> bool:
    if path.name.startswith(".claude_"):
        return False
    if path.name == "__pycache__":
        return False
    return True


def copy_memory_tree(source_dir: Path, target_dir: Path) -> list[str]:
    copied: list[str] = []
    target_dir.mkdir(parents=True, exist_ok=True)

    for source_path in source_dir.rglob("*"):
        if not should_copy_memory_item(source_path):
            continue
        relative = source_path.relative_to(source_dir)
        if any(part.startswith(".claude_") or part == "__pycache__" for part in relative.parts):
            continue
        target_path = target_dir / relative
        if target_path.exists():
            continue
        if source_path.is_dir():
            target_path.mkdir(parents=True, exist_ok=True)
            copied.append(str(relative).replace("\\", "/") + "/")
        elif source_path.is_file():
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)
            copied.append(str(relative).replace("\\", "/"))

    return copied


def get_branch_purpose(branch: str):
    if branch.startswith("feat/") or "feature" in branch:
        return "New Feature Development"
    if branch.startswith("fix/") or "bugfix" in branch:
        return "Bug Fixing & Maintenance"
    if branch.startswith("docs/"):
        return "Documentation Update"
    if branch in ["main", "master", "develop"]:
        return "Production/Stable Branch"
    return "General Development"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    root_dir = repo_root()
    branch, is_worktree, last_msg = get_git_info()
    sync_status = sync_memory_if_needed(root_dir)
    taxonomy_init_status = initialize_memory_taxonomy(root_dir, branch)
    purpose = get_branch_purpose(branch)
    claude_instructions = read_claude_instructions(root_dir)
    memory_content = read_memory(root_dir, branch)
    user_md_content = read_user_md(root_dir)
    lessons_tail = read_lessons_tail(root_dir)

    mission_alert = ""
    if "[MISSION REQUIRED]" in memory_content:
        mission_alert = f"""
> [!IMPORTANT]
> **UNINITIALIZED BRANCH MISSION DETECTED**
> This worktree was recently created for branch `{branch}`.
> **ACTION REQUIRED**: Please define the 'Branch Goal' and 'Definition of Done' in the `Doing` section of `MEMORY.md` before starting technical tasks.
"""

    worktree_memory_alert = ""
    if is_worktree:
        worktree_memory_alert = """
> [!NOTE]
> **WORKTREE MEMORY INITIALIZATION**
> Ignored memory is copied from the main repository without overwriting local worktree memory.
> Review `MEMORY.md` and active `changes/` plans for branch-specific goals before starting implementation.
"""

    additional_context = f"""
## [System: Session Auto-Initialization]
- **Current Git Branch**: `{branch}` ({purpose})
- **Git Worktree Status**: {"Active Worktree" if is_worktree else "Main Workspace"}
- **Memory Sync Status**: {sync_status if sync_status else "Up to date"}
- **Memory Initialization Status**: {taxonomy_init_status if taxonomy_init_status else "Up to date"}
{mission_alert}
{worktree_memory_alert}

### [Goal Alignment Suggestion]
Based on the branch name `{branch}`, you should focus on: **{purpose}**.
**Context Clue (Last Commit)**: `{last_msg}`

Please check the Claude instructions, project context, and auto-loaded lesson tail below before repository work.

### [Claude Repository Instructions: CLAUDE.md]
{claude_instructions}

### [Project Context: MEMORY.md]
{memory_content}
{f"### [User Context: USER.md]{chr(10)}{user_md_content}{chr(10)}" if user_md_content else ""}
### [Auto-loaded Lessons: lessons.md Tail]
{lessons_tail}

---
*Note: This context was automatically injected by the Claude Code SessionStart hook.*
"""

    sys.stdout.write(additional_context + "\n")


if __name__ == "__main__":
    main()
