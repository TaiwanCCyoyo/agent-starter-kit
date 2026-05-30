---
description: Generate a high-quality Git commit message using the commit_specialist subagent. Use when asked to commit, gen-commit, or create a commit message.
---

# Gen Commit

Delegate this task to the `commit_specialist` subagent.

The subagent MUST follow `.claude/skills/commit-helper/SKILL.md` as the quality standard.

## Workflow

1. Run `git status` and `git diff --cached` to confirm staged scope.
2. If nothing is staged, inspect unstaged changes and ask before staging unless the user explicitly requested autonomous staging.
3. Delegate to `commit_specialist` for both message drafting and commit execution.
4. If the user requested only a message, instruct `commit_specialist` to return the message without committing.
5. If the user requested a commit, instruct `commit_specialist` to execute `git commit` and handle any hook failures.
