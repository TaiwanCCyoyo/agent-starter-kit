---
name: python-testing
description: Repository-specific Python behavioral test, hook fixture, Windows path, and optional coverage requirements.
---

# Python Testing — Repository-Specific Requirements

This skill contains the verification requirements specific to this repository. Use Antigravity's native test-first workflow when appropriate.

## Running Tests

```bash
# Complete repository suite — includes shared scripts and all agent hook tests
uv run python -m pytest scripts/tests .codex/hooks/tests .claude/hooks/tests

# Cross-agent script and contract tests
uv run python -m pytest scripts/tests
```

Invoke pytest through `uv run python -m pytest` so the repository root remains importable on Windows. Pass hidden hook test directories (`.claude/`, `.codex/`) explicitly because pytest discovery excludes them.

## Hook and Script Tests

- Invoke the real entry point with representative JSON stdin payloads and assert the resulting stdout JSON and CLI arguments.
- Include positive fixtures (clean input -> no output), blocking failures, warning-only responses, and malformed JSON.
- Cover Windows path behavior: hooks receive Windows-style paths on this machine; scripts must handle both separators.
- Keep failure output independent of a specific shell — use Python's `subprocess` or `sys.stderr`, not shell-specific constructs.

## Coverage Target

Coverage is optional unless the user requests it or the change is high risk. Run:

```bash
uv run python -m pytest scripts/tests .codex/hooks/tests .claude/hooks/tests --cov --cov-report=term-missing
```

Use coverage to find meaningful untested behavior, not to satisfy a universal percentage. If a task defines a threshold, report the measured result against that threshold.
