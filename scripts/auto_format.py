import sys
import json
import subprocess
from pathlib import Path
import argparse


def run_hygiene(target_path):
    """
    Runs ruff check and ruff format on the specified path.
    Prints errors if they occur.
    """
    cmd_check = ["uv", "run", "ruff", "check", "--fix", "--force-exclude", str(target_path)]
    cmd_format = ["uv", "run", "ruff", "format", "--force-exclude", str(target_path)]

    print(f"  -> Executing: {' '.join(cmd_check)}")
    lint_res = subprocess.run(cmd_check, capture_output=True, text=True)

    if lint_res.returncode != 0:
        print(f"  [LINT ERROR] Findings in {target_path}:")
        if lint_res.stdout:
            print(lint_res.stdout, file=sys.stderr)
        if lint_res.stderr:
            print(lint_res.stderr, file=sys.stderr)
    else:
        print(f"  [OK] Lint check/fix passed for {target_path}")

    print(f"  -> Executing: {' '.join(cmd_format)}")
    subprocess.run(cmd_format, capture_output=True)


def main():
    parser = argparse.ArgumentParser(description="Python Hygiene Script: Automated formatting & linting.")
    parser.add_argument("--hook", action="store_true", help="Run in Hook mode, reading JSON from stdin.")
    parser.add_argument("targets", nargs="*", default=["."], help="Files or directories to check/format (default: current directory).")

    args = parser.parse_args()

    if args.hook:
        # Piped mode (Gemini Hook)
        try:
            content = sys.stdin.read()
            if not content:
                # Always output empty JSON for Gemini compatibility
                print(json.dumps({}))
                return
            data = json.loads(content)
        except Exception:
            # Output empty dict if stdin wasn't valid JSON to satisfy the hook
            print(json.dumps({}))
            return

        tool_input = data.get("tool_input", {})
        tool_response = data.get("tool_response", {})
        file_path = tool_input.get("file_path") or tool_input.get("TargetFile")

        if file_path and file_path.endswith(".py") and not tool_response.get("error"):
            path = Path(file_path)
            if path.exists():
                run_hygiene(path)

        print(json.dumps({}))
    else:
        # CLI Mode
        print("=== Python Hygiene CLI Mode ===")
        print(f"Targets: {args.targets}")

        for t in args.targets:
            path = Path(t)
            if path.exists():
                print(f"[*] Processing: {t}")
                run_hygiene(path)
            else:
                print(f"[!] Error: Path not found: {t}", file=sys.stderr)
        print("=== Done ===")


if __name__ == "__main__":
    main()
