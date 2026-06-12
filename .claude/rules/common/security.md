# Security Routing

## Security-Sensitive Triggers

**Use `security-reviewer` agent when the change touches:**

- Authentication or authorization
- Untrusted user input
- Database queries
- Filesystem access
- External API calls
- Cryptographic operations
- Payments or financial data

## Response Protocol

If a security issue is found:
1. STOP and use **security-reviewer** before continuing
2. Rotate any exposed secrets immediately
3. Review the codebase for similar issues

## Secrets

Never hardcode secrets in source code.

- Use environment variables or a secret manager — never inline secrets.
- Validate that required secrets are present at startup.

Commit-time gate: `commit-helper` skill (detect-secrets). Python-specific guidance: `rules/python/security.md`.
