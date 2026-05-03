import json
import subprocess
import sys
from pathlib import Path


def hook_file_path(event: dict) -> str:
    tool_input = event.get("tool_input", {})
    return tool_input.get("file_path") or tool_input.get("TargetFile") or ""


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        print(json.dumps({}))
        return 0

    file_path = hook_file_path(event)
    tool_response = event.get("tool_response", {})
    if file_path and file_path.endswith(".py") and not tool_response.get("error") and Path(file_path).exists():
        subprocess.run(["uv", "run", "python", "./scripts/auto_format.py", file_path], check=False)

    print(json.dumps({}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
