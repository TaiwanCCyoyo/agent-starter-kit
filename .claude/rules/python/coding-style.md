---
paths:
    - "**/*.py"
    - "**/*.pyi"
---

# Python Coding Style

## Logging

Use `logging` for diagnostics; CLI output and hook protocol responses belong on the required stdout/stderr stream.

Include diagnostic logging at meaningful boundaries of multi-step work: identify the operation and inputs by safe identifiers or counts, record consequential decisions and external-call outcomes, and capture exception context. A later failure should be traceable without rerunning the job.

During debugging, add targeted logs when code inspection and existing evidence cannot explain the failure. Retain useful diagnostic logs at appropriate levels after the fix. Avoid logging every statement, full payloads, credentials, tokens, or personal data.
