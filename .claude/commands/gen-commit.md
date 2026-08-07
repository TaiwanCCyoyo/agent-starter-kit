---
description: Generate a high-quality Git commit message using the commit_specialist subagent. Use when asked to commit, gen-commit, or create a commit message.
---

# Gen Commit

Delegate this task to the `commit_specialist` subagent.

The subagent MUST follow `.claude/skills/commit-helper/SKILL.md` as the quality standard.
The final commit message MUST include the formal co-author identity trailer defined in that skill.

## Workflow

1. Confirm whether the user wants only a commit message or wants Claude to execute a commit.
2. Do a filename/status-level-only preflight of the staged (or, if nothing is staged, unstaged) scope. Do not inspect staged file contents in the main agent.
3. Stop and ask before delegating if that preflight shows obvious forbidden or suspicious paths such as `.env`, credentials, `.memories/`, generated state, or unrelated files. If nothing is staged, ask before staging unless the user explicitly requested autonomous staging.
4. When the user explicitly authorizes commit execution or autonomous staging, identify intended submodule paths. Confirm each submodule has a committed `HEAD`, run `git add -- <submodule-path>` in the superproject, and record its staged gitlink state. Do not stage a submodule without that authorization.
5. Delegate one concrete objective with explicit paths, requested output, acceptance criteria, the user's intent, filename-level staged scope, contributor-model context and roles, and every staged submodule gitlink state to `commit_specialist` for staged-content analysis, security and hygiene checks, message drafting, commit execution, pre-commit fixes, and hook failure handling.
6. The specialist verifies each handed-off gitlink and must not commit inside a submodule. It must return a handoff failure for an uncommitted submodule, unexpected gitlink delta, or unresolved hook failure; the main agent decides the next step.
7. If the user requested only a message, instruct `commit_specialist` to return the message without committing.
8. If the user requested a commit, instruct `commit_specialist` to execute `git commit` and handle any hook failures.
9. After `commit_specialist` reports a successful commit, the main agent — not the subagent — runs `commit-helper` SKILL.md's Post-Commit Memory Check itself, since only the main agent has the full session context needed to judge it. This includes explicitly running `/learn-eval` when the session had a user correction, a non-obvious technique, or a reusable workflow worth evaluating.
