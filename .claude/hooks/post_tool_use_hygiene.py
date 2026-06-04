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
    warnings: list[str] = []

    if suffix == ".py":
        # 1. Auto-format (ruff format modifies the file in place; non-zero only on error)
        run(root, ["uv", "run", "ruff", "format", file_path])

        # 2. Lint
        code, stdout, stderr = run(root, ["uv", "run", "ruff", "check", file_path])
        if code != 0:
            checks.append(f"`ruff check` failed on `{rel_path}`.\n" + "\n".join(p for p in [stdout, stderr] if p))

        # 3. Type check
        code, stdout, stderr = run(root, ["uv", "run", "mypy", file_path, "--ignore-missing-imports"])
        if code != 0:
            checks.append(f"`mypy` failed on `{rel_path}`.\n" + "\n".join(p for p in [stdout, stderr] if p))

        # 4. Warn on print() usage (project uses logging); exclude comments and string literals
        code, stdout, _ = run(root, ["grep", "-nE", r"(^|[^.#\w])print\(", file_path])
        if code == 0 and stdout:
            warnings.append(f"`print()` found in `{rel_path}` — use `logging` instead:\n{stdout}")

    if suffix in {".md", ".py", ".toml", ".json", ".yaml", ".yml"}:
        code, stdout, stderr = run(root, ["uv", "run", "python", "scripts/file_hygiene.py", "--file", rel_path])
        if code != 0:
            checks.append(f"`file_hygiene` failed on `{rel_path}`.\n" + "\n".join(p for p in [stdout, stderr] if p))

    if checks:
        msg = "\n\n".join(checks)
        if warnings:
            msg += "\n\n⚠️ Warnings:\n" + "\n".join(warnings)
        print(json.dumps({"systemMessage": msg, "continue": False, "stopReason": "Claude Code post-edit hygiene check failed."}))
    elif warnings:
        print(json.dumps({"systemMessage": "⚠️ Warnings:\n" + "\n".join(warnings)}))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
