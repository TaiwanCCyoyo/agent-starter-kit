import json
import subprocess
import sys
from pathlib import Path

MEMORY_REMINDER_INTERVAL = 5
MEMORY_CHAR_LIMIT = 2200
MEMORY_LINE_LIMIT = 100
USER_CHAR_LIMIT = 500
SKILL_REVIEW_INTERVAL = 5
MEMORY_ROOT = Path(".memories")
MEMORY_DIR = MEMORY_ROOT / "memories"
STATE_FILE = MEMORY_ROOT / ".codex_stop_memory_state.json"
APPROVED_ROOT_FILES = {"memory_store.db"}
APPROVED_ROOT_DIRS = {"memories"}
APPROVED_MEMORY_FILES = {"MEMORY.md", "USER.md"}


def repo_root(cwd: str) -> Path:
    try:
        root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd,
            text=True,
            encoding="utf-8",
        ).strip()
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
    return path.stat().st_mtime if path.exists() else 0.0


def changed_non_memory_files(root: Path) -> list[str]:
    changed = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=root,
        text=True,
        capture_output=True,
    )
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
        "Keep planning outside memory: use native planning state, project-owned OpenSpec files when initialized, "
        "disposable artifacts under `.tmp/`, and maintained documentation under `docs/`."
    )


def memory_health_message(root: Path, state: dict) -> str:
    path = memory_path(root)
    if not path.exists():
        return "No MEMORY.md found."

    current_mtime = memory_mtime(root)
    previous_mtime = float(state.get("health_memory_mtime", 0.0))
    content = path.read_text(encoding="utf-8")
    chars = len(content)
    lines = len(content.splitlines())
    state["health_memory_mtime"] = current_mtime
    state["health_chars"] = chars
    state["health_lines"] = lines

    if current_mtime <= previous_mtime:
        return ""
    if chars <= MEMORY_CHAR_LIMIT and lines <= MEMORY_LINE_LIMIT:
        return ""
    return (
        f"Memory compression reminder: `.memories/memories/MEMORY.md` is getting large "
        f"({chars} chars, {lines} lines; limit {MEMORY_CHAR_LIMIT} chars / {MEMORY_LINE_LIMIT} lines). "
        "Use `compress-memory`; move searchable durable facts and problem history to `memory_store.db` with `memory-sql`."
    )


def user_health_message(root: Path) -> str:
    path = user_path(root)
    if not path.exists():
        return ""
    try:
        chars = len(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return f"USER.md health check failed: {exc}"
    if chars <= USER_CHAR_LIMIT:
        return ""
    return (
        f"USER.md size reminder: `.memories/memories/USER.md` has {chars} chars (limit {USER_CHAR_LIMIT}). "
        "Keep only essential communication and collaboration preferences."
    )


def memory_update_message(root: Path, state: dict) -> str:
    current_mtime = memory_mtime(root)
    previous_mtime = float(state.get("memory_mtime", 0.0))
    response_count = int(state.get("response_count", 0))
    if current_mtime > previous_mtime:
        response_count = 0

    non_memory_changes = changed_non_memory_files(root)
    if not non_memory_changes:
        state["memory_mtime"] = current_mtime
        state["response_count"] = 0
        return ""

    response_count += 1
    state["memory_mtime"] = current_mtime
    state["response_count"] = response_count
    if response_count < MEMORY_REMINDER_INTERVAL:
        return ""

    return (
        f"[System] Memory checkpoint: {response_count} responses, {len(non_memory_changes)} files changed this session.\n"
        "Multiple conversations have accumulated — if important facts, decisions, or patterns emerged, persist them now:\n"
        "stable project facts → update MEMORY.md; searchable decisions and lessons → `mcp__memory-db__write_query` into facts table.\n"
        "Nothing important to save? Call `mcp__memory-control__dismiss_reminder` to reset this counter."
    )


def skill_review_message(state: dict) -> str:
    if state.get("skill_review_prompted"):
        return ""
    response_count = int(state.get("response_count", 0))
    if response_count < SKILL_REVIEW_INTERVAL:
        return ""
    state["skill_review_prompted"] = True
    return (
        f"[System] Skill review reminder: {response_count} responses with repository changes this session. "
        "Use the `skill-review` skill to decide whether a correction, technique, or workflow should update an existing skill, "
        "become a new project skill, remain memory, or be dropped."
    )


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        event = {}

    root = repo_root(event.get("cwd") or ".")
    state = read_state(root, event.get("session_id", ""))
    messages = [
        message
        for message in (
            memory_update_message(root, state),
            skill_review_message(state),
            memory_health_message(root, state),
            user_health_message(root),
            memory_taxonomy_message(root),
        )
        if message
    ]
    write_state(root, state)
    if messages:
        sys.stdout.write(json.dumps({"systemMessage": "\n\n".join(messages)}) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
