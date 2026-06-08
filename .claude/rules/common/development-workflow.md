# Development Workflow

## Feature Implementation Workflow

### 0. Research & Reuse _(mandatory before any new implementation)_

- **GitHub code search first:** Run `gh search repos` and `gh search code` to find existing implementations, templates, and patterns before writing anything new.
- **Library docs second:** Use Context7 or primary vendor docs to confirm API behavior, package usage, and version-specific details before implementing.
- **Exa only when the first two are insufficient:** Use Exa for broader web research or discovery after GitHub search and primary docs.
- **Check package registries:** Search PyPI and other registries before writing utility code. Prefer battle-tested libraries over hand-rolled solutions.
- **Search for adaptable implementations:** Look for open-source projects that solve 80%+ of the problem and can be forked, ported, or wrapped.

### 1. Plan First

Use `/plan` or Native Plan Mode to create an implementation plan. Identify dependencies and risks, and break down into phases before writing any code.

### 2. TDD Approach

Follow `superpowers: test-driven-development` for the red-green-refactor cycle. Use the `tdd-guide` agent when delegating TDD work. Verify 80%+ coverage.

### 3. Code Review

Use the `code-reviewer` agent immediately after writing code. Address CRITICAL and HIGH issues before committing.

### 4. Commit & Push

Follow conventional commits format. See [git-workflow.md](./git-workflow.md) for commit message format and PR process.

### 5. Pre-Review Checks

- All automated checks (CI/CD) passing
- Merge conflicts resolved
- Branch up to date with target branch
