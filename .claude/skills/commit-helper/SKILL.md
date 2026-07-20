---
name: commit-helper
description: Quality standards for Git commits. Defines pre-commit checklists, Conventional Commits format, agent trailers, and high-quality log criteria.
---

# Skill: Commit-Helper

This skill is the source of truth for high-quality commits in this project. All Claude commit generation workflows must refer to this helper.

## Pre-commit Checklist

1. **Hook Awareness**: Ensure `pre-commit` hooks are active. If a commit is blocked by hooks, fix the specific issue and re-stage before retrying.
2. **Scope Verification**: The main agent performs filename-level staged-scope preflight only. The `commit_specialist` performs the full staged-content review with `git status` and `git diff --cached` to ensure only intended changes are staged.
3. **Local State Guard**: Avoid staging `.env`, credentials, temporary build artifacts, generated junk, or ignored local memory state.
4. **Submodule Handoff**: When commit execution or autonomous staging is explicitly authorized, confirm each intended submodule has a committed `HEAD`, run `git add -- <submodule-path>` in the superproject, and give its staged gitlink state to `commit_specialist`. The specialist verifies it and must not commit inside a submodule.

## Security And Hygiene

1. **Sensitive Data**: Never commit `.env` files, private keys, tokens, passwords, or credentials.
2. **No Junk**: Reject or warn if generated binaries, temporary build artifacts, unrelated `__pycache__` files, or local settings are staged.
3. **Local State Safety**: Never include ignored local state under `.memories/`.
4. **Surgical Changes**: Ensure changes are relevant to the requested task. Reject unrelated cleanup or noisy diffs unless requested.

## Commit Message Standard

1. **Language**: English only for all commit metadata: subject, body, and trailers.
2. **Format**: `<type>[optional scope]: <description>`
    - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`.
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

## AI Commit Trailers

- Every commit drafted or executed by Claude must include a formal `Co-authored-by:` identity trailer.
- Before delegating, the main agent must provide `commit-specialist` with contributor-model context and roles for models that materially contributed; committing alone is not a material contribution.
- When the resolved model display name is reliably known, use the format `Co-authored-by: Claude <resolved model display name> <noreply@anthropic.com>` and replace the placeholder with that name, for example `Co-authored-by: Claude Haiku 4.5 <noreply@anthropic.com>`.
- When the exact model display name is unavailable, use `Co-authored-by: Claude <noreply@anthropic.com>`.
- Never emit the literal `<resolved model display name>` placeholder.
- Do not add an `AI-Model` trailer; Claude model aliases and runtime overrides may vary.
- If contributor-model context is missing or unclear and multiple agents materially contributed, `commit_specialist` must request it before drafting or committing.
- Every agent-created commit must include exactly one `Agent-Status` trailer:
    - `Agent-Status: autonomous` when Claude staged and committed without manual review of the final staged diff.
    - `Agent-Status: assisted` when the user reviewed or explicitly approved the final staged diff or commit message before commit execution.
- Place trailers after a blank line following the body, or after the subject if there is no body.
- If multiple agents materially contributed before the commit, add one valid `Co-authored-by:` trailer per contributor and one shared `Agent-Status:` trailer for the commit execution mode. Do not invent contributor email addresses.

Example:

```text
fix(claude): align hygiene hook behavior

Remove per-file type checks from the post-edit hook.

Agent-Status: assisted
Co-authored-by: Claude Haiku 4.5 <noreply@anthropic.com>
```

## Interaction And Summary

- The commit message itself is always in English.
- The summary provided to the user must be in Traditional Chinese (zh-TW).
- The main agent should not inspect staged file contents in this workflow. It confirms intent, checks staged filenames/status for obvious forbidden paths, and delegates one concrete objective with explicit paths, requested output, acceptance criteria, contributor-model context and roles, and staged submodule gitlink state to `commit_specialist` for content-level review.
- For an uncommitted submodule, unexpected gitlink delta, or unresolved hook failure, `commit_specialist` stops and returns the failed step, evidence, and the precise parent-agent decision required.

## Execution And Failure Mitigation

- Commit execution is delegated to the `commit_specialist` subagent, including staged-content analysis, security and hygiene checks, running `git commit`, reading hook output, and retrying after fixes.
- If `git commit` fails due to hooks, enter Fix Mode: read the specific error output, apply the minimal fix, re-stage changed files, and retry.
- Do not bypass hooks unless the user explicitly authorizes it.

## Post-Commit Memory Check

After a successful commit:

1. If a related OpenSpec change exists, update its tasks, verification notes, or specs when the commit changes implementation status. Do not create a change retroactively for a simple commit.
2. Review whether the session produced durable project facts, user preferences, decisions, lessons, environment constraints, recurring problems, or verified resolutions.
3. Route durable knowledge through `/save-memory` or `/memory-maintenance` only when it will help future sessions; do not save commit narration or duplicate the plan.
4. Run `/learn-eval` when a user correction, non-obvious technique, reusable workflow, or corrected skill may deserve absorption into an existing skill or a new skill candidate.
