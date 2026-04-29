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
    changed = subprocess.run(["git", "diff", "--name-only"], cwd=root, text=True, capture_output=True)
    changed_files = [line for line in changed.stdout.splitlines() if line.strip()]
    return [path for path in changed_files if "MEMORY.md" not in path.replace("\\", "/")]


def count_tokens(text: str) -> int:
    """Estimate tokens roughly enough for hook-time memory health checks."""
    return len(text) // 4


def memory_health_message(root: Path) -> str:
    path = memory_path(root)
    if not path.exists():
        return "No MEMORY.md found."

    content = path.read_text(encoding="utf-8")
    tokens = count_tokens(content)
    lines = len(content.splitlines())

    report = ["--- Memory Health Report ---", f"Approximate Tokens: {tokens}", f"Line Count: {lines}"]
    if tokens > MEMORY_TOKEN_LIMIT or lines > MEMORY_LINE_LIMIT:
        report.extend(["", "[STATUS: VERBOSE]", "Recommendation: Use the `compress-memory` skill to summarize historical data."])
    else:
        report.extend(["", "[STATUS: LEAN]", "No immediate compression required."])

    return "\n".join(report)


def memory_update_message(root: Path) -> str:
    state = read_state(root)
    current_memory_mtime = memory_mtime(root)
    previous_memory_mtime = float(state.get("memory_mtime", 0.0))
    response_count = int(state.get("response_count", 0))

    if current_memory_mtime > previous_memory_mtime:
        response_count = 0

    non_memory_changes = changed_non_memory_files(root)
    if not non_memory_changes:
        write_state(root, {"memory_mtime": current_memory_mtime, "response_count": 0})
        return ""

    response_count += 1
    write_state(root, {"memory_mtime": current_memory_mtime, "response_count": response_count})

    if response_count < MEMORY_REMINDER_INTERVAL:
        return ""

    return (
        f"{response_count} Codex responses have passed while repository changes are pending. "
        "Before finishing, update `.agents/memory/MEMORY.md` using the `save-memory` skill unless the task was read-only "
        "or the user explicitly skipped memory updates."
    )


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        event = {}

    root = repo_root(event.get("cwd") or ".")

    messages = []
    memory_update_reminder = memory_update_message(root)
    if memory_update_reminder:
        messages.append(memory_update_reminder)
    memory_message = memory_health_message(root)
    if memory_message:
        messages.append(memory_message)

    if messages:
        print(json.dumps({"systemMessage": "\n\n".join(messages)}))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
