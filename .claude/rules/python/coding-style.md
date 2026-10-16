---
paths:
    - "**/*.py"
    - "**/*.pyi"
---

# Python Coding Style

## Logging

Use `logging` for diagnostics; CLI output and hook protocol responses belong on the required stdout/stderr stream.

Add diagnostic logs where they help explain otherwise hard-to-observe failures. Log identifiers and summaries rather than credentials, tokens, or personal data.

When existing evidence does not explain a failure, use targeted logging to gather the missing evidence. Retain logs that help diagnose future failures at an appropriate level.
