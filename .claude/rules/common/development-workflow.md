# Development Workflow

## Feature Implementation Workflow

### 0. Research & Reuse

- Read the relevant repository implementation and tests first.
- Use existing local helpers and patterns before adding dependencies or abstractions.
- Check primary vendor documentation when API behavior or version compatibility is uncertain.
- Search GitHub or package registries only when local patterns and primary documentation are insufficient.

### 1. Plan First

Use `/plan` or Native Plan Mode to create an implementation plan. Identify dependencies and risks, and break down into phases before writing any code.

### 2. TDD Approach

Follow `superpowers:test-driven-development` for behavior changes. Use `tdd-guide` only when delegating a bounded TDD implementation. Run coverage when requested or justified by risk.

### 3. Code Review

Use `implementation-reviewer` before committing meaningful changes. Use `code-reviewer` for broader quality review when requested. Resolve CRITICAL findings; resolve HIGH findings or disclose why they remain.

### 4. Commit & Push

Follow conventional commits format. See [git-workflow.md](./git-workflow.md) for commit message format and PR process.

### 5. Pre-Review Checks

- All automated checks (CI/CD) passing
- Merge conflicts resolved
- Branch up to date with target branch
