---
name: gen-commit
description: Use when the user says /gen-commit, gen-commit, generate commit, create commit message, commit staged changes, commit changes, or asks Codex to perform a Git commit; enforces staged-change review, secret checks, Conventional Commits, English metadata, hook failure handling, and AI identity trailers.
---

# Gen Commit

This is a command-like Codex skill that can be invoked with plain text such as `/gen-commit`.

The main agent performs filename-level preflight and delegates execution or message drafting to `commit-specialist`.

## Workflow

1. Confirm whether the user wants only a commit message or wants Codex to execute a commit.
2. Inspect staged scope at filename/status level only, such as with `git status --short` or `git diff --cached --name-status`.
3. If nothing is staged, inspect unstaged filenames/status only and ask before staging unless the user explicitly requested autonomous staging.
4. Stop and ask before delegating if filename-level preflight shows obvious forbidden or suspicious paths such as `.env`, credentials, `.memories/`, generated state, or unrelated files.
5. When the user explicitly authorizes commit execution or autonomous staging, identify intended submodule paths. Confirm each submodule has a committed `HEAD`, run `git add -- <submodule-path>` in the superproject, and record its staged gitlink state. Do not stage a submodule without that authorization.
6. Select and state the delegation mode based on the main agent's confidence in the staged changes. Do not duplicate diff review: if the main agent needs a diff review, delegate it to `commit-specialist` instead of reading the diff itself. Use **execute supplied message**, **review supplied message**, or **complete rough or missing message**.
7. Delegate one concrete objective with explicit paths, requested output, acceptance criteria, the user's intent, filename-level staged scope, delegation mode, any supplied commit message, and every staged submodule gitlink state to `commit-specialist`.
8. The specialist verifies each handed-off gitlink and must not commit inside a submodule. It must return a handoff failure for an uncommitted submodule, unexpected gitlink delta, or a pre-commit failure that cannot be fixed simply; the main agent decides the next step.
9. If the user requested only a message, instruct `commit-specialist` to return the message without committing. If the user requested a commit, instruct it to execute `git commit`.
10. After a successful commit, the main agent, not `commit-specialist`, runs the Post-Commit Review because only the main agent has the full session context.

## Commit Message Standard

- Use English only.
- Use Conventional Commits: `<type>[optional scope]: <description>`.
- Use imperative mood.
- Start the description with lowercase.
- Do not end the subject with a period.
- Keep the subject under 50 characters when practical.
- Use the body to explain why and how for complex changes.

## AI Commit Trailers

- Every commit drafted or executed by Codex must include `Co-authored-by: Codex gpt-5.6 <codex@openai.com>` as its formal AI identity.
- Place trailers after a blank line following the body, or after the subject if there is no body.
- Example:

```text
feat(codex): add targeted hygiene checks

Add file-scoped hook checks and repository-level Python gates.

Co-authored-by: Codex gpt-5.6 <codex@openai.com>
```

## Safety

- Never stage or commit secrets.
- Never include ignored local state under `.memories/`.
- Respect dirty worktrees; do not revert user changes.
- Do not bypass hooks unless the user explicitly authorizes it.
- The main agent must not perform full staged-content diff review during this workflow; content-level review, secret detection, hygiene checks, and pre-commit remediation belong to `commit-specialist`.

## Delegation Modes

- **Execute supplied message**: Do not inspect the staged diff or revise the complete supplied message; commit it directly with the required Codex trailer.
- **Review supplied message**: Inspect the staged diff only when the main agent explicitly requests a review. Use the supplied message unless the main agent requests revisions.
- **Complete rough or missing message**: Inspect the staged diff and draft a complete message before returning it or committing.

## Hook Recovery

For any execution mode, fix only a simple, directly actionable pre-commit failure, re-stage the affected files, and retry once. For any failure requiring non-trivial investigation, a broader change, or an unclear fix, stop and return the error, attempted fix, affected paths, and the parent-agent decision required.

## Post-Commit Review

After a successful commit:

1. If a related OpenSpec change exists, update its tasks, verification notes, or specs when the commit changes implementation status. Do not create a change retroactively for a simple commit.
2. Decide whether the session produced durable facts, decisions, lessons, environment constraints, recurring problems, or verified resolutions worth routing through `save-memory` or `memory-sql`.
3. Use `skill-review` for user corrections, non-obvious techniques, reusable workflows, or corrected skill guidance.
4. Do not store commit narration, duplicate plan content, or transient failures in memory.
