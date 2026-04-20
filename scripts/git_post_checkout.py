import shutil
import subprocess
import re
from pathlib import Path


def get_current_branch():
    """Gets the current git branch name."""
    try:
        return subprocess.check_output("git branch --show-current", shell=True, text=True, encoding="utf-8").strip()
    except Exception:
        return "unknown"


def update_memory_doing(memory_path, branch_name):
    """Updates the 'Doing' section in MEMORY.md based on the branch name."""
    if not memory_path.exists():
        return

    try:
        content = memory_path.read_text(encoding="utf-8")

        # Reset the 'Doing' section
        # Pattern looks for '### Doing' and the next section or end of file

        # Simple regex to replace the content under '### Doing'

        pattern = re.compile(r"(### Doing\n)(.*?)(\n###|\Z)", re.DOTALL)
        if pattern.search(content):
            mission_prompt = (
                f"- **[MISSION REQUIRED]**: This worktree is for branch '{branch_name}'.\n"
                f"  - **Branch Goal**: [Agent: PLEASE DEFINE THE SPECIFIC GOAL OF THIS BRANCH HERE]\n"
                f"  - **Definition of Done**: [Agent: LIST 2-3 CRITERIA THAT SIGNIFY COMPLETION]\n"
            )
            updated_content = pattern.sub(rf"\1{mission_prompt}\n\3", content)
            memory_path.write_text(updated_content, encoding="utf-8")
            print(f">>> [Git Hook] Initialized MEMORY.md for branch '{branch_name}' with a mission prompt.")
    except Exception as e:
        print(f">>> [Git Hook] Failed to update MEMORY.md: {e}")


def install_hooks_in_worktree():
    """Installs pre-commit and custom hooks in the current worktree."""
    try:
        # Install standard pre-commit
        subprocess.run(["uv", "run", "pre-commit", "install"], capture_output=True, text=True)

        # Register custom sync protocol (Linux/macOS)
        # Note: In a worktree, .git is a file, so we need to find the actual hooks dir
        git_dir = subprocess.check_output("git rev-parse --git-dir", shell=True, text=True, encoding="utf-8").strip()
        hooks_dir = Path(git_dir) / "hooks"
        hooks_dir.mkdir(parents=True, exist_ok=True)

        post_checkout_path = hooks_dir / "post-checkout"
        hook_content = '#!/bin/bash\nuv run python scripts/git_post_checkout.py "$@"'

        post_checkout_path.write_text(hook_content, encoding="utf-8")
        post_checkout_path.chmod(0o755)

        print(">>> [Git Hook] Successfully installed Git hooks in the new worktree.")
    except Exception as e:
        print(f">>> [Git Hook] Failed to install hooks in worktree: {e}")


def main():
    """
    Git post-checkout hook for memory synchronization.
    Triggered after 'git worktree add' or 'git checkout'.
    """
    try:
        # Detect if we are in a git repo
        common_dir = subprocess.check_output("git rev-parse --git-common-dir", shell=True, text=True, encoding="utf-8").strip()
        main_root = Path(common_dir).resolve().parent
        curr_root = Path(".").resolve()

        # If current is same as main, we don't do 'worktree sync' logic
        if main_root == curr_root:
            return

        mem_rel = Path(".agents/memory/MEMORY.md")
        src = main_root / mem_rel
        dst = curr_root / mem_rel

        branch_name = get_current_branch()

        # 1. Proactive Memory Sync
        if src.exists() and not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"\n>>> [Git Hook] Proactively synced MEMORY.md from main repo to worktree '{branch_name}'.")

            # 2. Intelligent Memory Initialization
            update_memory_doing(dst, branch_name)

            # 3. Automatic Hook Installation
            install_hooks_in_worktree()

            print(f">>> Target: {dst}\n")
    except Exception:
        # Hooks should fail silently to not block git operations
        pass


if __name__ == "__main__":
    main()
