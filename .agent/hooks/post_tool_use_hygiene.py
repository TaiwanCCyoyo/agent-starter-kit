import json
import subprocess
import sys
from pathlib import Path

TEXT_SUFFIXES = {".json", ".md", ".py", ".toml", ".yaml", ".yml"}


def repo_root(cwd: str) -> Path:
    try:
        root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd,
            text=True,
            encoding="utf-8",
        ).strip()
        return Path(root)
    except Exception:
        return Path(cwd).resolve()


def run(root: Path, args: list[str]) -> tuple[int, str]:
    result = subprocess.run(args, cwd=root, text=True, capture_output=True)
    output = "\n".join(part.strip() for part in (result.stdout, result.stderr) if part.strip())
    return result.returncode, output


def changed_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    files: list[str] = []
    for line in result.stdout.splitlines():
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1].strip()
        if path and (root / path).is_file():
            files.append(path)
    return files


def event_files(event: dict, root: Path) -> list[str]:
    tool_input = event.get("tool_input") or event.get("toolInput") or {}
    candidates: list[str] = []
    for key in ("file_path", "filePath"):
        value = tool_input.get(key)
        if isinstance(value, str):
            candidates.append(value)
    for key in ("files", "file_paths", "filePaths", "paths"):
        value = tool_input.get(key)
        if isinstance(value, list):
            candidates.extend(item for item in value if isinstance(item, str))

    relative: list[str] = []
    for candidate in candidates:
        path = Path(candidate)
        if not path.is_absolute():
            path = root / path
        try:
            path = path.resolve().relative_to(root)
        except (OSError, ValueError):
            pass
        rel_path = path.as_posix()
        if (root / rel_path).is_file():
            relative.append(rel_path)
    return relative or changed_files(root)


def main() -> int:
    try:
        import datetime
        from pathlib import Path

        root = repo_root(".")
        log_path = root / "hook_debug.log"
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now()}] post_tool_use_hygiene.py executed\n")
    except Exception:
        pass

    try:
        event = json.load(sys.stdin)
    except Exception:
        event = {}

    root = repo_root(event.get("cwd") or ".")
    failures: list[str] = []
    files = [path for path in dict.fromkeys(event_files(event, root)) if Path(path).suffix.lower() in TEXT_SUFFIXES]

    for rel_path in files:
        if Path(rel_path).suffix.lower() == ".py":
            for args in (
                ["uv", "run", "ruff", "format", rel_path],
                ["uv", "run", "ruff", "check", rel_path],
                ["uv", "run", "mypy", rel_path],
            ):
                code, output = run(root, args)
                if code != 0:
                    command = " ".join(args[2:])
                    failures.append(f"`{command}` failed for `{rel_path}`.\n{output}")

        code, output = run(
            root,
            ["uv", "run", "python", "scripts/file_hygiene.py", "--file", rel_path],
        )
        if code != 0:
            failures.append(f"`file_hygiene` failed for `{rel_path}`.\n{output}")

    if failures:
        sys.stdout.write("\n\n".join(failures) + "\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
