---
paths:
    - "**/*.py"
    - "**/*.pyi"
---

# Python Coding Style

> This file extends [common/coding-style.md](../common/coding-style.md) with Python specific content.

## Standards

- Follow **PEP 8** conventions
- Use **type annotations** on all function signatures

## Immutability

Prefer immutable data structures:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    name: str
    email: str

from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float
```

## Formatting

- Follow the repository's `ruff.toml`; Ruff enforces formatting, import sorting, and the `T201` ban on production `print()` calls.

## Logging

Use `logging` module only. Do not use `print()` statements in production code.

## Reference

See skill: `python-testing` for pytest patterns and coverage requirements.
