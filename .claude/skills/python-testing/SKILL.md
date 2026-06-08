---
name: python-testing
description: Repository-specific Python verification requirements. Run all Python commands through uv run; use these exact commands for type checking and linting.
origin: ECC (narrowed — general pytest workflow is owned by superpowers:test-driven-development)
---

# Python Testing — Repository-Specific Requirements

General TDD workflow is provided by `superpowers:test-driven-development`. This skill contains only the requirements specific to this repository.

## Running Tests

```bash
# Correct — imports repository package from root
uv run python -m pytest

# Wrong on Windows — console entry point does not place repo root on sys.path
uv run pytest
```

## Linting and Type Checking

```bash
# Lint
uv run ruff check .

# Type gate — run against the whole project, not a single file
uv run mypy .
```

Do not use single-file mypy as final evidence of type correctness. `uv run mypy .` is the accepted gate.

## Hook and Script Tests

- Test representative hook JSON stdin payloads and CLI argument combinations.
- Include both positive fixtures (valid input → expected output) and negative fixtures (invalid input → expected error).
- Cover Windows path behavior: hooks receive Windows-style paths on this machine; scripts must handle both separators.
- Keep failure output independent of a specific shell — use Python's `subprocess` or `sys.stderr`, not `bash`-specific constructs.

## Coverage Target

80%+ coverage required. Critical paths (hooks, memory scripts) require 100%.
