import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

MEMORY_REMINDER_INTERVAL = 3
STATE_FILE = Path(".agents/memory/.gemini_session_state.json")


def repo_root() -> Path:
    """Resolve the repository root from the current working directory."""
    try:
        root = subprocess.check_output("git rev-parse --show-toplevel", shell=True, text=True, encoding="utf-8", stderr=subprocess.DEVNULL).strip()
        return Path(root)
    except Exception:
        return Path.cwd().resolve()


def memory_path(root: Path) -> Path:
    return root / ".agents" / "memory" / "MEMORY.md"


def state_path(root: Path) -> Path:
    return root / STATE_FILE


def read_state(root: Path) -> dict:
    path = state_path(root)
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def write_state(root: Path, state: dict) -> None:
    path = state_path(root)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, temp_path = tempfile.mkstemp(dir=str(path.parent), text=True)
        try:
            os.chmod(temp_path, 0o644)
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, sort_keys=True)
                f.write("\n")
            os.replace(temp_path, str(path))
        except Exception:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise
    except Exception:
        pass


def get_memory_mtime(root: Path) -> float:
    path = memory_path(root)
    if not path.exists():
        return 0.0
    return path.stat().st_mtime


def changed_non_memory_files(root: Path) -> list[str]:
    """Detect changed files, including untracked ones, excluding memory."""
    try:
        changed = subprocess.check_output("git status --porcelain", shell=True, text=True, encoding="utf-8", stderr=subprocess.DEVNULL)
        changed_files: list[str] = []
        for line in changed.splitlines():
            if not line.strip():
                continue
            path = line[3:].strip().strip('"')
            if " -> " in path:
                path = path.split(" -> ", 1)[1].strip().strip('"')

            normalized = path.replace("\\", "/")
            if normalized.startswith(".agents/memory/"):
                continue
            changed_files.append(path)
        return changed_files
    except Exception:
        return []


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    root = repo_root()
    state = read_state(root)

    current_memory_mtime = get_memory_mtime(root)
    previous_memory_mtime = float(state.get("memory_mtime", 0.0))
    response_count = int(state.get("response_count", 0))

    if current_memory_mtime > previous_memory_mtime:
        response_count = 0

    non_memory_changes = changed_non_memory_files(root)
    if not non_memory_changes:
        state["memory_mtime"] = current_memory_mtime
        state["response_count"] = 0
        write_state(root, state)
        return

    response_count += 1
    state["memory_mtime"] = current_memory_mtime
    state["response_count"] = response_count
    write_state(root, state)

    if response_count >= MEMORY_REMINDER_INTERVAL:
        output = {
            "reason": f"Significant changes detected after {response_count} turns. Prompting for layered memory routing.",
            "systemMessage": (
                f"[System] Memory Reminder: {len(non_memory_changes)} files changed over {response_count} turns.\n"
                "Before finishing this task, you MUST:\n"
                "1. Update Hot Memory only when the boot index/current summary changed: `.agents/memory/MEMORY.md`.\n"
                "2. Route durable decisions to `.agents/memory/decisions.md`.\n"
                "3. Route concise recurring lessons to `.agents/memory/lessons.md`; move stale or lower-priority lessons to `lessons-archive.md` or `archive/`.\n"
                "4. Route active handoff detail to `.agents/memory/current-state.md`.\n"
                "5. Route active plans to `.agents/memory/changes/<change-id>/`; archive completed or superseded plans under `.agents/memory/archive/changes/`.\n"
                "6. Preserve important run evidence under `.agents/memory/runs/` as Markdown plus JSONL when useful.\n\n"
                "Note: Technical memory should be concise and high-signal. Discuss progress with the user in Traditional Chinese (zh-TW)."
            ),
        }
        print(json.dumps(output))


if __name__ == "__main__":
    main()
