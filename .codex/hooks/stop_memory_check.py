import json
import subprocess
import sys
from pathlib import Path

MEMORY_REMINDER_INTERVAL = 3
MEMORY_CHAR_LIMIT = 2200
MEMORY_LINE_LIMIT = 100
USER_CHAR_LIMIT = 500
LESSONS_LINE_LIMIT = 50
SKILL_REVIEW_INTERVAL = 5
STATE_FILE = Path(".agents/memory/.codex_stop_memory_state.json")
APPROVED_MEMORY_FILES = {"MEMORY.md", "USER.md", "decisions.md", "lessons.md"}
APPROVED_MEMORY_DIRS = {"changes", "archive"}


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
    return root / ".agents" / "memory" / "MEMORY.md"


def user_path(root: Path) -> Path:
    return root / ".agents" / "memory" / "USER.md"


def lessons_path(root: Path) -> Path:
    return root / ".agents" / "memory" / "lessons.md"


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
        if not path.replace("\\", "/").startswith(".agents/memory/"):
            changed_files.append(path)
    return changed_files


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
        elif child.suffix.lower() == ".md" and child.name not in APPROVED_MEMORY_FILES:
            unexpected.append(child.name)

    if not unexpected:
        return ""
    return (
        "Memory taxonomy reminder: unexpected files or directories under `.agents/memory/`: "
        + ", ".join(sorted(unexpected))
        + ". Approved files are MEMORY.md, USER.md, decisions.md, and lessons.md; approved directories are changes/ and archive/. "
        "Keep reference clones under `.references/` and disposable files under `.tmp/`."
    )


def lessons_health_message(root: Path, state: dict) -> str:
    path = lessons_path(root)
    if not path.exists():
        return ""
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as exc:
        return f"Lessons health check failed: {exc}"

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
        f"Lessons pruning reminder: `.agents/memory/lessons.md` has {lines} lines; session start loads only the last "
        f"{LESSONS_LINE_LIMIT}. Keep recent and high-impact lessons near the bottom, then use `memory-sql` to graduate stale entries "
        "to `memory.db` or move non-searchable history to `archive/`."
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
        f"Memory compression reminder: `.agents/memory/MEMORY.md` is getting large "
        f"({chars} chars, {lines} lines; limit {MEMORY_CHAR_LIMIT} chars / {MEMORY_LINE_LIMIT} lines). "
        "Use `compress-memory`, keep active decisions in `decisions.md`, and graduate stale searchable history with `memory-sql`."
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
        f"USER.md size reminder: `.agents/memory/USER.md` has {chars} chars (limit {USER_CHAR_LIMIT}). "
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
        f"[System] Memory reminder: {len(non_memory_changes)} files changed over {response_count} Codex responses.\n"
        "Before finishing:\n"
        "1. Update MEMORY.md only if mission or current state changed (limit 2,200 chars).\n"
        "2. Put user preferences in USER.md (limit 500 chars).\n"
        "3. Put active decisions in decisions.md and recurring lessons in lessons.md (limit 50 lines).\n"
        "4. Put active multi-step plans in changes/<id>/ and completed historical material in archive/.\n"
        "5. When memory-db is connected, use the memory-sql skill to deduplicate and graduate stale entries or record session metadata.\n"
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
            lessons_health_message(root, state),
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
