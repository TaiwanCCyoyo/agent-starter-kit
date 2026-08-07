---
paths:
    - "*"
---

# Development Workflow

## Research & Reuse

Before writing any code:

- Read the relevant repository implementation and tests first.
- Use existing local helpers and patterns before adding dependencies or abstractions.
- Check primary vendor documentation when API behavior or version compatibility is uncertain.

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

## Pre-Review Checks

- All automated checks (CI/CD) passing
- Merge conflicts resolved
- Branch up to date with target branch
