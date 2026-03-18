---
description: Dynamic SOP for Pre-Commit Checks
---
# Pre-Commit SOP (Evolving)

**CRITICAL: This SOP must be run before every git commit.**

## 1. [CORE / MANDATORY] Credential Scanning
- **Action**: Run `gitleaks detect --staged --verbose` (or equivalent secret scanner).
- **Status**: MANDATORY / IMMUTABLE.
- **Goal**: Ensure no secrets are leaked.

## 2. [EVOLUTIONARY] Code Quality & Linting
- **Current Active Checks**: (Agent: Update this list as project grows)
  - [ ] *No project-specific linters yet.*

## 3. [EVOLUTIONARY] Basic Testing
- **Current Active Checks**: (Agent: Update this list as project grows)
  - [ ] *No test suites yet.*

---
*(Agent Note: To evolve this SOP, update the sections above and synchronize the "Active Checks" list with `.agents/MEMORY.md`.)*
