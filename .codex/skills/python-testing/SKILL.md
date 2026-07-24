---
name: python-testing
description: Apply repository-specific verification requirements to Python scripts, hooks, and tooling.
---

# Python Testing

Use this skill when Python scripts, hooks, or reusable tooling change.
Use `python-development` separately for coding style, typing, logging, secrets, security routing, and FastAPI design.

## Repository Checks

- Run Python commands through the project-managed environment with `uv run`.
- Use `uv run python -m pytest scripts/tests .codex/hooks/tests` for the complete repository test suite so the repository root is importable on Windows and Codex hook tests are included.
- Use `uv run python -m pytest .codex/hooks/tests` for focused Codex hook verification.
- Do not use `uv run pytest` as final evidence on this repository; its console entry point may omit the repository root from `sys.path`.
- Do not rely on pytest's default recursive discovery for Codex hook tests because hidden directories such as `.codex/` are excluded by default.
- A successful post-edit hygiene hook is sufficient Ruff evidence for its touched files; do not rerun Ruff by default.
- For an explicit full-repository check (hook changes/debugging, commit workflow, or user request), use `uv run ruff check .` and `uv run ruff format --check .` so verification does not modify files.
- Use `uv run mypy .` as the full-project type gate.
- Do not treat single-file mypy results as final evidence because project context can affect type checking.

## Hook And Script Coverage

- Keep Codex-specific hook contract and cross-agent hook regression tests under `.codex/hooks/tests/`; keep shared script tests under `scripts/tests/`.
- For hook scripts, invoke the real entry point with representative JSON stdin and assert the resulting stdout JSON and CLI arguments.
- Include positive input, blocking failures, warning-only responses, and malformed JSON.
- For hygiene scripts, use small positive and negative fixtures.
- Cover Windows path behavior when scripts are used by agent hooks.
- Keep failure output readable and independent of a specific shell.

## Optional Coverage

Run `uv run python -m pytest scripts/tests .codex/hooks/tests --cov --cov-report=term-missing` when the user requests coverage or the change is high risk. Use the report to find meaningful untested behavior; do not impose a universal percentage.
