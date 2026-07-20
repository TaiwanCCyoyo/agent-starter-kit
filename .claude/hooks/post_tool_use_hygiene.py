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
import os
import re
import subprocess
import sys
from pathlib import Path

from identify.identify import tags_from_filename

# Formatters with a fixed, narrow scope get an explicit mapping. Every other
# text file falls through to `prettier`, which uses --ignore-unknown to no-op
# on any extension it doesn't support — so new prettier-supported languages
# (ts, html, css, ...) never need a new entry here.
FORMATTER_HOOKS: dict[str, tuple[str, ...]] = {".py": ("ruff", "ruff-format"), ".toml": ("taplo-format",)}
DEFAULT_FORMATTER_HOOKS: tuple[str, ...] = ("prettier",)

# Mirrors the `file-validation` hook's `exclude` in .pre-commit-config.yaml so
# the Claude hook and pre-commit agree on which files skip the English/UTF-8 check.
FILE_VALIDATION_EXCLUDE = re.compile(r"^(uv\.lock|.*\.json)$")


def is_text_file(rel_path: str) -> bool:
    """Return True for files pre-commit would classify with the `text` tag.

    Delegates to `identify` (a pre-commit dependency) instead of hand-maintaining
    a suffix allowlist, so this stays in sync with the `types: [text]` filters
    already used in .pre-commit-config.yaml.
    """
    return "text" in tags_from_filename(rel_path)


def repo_root(cwd: str) -> Path:
    """Return the main repo root, anchored to CLAUDE_PROJECT_DIR when available.

    Claude Code exports CLAUDE_PROJECT_DIR to hook subprocesses pointing at the
    main project root. Preferring it over `git rev-parse --show-toplevel`
    keeps hygiene checks anchored to the main repo even when the session cwd
    drifts into a nested git submodule (e.g. shioaji_stock_prices, which has
    its own .git and would otherwise resolve to the wrong repo root).
    """
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_dir:
        path = Path(project_dir)
        if path.is_dir():
            return path.resolve()

    try:
        root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=cwd, text=True, encoding="utf-8").strip()
        return Path(root)
    except Exception:
        return Path(cwd).resolve()


def run(root: Path, args: list[str]) -> tuple[int, str, str]:
    """Run a hygiene command from the repo root and normalize text output."""
    result = subprocess.run(args, cwd=root, text=True, capture_output=True, encoding="utf-8", errors="replace")
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def run_hook(root: Path, hook: str, rel_path: str) -> tuple[int, str, str]:
    """Run a targeted pre-commit hook, retrying after an expected rewrite."""
    args = ["uv", "run", "pre-commit", "run", hook, "--files", rel_path]
    code, stdout, stderr = run(root, args)
    if code == 1 and "files were modified by this hook" in stdout:
        return run(root, args)
    return code, stdout, stderr


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

    files = [f for f in event_files(event, root) if is_text_file(f)]
    for rel_path in dict.fromkeys(files):
        suffix = Path(rel_path).suffix.lower()

        for formatter_hook in FORMATTER_HOOKS.get(suffix, DEFAULT_FORMATTER_HOOKS):
            code, stdout, stderr = run_hook(root, formatter_hook, rel_path)
            if code != 0:
                checks.append(f"`{formatter_hook}` failed on `{rel_path}`.\n" + "\n".join(part for part in [stdout, stderr] if part))

        if FILE_VALIDATION_EXCLUDE.match(rel_path):
            continue

        code, stdout, stderr = run_hook(root, "file-validation", rel_path)
        if code != 0:
            checks.append(f"`file-validation` failed on `{rel_path}`.\n" + "\n".join(part for part in [stdout, stderr] if part))

    if checks:
        message = "\n\n".join(checks)
        sys.stdout.write(json.dumps({"decision": "block", "reason": message}) + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
