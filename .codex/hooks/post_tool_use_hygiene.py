import json
import subprocess
import sys
from pathlib import Path


def repo_root(cwd: str) -> Path:
    try:
        root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=cwd, text=True, encoding="utf-8").strip()
        return Path(root)
    except Exception:
        return Path(cwd).resolve()


def run(root: Path, args: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(args, cwd=root, text=True, capture_output=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0

    root = repo_root(event.get("cwd") or ".")
    if not root.exists():
        return 0

    checks: list[str] = []

    code, stdout, stderr = run(root, ["uv", "run", "ruff", "check", "."])
    if code != 0:
        checks.append("`uv run ruff check .` failed.\n" + "\n".join(part for part in [stdout, stderr] if part))

    changed = subprocess.run(["git", "diff", "--name-only"], cwd=root, text=True, capture_output=True)
    files = [line.strip() for line in changed.stdout.splitlines() if line.strip()]
    text_files = [f for f in files if Path(f).suffix.lower() in {".md", ".py", ".toml", ".json", ".yaml", ".yml"}]
    if text_files:
        code, stdout, stderr = run(root, ["uv", "run", "python", "scripts/file_hygiene.py", "--file", *text_files])
        if code != 0:
            checks.append("`uv run python scripts/file_hygiene.py --file ...` failed.\n" + "\n".join(part for part in [stdout, stderr] if part))

    if checks:
        print(json.dumps({"systemMessage": "\n\n".join(checks), "continue": False, "stopReason": "Codex post-edit hygiene check failed."}))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
