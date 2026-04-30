import json
import subprocess
import sys
from pathlib import Path

MEMORY_REMINDER_INTERVAL = 3
MEMORY_TOKEN_LIMIT = 2000
MEMORY_LINE_LIMIT = 100
STATE_FILE = Path(".agents/memory/.codex_stop_memory_state.json")


def repo_root(cwd: str) -> Path:
    try:
        root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=cwd, text=True, encoding="utf-8").strip()
        return Path(root)
    except Exception:
        return Path(cwd).resolve()


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
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def memory_mtime(root: Path) -> float:
    path = memory_path(root)
    if not path.exists():
        return 0.0
    return path.stat().st_mtime


def changed_non_memory_files(root: Path) -> list[str]:
    changed = subprocess.run(["git", "status", "--porcelain"], cwd=root, text=True, capture_output=True)
    changed_files: list[str] = []
    for line in changed.stdout.splitlines():
        if not line.strip():
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1].strip()
        normalized = path.replace("\\", "/")
        if normalized.startswith(".agents/memory/"):
            continue
        changed_files.append(path)
    return changed_files


def count_tokens(text: str) -> int:
    """Estimate tokens roughly enough for hook-time memory health checks."""
    return len(text) // 4


def memory_health_message(root: Path, state: dict) -> str:
    path = memory_path(root)
    if not path.exists():
        return "No MEMORY.md found."

    current_memory_mtime = memory_mtime(root)
    previous_health_mtime = float(state.get("health_memory_mtime", 0.0))
    content = path.read_text(encoding="utf-8")
    tokens = count_tokens(content)
    lines = len(content.splitlines())
    state["health_memory_mtime"] = current_memory_mtime
    state["health_tokens"] = tokens
    state["health_lines"] = lines

    if current_memory_mtime <= previous_health_mtime:
        return ""

    if tokens <= MEMORY_TOKEN_LIMIT and lines <= MEMORY_LINE_LIMIT:
        return ""

    return (
        f"Memory compression reminder: `.agents/memory/MEMORY.md` is getting large ({tokens} approximate tokens, {lines} lines). "
        "Use `compress-memory` to preserve current decisions and lessons while summarizing historical detail."
    )


def memory_update_message(root: Path, state: dict) -> str:
    current_memory_mtime = memory_mtime(root)
    previous_memory_mtime = float(state.get("memory_mtime", 0.0))
    response_count = int(state.get("response_count", 0))

    if current_memory_mtime > previous_memory_mtime:
        response_count = 0

    non_memory_changes = changed_non_memory_files(root)
    if not non_memory_changes:
        state["memory_mtime"] = current_memory_mtime
        state["response_count"] = 0
        return ""

    response_count += 1
    state["memory_mtime"] = current_memory_mtime
    state["response_count"] = response_count

    if response_count < MEMORY_REMINDER_INTERVAL:
        return ""

    return (
        f"[System] Memory & Session Log Reminder: {len(non_memory_changes)} files changed over {response_count} Codex responses.\n"
        "Before finishing this task, you MUST:\n"
        "1. Update `.agents/memory/MEMORY.md` (Done & Lessons Learned).\n"
        "2. Append a session summary to `.agents/memory/SESSION_LOG.md` using this format:\n\n"
        "### [YYYY-MM-DD] Session Summary\n"
        "- **Goal**: [Brief statement]\n"
        "- **Achievements**: [Concise bullets]\n"
        "- **Pending**: [Remaining work/issues]\n\n"
        "Note: Summaries must be in English. Discuss progress with the user in Traditional Chinese (zh-TW)."
    )


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        event = {}

    root = repo_root(event.get("cwd") or ".")

    state = read_state(root)
    messages = []
    memory_update_reminder = memory_update_message(root, state)
    if memory_update_reminder:
        messages.append(memory_update_reminder)
    memory_message = memory_health_message(root, state)
    if memory_message:
        messages.append(memory_message)
    write_state(root, state)

    if messages:
        print(json.dumps({"systemMessage": "\n\n".join(messages)}))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
