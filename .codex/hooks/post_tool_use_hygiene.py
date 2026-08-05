"""Report high-value Ruff correctness diagnostics after Codex edits."""

import json
import re
import subprocess
import sys
from pathlib import Path

PYTHON_SUFFIXES = {".py", ".pyi"}
RUFF_ARGS = (
    "ruff",
    "check",
    "--select",
    "F",
    "--ignore",
    "F401,F841,F842",
    "--output-format",
    "concise",
)
PATCH_FILE_RE = re.compile(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$")
PATCH_MOVE_RE = re.compile(r"^\*\*\* Move to: (.+)$")


def repo_root(cwd: str) -> Path:
    """Return the Git repository root for the hook cwd."""
    try:
        root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd,
            text=True,
            encoding="utf-8",
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return Path(cwd).resolve()
    return Path(root).resolve()


def run(root: Path, args: list[str]) -> tuple[int, str, str]:
    """Run a project command without invoking a shell."""
    try:
        result = subprocess.run(
            args,
            cwd=root,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
    except OSError as exc:
        return 127, "", str(exc)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def to_relative_path(root: Path, file_path: str) -> str:
    """Convert a direct event path to a safe repository-relative POSIX path."""
    path = Path(file_path)
    if not path.is_absolute():
        path = root / path
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except (OSError, ValueError):
        return ""


def patch_files(patch_text: str) -> list[str]:
    """Extract file targets from apply_patch header lines."""
    files: list[str] = []
    for line in patch_text.splitlines():
        match = PATCH_FILE_RE.match(line) or PATCH_MOVE_RE.match(line)
        if match:
            files.append(match.group(1).strip())
    return files


def string_values(value: object) -> list[str]:
    """Collect strings from nested tool input values."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [item for child in value.values() for item in string_values(child)]
    if isinstance(value, list):
        return [item for child in value for item in string_values(child)]
    return []


def event_files(event: dict[str, object], root: Path) -> list[str]:
    """Extract only explicit existing file paths from a Codex event."""
    tool_input = event.get("tool_input") or {}
    candidates: list[str] = []
    if isinstance(tool_input, dict):
        file_path = tool_input.get("file_path")
        if isinstance(file_path, str) and file_path:
            candidates.append(file_path)
        for key in ("files", "file_paths", "paths"):
            value = tool_input.get(key)
            if isinstance(value, list):
                candidates.extend(item for item in value if isinstance(item, str))
        for value in string_values(tool_input):
            if "*** Begin Patch" in value:
                candidates.extend(patch_files(value))

    files: list[str] = []
    for candidate in candidates:
        rel_path = to_relative_path(root, candidate)
        if rel_path and (root / rel_path).is_file():
            files.append(rel_path)
    return list(dict.fromkeys(files))


def main() -> int:
    """Emit Codex diagnostics without modifying files."""
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, TypeError, ValueError):
        return 0
    if not isinstance(event, dict):
        return 0

    root = repo_root(str(event.get("cwd") or "."))
    if not root.is_dir():
        return 0

    diagnostics: list[str] = []
    for rel_path in event_files(event, root):
        if Path(rel_path).suffix.lower() not in PYTHON_SUFFIXES:
            continue
        code, stdout, stderr = run(root, ["uv", "run", "--project", str(root), *RUFF_ARGS, rel_path])
        if code == 0:
            continue
        details = "\n".join(part for part in (stdout, stderr) if part)
        diagnostics.append(f"`ruff check` failed on `{rel_path}`.\n{details}".rstrip())

    if diagnostics:
        sys.stdout.write(
            json.dumps({
                "systemMessage": "\n\n".join(diagnostics),
                "continue": False,
                "stopReason": "Codex post-edit Ruff check failed.",
            })
            + "\n"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
