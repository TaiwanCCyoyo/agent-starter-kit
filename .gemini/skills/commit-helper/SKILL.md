---
name: commit-helper
description: Quality standards for Git commits. Defines pre-commit checklists, Conventional Commits format, and high-quality log criteria.
---

# Skill: Commit-Helper (The Quality Standards)

This skill serves as the "source of truth" for what constitutes a high-quality commit in this project. All commit generation workflows MUST refer to this helper.

## 📋 Pre-commit Checklist
1.  **Hook Awareness**: Ensure `pre-commit` hooks are active. If a commit is blocked by hooks (e.g., Ruff), the agent must fix the code issues and re-stage before retrying.
2.  **Scope Verification**: Use `git status` and `git diff` to ensure only intended changes are staged. Proactively avoid staging `.env` or temporary build artifacts.

## 🛡️ Security & Hygiene
1.  **Sensitive Data**: NEVER commit `.env` files, private keys, or credentials.
2.  **No Junk**: Reject or warn if generated binaries, temporary build artifacts, or unrelated `__pycache__` files are staged.
3.  **Surgical Changes**: Ensure changes are relevant to the requested task. Reject unrelated "cleanup" or noisy diffs unless requested.

## ✍️ High-Quality Log Standards
1.  **Language**: **English** only for all commit metadata (subject, body, trailers).
2.  **Format**: `<type>[optional scope]: <description>`
    -   Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`.
3.  **Subject Line**:
    -   Imperative mood (e.g., "add" instead of "added").
    -   Starts with lowercase.
    -   No trailing period.
    -   Length < 50 characters.
4.  **Body**: Use for complex changes to explain *why* and *how* (wrapped at 72 chars).
5.  **Agent Identity**: Commits executed without manual review MUST include the trailer: `Agent-Status: autonomous`.

## 🌐 Interaction & Summary
1.  **Bilingual Response**: The commit message itself is always in **English**, but the summary provided to the user MUST be in **Traditional Chinese (zh-TW)**.

## 🛡️ Failure Mitigation
If `git commit` fails due to local configuration or hooks, the logic must transition into "Fix Mode" to address the specific error output from the terminal.
