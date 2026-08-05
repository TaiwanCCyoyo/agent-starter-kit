---
paths:
    - "**/*.py"
    - "**/*.pyi"
---

# Python Hooks

## Project Hooks

The Pyright LSP owns immediate type-aware diagnostics without modifying files. Claude's PostToolUse hook runs a read-only targeted Ruff check with `E722`, `F601`, `F602`, and `F634` for `.py` and `.pyi` edits because those rules complement Pyright. Codex has no Python LSP, so its hook uses the broader Ruff `F` check while ignoring `F401`, `F841`, and `F842`. Pre-commit owns complete Ruff linting, formatting, type checking, file validation, and other staged gates; CI owns repository-wide gates.
