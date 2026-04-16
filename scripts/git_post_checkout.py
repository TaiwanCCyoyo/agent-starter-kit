import shutil
import subprocess
from pathlib import Path


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

        # If current is same as main, nothing to sync
        if main_root == curr_root:
            return

        mem_rel = Path(".agents/memory/MEMORY.md")
        src = main_root / mem_rel
        dst = curr_root / mem_rel

        # Proactive sync
        if src.exists() and not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print("\n>>> [Git Hook] Proactively synced MEMORY.md from main repo to worktree.")
            print(f">>> Target: {dst}\n")
    except Exception:
        # Hooks should fail silently to not block git operations
        pass


if __name__ == "__main__":
    main()
