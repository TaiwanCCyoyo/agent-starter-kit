---
name: gen-commit
description: Use when the user says /gen-commit, gen-commit, generate commit, create commit message, commit staged changes, commit changes, or asks Codex to perform a Git commit; enforces staged-change review, secret checks, Conventional Commits, English metadata, hook failure handling, and autonomous commit trailers when needed.
---

# Gen Commit

This is a command-like Codex skill. It replaces Gemini-style `/gen-commit` with a skill trigger that can be invoked by plain text.

## Workflow

1. Inspect `git status`.
2. Inspect staged changes with `git diff --cached`.
3. If nothing is staged, inspect unstaged changes and ask before staging unless the user explicitly requested autonomous staging.
4. Confirm that no `.env`, credentials, local memory noise, generated state, or unrelated files are staged.
5. Draft an English Conventional Commit message.
6. If the user requested only a message, return the message without committing.
7. If the user requested a commit, run the commit.
8. If hooks fail, fix the issue, restage only affected intended files, and retry.

## Commit Message Standard

- Use English only.
- Use Conventional Commits: `<type>[optional scope]: <description>`.
- Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`.
- Use imperative mood.
- Start the description with lowercase.
- Do not end the subject with a period.
- Keep the subject under 50 characters when practical.
- Use the body to explain why and how for complex changes.
- Autonomous commits must include `Agent-Status: autonomous` in the commit body.

## Safety

- Never stage or commit secrets.
- Never include ignored local state such as `.agents/memory/.codex_stop_memory_state.json`.
- Respect dirty worktrees; do not revert user changes.
- Do not bypass hooks unless the user explicitly authorizes it.
