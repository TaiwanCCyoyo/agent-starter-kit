"""
Launch the SQLite MCP server pointed at this project's memory database.

Path resolution: this file lives at .claude/scripts/start_memory_mcp.py
  parent        = .claude/scripts/
  parent.parent = .claude/
  parent.parent.parent = project root
"""

import subprocess
import sys
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).resolve().parent.parent.parent
    db_path = project_root / ".agents" / "memory" / "memory.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        ["uvx", "mcp-server-sqlite", "--db-path", str(db_path)],
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
