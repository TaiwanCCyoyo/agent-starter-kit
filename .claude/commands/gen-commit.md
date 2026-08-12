---
description: Generate or execute a Git commit through the commit_specialist subagent.
---

# Gen Commit

Delegate this task to the `commit_specialist` subagent, which MUST follow `.claude/skills/commit-helper/SKILL.md`.

## Workflow

1. Confirm whether the user wants only a commit message or wants Claude to execute a commit.
2. Do a filename/status-level-only preflight of the staged (or, if nothing is staged, unstaged) scope. Do not inspect staged file contents in the main agent.
3. Stop and ask before delegating if that preflight shows obvious forbidden or suspicious paths. If nothing is staged, ask before staging unless the user explicitly requested autonomous staging.
4. When the user explicitly authorizes commit execution or autonomous staging, identify intended submodule paths. Confirm each submodule has a committed `HEAD`, run `git add -- <submodule-path>` in the superproject, and record its staged gitlink state. Do not stage a submodule without that authorization.
5. Select and state the delegation mode: `execute supplied message`, `review supplied message`, or `complete rough or missing message`.
6. Delegate one concrete objective with explicit paths, requested output, acceptance criteria, the user's intent, filename-level staged scope, delegation mode, any supplied commit message, and every staged submodule gitlink state to `commit_specialist`.
7. The specialist verifies each handed-off gitlink and must not commit inside a submodule. It must return a handoff failure for an uncommitted submodule, unexpected gitlink delta, or a pre-commit failure that cannot be fixed simply; the main agent decides the next step.
8. If the user requested only a message, instruct `commit_specialist` to return the message without committing.
9. If the user requested a commit, instruct `commit_specialist` to execute `git commit` and handle only simple hook failures.
10. After `commit_specialist` reports a successful commit, the main agent, not the subagent, runs `commit-helper` SKILL.md's Post-Commit Memory Check itself.
