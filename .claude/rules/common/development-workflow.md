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
