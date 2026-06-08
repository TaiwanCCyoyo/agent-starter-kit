import argparse
import logging
import os
import re
import sys
from pathlib import Path
from typing import Any

RichHandler: Any
try:
    from rich.logging import RichHandler
except ImportError:
    RichHandler = None

LOGGER = logging.getLogger("file_hygiene")

# CJK Unified Ideographs plus common CJK punctuation (indicates non-English content or Mojibake)
CJK_RE = re.compile(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]")

# Paths where non-English content is EXPLICITLY allowed
ALLOWED_PATHS = [
    ".memories/",
    ".references/",
    ".tmp/",
    "docs/zh-TW/",
]

MARKDOWN_LANGUAGE_LINK_LINES = 5


def is_path_allowed(filepath: str):
    """
    Checks if the given file path is in a directory allowed to contain non-English characters.
    """
    norm_path = Path(filepath).as_posix()
    for allowed in ALLOWED_PATHS:
        if norm_path.startswith(allowed):
            return True
    return False


def check_file_hygiene(filepath: str):
    """
    Validates file encoding and language constraints.
    Returns True if valid, False if invalid.
    """
    if not os.path.exists(filepath):
        return True

    # 1. Encoding Check (Must be UTF-8)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        LOGGER.error("Error: %s is NOT valid UTF-8. Please ensure file encoding is UTF-8 (without BOM).", filepath)
        return False
    except Exception as e:
        LOGGER.error("Error reading %s: %s", filepath, e)
        return False

    # 2. Language Check (If NOT in allowed paths)
    if not is_path_allowed(filepath):
        eval_lines = content.splitlines()
        start_index = MARKDOWN_LANGUAGE_LINK_LINES if Path(filepath).suffix.lower() == ".md" else 0

        for i in range(start_index, len(eval_lines)):
            line = eval_lines[i]
            if CJK_RE.search(line):
                # Double-check: If the file IS actually allowed but prefix matching missed it,
                # this would still trigger. But based on is_path_allowed, we skip this whole block.
                LOGGER.error("Error: Non-English (CJK) character or Mojibake found in %s at line %s:", filepath, i + 1)
                LOGGER.error("  > %s", line.strip())
                LOGGER.error("Note: If this is intentional, move the content to an allowed path (docs/zh-TW/, .memories/, .references/, or .tmp/).")
                return False
    else:
        # In allowed paths, we already did the UTF-8 encoding check above.
        # This prevents Traditional Chinese from being flagged as "Mojibake"
        # simply because they are non-ASCII.
        pass

    return True


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    handler: logging.Handler
    if RichHandler is not None:
        handler = RichHandler(markup=False, show_path=False, show_time=False)
    else:
        handler = logging.StreamHandler()
    logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=[handler])

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
