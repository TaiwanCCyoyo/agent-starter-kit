---
name: python-testing
description: Write or run Python tests in this repository with Windows imports, hidden hook test directories, and hook JSON fixtures.
---

# Python Testing

Repository-specific test execution and fixture reference.

## Running Tests

- Use `uv run python -m pytest <affected-test-paths>` so the repository root remains importable on Windows.
- Pass hidden hook test directories explicitly; pytest discovery excludes them. Shared script tests live in `scripts/tests/`, Codex hook tests in `.codex/hooks/tests/`, and Claude hook tests in `.claude/hooks/tests/`.
- Give hook test files agent-prefixed basenames to avoid module-name collisions when running both agents' suites together.

## Hook Fixtures

- Hook fixtures invoke the real entry point with representative JSON stdin and inspect its response and CLI arguments.
- Windows path fixtures cover both separators; subprocess fixtures remain independent of a particular shell.

## Coverage

The coverage-report options are `--cov --cov-report=term-missing`; append them to the selected pytest command.
