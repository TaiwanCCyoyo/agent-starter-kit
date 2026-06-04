import json
import logging
import subprocess
import sys
from pathlib import Path

try:
    from rich.logging import RichHandler
except ImportError:
    RichHandler = None

TEXT_SUFFIXES = {".md", ".py", ".toml", ".json", ".yaml", ".yml"}
LOGGER = logging.getLogger("gemini_file_hygiene")


def configure_logging() -> None:
    handler: logging.Handler
    if RichHandler is not None:
        handler = RichHandler(markup=False, show_path=False, show_time=False)
    else:
        handler = logging.StreamHandler()
    logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=[handler])


def hook_file_path(event: dict) -> str:
    tool_input = event.get("tool_input", {})
    return tool_input.get("file_path") or tool_input.get("TargetFile") or ""


def sync_targets(filepath: str) -> list[str]:
    path = Path(filepath).as_posix()
    targets: list[str] = []

    if path == "README.md":
        docs_dir = Path("docs")
        if docs_dir.exists():
            for lang_dir in docs_dir.iterdir():
                if lang_dir.is_dir():
                    target = lang_dir / "README.md"
                    if target.exists():
                        targets.append(target.as_posix())

    elif path.startswith("docs/"):
        parts = Path(path).parts
        if len(parts) >= 3:
            current_lang = parts[1]
            filename = "/".join(parts[2:])

            if filename.lower() == "readme.md":
                targets.append("README.md")

            docs_dir = Path("docs")
            if docs_dir.exists():
                for lang_dir in docs_dir.iterdir():
                    if lang_dir.is_dir() and lang_dir.name != current_lang:
                        target = lang_dir / filename
                        if target.exists():
                            targets.append(target.as_posix())

    return targets


def clean_trailing_whitespace(path: Path) -> None:
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return

    lines = content.splitlines(keepends=True)
    cleaned_lines = []
    modified = False
    for line in lines:
        if line.endswith("\r\n"):
            ending = "\r\n"
        elif line.endswith("\n"):
            ending = "\n"
        else:
            ending = ""

        cleaned = line.rstrip("\r\n").rstrip(" \t") + ending
        if cleaned != line:
            modified = True
        cleaned_lines.append(cleaned)

    if modified:
        path.write_text("".join(cleaned_lines), encoding="utf-8", newline="")
        LOGGER.info("Hygiene: Removed trailing whitespace in %s", path)


def print_sync_alert(filepath: str) -> None:
    targets = sync_targets(filepath)
    if not targets:
        return

    LOGGER.warning("")
    LOGGER.warning("%s", "!" * 60)
    LOGGER.warning(">>> [SYNC ALERT] '%s' was modified.", filepath)
    LOGGER.warning(">>> Please ensure the following related files are updated:")
    for target in targets:
        LOGGER.warning("    [ ] %s", target)
    LOGGER.warning("%s", "!" * 60)
    LOGGER.warning("")


def main() -> int:
    configure_logging()
    try:
        event = json.load(sys.stdin)
    except Exception:
        sys.stdout.write(json.dumps({}) + "\n")
        return 0

    file_path = hook_file_path(event)
    path = Path(file_path) if file_path else None
    return_code = 0
    if path and path.exists() and path.suffix.lower() in TEXT_SUFFIXES:
        clean_trailing_whitespace(path)
        result = subprocess.run(["uv", "run", "python", "./scripts/file_hygiene.py", "--file", file_path], check=False)
        return_code = result.returncode
        print_sync_alert(file_path)

    sys.stdout.write(json.dumps({}) + "\n")
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
