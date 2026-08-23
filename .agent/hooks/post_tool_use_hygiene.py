"""Report high-value Ruff correctness diagnostics after Antigravity edits."""

import io
import json
import subprocess
import sys
from pathlib import Path

PYTHON_SUFFIXES = {".py", ".pyi"}
RUFF_ARGS = (
    "ruff",
    "check",
    "--no-fix",
    "--select",
    "E722,F601,F602,F634",
    "--output-format",
    "concise",
)


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
    """Extract explicit existing file paths from an Antigravity event."""
    candidates: list[str] = []

    tool_call = event.get("toolCall") or event.get("tool_call")
    if isinstance(tool_call, dict):
        args = tool_call.get("args")
        if isinstance(args, dict):
            for key in ("TargetFile", "targetFile", "target_file", "file_path", "filePath"):
                val = args.get(key)
                if isinstance(val, str) and val:
                    candidates.append(val)
            for key in ("files", "file_paths", "filePaths", "paths"):
                val = args.get(key)
                if isinstance(val, list):
                    candidates.extend(item for item in val if isinstance(item, str))

    tool_input = event.get("tool_input") or event.get("toolInput")
    if isinstance(tool_input, dict):
        for key in ("TargetFile", "targetFile", "target_file", "file_path", "filePath"):
            val = tool_input.get(key)
            if isinstance(val, str) and val:
                candidates.append(val)
        for key in ("files", "file_paths", "filePaths", "paths"):
            val = tool_input.get(key)
            if isinstance(val, list):
                candidates.extend(item for item in val if isinstance(item, str))

    for key in ("filePath", "file_path", "TargetFile", "target_file"):
        val = event.get(key)
        if isinstance(val, str) and val:
            candidates.append(val)

    files: list[str] = []
    for candidate in candidates:
        rel_path = to_relative_path(root, candidate)
        if rel_path and (root / rel_path).is_file():
            files.append(rel_path)
    return list(dict.fromkeys(files))


def main() -> int:
    """Emit read-only diagnostics without modifying files."""
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, TypeError, ValueError):
        return 0
    if not isinstance(event, dict):
        return 0

    workspace_paths = event.get("workspacePaths") or event.get("workspace_paths")
    default_cwd = "."
    if isinstance(workspace_paths, list) and workspace_paths and isinstance(workspace_paths[0], str):
        default_cwd = workspace_paths[0]

    root = repo_root(str(event.get("cwd") or default_cwd))
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
        sys.stdout.write(json.dumps({"error": "\n\n".join(diagnostics)}) + "\n")
    else:
        sys.stdout.write("{}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
