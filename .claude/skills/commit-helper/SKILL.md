---
name: commit-helper
description: Quality standards for Git commits. Defines pre-commit checklists, Conventional Commits format, and high-quality log criteria.
---

# Skill: Commit-Helper (The Quality Standards)

This skill serves as the "source of truth" for what constitutes a high-quality commit in this project. All commit generation workflows MUST refer to this helper.

## Pre-commit Checklist

1. **Hook Awareness**: Ensure `pre-commit` hooks are active. If a commit is blocked by hooks (e.g., Ruff), fix the code issues and re-stage before retrying.
2. **Scope Verification**: Use `git status` and `git diff --cached` to ensure only intended changes are staged. Proactively avoid staging `.env`, temporary build artifacts, or ignored local memory state.

## Security & Hygiene

1. **Sensitive Data**: NEVER commit `.env` files, private keys, or credentials.
2. **No Junk**: Reject or warn if generated binaries, temporary build artifacts, or unrelated `__pycache__` files are staged.
3. **Memory Safety**: Never include ignored local state such as `.agents/memory/.claude_stop_memory_state.json`.
4. **Surgical Changes**: Ensure changes are relevant to the requested task. Reject unrelated "cleanup" or noisy diffs unless requested.

## High-Quality Log Standards

1. **Language**: **English** only for all commit metadata (subject, body, trailers).
2. **Format**: `<type>[optional scope]: <description>`
   - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`.
3. **Subject Line**:
   - Imperative mood (e.g., "add" instead of "added").
   - Starts with lowercase.
   - No trailing period.
   - Length < 50 characters.
4. **Body**:
   - Use for complex changes to explain *why* and *how*.
   - Use a simple bullet list (`-`). Do NOT add a header line before the bullets.
   - Wrap each line at 72 characters.
   - One blank line between subject and body.
5. **Trailers** (after a blank line following the body, or following the subject if no body):
   - `Agent-Status: autonomous` — required for commits executed without manual review.
   - `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>` — required for all commits drafted or executed by Claude Code.

## Interaction & Summary

- **Bilingual Response**: The commit message itself is always in **English**, but the summary provided to the user MUST be in **Traditional Chinese (zh-TW)**.

## Execution & Failure Mitigation

Commit execution is always delegated to the `commit_specialist` subagent — including running `git commit`, reading hook output, and retrying after fixes. The main agent must not run `git commit` directly.

If `git commit` fails due to hooks, `commit_specialist` must transition into "Fix Mode": read the specific error output, apply only the minimal fix (e.g. restage after `end-of-file-fixer`), and retry. Do not bypass hooks.
