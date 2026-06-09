# Coding Style

## Core Practice

- Match existing repository patterns before introducing a new abstraction.
- Prefer explicit, readable code over cleverness.
- Keep changes scoped to requested behavior and direct verification.
- Prefer immutable values when they reduce hidden state, but allow clear local mutation when it is simpler and safe.
- Use early returns or extraction when nesting obscures control flow.

## Review Heuristics

File length, function length, parameter count, and nesting depth are signals for review, not universal failure thresholds. Request a split only when the current structure creates a concrete correctness, testing, or maintenance risk.

Before marking work complete, confirm names are clear, error handling fits local patterns, constants are intentional, and no unrelated refactor was introduced.
