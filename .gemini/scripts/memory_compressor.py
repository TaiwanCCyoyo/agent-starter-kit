import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

MEMORY_TOKEN_LIMIT = 2000
MEMORY_LINE_LIMIT = 100
LESSONS_LINE_LIMIT = 50
STATE_FILE = Path(".agents/memory/.gemini_session_state.json")
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


def repo_root() -> Path:
    """Resolve the repository root from the current working directory."""
    try:
        root = subprocess.check_output("git rev-parse --show-toplevel", shell=True, text=True, encoding="utf-8", stderr=subprocess.DEVNULL).strip()
        return Path(root)
    except Exception:
        return Path.cwd().resolve()


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
        return ""

    current_mtime = path.stat().st_mtime
    previous_health_mtime = float(state.get("health_memory_mtime", 0.0))

    if current_mtime <= previous_health_mtime:
        return ""

    content = path.read_text(encoding="utf-8")
    tokens = count_tokens(content)
    lines = len(content.splitlines())

    state["health_memory_mtime"] = current_mtime
    state["health_tokens"] = tokens
    state["health_lines"] = lines

    if tokens <= MEMORY_TOKEN_LIMIT and lines <= MEMORY_LINE_LIMIT:
        return ""

    return (
        f"Memory compression reminder: `.agents/memory/MEMORY.md` is getting large ({tokens} approximate tokens, {lines} lines). "
        "Use `compress-memory` to keep `MEMORY.md` as Hot Memory, route decisions to `decisions.md`, keep concise recurring lessons in "
        "`lessons.md`, and move historical detail to Warm/Cold memory."
    )


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    root = repo_root()
    state = read_state(root)
    messages = []

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


if __name__ == "__main__":
    main()
