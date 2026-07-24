---
name: python-development
description: Use when creating, modifying, or reviewing non-test Python production code, including APIs, services, configuration access, logging, typing, or FastAPI applications.
---

# Python Development

Apply the repository's Python development baseline without duplicating test commands owned by `python-testing`.

## Core Rules

- Follow PEP 8 and add type annotations to all function signatures.
- Use repository Ruff configuration for formatting, linting, and import sorting.
- Use `logging` in production code; do not add `print()` calls.
- Prefer immutable values when they reduce hidden state, while allowing clear local mutation.
- Use `Protocol` for structural interfaces, dataclasses for data transfer objects, context managers for resource lifetimes, and generators for meaningful lazy iteration.
- Read existing implementation and tests before introducing a new Python pattern or dependency.

## Secrets And Security

- Read required secrets with `os.environ["NAME"]` or the application's existing configuration layer.
- Do not add dotenv or a security scanner unless the repository explicitly adopts and configures it.
- Use `security_reviewer` for authentication, authorization, untrusted input, database queries, filesystem access, external APIs, cryptography, payments, or sensitive data flows.
- Rely on the repository's configured `detect-secrets` commit gate.

## Hooks And Verification

- Treat `.codex/hooks/post_tool_use_hygiene.py` as authoritative targeted feedback for Codex edits. A successful result is sufficient evidence for the touched file; do not manually rerun Ruff.
- Keep full-project mypy as an explicit, pre-commit, or CI gate rather than a post-edit hook.
- Use `python-testing` for exact pytest, Ruff, mypy, coverage, hook-fixture, and Windows-path verification.

## FastAPI

When the code imports FastAPI or changes API routes, dependencies, schemas, or app construction, read [references/fastapi.md](references/fastapi.md) before editing.
