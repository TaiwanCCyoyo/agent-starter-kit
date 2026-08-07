---
paths:
    - "*"
---

# Development Workflow

## Phase Routing

Each phase has a designated owner — use it rather than re-deriving the workflow:

| Phase         | Owner                                                                                                   |
| ------------- | ------------------------------------------------------------------------------------------------------- |
| Plan          | Native Plan Mode / optional OpenSpec project files / `plan-reviewer`                                    |
| TDD           | Native test-first workflow / `python-testing` skill                                                     |
| Debug         | Main session evidence-driven debugging / repository tests                                               |
| Review        | `implementation-reviewer` or built-in `/code-review`                                                    |
| Verify        | Task-specific tests / pre-commit                                                                        |
| Commit        | `/gen-commit` (`commit-helper` skill)                                                                   |
| Prepare PR    | `github-ops` skill (full branch history, `base...HEAD` diff, summary, test plan)                        |
| Finish branch | Native Git operations / `github-ops`, with explicit authorization for publishing or destructive actions |
