import sys
import json
import subprocess
from pathlib import Path


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        print(json.dumps({}))
        return

    tool_input = data.get("tool_input", {})
    tool_response = data.get("tool_response", {})

    file_path = tool_input.get("file_path")

    if file_path and file_path.endswith(".py") and not tool_response.get("error"):
        path = Path(file_path)
        if path.exists():
            # Run lint fix
            subprocess.run(["uv", "run", "ruff", "check", "--fix", str(path)], capture_output=True)
            # Run formatting
            subprocess.run(["uv", "run", "ruff", "format", str(path)], capture_output=True)

    print(json.dumps({}))


if __name__ == "__main__":
    main()
