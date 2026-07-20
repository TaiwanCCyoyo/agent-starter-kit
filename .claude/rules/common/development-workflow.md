# Development Workflow

## Research & Reuse

Before writing any code:

- Read the relevant repository implementation and tests first.
- Use existing local helpers and patterns before adding dependencies or abstractions.
- Check primary vendor documentation when API behavior or version compatibility is uncertain.

## Phase Routing

Each phase has a designated owner — use it rather than re-deriving the workflow:

| Phase         | Owner                                                                                                                  |
| ------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Plan          | Native Plan Mode / optional OpenSpec project files / `superpowers:writing-plans` + `executing-plans` / `plan-reviewer` |
| TDD           | `superpowers:test-driven-development`                                                                                  |
| Debug         | `superpowers:systematic-debugging`                                                                                     |
| Review        | `implementation-reviewer` → `code-reviewer` → `superpowers:requesting-code-review`                                     |
| Verify        | `superpowers:verification-before-completion`                                                                           |
| Commit        | `/gen-commit` (`commit-helper` skill)                                                                                  |
| Prepare PR    | `github-ops` skill (full branch history, `base...HEAD` diff, summary, test plan)                                       |
| Finish branch | `superpowers:finishing-a-development-branch`                                                                           |

## Pre-Review Checks

- All automated checks (CI/CD) passing
- Merge conflicts resolved
- Branch up to date with target branch
