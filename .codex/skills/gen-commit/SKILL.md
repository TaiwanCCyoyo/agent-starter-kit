---
name: gen-commit
description: Use when the user says /gen-commit, gen-commit, generate commit, create commit message, commit staged changes, commit changes, or asks Codex to perform a Git commit; enforces staged-change review, secret checks, Conventional Commits, English metadata, hook failure handling, and agent identity trailers.
---

# Gen Commit

This is a command-like Codex skill that can be invoked with plain text such as `/gen-commit`.

Delegate staged-change content analysis, commit-message drafting, commit execution, hook failure handling, and any pre-commit fixes to the `commit_specialist` subagent. The main agent is responsible only for confirming user intent and doing a filename-level staged-scope preflight.

## Workflow

1. Confirm whether the user wants only a commit message or wants Codex to execute a commit.
2. Inspect staged scope at filename/status level only, such as with `git status --short` or `git diff --cached --name-status`.
3. If nothing is staged, inspect unstaged filenames/status only and ask before staging unless the user explicitly requested autonomous staging.
4. Stop and ask before delegating if filename-level preflight shows obvious forbidden or suspicious paths such as `.env`, credentials, `.memories/`, generated state, or unrelated files.
5. Select an explicit, ordered list of material contributor models, then delegate it with the user's intent and filename-level staged scope to `commit_specialist`. Do not inspect staged file contents in the main agent.
6. If the user requested only a message, instruct `commit_specialist` to return the message without committing.
7. If the user requested a commit, instruct `commit_specialist` to execute `git commit`, perform full staged-content review, run security and hygiene checks, and handle any hook failures or pre-commit fixes.

## Commit Message Standard

- Use English only.
- Use Conventional Commits: `<type>[optional scope]: <description>`.
- Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`.
- Use imperative mood.
- Start the description with lowercase.
- Do not end the subject with a period.
- Keep the subject under 50 characters when practical.
- Use the body to explain why and how for complex changes.

## AI Commit Trailers

- Every commit drafted or executed by Codex must include `Co-authored-by: Codex <codex@openai.com>` as its formal AI identity.
- The main agent selects the ordered list of models that materially contributed to the committed work and supplies it to `commit_specialist`; committing alone is not a material contribution.
- Emit one `AI-Model:` trailer per supplied model, in that order. The commit specialist must request it before drafting or committing when the list is missing, and must not infer or substitute its configured model.
- Every agent-created commit must include exactly one `Agent-Status` trailer:
  - `Agent-Status: autonomous` when Codex staged and committed without manual review of the final staged diff.
  - `Agent-Status: assisted` when the user reviewed or explicitly approved the final staged diff or commit message before commit execution.
- Place trailers after a blank line following the body, or after the subject if there is no body.
- If multiple agents materially contributed before the commit, add one valid `Co-authored-by:` trailer per contributor and one shared `Agent-Status:` trailer for the commit execution mode. Do not invent contributor email addresses.
- Example:

```text
feat(codex): add targeted hygiene checks

Add file-scoped hook checks and repository-level Python gates.

Agent-Status: autonomous
AI-Model: gpt-5.6
AI-Model: gpt-5.6-terra
Co-authored-by: Codex <codex@openai.com>
```

## Safety

- Never stage or commit secrets.
- Never include ignored local state under `.memories/`.
- Respect dirty worktrees; do not revert user changes.
- Do not bypass hooks unless the user explicitly authorizes it.
- The main agent must not perform full staged-content diff review during this workflow; content-level review, secret detection, hygiene checks, and pre-commit remediation belong to `commit_specialist`.

## Post-Commit Review

After a successful commit:

1. If a related OpenSpec change exists, update its tasks, verification notes, or specs when the commit changes implementation status. Do not create a change retroactively for a simple commit.
2. Decide whether the session produced durable facts, decisions, lessons, environment constraints, recurring problems, or verified resolutions worth routing through `save-memory` or `memory-sql`.
3. Use `skill-review` for user corrections, non-obvious techniques, reusable workflows, or corrected skill guidance.
4. Do not store commit narration, duplicate plan content, or transient failures in memory.
