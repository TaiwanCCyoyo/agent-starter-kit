---
description: Generate or execute a Git commit following commit-helper standards.
---

# Gen Commit

Follow `.agent/skills/commit-helper/SKILL.md` as the source of truth for all commit operations.

## Workflow

1. Confirm whether the user wants only a commit message or wants Antigravity to execute a commit.
2. Perform a filename/status-level-only preflight of the staged (or, if nothing is staged, unstaged) scope.
3. Stop and ask before proceeding if preflight shows obvious forbidden or suspicious paths. If nothing is staged, ask before staging unless autonomous staging was explicitly requested.
4. When the user explicitly authorizes commit execution or autonomous staging, identify intended submodule paths. Confirm each submodule has a committed `HEAD`, run `git add -- <submodule-path>` in the superproject, and record its staged gitlink state. Do not stage a submodule without that authorization.
5. Select and state the execution mode: `execute supplied message`, `review supplied message`, or `complete rough or missing message`.
6. Follow Conventional Commits format and append the required `Agent: Antigravity` commit trailer.
7. Execute the commit and handle only simple, directly actionable pre-commit failures with a single retry.
8. Present the summary to the user in Traditional Chinese (zh-TW) and the commit message in English.
