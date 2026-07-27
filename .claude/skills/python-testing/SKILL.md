---
name: python-testing
description: Repository-specific Python behavioral test, hook fixture, Windows path, and optional coverage requirements.
origin: ECC (narrowed — general pytest workflow is owned by superpowers:test-driven-development)
---

# Python Testing — Repository-Specific Requirements

General TDD workflow is provided by `superpowers:test-driven-development`. This skill contains only the requirements specific to this repository.

## Running Tests

```bash
# Complete repository suite — includes shared scripts and all agent hook tests
uv run python -m pytest scripts/tests .codex/hooks/tests .claude/hooks/tests

# Claude hook tests only
uv run python -m pytest .claude/hooks/tests

```

Invoke pytest through `uv run python -m pytest` so the repository root remains importable on Windows. Pass hidden hook test directories (`.claude/`, `.codex/`) explicitly because pytest discovery excludes them.

## Hook Test Location

- Keep Claude-specific hook contract tests under `.claude/hooks/tests/`.
- Keep Codex-specific hook contract tests under `.codex/hooks/tests/`.
- Keep cross-agent script tests (e.g. `scripts/file_hygiene.py`) under `scripts/tests/`.
- Use each agent's own hook tests as evidence for that agent's contracts.
- Give test files agent-prefixed basenames (e.g. `test_claude_post_tool_use_hygiene.py`) to avoid pytest module name collisions when the same logical test exists in both `.claude/` and `.codex/` directories.

## Hook and Script Tests

- Invoke the real entry point with representative JSON stdin payloads and assert the resulting stdout JSON and CLI arguments.
- Include positive fixtures (clean input → no output), blocking failures, warning-only responses, and malformed JSON.
- Cover Windows path behavior: hooks receive Windows-style paths on this machine; scripts must handle both separators.
- Keep failure output independent of a specific shell — use Python's `subprocess` or `sys.stderr`, not `bash`-specific constructs.

## Coverage Target

Coverage is optional unless the user requests it or the change is high risk. Run:

```bash
uv run python -m pytest scripts/tests .codex/hooks/tests .claude/hooks/tests --cov --cov-report=term-missing
```

Use coverage to find meaningful untested behavior, not to satisfy a universal percentage. If a task defines a threshold, report the measured result against that threshold.
