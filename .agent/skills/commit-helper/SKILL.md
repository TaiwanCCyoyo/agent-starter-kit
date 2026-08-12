---
name: commit-helper
description: Quality standards for Git commits. Defines pre-commit checklists, Conventional Commits format, agent attribution, security checks, and high-quality log criteria.
---

# Skill: Commit-Helper

This skill is the source of truth for high-quality commits in this project. All Antigravity commit generation workflows must refer to this helper.

## Pre-commit Checklist

1. **Hook Awareness**: Ensure `pre-commit` hooks are active. If hooks block a commit, fix the concrete issue and re-stage before retrying.
2. **Scope Verification**: Verify that only intended files are staged with `git status` and `git diff --cached`.
3. **Local State Guard**: Avoid staging credentials, temporary build artifacts, generated junk, local settings, or ignored memory state.

## Security And Hygiene

1. **Sensitive Data**: Never commit `.env` files, private keys, tokens, passwords, or credentials.
2. **No Junk**: Reject or warn if generated binaries, temporary build artifacts, unrelated `__pycache__` files, or local settings are staged.
3. **Memory Safety**: Never include ignored local state from `.memories/`.
4. **Surgical Changes**: Ensure changes are relevant to the requested task. Reject unrelated cleanup or noisy diffs unless requested.

## Commit Message Standard

1. **Language**: English only for all commit metadata: subject, body, and trailers.
2. **Format**: `<type>[optional scope]: <description>`
3. **Subject Line**:
    - Use imperative mood, such as `add` instead of `added`.
    - Start with lowercase.
    - Do not end with a period.
    - Keep under 50 characters when practical.
4. **Body**:
    - Use for complex changes to explain why and how.
    - Wrap each line at 72 characters.

## Agent Commit Attribution

- Every commit drafted or executed by Antigravity must include `Agent: Antigravity`.
- Place trailers after a blank line following the body, or after the subject if there is no body.
- If multiple agents materially contributed before the commit, add one `Agent:` trailer per agent in contribution order.

Example:

```text
chore(agent): update commit workflow

Agent: Antigravity
```

## Interaction And Summary

1. The commit message itself is always in English.
2. The summary provided to the user must be in Traditional Chinese (zh-TW).
