# Code Review Standards

## Severity Levels

| Level    | Meaning                                       | Action                                                                      |
| -------- | --------------------------------------------- | --------------------------------------------------------------------------- |
| CRITICAL | Security vulnerability or data loss risk      | **BLOCK** — Must fix before merge                                           |
| HIGH     | Likely bug or significant behavior regression | **FIX OR DISCLOSE** — Resolve before merge unless the user accepts the risk |
| MEDIUM   | Maintainability concern                       | **INFO** — Consider fixing                                                  |
| LOW      | Style or minor suggestion                     | **NOTE** — Optional                                                         |

## Security Review Triggers

Security-sensitive changes → see the trigger list in `security.md`; route to `security-reviewer`.

## Approval Criteria

- **Approve**: No CRITICAL or HIGH issues
- **Warning**: HIGH issues remain with explicit risk acceptance
- **Block**: Any CRITICAL issue found

## Reviewers

- Pre-commit correctness → `implementation-reviewer`
- Broader quality review → `code-reviewer`
- Security-sensitive changes → `security-reviewer`
