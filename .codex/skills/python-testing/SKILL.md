---
name: python-testing
description: Write or run Python tests in this repository with Windows imports, hidden hook test directories, and hook JSON fixtures. Use when tests are warranted or requested, not for every Python file edit or move.
---

# Python Testing

Use this reference when writing or running Python tests. It supplies repository-specific execution and fixture details.

## Running Tests

- Use `uv run python -m pytest <affected-test-paths>` so the repository root remains importable on Windows.
- Pass hidden hook test directories explicitly; pytest discovery excludes them. Shared script tests live in `scripts/tests/`, Codex hook tests in `.codex/hooks/tests/`, and Claude hook tests in `.claude/hooks/tests/`.
- Give hook test files agent-prefixed basenames to avoid module-name collisions when running both agents' suites together.

## Hook Fixtures

- When entry-point or protocol behavior changes, exercise the real hook with representative JSON stdin and check its response and CLI arguments.
- Select cases for affected, supported behavior; success, failure, warnings, and malformed input are possibilities, not a mandatory checklist.
- Exercise Windows paths when path handling is affected. Keep subprocess fixtures independent of a particular shell.

## Coverage

When a coverage report helps assess an identified risk or the user requests it, add `--cov --cov-report=term-missing` to the affected test run. Use it to find meaningful gaps; do not impose a universal percentage or expand to the full suite solely because coverage is enabled.
