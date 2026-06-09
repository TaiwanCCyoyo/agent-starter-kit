import json
import subprocess
import sys
from pathlib import Path

MEMORY_REMINDER_INTERVAL = 3
MEMORY_CHAR_LIMIT = 2200
MEMORY_LINE_LIMIT = 100
USER_CHAR_LIMIT = 500
SKILL_REVIEW_INTERVAL = 5
MEMORY_ROOT = Path(".memories")
MEMORY_DIR = MEMORY_ROOT / "memories"
STATE_FILE = MEMORY_ROOT / ".claude_stop_memory_state.json"
APPROVED_ROOT_FILES = {"memory_store.db"}
APPROVED_ROOT_DIRS = {"memories"}
APPROVED_MEMORY_FILES = {"MEMORY.md", "USER.md"}


def repo_root(cwd: str) -> Path:
    try:
        root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=cwd, text=True, encoding="utf-8").strip()
        return Path(root)
    except Exception:
        return Path(cwd).resolve()


def memory_path(root: Path) -> Path:
    return root / MEMORY_DIR / "MEMORY.md"


def user_path(root: Path) -> Path:
    return root / MEMORY_DIR / "USER.md"


def state_path(root: Path) -> Path:
    return root / STATE_FILE


def read_state(root: Path, session_id: str) -> dict:
    path = state_path(root)
    if path.exists():
        try:
            state = json.loads(path.read_text(encoding="utf-8"))
            if state.get("session_id") == session_id:
                return state
        except Exception:
            pass
    return {"session_id": session_id}


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
        if not path.replace("\\", "/").startswith(".memories/"):
            changed_files.append(path)
    return changed_files


def memory_taxonomy_message(root: Path) -> str:
    memory_root = root / MEMORY_ROOT
    if not memory_root.exists():
        return ""

    unexpected: list[str] = []
    for child in memory_root.iterdir():
        if child.name.startswith("."):
            continue
        if child.is_dir():
            if child.name not in APPROVED_ROOT_DIRS:
                unexpected.append(child.name + "/")
        elif child.name not in APPROVED_ROOT_FILES:
            unexpected.append(child.name)

    memory_dir = memory_root / "memories"
    if memory_dir.exists():
        for child in memory_dir.iterdir():
            relative = f"memories/{child.name}"
            if child.is_dir() or child.name not in APPROVED_MEMORY_FILES:
                unexpected.append(relative + ("/" if child.is_dir() else ""))

    if not unexpected:
        return ""
    return (
        "Memory taxonomy reminder: unexpected files or directories under `.memories/`: "
        + ", ".join(sorted(unexpected))
        + ". Approved items are `memories/MEMORY.md`, `memories/USER.md`, and `memory_store.db`. "
        "Keep approved cross-session plans under `.references/plans/`, disposable artifacts under `.tmp/`, "
        "and maintained documentation under `docs/`."
    )


def memory_health_message(root: Path, state: dict) -> str:
    path = memory_path(root)
    if not path.exists():
        return "No MEMORY.md found."

    current_memory_mtime = memory_mtime(root)
    previous_health_mtime = float(state.get("health_memory_mtime", 0.0))
    content = path.read_text(encoding="utf-8")
    chars = len(content)
    lines = len(content.splitlines())
    state["health_memory_mtime"] = current_memory_mtime
    state["health_chars"] = chars
    state["health_lines"] = lines

    if current_memory_mtime <= previous_health_mtime:
        return ""

    if chars <= MEMORY_CHAR_LIMIT and lines <= MEMORY_LINE_LIMIT:
        return ""

    return (
        f"Memory compression reminder: `.memories/memories/MEMORY.md` is getting large "
        f"({chars} chars, {lines} lines; limit {MEMORY_CHAR_LIMIT} chars / {MEMORY_LINE_LIMIT} lines). "
        "Use `/compress-memory`; move searchable durable facts and problem history to `memory_store.db` with `/memory-sql`."
    )


def user_health_message(root: Path) -> str:
    path = user_path(root)
    if not path.exists():
        return ""
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return f"USER.md health check failed: {str(e)}"
    chars = len(content)
    if chars <= USER_CHAR_LIMIT:
        return ""
    return (
        f"USER.md size reminder: `.memories/memories/USER.md` has {chars} chars (limit {USER_CHAR_LIMIT} chars). "
        "Keep only essential communication and collaboration preferences."
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
        f"[System] Memory reminder: {len(non_memory_changes)} files changed over {response_count} Claude responses.\n"
        "Before finishing:\n"
        "1. Update `.memories/memories/MEMORY.md` only for stable project facts needed in most future sessions (limit 2,200 chars).\n"
        "2. Put stable user preferences in `.memories/memories/USER.md` (limit 500 chars).\n"
        "3. Put searchable decisions, lessons, workflows, tool facts, and environment facts in `memory_store.db`.\n"
        "4. If a blocker, workaround, mistaken assumption, or confusion recurred, query `problem_patterns` and `problem_occurrences`, "
        "stop repeating an unverified workaround, and record a root cause plus verified resolution or explicit external blocker.\n"
        "5. Keep approved cross-session plans in `.references/plans/`; plans are not long-term memory.\n"
        "Keep technical memory concise and discuss progress with the user in Traditional Chinese."
    )


def skill_review_message(state: dict) -> str:
    if state.get("skill_review_prompted"):
        return ""
    response_count = int(state.get("response_count", 0))
    if response_count < SKILL_REVIEW_INTERVAL:
        return ""
    state["skill_review_prompted"] = True
    return (
        f"[System] Skill Review Reminder: {response_count} responses with code changes this session. "
        "Run `/learn-eval` to check whether any non-obvious techniques or reusable workflows "
        "from this session deserve skill extraction. See `.claude/skills/skill-curator/SKILL.md`."
    )


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        event = {}

    root = repo_root(event.get("cwd") or ".")
    session_id = event.get("session_id", "")

    state = read_state(root, session_id)
    messages = []
    memory_update_reminder = memory_update_message(root, state)
    if memory_update_reminder:
        messages.append(memory_update_reminder)
    skill_reminder = skill_review_message(state)
    if skill_reminder:
        messages.append(skill_reminder)
    memory_message = memory_health_message(root, state)
    if memory_message:
        messages.append(memory_message)
    user_message = user_health_message(root)
    if user_message:
        messages.append(user_message)
    taxonomy_message = memory_taxonomy_message(root)
    if taxonomy_message:
        messages.append(taxonomy_message)
    write_state(root, state)

    if messages:
        sys.stdout.write(json.dumps({"systemMessage": "\n\n".join(messages)}) + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
