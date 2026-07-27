---
name: python-testing
description: Apply repository-specific verification requirements to Python scripts, hooks, and tooling.
---

# Python Testing

Use this skill when Python scripts, hooks, or reusable tooling change.
Use `python-development` separately for coding style, typing, logging, secrets, security routing, and FastAPI design.

## Repository Tests

- Run Python commands through the project-managed environment with `uv run`.
- Use `uv run python -m pytest scripts/tests .codex/hooks/tests` for the complete repository test suite so the repository root is importable on Windows and Codex hook tests are included.
- Use `uv run python -m pytest .codex/hooks/tests` for focused Codex hook verification.
- Invoke pytest through `uv run python -m pytest` so the repository root remains importable on Windows.
- Pass hidden hook test directories explicitly because pytest discovery excludes them.

## Hook And Script Coverage

- Keep Codex-specific hook contract and cross-agent hook regression tests under `.codex/hooks/tests/`; keep shared script tests under `scripts/tests/`.
- For hook scripts, invoke the real entry point with representative JSON stdin and assert the resulting stdout JSON and CLI arguments.
- Include positive input, blocking failures, warning-only responses, and malformed JSON.
- For hygiene scripts, use small positive and negative fixtures.
- Cover Windows path behavior when scripts are used by agent hooks.
- Keep failure output readable and independent of a specific shell.

## Optional Coverage

Run `uv run python -m pytest scripts/tests .codex/hooks/tests --cov --cov-report=term-missing` when the user requests coverage or the change is high risk. Use the report to find meaningful untested behavior; do not impose a universal percentage.
