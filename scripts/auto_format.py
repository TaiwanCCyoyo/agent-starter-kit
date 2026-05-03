import argparse
import subprocess
import sys
from pathlib import Path


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
    parser.add_argument("targets", nargs="*", default=["."], help="Files or directories to check/format (default: current directory).")
    args = parser.parse_args()

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
