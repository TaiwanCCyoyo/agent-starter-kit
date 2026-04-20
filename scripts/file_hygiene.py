import sys
import re
import os
import argparse
import json
from pathlib import Path

# CJK Unified Ideographs plus common CJK punctuation (indicates non-English content or Mojibake)
CJK_RE = re.compile(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]")

# Paths where non-English content is EXPLICITLY allowed
ALLOWED_PATHS = [
    ".agents/memory/",
    "docs/zh-TW/",
]


def is_path_allowed(filepath):
    """
    Checks if the given file path is in a directory allowed to contain non-English characters.
    """
    norm_path = Path(filepath).as_posix()
    for allowed in ALLOWED_PATHS:
        if norm_path.startswith(allowed):
            return True
    return False


def get_sync_targets(filepath):
    """
    Identifies related documentation files that may need synchronization.
    """
    path = Path(filepath).as_posix()
    targets = []

    # Case 1: Root README.md modified -> check all docs/*/README.md
    if path == "README.md":
        docs_dir = Path("docs")
        if docs_dir.exists():
            for lang_dir in docs_dir.iterdir():
                if lang_dir.is_dir():
                    target = lang_dir / "README.md"
                    if target.exists():
                        targets.append(target.as_posix())

    # Case 2: docs/<lang>/<filename> modified
    elif path.startswith("docs/"):
        parts = Path(path).parts
        if len(parts) >= 3:
            current_lang = parts[1]
            filename = "/".join(parts[2:])

            # 2a. Check root README if it's a README
            if filename.lower() == "readme.md":
                targets.append("README.md")

            # 2b. Check other languages in docs/
            docs_dir = Path("docs")
            for lang_dir in docs_dir.iterdir():
                if lang_dir.is_dir() and lang_dir.name != current_lang:
                    target = lang_dir / filename
                    if target.exists():
                        targets.append(target.as_posix())

    return targets


def check_file_hygiene(filepath, is_hook=False):
    """
    Validates file encoding, language constraints, and cleans up hygiene issues.
    Returns True if valid and unchanged, False if invalid or modified.
    """
    basename = os.path.basename(filepath)
    if not os.path.exists(filepath):
        return True

    # 1. Encoding Check (Must be UTF-8)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"Error: {filepath} is NOT valid UTF-8. Please ensure file encoding is UTF-8 (without BOM).")
        return False
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    # 2. Trailing Whitespace Cleanup (ONLY in hook mode)
    lines = content.splitlines(keepends=True)
    new_lines = lines
    if is_hook:
        new_lines = []
        modified = False
        for line in lines:
            # Detect the line ending
            if line.endswith("\r\n"):
                ending = "\r\n"
            elif line.endswith("\n"):
                ending = "\n"
            else:
                ending = ""

            # Remove trailing spaces/tabs but keep the line ending
            stripped = line.rstrip("\r\n").rstrip(" \t")
            new_line = stripped + ending
            if new_line != line:
                modified = True
            new_lines.append(new_line)

        if modified:
            try:
                with open(filepath, "w", encoding="utf-8", newline="") as f:
                    f.writelines(new_lines)
                print(f"Hygiene: Removed trailing whitespace in {filepath} (Hook Mode)")
                return True
            except Exception as e:
                print(f"Error cleaning whitespace in {filepath}: {e}")
                return False

    # 3. Language Check (If NOT in allowed paths)
    if not is_path_allowed(filepath):
        # We re-evaluate content from new_lines if modified, or just use original
        eval_content = "".join(new_lines)
        eval_lines = eval_content.splitlines()
        start_index = 0
        if basename.lower() == "readme.md":
            # README.md allows a mandatory Chinese link on the first line (per GEMINI.md)
            start_index = 1

        for i in range(start_index, len(eval_lines)):
            line = eval_lines[i]
            if CJK_RE.search(line):
                print(f"Error: Non-English (CJK) character or Mojibake found in {filepath} at line {i + 1}:")
                print(f"  > {line.strip()}")
                return False

    # 4. Universal Documentation Sync Alert
    sync_targets = get_sync_targets(filepath)
    if sync_targets:
        print("\n" + "!" * 60)
        print(f">>> [SYNC ALERT] '{filepath}' was modified.")
        print(">>> Please ensure the following related files are updated:")
        for t in sync_targets:
            print(f"    [ ] {t}")
        print("!" * 60 + "\n")

    return True


def main():
    parser = argparse.ArgumentParser(description="File Hygiene Tool: Validates encoding, language, and cleanliness.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--hook", action="store_true", help="Run in Hook mode, reading JSON from stdin for Gemini CLI.")
    group.add_argument("--file", nargs="+", dest="files", help="Specific files to check (for manual use or pre-commit).")

    args = parser.parse_args()
    files = []

    if args.files:
        files = args.files
    elif args.hook:
        # Piped mode (Gemini Hook). Only read stdin if it's not a terminal to avoid hanging.
        try:
            if not sys.stdin.isatty():
                content = sys.stdin.read()
                if content:
                    data = json.loads(content)
                    file_path = data.get("tool_input", {}).get("file_path") or data.get("tool_input", {}).get("TargetFile")
                    if file_path:
                        files = [file_path]
        except Exception:
            pass

    if not files:
        # If no files found in hook mode or empty --file, exit quietly
        sys.exit(0)

    failed = False
    for f in files:
        if not check_file_hygiene(f, is_hook=args.hook):
            failed = True

    if failed:
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
