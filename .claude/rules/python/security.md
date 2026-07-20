---
paths:
    - "**/*.py"
    - "**/*.pyi"
---

# Python Security

> This file extends [common/security.md](../common/security.md) with Python specific content.

## Secret Management

Use `os.environ["NAME"]` or the application's existing configuration layer for required secrets. Do not add a dotenv dependency unless the project explicitly adopts one.

## Security Review

- `detect-secrets` runs in pre-commit.
- Use `security-reviewer` for authentication, authorization, untrusted input, database queries, filesystem access, external APIs, cryptography, payments, or sensitive data flows.
- Add a security scanner only when it is installed and configured as a repository dependency or CI gate.
