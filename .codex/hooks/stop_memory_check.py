import json
import subprocess
import sys
from pathlib import Path

MEMORY_REMINDER_INTERVAL = 3
MEMORY_TOKEN_LIMIT = 2000
MEMORY_LINE_LIMIT = 100
LESSONS_LINE_LIMIT = 50
STATE_FILE = Path(".agents/memory/.codex_stop_memory_state.json")
APPROVED_MEMORY_FILES = {
    "MEMORY.md",
    "decisions.md",
    "lessons.md",
    "lessons-archive.md",
    "current-state.md",
    "user-preferences.md",
    "workflows.md",
}
APPROVED_MEMORY_DIRS = {"changes", "archive", "runs", "candidates"}


def repo_root(cwd: str) -> Path:
    try:
        root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=cwd, text=True, encoding="utf-8").strip()
        return Path(root)
    except Exception:
        return Path(cwd).resolve()


def memory_path(root: Path) -> Path:
    return root / ".agents" / "memory" / "MEMORY.md"


def lessons_path(root: Path) -> Path:
    return root / ".agents" / "memory" / "lessons.md"


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


def memory_taxonomy_message(root: Path) -> str:
    memory_dir = root / ".agents" / "memory"
    if not memory_dir.exists():
        return ""

    unexpected: list[str] = []
    for child in memory_dir.iterdir():
        if child.name.startswith("."):
            continue
        if child.is_dir():
            if child.name not in APPROVED_MEMORY_DIRS:
                unexpected.append(child.name + "/")
            continue
        if child.suffix.lower() != ".md":
            continue
        if child.name not in APPROVED_MEMORY_FILES:
            unexpected.append(child.name)

    if not unexpected:
        return ""

    return (
        "Memory taxonomy reminder: unexpected memory files or directories found under `.agents/memory/`: "
        + ", ".join(sorted(unexpected))
        + ". Prefer the approved Hot/Warm/Cold taxonomy. Put active plans in `.agents/memory/changes/<change-id>/` "
        "and completed or superseded plans under `.agents/memory/archive/changes/` after consolidating durable knowledge."
    )


def lessons_health_message(root: Path, state: dict) -> str:
    path = lessons_path(root)
    if not path.exists():
        return ""

    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Lessons health check failed: {str(e)}"

    current_mtime = path.stat().st_mtime
    previous_mtime = float(state.get("lessons_mtime", 0.0))
    state["lessons_mtime"] = current_mtime

    if current_mtime <= previous_mtime:
        return ""

    lines = len(content.splitlines())
    state["lessons_lines"] = lines

    if lines <= LESSONS_LINE_LIMIT:
        return ""

    return (
        f"Lessons pruning reminder: `.agents/memory/lessons.md` has {lines} lines, but session start auto-loads only the last "
        f"{LESSONS_LINE_LIMIT} lines. Keep recent/repeated/high-impact lessons near the bottom and move stale or lower-priority "
        "lessons to `lessons-archive.md` or `archive/`."
    )


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
        "Use `compress-memory` to keep `MEMORY.md` as Hot Memory, route decisions to `decisions.md`, keep concise recurring lessons in "
        "`lessons.md`, and move historical detail to Warm/Cold memory."
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
        "1. Update Hot Memory only when the boot index/current summary changed: `.agents/memory/MEMORY.md`.\n"
        "2. Route durable decisions to `.agents/memory/decisions.md`.\n"
        "3. Route concise recurring lessons to `.agents/memory/lessons.md`; move stale or lower-priority lessons to `lessons-archive.md` or `archive/`.\n"
        "4. Route active handoff detail to `.agents/memory/current-state.md`.\n"
        "5. Route active plans to `.agents/memory/changes/<change-id>/`; archive completed or superseded plans under `.agents/memory/archive/changes/`.\n"
        "6. Preserve important run evidence under `.agents/memory/runs/` as Markdown plus JSONL when useful.\n\n"
        "Note: Technical memory should be concise and high-signal. Discuss progress with the user in Traditional Chinese (zh-TW)."
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
    lessons_message = lessons_health_message(root, state)
    if lessons_message:
        messages.append(lessons_message)
    taxonomy_message = memory_taxonomy_message(root)
    if taxonomy_message:
        messages.append(taxonomy_message)
    write_state(root, state)

    if messages:
        print(json.dumps({"systemMessage": "\n\n".join(messages)}))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
