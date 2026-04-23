import json
import subprocess
import sys
from pathlib import Path


def get_git_info():
    """Detect current git branch and worktree status."""
    try:
        # Use shell=True for PowerShell and specify encoding for Windows
        branch = subprocess.check_output("git branch --show-current", shell=True, text=True, encoding="utf-8").strip()
        worktree_list = subprocess.check_output("git worktree list", shell=True, text=True, encoding="utf-8").strip()
        is_worktree = len(worktree_list.splitlines()) > 1

        # Get recent commit message as a hint for the branch mission
        last_commit_msg = subprocess.check_output("git log -1 --pretty=%B", shell=True, text=True, encoding="utf-8").strip()

        return branch or "detached", is_worktree, last_commit_msg
    except Exception as e:
        return f"unknown (error: {str(e)})", False, "No history found"


DEFAULT_MEMORY_TEMPLATE = """# Long-term Project Memory & State

*(Agent Note: This is your Soul. Update this BEFORE starting and AFTER finishing tasks. All files in `.agents/memory/` are git-ignored by default.)*

## 1. Project Mission & Long-term Goals
[Define the ultimate goal of this project and architectural rules here]

## 2. Lessons Learned (Avoid Repeating Mistakes)
- **Git Hook Initialization**: Merely having a `.pre-commit-config.yaml` is not enough; hooks must be explicitly installed using `uv run pre-commit install`. Always check if `.git/hooks/pre-commit` exists before assuming protection is active.

## 3. Session Handover & Delegated Tasks
- [ ] [List unfinished tasks or things the next session needs to pick up]

## 4. Current State & Unfinished Business

| Feature | Status | Evidence/Notes |
| :--- | :--- | :--- |
| **Initial Setup** | [ ] | Base project structure |

### Doing
- **[Session Name]**: [MISSION REQUIRED] Define the 'Branch Goal' and 'Definition of Done' here.

### Done
- [Record completed tasks here]
"""


def read_memory(root_dir: Path):
    """Read or initialize the project memory file."""
    memory_dir = root_dir / ".agents" / "memory"
    memory_path = memory_dir / "MEMORY.md"

    if not memory_path.exists():
        try:
            memory_dir.mkdir(parents=True, exist_ok=True)
            memory_path.write_text(DEFAULT_MEMORY_TEMPLATE, encoding="utf-8")
        except Exception as e:
            return f"Error initializing memory: {str(e)}"

    try:
        return memory_path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading memory: {str(e)}"


def get_branch_purpose(branch):
    """Infer the purpose of the branch from its name."""
    if branch.startswith("feat/") or "feature" in branch:
        return "New Feature Development"
    if branch.startswith("fix/") or "bugfix" in branch:
        return "Bug Fixing & Maintenance"
    if branch.startswith("docs/"):
        return "Documentation Update"
    if branch in ["main", "master", "develop"]:
        return "Production/Stable Branch"
    return "General Development"


def sync_memory_if_needed(current_root: Path):
    """Ensure MEMORY.md exists in worktree by copying from main repo if needed."""
    memory_rel_path = Path(".agents/memory/MEMORY.md")
    target_path = current_root / memory_rel_path

    if target_path.exists():
        return  # Already synced

    try:
        # Find the main repository root
        main_git_dir = subprocess.check_output("git rev-parse --git-common-dir", shell=True, text=True, encoding="utf-8").strip()
        main_root = Path(main_git_dir).resolve().parent  # Usually .git is inside main_root

        # In some worktree setups, git-common-dir points elsewhere,
        # let's try a more robust way to find main root if it's a sibling.
        if not (main_root / memory_rel_path).exists():
            # Fallback: check sibling directory based on our naming convention
            for sibling in current_root.parent.iterdir():
                if sibling.is_dir() and (sibling / memory_rel_path).exists() and sibling != current_root:
                    main_root = sibling
                    break

        source_path = main_root / memory_rel_path
        if source_path.exists():
            target_path.parent.mkdir(parents=True, exist_ok=True)
            import shutil

            shutil.copy2(source_path, target_path)
            return f"Synchronized from {main_root.name}"
    except Exception as e:
        return f"Sync failed: {str(e)}"
    return "No source memory found for sync."


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    root_dir = Path(__file__).resolve().parent.parent

    # Sync memory before reading
    sync_status = sync_memory_if_needed(root_dir)

    # Read input from stdin if any
    try:
        if not sys.stdin.isatty():
            json.load(sys.stdin)
    except Exception:
        pass

    branch, is_worktree, last_msg = get_git_info()
    purpose = get_branch_purpose(branch)
    memory_content = read_memory(root_dir)

    # Check if mission is uninitialized
    mission_alert = ""
    if "[MISSION REQUIRED]" in memory_content:
        mission_alert = f"""
> [!IMPORTANT]
> **UNINITIALIZED BRANCH MISSION DETECTED**
> This worktree was recently created for branch `{branch}`.
> **ACTION REQUIRED**: Please define the 'Branch Goal' and 'Definition of Done' in the `Doing` section of `MEMORY.md` before starting technical tasks.
"""

    # Construct context
    additional_context = f"""
## [System: Session Auto-Initialization]
- **Current Git Branch**: `{branch}` ({purpose})
- **Git Worktree Status**: {"Active Worktree" if is_worktree else "Main Workspace"}
- **Memory Sync Status**: {sync_status if sync_status else "Up to date"}
{mission_alert}

### [Goal Alignment Suggestion]
Based on the branch name `{branch}`, you should focus on: **{purpose}**.
**Context Clue (Last Commit)**: `{last_msg}`

Please check the `MEMORY.md` below and align your current task with the project mission.

### [Project Memory: MEMORY.md]
{memory_content}

---
*Note: This context was automatically injected by the SessionStart hook.*
"""

    # Print directly as Markdown to be captured by the hook
    print(additional_context)


if __name__ == "__main__":
    main()
