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

    cwd = event.get("cwd") or "."
    root = repo_root(cwd)
    if not root.exists():
        return 0

    file_path = event.get("tool_input", {}).get("file_path", "")
    if not file_path:
        return 0

    # Normalise to relative path for file_hygiene.py (which matches against allowed prefixes)
    try:
        rel_path = Path(file_path).relative_to(root).as_posix()
    except ValueError:
        rel_path = Path(file_path).as_posix()

    suffix = Path(file_path).suffix.lower()
    checks: list[str] = []

    if suffix == ".py":
        code, stdout, stderr = run(root, ["uv", "run", "ruff", "check", file_path])
        if code != 0:
            checks.append(f"`ruff check` failed on `{rel_path}`.\n" + "\n".join(p for p in [stdout, stderr] if p))

    if suffix in {".md", ".py", ".toml", ".json", ".yaml", ".yml"}:
        code, stdout, stderr = run(root, ["uv", "run", "python", "scripts/file_hygiene.py", "--file", rel_path])
        if code != 0:
            checks.append(f"`file_hygiene` failed on `{rel_path}`.\n" + "\n".join(p for p in [stdout, stderr] if p))

    if checks:
        print(json.dumps({"systemMessage": "\n\n".join(checks), "continue": False, "stopReason": "Claude Code post-edit hygiene check failed."}))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
