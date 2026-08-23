---
paths:
    - "*"
---

# Development Workflow

## Phase Routing

Each phase has a designated owner — use it rather than re-deriving the workflow:

- **Plan** — Native Plan Mode / optional OpenSpec project files / `plan-reviewer`
- **TDD** — Native test-first workflow / `python-testing` skill
- **Commit** — `/gen-commit` (`commit-helper` skill)
- **Prepare PR** — `github-ops` skill (full branch history, `base...HEAD` diff, summary, test plan)
- **Finish branch** — `github-ops` skill

Review, verification, and authorization requirements for merges are covered in `code-review.md`, the Verification section of `CLAUDE.md`, and the Operating Contract, respectively — not repeated here.

## Low-Cost External Delegation

When Antigravity CLI is available, prefer `agy -p --mode plan --sandbox` for bounded, read-only research, inspection, concise review, or mechanical analysis with explicit scope and acceptance criteria. Keep ambiguous, architectural, security-sensitive, and final integration judgment with the main session or a designated reviewer. Never use `--dangerously-skip-permissions`; review the response before acting on it. If it reports `RESOURCE_EXHAUSTED` or `Individual quota reached`, stop that delegation and use another suitable route.
