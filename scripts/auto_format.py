import argparse
import logging
import subprocess
from pathlib import Path
from typing import Any

RichHandler: Any
try:
    from rich.logging import RichHandler
except ImportError:
    RichHandler = None

LOGGER = logging.getLogger("auto_format")


def configure_logging() -> None:
    handler: logging.Handler
    if RichHandler is not None:
        handler = RichHandler(markup=False, show_path=False, show_time=False)
    else:
        handler = logging.StreamHandler()
    logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=[handler])


def run_hygiene(target_path: Path):
    """
    Runs ruff check --fix and ruff format on the specified path.
    Prints errors if they occur.
    """
    cmd_check = ["uv", "run", "ruff", "check", "--fix", "--force-exclude", str(target_path)]
    cmd_format = ["uv", "run", "ruff", "format", "--force-exclude", str(target_path)]

    LOGGER.info("  -> Executing: %s", " ".join(cmd_check))
    lint_res = subprocess.run(cmd_check, capture_output=True, text=True)

    if lint_res.returncode != 0:
        LOGGER.error("  [LINT ERROR] Findings in %s:", target_path)
        if lint_res.stdout:
            LOGGER.error(lint_res.stdout)
        if lint_res.stderr:
            LOGGER.error(lint_res.stderr)
    else:
        LOGGER.info("  [OK] Lint check/fix passed for %s", target_path)

    LOGGER.info("  -> Executing: %s", " ".join(cmd_format))
    subprocess.run(cmd_format, capture_output=True)


def main():
    configure_logging()
    parser = argparse.ArgumentParser(description="Python Hygiene Script: Automated formatting & linting.")
    parser.add_argument("targets", nargs="*", default=["."], help="Files or directories to check/format (default: current directory).")
    args = parser.parse_args()

    LOGGER.info("=== Python Hygiene CLI Mode ===")
    LOGGER.info("Targets: %s", args.targets)

    for t in args.targets:
        path = Path(t)
        if path.exists():
            LOGGER.info("[*] Processing: %s", t)
            run_hygiene(path)
        else:
            LOGGER.error("[!] Error: Path not found: %s", t)
    LOGGER.info("=== Done ===")


if __name__ == "__main__":
    main()
