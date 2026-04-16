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
        return branch or "detached", is_worktree
    except Exception as e:
        return f"unknown (error: {str(e)})", False


def read_memory(root_dir: Path):
    """Read the project memory file from root."""
    memory_path = root_dir / ".agents" / "memory" / "MEMORY.md"
    if memory_path.exists():
        try:
            return memory_path.read_text(encoding="utf-8")
        except Exception as e:
            return f"Error reading memory: {str(e)}"
    return "No project memory found. Please initialize .agents/memory/MEMORY.md."


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
    # ... (header same as before)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    root_dir = Path(__file__).resolve().parent.parent

    # NEW: Sync memory before reading
    sync_status = sync_memory_if_needed(root_dir)

    # Read input from stdin if any
    try:
        if not sys.stdin.isatty():
            json.load(sys.stdin)
    except Exception:
        pass

    branch, is_worktree = get_git_info()
    purpose = get_branch_purpose(branch)
    memory_content = read_memory(root_dir)

    # Construct context
    additional_context = f"""
## [System: Session Auto-Initialization]
- **Current Git Branch**: `{branch}` ({purpose})
- **Git Worktree Status**: {"Active Worktree" if is_worktree else "Main Workspace"}
- **Memory Sync Status**: {sync_status if sync_status else "Up to date"}
...

### [Goal Alignment Suggestion]
Based on the branch name `{branch}`, you should focus on: **{purpose}**.
Please check the `MEMORY.md` below and move relevant items to the `Doing` section if they match this goal.

### [Project Memory: MEMORY.md]
{memory_content}

---
*Note: This context was automatically injected by the SessionStart hook. Align your current 'Doing' task with the branch mission.*
"""

    # Prepare output following Gemini CLI hook schema
    output = {
        "hookSpecificOutput": {"additionalContext": additional_context},
        "systemMessage": f"Memory loaded for branch '{branch}' ({purpose}). Welcome back, task synchronized.",
    }

    # Print to stdout
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
