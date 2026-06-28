"""Run targeted hygiene checks after Codex edit tools.

Expected PostToolUse payload shapes:

Write/Edit-style tools usually provide one direct path:

{
  "cwd": "C:/repo",
  "tool_name": "Write",
  "tool_input": {"file_path": "docs/example.md"}
}

Some tools may provide multiple direct paths:

{
  "cwd": "C:/repo",
  "tool_name": "Edit",
  "tool_input": {"files": ["docs/a.md", "src/b.py"]}
}

Codex apply_patch provides patch text rather than a direct file_path. The hook
extracts targets from patch headers:

{
  "cwd": "C:/repo",
  "tool_name": "apply_patch",
  "tool_input": {
    "cmd": "*** Begin Patch\n*** Update File: docs/example.md\n*** End Patch\n"
  }
}

Design note — two-tier file resolution:

1. Explicit paths (preferred): when tool_input advertises one or more file
   paths (or patch headers), only those files are checked. This is the fast,
   precise path.

2. Dirty-worktree fallback: when no paths can be extracted (unexpected JSON
   shape or a tool that doesn't report its target), the hook falls back to
   `git status --porcelain`. This ensures hygiene still runs even if the
   event format changes, so the hook never silently becomes a no-op.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

TEXT_SUFFIXES = {".md", ".py", ".toml", ".json", ".yaml", ".yml"}
PATCH_FILE_RE = re.compile(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$")
PATCH_MOVE_RE = re.compile(r"^\*\*\* Move to: (.+)$")


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


def patch_files(patch_text: str) -> list[str]:
    """Extract file targets from apply_patch header lines."""
    files: list[str] = []
    for line in patch_text.splitlines():
        match = PATCH_FILE_RE.match(line) or PATCH_MOVE_RE.match(line)
        if match:
            files.append(match.group(1).strip())
    return files


def string_values(value: object) -> list[str]:
    """Collect strings from unknown nested tool_input JSON structures."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        strings: list[str] = []
        for item in value.values():
            strings.extend(string_values(item))
        return strings
    if isinstance(value, list):
        strings = []
        for item in value:
            strings.extend(string_values(item))
        return strings
    return []


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

    Prefer paths explicitly listed in tool_input or patch headers (fast,
    precise). Fall back to changed_files() only when tool_input carries no
    recognisable path — this keeps the hook alive if the event JSON format
    is unexpected.
    """
    tool_input = event.get("tool_input") or {}
    files: list[str] = []
    if isinstance(tool_input, dict):
        # Write/Edit-style tools commonly pass a single file_path.
        file_path = tool_input.get("file_path")
        if isinstance(file_path, str) and file_path:
            files.append(file_path)

        # Keep a small allowlist for batch-style path fields without scanning Git.
        for key in ("files", "file_paths", "paths"):
            value = tool_input.get(key)
            if isinstance(value, list):
                files.extend(item for item in value if isinstance(item, str))

    # apply_patch can place patch text under different tool_input keys, so scan
    # all nested string values for patch headers instead of depending on one key.
    for value in string_values(tool_input):
        if "*** Begin Patch" in value:
            files.extend(patch_files(value))

    # Deleted files and non-text paths are ignored by callers after this point.
    existing_files: list[str] = []
    for file_path in files:
        rel_path = to_relative_path(root, file_path)
        if (root / rel_path).is_file() or Path(file_path).is_file():
            existing_files.append(rel_path)

    return existing_files or changed_files(root)


def main() -> int:
    """Read a PostToolUse event from stdin and emit blocking JSON on failure."""
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
        sys.stdout.write(json.dumps({"systemMessage": message, "continue": False, "stopReason": "Codex post-edit hygiene check failed."}) + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
