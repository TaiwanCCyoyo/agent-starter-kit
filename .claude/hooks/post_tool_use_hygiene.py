import json
import subprocess
import sys
from pathlib import Path

TEXT_SUFFIXES = {".md", ".py", ".toml", ".json", ".yaml", ".yml"}
PRINT_WARNING_EXCLUDED_PREFIXES = (".claude/hooks/", ".codex/hooks/")
PRINT_WARNING_EXCLUDED_FILES = {"scripts/auto_format.py", "scripts/file_hygiene.py"}


def repo_root(cwd: str) -> Path:
    try:
        root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=cwd, text=True, encoding="utf-8").strip()
        return Path(root)
    except Exception:
        return Path(cwd).resolve()


def run(root: Path, args: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(args, cwd=root, text=True, capture_output=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def to_relative_path(root: Path, file_path: str) -> str:
    path = Path(file_path)
    try:
        return path.resolve().relative_to(root).as_posix()
    except (OSError, ValueError):
        return path.as_posix()


def changed_files(root: Path) -> list[str]:
    changed = subprocess.run(["git", "status", "--porcelain"], cwd=root, text=True, capture_output=True)
    files: list[str] = []
    for line in changed.stdout.splitlines():
        if not line.strip():
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1].strip()
        if path and (root / path).is_file():
            files.append(path)
    return files


def event_files(event: dict, root: Path) -> list[str]:
    tool_input = event.get("tool_input") or {}
    file_path = tool_input.get("file_path")
    if isinstance(file_path, str) and file_path:
        rel_path = to_relative_path(root, file_path)
        return [rel_path] if (root / rel_path).is_file() or Path(file_path).is_file() else []

    files: list[str] = []
    for key in ("files", "file_paths", "paths"):
        value = tool_input.get(key)
        if isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    rel_path = to_relative_path(root, item)
                    if (root / rel_path).is_file() or Path(item).is_file():
                        files.append(rel_path)

    return files or changed_files(root)


def should_warn_on_print(rel_path: str) -> bool:
    return not rel_path.startswith(PRINT_WARNING_EXCLUDED_PREFIXES) and rel_path not in PRINT_WARNING_EXCLUDED_FILES


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0

    root = repo_root(event.get("cwd") or ".")
    if not root.exists():
        return 0

    checks: list[str] = []
    warnings: list[str] = []

    files = [f for f in event_files(event, root) if Path(f).suffix.lower() in TEXT_SUFFIXES]
    for rel_path in dict.fromkeys(files):
        suffix = Path(rel_path).suffix.lower()

        if suffix == ".py":
            code, stdout, stderr = run(root, ["uv", "run", "ruff", "format", rel_path])
            if code != 0:
                checks.append(f"`ruff format` failed on `{rel_path}`.\n" + "\n".join(part for part in [stdout, stderr] if part))

            code, stdout, stderr = run(root, ["uv", "run", "ruff", "check", rel_path])
            if code != 0:
                checks.append(f"`ruff check` failed on `{rel_path}`.\n" + "\n".join(part for part in [stdout, stderr] if part))

            if should_warn_on_print(rel_path):
                code, stdout, stderr = run(root, ["uv", "run", "python", "scripts/python_hygiene.py", "--no-print", rel_path])
                if code != 0:
                    warnings.append(f"`python_hygiene` found warnings in `{rel_path}`.\n" + "\n".join(part for part in [stdout, stderr] if part))

        code, stdout, stderr = run(root, ["uv", "run", "python", "scripts/file_hygiene.py", "--file", rel_path])
        if code != 0:
            checks.append(f"`file_hygiene` failed on `{rel_path}`.\n" + "\n".join(part for part in [stdout, stderr] if part))

    if checks:
        message = "\n\n".join(checks)
        if warnings:
            message += "\n\nWarnings:\n" + "\n".join(warnings)
        sys.stdout.write(json.dumps({"systemMessage": message, "continue": False, "stopReason": "Claude Code post-edit hygiene check failed."}) + "\n")
    elif warnings:
        sys.stdout.write(json.dumps({"systemMessage": "Warnings:\n" + "\n".join(warnings)}) + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
