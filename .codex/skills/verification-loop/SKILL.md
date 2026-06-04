---
name: verification-loop
description: Drive Codex work through a concise implement-check-fix loop without adding a separate loop operator agent.
---

# Verification Loop

Use this skill when a change needs iterative validation.

## Loop

1. Identify the smallest meaningful verification command.
2. Run it after the relevant implementation step.
3. Read failures before changing code.
4. Apply the smallest fix that addresses the failure.
5. Rerun the same check, then broaden only if the risk requires it.

## Boundaries

- Do not run broad checks only to create activity.
- Do not bypass hooks or pre-commit gates.
- Do not leave long-running sessions open.
- State skipped checks and residual risk clearly.

## Common Gates

- `uv run ruff check .`
- `uv run mypy .`
- `uv run pre-commit run --all-files`
