---
name: python-testing
description: Plan and verify Python changes with focused tests, mypy awareness, ruff compatibility, and regression-oriented scenarios.
---

# Python Testing

Use this skill when Python behavior, scripts, hooks, or reusable tooling changes.

## Test Selection

- Prefer focused tests around changed behavior and failure modes.
- For hook scripts, validate representative JSON stdin or CLI arguments.
- For hygiene scripts, use small fixtures that cover positive and negative cases.
- Include Windows path behavior when scripts are used by agent hooks.

## Static Checks

- Use `uv run ruff check .` for lint verification.
- Use `uv run mypy .` as the full-project type gate.
- Avoid relying on single-file mypy as final evidence because project context can matter.

## Acceptance

- The changed behavior is covered by direct tests or equivalent scripted checks.
- Formatting and linting pass.
- Failure output is readable and does not require a specific shell.
