# Code Review Standards

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| CRITICAL | Security vulnerability or data loss risk | **BLOCK** — Must fix before merge |
| HIGH | Bug or significant quality issue | **WARN** — Should fix before merge |
| MEDIUM | Maintainability concern | **INFO** — Consider fixing |
| LOW | Style or minor suggestion | **NOTE** — Optional |

## Security Review Triggers

**STOP and use `security-reviewer` agent when:**

- Authentication or authorization code
- User input handling
- Database queries
- File system operations
- External API calls
- Cryptographic operations
- Payment or financial code

## Approval Criteria

- **Approve**: No CRITICAL or HIGH issues
- **Warning**: Only HIGH issues (merge with caution)
- **Block**: Any CRITICAL issue found
