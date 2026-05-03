import argparse
import os
import re
import sys
from pathlib import Path

# CJK Unified Ideographs plus common CJK punctuation (indicates non-English content or Mojibake)
CJK_RE = re.compile(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]")

# Paths where non-English content is EXPLICITLY allowed
ALLOWED_PATHS = [
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
    Validates file encoding and language constraints.
    Returns True if valid, False if invalid.
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

    # 2. Language Check (If NOT in allowed paths)
    if not is_path_allowed(filepath):
        eval_lines = content.splitlines()
        start_index = 0
        if basename.lower() == "readme.md":
            # README.md allows a Traditional Chinese link on the first line.
            start_index = 1

        for i in range(start_index, len(eval_lines)):
            line = eval_lines[i]
            if CJK_RE.search(line):
                # Double-check: If the file IS actually allowed but prefix matching missed it,
                # this would still trigger. But based on is_path_allowed, we skip this whole block.
                print(f"Error: Non-English (CJK) character or Mojibake found in {filepath} at line {i + 1}:")
                print(f"  > {line.strip()}")
                print("Note: If this is intentional, move the content to an allowed path (docs/zh-TW/ or .agents/memory/).")
                return False
    else:
        # In allowed paths, we already did the UTF-8 encoding check above.
        # This prevents Traditional Chinese from being flagged as "Mojibake"
        # simply because they are non-ASCII.
        pass

    return True


def main():
    parser = argparse.ArgumentParser(description="File Hygiene Tool: Validates encoding, language, and cleanliness.")
    parser.add_argument("--file", nargs="+", dest="files", required=True, help="Specific files to check.")
    args = parser.parse_args()

    failed = False
    for f in args.files:
        if not check_file_hygiene(f):
            failed = True

    if failed:
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
