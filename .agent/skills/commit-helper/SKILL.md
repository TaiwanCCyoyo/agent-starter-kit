---
name: commit-helper
description: Quality standards and delegation rules for Git commits — pre-commit handoff, Conventional Commits format, agent attribution, and post-commit checks. Load this BEFORE staging, drafting a commit message, or running `git commit`, for ANY commit request — triggers on "commit", "commit this", "commit changes", "write a commit message", or any request to record staged work as a commit.
---

# Skill: Commit-Helper

This skill is the source of truth for high-quality commits in this project. All Antigravity commit generation workflows must refer to this helper.

## Pre-commit Checklist

1. **Scope Verification**: Perform filename-level staged-scope preflight first. Verify that only intended files are staged with `git status` and `git diff --cached --name-status`.
2. **Submodule Handoff**: When commit execution or autonomous staging is explicitly authorized, confirm each intended submodule has a committed `HEAD`, run `git add -- <submodule-path>` in the superproject, and record its staged gitlink state. You must not commit inside a submodule without explicit authorization.

## Security And Hygiene

1. **Sensitive Data**: Never commit `.env` files, private keys, tokens, passwords, or credentials.
2. **No Junk**: Reject or warn if generated binaries, temporary build artifacts, unrelated `__pycache__` files, or local settings are staged.
3. **Surgical Changes**: Ensure changes are relevant to the requested task. Reject unrelated cleanup or noisy diffs unless requested.

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
    - Use a simple bullet list when helpful.
    - Wrap each line at 72 characters.
    - Leave one blank line between subject and body.

## AI Commit Attribution

- Every commit drafted or executed by Antigravity must include `Agent: Antigravity` as its commit trailer.
- Place trailers after a blank line following the body, or after the subject if there is no body.

Example:

```text
feat(agent): update antigravity configuration

Update root GEMINI.md and streamline project skills.

Agent: Antigravity
```

## Delegation Modes

The main agent must select one mode based on its confidence in the staged changes:

1. **Execute supplied message**: A complete commit message was supplied. Commit directly with the required trailer.
2. **Review supplied message**: A complete commit message was supplied and explicit review is requested. Inspect the staged diff to validate the requested scope, then commit the supplied message unless revisions are requested.
3. **Complete rough or missing message**: The message is rough or absent. Inspect the staged diff and draft a complete commit message before returning it or committing.

In every execution mode, run the normal commit command. Fix only a simple, directly actionable pre-commit failure, re-stage the affected files, and retry once. For any failure requiring non-trivial investigation, a broader change, or an unclear fix, stop and return the error, attempted fix, affected paths, and the required decision.

## Interaction And Summary

- The commit message itself is always in English.
- The summary provided to the user must be in Traditional Chinese (zh-TW).

## Post-Commit Check

1. If a related OpenSpec change exists, update its tasks, verification notes, or specs when the commit changes implementation status. Do not create a change retroactively for a simple commit.
2. Review whether the session produced durable project facts, user preferences, decisions, lessons, environment constraints, recurring problems, or verified resolutions.
3. Keep durable repository conventions and reusable workflows in checked-in instructions or skills.
