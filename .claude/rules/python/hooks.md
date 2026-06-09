---
paths:
  - "**/*.py"
  - "**/*.pyi"
---
# Python Hooks

## Project Hooks

The repository hook in `.claude/settings.json` runs `.claude/hooks/post_tool_use_hygiene.py` after edits. For Python files it uses the project-managed environment to run targeted Ruff formatting/linting, mypy-aware checks, file hygiene, and the no-print check.

## Warnings

- Production `print()` calls are rejected by the project hygiene checks; use `logging`.
- Full-project `uv run mypy .` remains a pre-commit or explicit verification gate.
