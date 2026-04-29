import shutil
import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    """Resolve the repository root from the current working directory."""
    try:
        root = subprocess.check_output("git rev-parse --show-toplevel", shell=True, text=True, encoding="utf-8").strip()
        return Path(root)
    except Exception:
        return Path.cwd().resolve()


def get_git_info():
    """Detect current git branch and worktree status."""
    try:
        branch = subprocess.check_output("git branch --show-current", shell=True, text=True, encoding="utf-8").strip()
        worktree_list = subprocess.check_output("git worktree list", shell=True, text=True, encoding="utf-8").strip()
        is_worktree = len(worktree_list.splitlines()) > 1

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


def read_memory(root_dir: Path, branch: str):
    """Read or initialize the project memory file with smart prompts."""
    memory_dir = root_dir / ".agents" / "memory"
    memory_path = memory_dir / "MEMORY.md"

    is_new = False
    if not memory_path.exists():
        is_new = True
        try:
            memory_dir.mkdir(parents=True, exist_ok=True)
            content = DEFAULT_MEMORY_TEMPLATE

            mission_prompt = f"""- **[MISSION REQUIRED]**: This is a new session on branch `{branch}`.
  - **Short-term Goal**: [What are we doing right now?]
  - **Mid-term Goal**: [What does this branch achieve?]
  - **Long-term Impact**: [How does this benefit the project?]
  - **Definition of Done**: [2-3 concrete criteria]"""

            content = content.replace("- **[Session Name]**: [MISSION REQUIRED] Define the 'Branch Goal' and 'Definition of Done' here.", mission_prompt)
            memory_path.write_text(content, encoding="utf-8")
        except Exception as e:
            return f"Error initializing memory: {str(e)}"

    try:
        content = memory_path.read_text(encoding="utf-8")
        if is_new:
            return f"*(Initialized new memory for branch `{branch}`)*\n\n" + content
        return content
    except Exception as e:
        return f"Error reading memory: {str(e)}"


def read_codex_instructions(root_dir: Path):
    """Read Codex-specific repository instructions for SessionStart context."""
    instructions_path = root_dir / ".codex" / "AGENTS.md"
    if not instructions_path.exists():
        return "Codex instructions not found at `.codex/AGENTS.md`."

    try:
        return instructions_path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading Codex instructions: {str(e)}"


def sync_memory_if_needed(current_root: Path):
    """Proactively sync MEMORY.md from main repo if missing in worktree."""
    memory_rel_path = Path(".agents/memory/MEMORY.md")
    target_path = current_root / memory_rel_path

    if target_path.exists():
        return "Memory exists"

    try:
        common_dir = subprocess.check_output("git rev-parse --git-common-dir", shell=True, text=True, encoding="utf-8").strip()
        main_root = Path(common_dir).resolve().parent

        if main_root == current_root:
            return "Main repository (no sync needed)"

        source_path = main_root / memory_rel_path
        if source_path.exists():
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)
            return f"Synchronized from main repo ({main_root.name})"
    except Exception as e:
        return f"Sync check failed: {str(e)}"
    return "No source memory found"


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


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    root_dir = repo_root()
    sync_status = sync_memory_if_needed(root_dir)
    branch, is_worktree, last_msg = get_git_info()
    purpose = get_branch_purpose(branch)
    codex_instructions = read_codex_instructions(root_dir)
    memory_content = read_memory(root_dir, branch)

    mission_alert = ""
    if "[MISSION REQUIRED]" in memory_content:
        mission_alert = f"""
> [!IMPORTANT]
> **UNINITIALIZED BRANCH MISSION DETECTED**
> This worktree was recently created for branch `{branch}`.
> **ACTION REQUIRED**: Please define the 'Branch Goal' and 'Definition of Done' in the `Doing` section of `MEMORY.md` before starting technical tasks.
"""

    additional_context = f"""
## [System: Session Auto-Initialization]
- **Current Git Branch**: `{branch}` ({purpose})
- **Git Worktree Status**: {"Active Worktree" if is_worktree else "Main Workspace"}
- **Memory Sync Status**: {sync_status if sync_status else "Up to date"}
{mission_alert}

### [Goal Alignment Suggestion]
Based on the branch name `{branch}`, you should focus on: **{purpose}**.
**Context Clue (Last Commit)**: `{last_msg}`

Please check the Codex instructions and `MEMORY.md` below before repository work.

### [Codex Repository Instructions: .codex/AGENTS.md]
{codex_instructions}

### [Project Memory: MEMORY.md]
{memory_content}

---
*Note: This context was automatically injected by the Codex SessionStart hook.*
"""

    print(additional_context)


if __name__ == "__main__":
    main()
