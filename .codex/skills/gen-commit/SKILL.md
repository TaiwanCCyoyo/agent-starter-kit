---
name: gen-commit
description: Use when the user says /gen-commit, gen-commit, generate commit, create commit message, commit staged changes, commit changes, or asks Codex to perform a Git commit; enforces staged-change review, secret checks, Conventional Commits, English metadata, hook failure handling, and agent identity trailers.
---

# Gen Commit

This is a command-like Codex skill. It replaces Gemini-style `/gen-commit` with a skill trigger that can be invoked by plain text.

Delegate staged-change analysis, commit-message drafting, commit execution, and hook failure handling to the `commit_specialist` subagent. The main agent is responsible for confirming user intent and staged scope only.

## Workflow

1. Inspect `git status`.
2. Inspect staged changes with `git diff --cached`.
3. If nothing is staged, inspect unstaged changes and ask before staging unless the user explicitly requested autonomous staging.
4. Confirm that no `.env`, credentials, local memory noise, generated state, or unrelated files are staged.
5. Delegate to `commit_specialist` for message drafting and, when the user requests a commit, execution.
6. If the user requested only a message, instruct `commit_specialist` to return the message without committing.
7. If the user requested a commit, instruct `commit_specialist` to execute `git commit` and handle any hook failures.

## Commit Message Standard

- Use English only.
- Use Conventional Commits: `<type>[optional scope]: <description>`.
- Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`.
- Use imperative mood.
- Start the description with lowercase.
- Do not end the subject with a period.
- Keep the subject under 50 characters when practical.
- Use the body to explain why and how for complex changes.

## Agent Commit Trailers

- Every commit drafted or executed by Codex must include `Agent: Codex`.
- Every agent-created commit must include exactly one `Agent-Status` trailer:
  - `Agent-Status: autonomous` when Codex staged and committed without manual review of the final staged diff.
  - `Agent-Status: assisted` when the user reviewed or explicitly approved the final staged diff or commit message before commit execution.
- Place trailers after a blank line following the body, or after the subject if there is no body.
- Do not use `Co-Authored-By` as the primary agent identity marker. Use it only when the user explicitly wants GitHub co-author attribution.
- If multiple agents materially contributed before the commit, add one `Agent:` trailer per agent in contribution order and one shared `Agent-Status:` trailer for the commit execution mode.
- Example:

```text
feat(codex): add targeted hygiene checks

Add file-scoped hook checks and repository-level Python gates.

Agent: Codex
Agent-Status: autonomous
```

## Safety

- Never stage or commit secrets.
- Never include ignored local state under `.memories/`.
- Respect dirty worktrees; do not revert user changes.
- Do not bypass hooks unless the user explicitly authorizes it.
