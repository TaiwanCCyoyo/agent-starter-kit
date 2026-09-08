---
paths:
    - "**/*.py"
    - "**/*.pyi"
---

# Python Coding Style

## Immutability

Prefer immutable data structures (frozen dataclasses, `NamedTuple`) over mutable ones.

## Logging

Use `logging` for diagnostics; CLI output and hook protocol responses belong on the required stdout/stderr stream. Do not add debug `print()` calls.

## Reference

See skill: `python-testing` for pytest patterns and coverage requirements.
