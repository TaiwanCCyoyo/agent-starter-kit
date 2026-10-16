---
name: python-development
description: Use when creating, modifying, debugging, or reviewing non-test Python production code, including services, scripts, hooks, logging, and typing.
---

# Python Development

Apply the repository's Python development baseline.

## Logging

- Use `logging` for diagnostics; CLI output and hook protocol responses belong on the required stdout/stderr stream.
- Include diagnostic logging at meaningful boundaries of multi-step work: identify the operation and inputs by safe identifiers or counts, record consequential decisions and external-call outcomes, and capture exception context. A later failure should be traceable without rerunning the job.
- During debugging, add targeted logs when code inspection and existing evidence cannot explain the failure. Retain useful diagnostic logs at appropriate levels after the fix. Avoid logging every statement, full payloads, credentials, tokens, or personal data.

## Verification

Follow `AGENTS.md` for verification decisions. Use `python-testing` when the task calls for writing or running Python tests.
