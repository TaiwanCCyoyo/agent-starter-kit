---
description: Generate a high-quality Git commit message using the commit_specialist subagent. Use when asked to commit, gen-commit, or create a commit message.
---

# Gen Commit

Delegate this task to the `commit_specialist` subagent.

The subagent MUST follow `.claude/skills/commit-helper/SKILL.md` as the quality standard.
The final commit message MUST include the formal co-author identity and status trailers defined in that skill.

## Workflow

1. Confirm whether the user wants only a commit message or wants Claude to execute a commit.
2. Inspect staged scope at filename/status level only, such as with `git status --short` or `git diff --cached --name-status`.
3. If nothing is staged, inspect unstaged filenames/status only and ask before staging unless the user explicitly requested autonomous staging.
4. Stop and ask before delegating if filename-level preflight shows obvious forbidden or suspicious paths such as `.env`, credentials, `.memories/`, generated state, or unrelated files.
5. When the user explicitly authorizes commit execution or autonomous staging, identify intended submodule paths. Confirm each submodule has a committed `HEAD`, run `git add -- <submodule-path>` in the superproject, and record its staged gitlink state. Do not stage a submodule without that authorization.
6. Delegate one concrete objective with explicit paths, requested output, acceptance criteria, the user's intent, filename-level staged scope, contributor-model context and roles, and every staged submodule gitlink state to `commit_specialist` for staged-content analysis, security and hygiene checks, message drafting, commit execution, pre-commit fixes, and hook failure handling. Do not inspect staged file contents in the main agent.
7. The specialist verifies each handed-off gitlink and must not commit inside a submodule. It must return a handoff failure for an uncommitted submodule, unexpected gitlink delta, or unresolved hook failure; the main agent decides the next step.
8. If the user requested only a message, instruct `commit_specialist` to return the message without committing.
9. If the user requested a commit, instruct `commit_specialist` to execute `git commit` and handle any hook failures.
