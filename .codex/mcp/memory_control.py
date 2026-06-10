import json
import os
import subprocess
from pathlib import Path

from fastmcp import FastMCP

mcp = FastMCP("memory-control")

_STATE_FILE = Path(".memories/.codex_stop_memory_state.json")


def _project_root() -> Path:
    env_dir = os.environ.get("CODEX_PROJECT_DIR")
    if env_dir:
        return Path(env_dir)
    try:
        root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True, encoding="utf-8").strip()
        return Path(root)
    except Exception:
        return Path(".").resolve()


@mcp.tool()
def dismiss_reminder() -> str:
    """Reset the memory reminder counter after evaluating that no update is needed.

    The Stop hook re-arms automatically after 3 more responses.
    Codex only — not available in Claude Code or Antigravity sessions.
    """
    root = _project_root()
    state_path = root / _STATE_FILE
    state: dict = {}
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    state["response_count"] = 0
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return "reminder counter reset"


if __name__ == "__main__":
    mcp.run()
