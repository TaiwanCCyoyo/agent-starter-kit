---
name: python-development
description: Use when creating, modifying, debugging, or reviewing non-test Python production code, including services, scripts, hooks, logging, and typing.
---

# Python Development

Apply the repository's Python development baseline.

## Logging

- Use `logging` for diagnostics; CLI output and hook protocol responses belong on the required stdout/stderr stream.
- Add diagnostic logs where they help explain otherwise hard-to-observe failures. Log identifiers and summaries rather than credentials, tokens, or personal data.
- When existing evidence does not explain a failure, use targeted logging to gather the missing evidence. Retain logs that help diagnose future failures at an appropriate level.

## Verification

Follow `AGENTS.md` for verification decisions. Use `python-testing` when the task calls for writing or running Python tests.
