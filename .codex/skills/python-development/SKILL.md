---
name: python-development
description: Use when creating, modifying, or reviewing non-test Python production code, including APIs, services, configuration access, logging, typing, or FastAPI applications.
---

# Python Development

Apply the repository's Python development baseline.

## Core Rules

- Use repository Ruff configuration for formatting, linting, and import sorting.
- Use `logging` for diagnostics; CLI output and hook protocol responses belong on the required stdout/stderr stream. Do not add debug `print()` calls.
- Prefer immutable values when they reduce hidden state, while allowing clear local mutation.
- Read existing implementation and tests before introducing a new Python pattern or dependency.

## Secrets And Security

- Read required secrets with `os.environ["NAME"]` or the application's existing configuration layer.
- Do not add dotenv or a security scanner unless the repository explicitly adopts and configures it.
- Use `security_reviewer` when the change affects a trust boundary, permissions, secrets, untrusted input handling, or sensitive data flow; ordinary file access alone is not a trigger.
- Rely on the repository's configured `detect-secrets` commit gate.

## Verification

- Run targeted tests while developing, then run pre-commit against changed files before reporting implementation work complete.
- If a formatter changes files, inspect the resulting diff and rerun the relevant checks.
- Use `python-testing` for pytest, coverage, hook fixtures, and Windows-path verification.

## FastAPI

When the code imports FastAPI or changes API routes, dependencies, schemas, or app construction, read [references/fastapi.md](references/fastapi.md) before editing.
