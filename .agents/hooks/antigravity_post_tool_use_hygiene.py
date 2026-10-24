"""Report high-value Ruff correctness diagnostics after Antigravity edits."""

import io
import json
import logging
import os
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
    if "\\" in cleaned and os.sep != "\\":
        cleaned = cleaned.replace("\\", "/")
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


def event_workspaces(event: dict[str, object]) -> list[str]:
    """Resolve all candidate workspace paths from an Antigravity hook payload."""
    workspaces: list[str] = []
    workspace_paths = event.get("workspacePaths")
    if isinstance(workspace_paths, list):
        for item in workspace_paths:
            if isinstance(item, str) and item.strip():
                workspaces.append(item.strip())
    cwd = event.get("cwd")
    if isinstance(cwd, str) and cwd.strip():
        workspaces.append(cwd.strip())
    if not workspaces:
        workspaces.append(".")
    return list(dict.fromkeys(workspaces))


def workspace_roots(event: dict[str, object]) -> list[Path]:
    """Return deduplicated existing repository roots for the event workspaces."""
    roots: list[Path] = []
    seen: set[Path] = set()
    for workspace in event_workspaces(event):
        root = repo_root(workspace)
        if not root.is_dir():
            continue
        resolved = root.resolve()
        if resolved not in seen:
            seen.add(resolved)
            roots.append(root)
    return roots


def event_candidates(event: dict[str, object]) -> list[str]:
    """Extract candidate file path strings from an Antigravity event."""
    candidates: list[str] = []
    tool_call = event.get("toolCall")
    if isinstance(tool_call, dict):
        args = tool_call.get("args")
        if isinstance(args, dict):
            candidates.extend(collect_dict_paths(args))

    tool_input = event.get("tool_input")
    if isinstance(tool_input, dict):
        candidates.extend(collect_dict_paths(tool_input))
    return candidates


def event_files(event: dict[str, object], root: Path) -> list[str]:
    """Extract only explicit existing file paths from an Antigravity event for a single root."""
    files: list[str] = []
    for candidate in event_candidates(event):
        rel_path = to_relative_path(root, candidate)
        if rel_path and (root / rel_path).is_file():
            files.append(rel_path)
    return list(dict.fromkeys(files))


def files_by_workspace(event: dict[str, object], roots: list[Path]) -> list[tuple[Path, list[str]]]:
    """Group existing Python files by their most specific owning workspace root."""
    grouped: dict[Path, list[str]] = {root: [] for root in roots}
    for candidate in event_candidates(event):
        cleaned = clean_path_value(candidate)
        if not cleaned:
            continue
        if "\\" in cleaned and os.sep != "\\":
            cleaned = cleaned.replace("\\", "/")
        is_abs = Path(cleaned).is_absolute()
        matches: list[tuple[Path, str]] = []
        for root in roots:
            rel_path = to_relative_path(root, cleaned)
            if rel_path and (root / rel_path).is_file() and Path(rel_path).suffix.lower() in PYTHON_SUFFIXES:
                matches.append((root, rel_path))
                if not is_abs:
                    break
        if not matches:
            continue
        chosen_root, chosen_rel = max(matches, key=lambda item: len(item[0].resolve().parts))
        if chosen_rel not in grouped[chosen_root]:
            grouped[chosen_root].append(chosen_rel)
    return [(root, files) for root, files in grouped.items() if files]


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

    roots = workspace_roots(event)
    if not roots:
        sys.stdout.write("{}\n")
        return 0

    for root, files in files_by_workspace(event, roots):
        code, stdout, stderr = run(root, ["uv", "run", "--no-sync", "--project", str(root), *RUFF_ARGS, "--", *files])
        if code != 0:
            details = "\n".join(part for part in (stdout, stderr) if part)
            LOGGER.warning("Post-edit Ruff diagnostics; fix relevant issues before completion.\n%s", details.rstrip())

    sys.stdout.write("{}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
