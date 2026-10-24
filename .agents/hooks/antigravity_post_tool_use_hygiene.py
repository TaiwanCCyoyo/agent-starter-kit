"""Report high-value Ruff correctness diagnostics after Antigravity edits."""

import io
import json
import logging
import subprocess
import sys
from pathlib import Path

LOGGER = logging.getLogger("antigravity_post_tool_use_hygiene")
PYTHON_SUFFIXES = {".py", ".pyi"}
RUFF_ARGS = (
    "ruff",
    "check",
    "--no-fix",
    "--select",
    "F",
    "--ignore",
    "F401,F841,F842",
    "--output-format",
    "concise",
)


def repo_root(cwd: str) -> Path:
    """Return the Git repository root for the hook workspace directory."""
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
            timeout=15,
        )
    except subprocess.TimeoutExpired:
        return 124, "", "Post-edit Ruff check exceeded 15 seconds; run targeted verification before completion."
    except OSError as exc:
        return 127, "", str(exc)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def clean_path_value(raw: str) -> str:
    """Strip optional protojson/transcript wrapping quotes from a path string."""
    value = raw.strip()
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        try:
            unquoted = json.loads(value)
            if isinstance(unquoted, str):
                return unquoted.strip()
        except (json.JSONDecodeError, TypeError, ValueError):
            return value[1:-1].strip()
    return value


def to_relative_path(root: Path, file_path: str) -> str:
    """Convert a direct event path to a safe repository-relative POSIX path."""
    cleaned = clean_path_value(file_path)
    if not cleaned:
        return ""
    path = Path(cleaned)
    if not path.is_absolute():
        path = root / path
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except (OSError, ValueError):
        return ""


def collect_dict_paths(mapping: dict[str, object]) -> list[str]:
    """Extract candidate file path strings from a tool argument mapping."""
    candidates: list[str] = []
    for key in ("Path", "TargetFile", "file_path", "path"):
        value = mapping.get(key)
        if isinstance(value, str) and value:
            candidates.append(value)
    for key in ("Paths", "files", "file_paths", "paths"):
        value = mapping.get(key)
        if isinstance(value, list):
            candidates.extend(item for item in value if isinstance(item, str) and item)
    return candidates


def event_workspace(event: dict[str, object]) -> str:
    """Resolve the active workspace path from an Antigravity hook payload."""
    workspace_paths = event.get("workspacePaths")
    if isinstance(workspace_paths, list):
        for item in workspace_paths:
            if isinstance(item, str) and item.strip():
                return item.strip()
    cwd = event.get("cwd")
    if isinstance(cwd, str) and cwd.strip():
        return cwd.strip()
    return "."


def event_files(event: dict[str, object], root: Path) -> list[str]:
    """Extract only explicit existing file paths from an Antigravity event."""
    candidates: list[str] = []
    tool_call = event.get("toolCall")
    if isinstance(tool_call, dict):
        args = tool_call.get("args")
        if isinstance(args, dict):
            candidates.extend(collect_dict_paths(args))

    tool_input = event.get("tool_input")
    if isinstance(tool_input, dict):
        candidates.extend(collect_dict_paths(tool_input))

    files: list[str] = []
    for candidate in candidates:
        rel_path = to_relative_path(root, candidate)
        if rel_path and (root / rel_path).is_file():
            files.append(rel_path)
    return list(dict.fromkeys(files))


def main() -> int:
    """Emit Antigravity PostToolUse response and log Ruff diagnostics without modifying files."""
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if isinstance(sys.stderr, io.TextIOWrapper):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=[logging.StreamHandler(sys.stderr)], force=True)

    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, TypeError, ValueError):
        return 0
    if not isinstance(event, dict):
        return 0

    root = repo_root(event_workspace(event))
    if not root.is_dir():
        sys.stdout.write("{}\n")
        return 0

    files = [path for path in event_files(event, root) if Path(path).suffix.lower() in PYTHON_SUFFIXES]
    if files:
        code, stdout, stderr = run(root, ["uv", "run", "--no-sync", "--project", str(root), *RUFF_ARGS, "--", *files])
        if code != 0:
            details = "\n".join(part for part in (stdout, stderr) if part)
            LOGGER.warning("Post-edit Ruff diagnostics; fix relevant issues before completion.\n%s", details.rstrip())

    sys.stdout.write("{}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
