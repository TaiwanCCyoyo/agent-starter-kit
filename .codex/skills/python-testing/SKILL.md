---
name: python-testing
description: Apply repository-specific verification requirements to Python scripts, hooks, and tooling.
---

# Python Testing

Use this skill when Python scripts, hooks, or reusable tooling change.

## Repository Checks

- Run Python commands through the project-managed environment with `uv run`.
- Use `uv run python -m pytest` for tests so the repository root is importable on Windows.
- Do not use `uv run pytest` as final evidence on this repository; its console entry point may omit the repository root from `sys.path`.
- Use `uv run ruff check .` for lint verification.
- Use `uv run mypy .` as the full-project type gate.
- Do not treat single-file mypy results as final evidence because project context can affect type checking.

## Hook And Script Coverage

- For hook scripts, test representative JSON stdin and CLI arguments.
- For hygiene scripts, use small positive and negative fixtures.
- Cover Windows path behavior when scripts are used by agent hooks.
- Keep failure output readable and independent of a specific shell.

## Optional Coverage

Run `uv run python -m pytest --cov --cov-report=term-missing` when the user requests coverage or the change is high risk. Use the report to find meaningful untested behavior; do not impose a universal percentage.
