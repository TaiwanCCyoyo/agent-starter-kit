"""Run targeted hygiene checks after Claude Code edit tools.

Expected PostToolUse payload shapes:

Write and Edit tools provide a single direct path:

{
  "cwd": "C:/repo",
  "tool_name": "Write",
  "tool_input": {"file_path": "docs/example.md", ...}
}

Some batch-style tools may provide multiple paths under list fields:

{
  "cwd": "C:/repo",
  "tool_name": "MultiEdit",
  "tool_input": {"files": ["docs/a.md", "src/b.py"], ...}
}

Design note — two-tier file resolution:

1. Explicit paths (preferred): when tool_input advertises one or more file
   paths, only those files are checked. This is the fast, precise path.

2. Dirty-worktree fallback: when no paths can be extracted (unexpected JSON
   shape or a tool that doesn't report its target), the hook falls back to
   `git status --porcelain`. This ensures hygiene still runs even if the
   event format changes, so the hook never silently becomes a no-op.
"""

import io
import json
import subprocess
import sys
from pathlib import Path

TEXT_SUFFIXES = {".md", ".py", ".toml", ".json", ".yaml", ".yml"}


def repo_root(cwd: str) -> Path:
    """Return the Git repository root for the hook cwd, or cwd itself."""
    try:
        root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=cwd, text=True, encoding="utf-8").strip()
        return Path(root)
    except Exception:
        return Path(cwd).resolve()


def run(root: Path, args: list[str]) -> tuple[int, str, str]:
    """Run a hygiene command from the repo root and normalize text output."""
    result = subprocess.run(args, cwd=root, text=True, capture_output=True, encoding="utf-8", errors="replace")
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def to_relative_path(root: Path, file_path: str) -> str:
    """Convert an absolute or repo-local path to a POSIX repo-relative path."""
    path = Path(file_path)
    try:
        return path.resolve().relative_to(root).as_posix()
    except (OSError, ValueError):
        return path.as_posix()


def changed_files(root: Path) -> list[str]:
    """Return all dirty tracked files from git status as a fallback list."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=root,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    files: list[str] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1].strip()
        if path and (root / path).is_file():
            files.append(path)
    return files


def event_files(event: dict, root: Path) -> list[str]:
    """Return files to check for this post-tool event.

    Prefer paths explicitly listed in tool_input (fast, precise). Fall back to
    changed_files() only when tool_input carries no recognisable path — this
    keeps the hook alive if the event JSON format is unexpected.
    """
    tool_input = event.get("tool_input") or {}
    files: list[str] = []

    if isinstance(tool_input, dict):
        # Write/Edit-style tools commonly pass a single file_path.
        file_path = tool_input.get("file_path")
        if isinstance(file_path, str) and file_path:
            files.append(file_path)

        # Small allowlist for batch-style path fields without scanning Git.
        for key in ("files", "file_paths", "paths"):
            value = tool_input.get(key)
            if isinstance(value, list):
                files.extend(item for item in value if isinstance(item, str))

    # Deleted files and non-text paths are filtered by the caller after this.
    existing_files: list[str] = []
    for file_path in files:
        rel_path = to_relative_path(root, file_path)
        if (root / rel_path).is_file() or Path(file_path).is_file():
            existing_files.append(rel_path)

    return existing_files or changed_files(root)


def main() -> int:
    """Read a PostToolUse event from stdin and emit blocking JSON on failure."""
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if isinstance(sys.stderr, io.TextIOWrapper):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0

    root = repo_root(event.get("cwd") or ".")
    if not root.exists():
        return 0

    checks: list[str] = []

    files = [f for f in event_files(event, root) if Path(f).suffix.lower() in TEXT_SUFFIXES]
    for rel_path in dict.fromkeys(files):
        suffix = Path(rel_path).suffix.lower()

        if suffix == ".py":
            code, stdout, stderr = run(root, ["uv", "run", "ruff", "format", rel_path])
            if code != 0:
                checks.append(f"`ruff format` failed on `{rel_path}`.\n" + "\n".join(part for part in [stdout, stderr] if part))

            code, stdout, stderr = run(root, ["uv", "run", "ruff", "check", "--fix", rel_path])
            if code != 0:
                checks.append(f"`ruff check --fix` failed on `{rel_path}`.\n" + "\n".join(part for part in [stdout, stderr] if part))

        code, stdout, stderr = run(root, ["uv", "run", "python", "scripts/file_hygiene.py", "--file", rel_path])
        if code != 0:
            checks.append(f"`file_hygiene` failed on `{rel_path}`.\n" + "\n".join(part for part in [stdout, stderr] if part))

    if checks:
        message = "\n\n".join(checks)
        sys.stdout.write(json.dumps({"decision": "block", "reason": message}) + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
