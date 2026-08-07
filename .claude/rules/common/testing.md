---
paths:
    - "*"
---

# Testing Requirements

## Risk-Based Coverage

- Add the smallest direct test for changed behavior and failure modes.
- Add integration tests when a change crosses a real component, process, database, filesystem, or network boundary.
- Add E2E tests only for critical user flows when the project has an E2E harness.
- Run coverage when requested or when risk makes untested paths important. Do not impose a universal percentage.

Use a native test-first workflow when it improves confidence. Repository-specific commands, fixtures, structure, and naming conventions are defined in `skill: python-testing`.
