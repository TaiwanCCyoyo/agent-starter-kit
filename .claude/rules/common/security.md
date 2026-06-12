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

Never hardcode secrets. See `commit-helper` skill and `rules/python/security.md` for details.
