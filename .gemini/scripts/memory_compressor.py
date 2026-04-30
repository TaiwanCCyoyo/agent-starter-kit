import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

MEMORY_TOKEN_LIMIT = 2000
MEMORY_LINE_LIMIT = 100
STATE_FILE = Path(".agents/memory/.gemini_session_state.json")


def repo_root() -> Path:
    """Resolve the repository root from the current working directory."""
    try:
        # Suppress stderr to prevent bleeding raw git errors into the console/prompt
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
        # Atomic write using a temporary file
        fd, temp_path = tempfile.mkstemp(dir=str(path.parent), text=True)
        try:
            # Set permissions to 0644 (readable by all, writable by owner)
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
        # Fail gracefully to avoid blocking the main workflow
        pass


def count_tokens(text: str) -> int:
    """Estimate tokens roughly enough for hook-time memory health checks."""
    return len(text) // 4


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    root = repo_root()
    path = memory_path(root)
    if not path.exists():
        return

    state = read_state(root)
    current_mtime = path.stat().st_mtime
    previous_health_mtime = float(state.get("health_memory_mtime", 0.0))

    # Only check if memory has changed since last health check
    if current_mtime <= previous_health_mtime:
        return

    content = path.read_text(encoding="utf-8")
    tokens = count_tokens(content)
    lines = len(content.splitlines())

    state["health_memory_mtime"] = current_mtime
    state["health_tokens"] = tokens
    state["health_lines"] = lines
    write_state(root, state)

    # Threshold Check - only emit if exceeding
    if tokens > MEMORY_TOKEN_LIMIT or lines > MEMORY_LINE_LIMIT:
        output = {
            "systemMessage": f"[System] Memory compression reminder: `.agents/memory/MEMORY.md` is getting large ({tokens} tokens, {lines} lines). "
            "Use `compress-memory` to preserve current decisions and lessons while summarizing historical detail."
        }
        print(json.dumps(output))


if __name__ == "__main__":
    main()
