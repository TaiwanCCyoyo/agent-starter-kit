---
paths:
    - "**/*.py"
    - "**/*.pyi"
---

# Python Coding Style

> Python specific style. General style expectations live in `CLAUDE.md`; review heuristics live in [common/code-review.md](../common/code-review.md).

## Immutability

Prefer immutable data structures (frozen dataclasses, `NamedTuple`) over mutable ones.

## Formatting

- Follow the repository's `ruff.toml`; Ruff enforces formatting, import sorting, and the `T201` ban on production `print()` calls.

## Logging

Use `logging` module only. Do not use `print()` statements in production code.

## Reference

See skill: `python-testing` for pytest patterns and coverage requirements.
