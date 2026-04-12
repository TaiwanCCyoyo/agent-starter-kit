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


def check_file_hygiene(filepath):
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

    # 2. Trailing Whitespace Cleanup
    lines = content.splitlines(keepends=True)
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
            print(f"Hygiene: Removed trailing whitespace in {filepath}")
            # Even if cleaned, we return False to inform pre-commit that the file was modified
            # and needs to be re-staged.
            return False
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

    return True


def main():
    parser = argparse.ArgumentParser(description="File Hygiene Tool: Validates encoding, language, and cleanliness.")
    parser.add_argument("--hook", action="store_true", help="Run in Hook mode, reading JSON from stdin for Gemini CLI.")
    parser.add_argument("files", nargs="*", help="Specific files to check.")

    args = parser.parse_args()
    files = args.files

    if args.hook:
        # Piped mode (Gemini Hook)
        try:
            content = sys.stdin.read()
            if not content:
                # Silent return for Gemini CLI
                return
            data = json.loads(content)
            file_path = data.get("tool_input", {}).get("file_path") or data.get("tool_input", {}).get("TargetFile")
            if file_path:
                files = [file_path]
        except Exception:
            # Fallback to empty if stdin parsing fails
            pass

    if not files:
        # No files provided, and not in hook mode or stdin empty
        if not args.hook:
            print("Usage: python file_hygiene.py <file1> <file2> ... or use --hook for Gemini CLI.")
        sys.exit(0)

    failed = False
    for f in files:
        if not check_file_hygiene(f):
            failed = True

    if failed:
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
