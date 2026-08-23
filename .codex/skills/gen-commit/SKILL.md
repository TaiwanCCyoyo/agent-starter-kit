---
name: gen-commit
description: Use when the user says /gen-commit, gen-commit, generate commit, create commit message, commit staged changes, commit changes, or asks Codex to perform a Git commit; delegates detailed diff review, pre-commit, message drafting, and commit execution while retaining a sandbox-aware main-agent fallback.
---

# Gen Commit

This is a command-like Codex skill that can be invoked with plain text such as `/gen-commit`.

The main agent owns filename-level scope preflight, staging authorization, sandbox fallback, and post-commit review. It delegates detailed staged-content review, pre-commit verification, bounded ordinary hook recovery, commit-message drafting, and commit execution to `commit-specialist`.

## Workflow

1. Confirm whether the user wants only a commit message or wants Codex to execute a commit.
2. Inspect staged scope at filename/status level only, such as with `git status --short` or `git diff --cached --name-status`.
3. If nothing is staged, inspect unstaged filenames/status only. Stage automatically when the operating contract authorizes a verified agent-owned commit or the user explicitly requested staging; otherwise ask first.
4. Stop and ask before delegating if filename-level preflight shows obvious forbidden or suspicious paths such as `.env`, credentials, generated state, or unrelated files.
5. When the user explicitly authorizes commit execution or autonomous staging, identify intended submodule paths. Confirm each submodule has a committed `HEAD`, run `git add -- <submodule-path>` in the superproject, and record its staged gitlink state. Do not stage a submodule without that authorization.
6. Select and state the delegation mode using Mode Selection below. Do not automatically escalate to diff review merely because review could provide extra confidence: use **accept supplied message**, **review supplied message**, or **complete rough or missing message** according to what the main agent actually knows and requests.
7. Delegate one review objective with explicit paths, acceptance criteria, the user's intent, filename-level staged scope, delegation mode, any supplied commit message, and every staged submodule gitlink state to `commit-specialist`.
8. The specialist verifies staged filenames and each handed-off gitlink, then follows only the selected mode's diff policy. It runs pre-commit against the approved paths in every mode and prepares or accepts an English Conventional Commit message with the required trailer. It must not commit inside a submodule or broaden the approved scope.
9. For a simple, directly actionable formatter or hook failure, the specialist applies Hook Recovery below. If the user requested only a message, it then returns the message without committing. If a commit is authorized, it executes `git commit` with the approved message and lets normal commit-time hooks run.
10. If pre-commit, hook recovery, or commit execution fails because the sandbox cannot write `.git/index.lock`, the user-level `uv` cache, a hook cache, or another permission-constrained path, the specialist must immediately return the exact error to the main agent. It must not retry that sandbox-failed step, relocate or rebuild caches, change ACLs, alter cache-related environment variables, bypass hooks, or attempt another environment workaround.
11. The main agent decides whether the reported error is a sandbox handoff case. If so, it resumes the same verification or commit step once in its authorized execution context without duplicating the specialist's completed detailed review.
12. After a successful commit, the main agent runs the Post-Commit Review because only it has the full session context.

## Why Commit Has A Main-Agent Fallback

On Codex Desktop for Windows, delegated agents can edit workspace files but may be unable to create `.git/index.lock`; their user-level `uv` cache may also be read-only. These restrictions can change as Codex sandbox behavior evolves, so they are not grounds for permanently preventing delegated commit execution.

The specialist therefore owns the token-heavy staged diff review, pre-commit run, ordinary bounded hook recovery, message drafting, and normal commit execution. A permission or sandbox failure is a handoff signal, not a debugging task: the specialist reports it without changing caches or permissions, and the main agent resumes the blocked step in the existing authorized context. This preserves delegation when it works while avoiding repeated environment churn when it does not. The fallback is an execution-boundary decision, not a reason to bypass hooks.

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
- Respect dirty worktrees; do not revert user changes.
- Do not bypass hooks unless the user explicitly authorizes it.
- The main agent must not duplicate the specialist's full staged-content review or pre-commit run. The specialist owns detailed review, pre-commit, exact re-staging within approved paths, ordinary bounded hook recovery, message drafting, and commit execution; the main agent owns filename-level scope, authorization, and sandbox fallback.

## Mode Selection

1. **Unknown change intent:** Use **complete rough or missing message**. The specialist inspects the staged diff and derives the message.
2. **Approximate change intent:** Use **complete rough or missing message** with the rough intent. The specialist inspects the staged diff, checks the rough intent, and writes the complete message.
3. **Exact intent in a clean, well-understood scope:** Use **accept supplied message**. The specialist must not inspect the staged diff or revise the complete supplied message; it verifies filenames and the required trailer, then focuses on pre-commit, bounded ordinary hook recovery, and commit execution.
4. **Exact intent but explicit double-check requested:** Use **review supplied message**. The specialist inspects only the approved staged diff, checks it against the supplied message, and still focuses on pre-commit, bounded ordinary hook recovery, and commit execution. Use this mode only when the main agent explicitly requests the extra review because of a dirty or shared worktree, unexplained state, or another concrete concern. The specialist must not promote itself into this mode merely because additional review might be useful.

## Hook Recovery

The specialist may fix one simple, directly actionable pre-commit or commit-hook failure, inspect the resulting diff, re-stage only the approved paths, and retry once. Sandbox or permission failures are excluded from recovery and must be handed off immediately under the workflow above. For any failure requiring non-trivial investigation, broader changes, or unclear ownership, stop and report the error, attempted fix, affected paths, and required user decision. Never bypass hooks without explicit authorization.

## Post-Commit Review

After a successful commit:

1. If a related OpenSpec change exists, update its tasks, verification notes, or specs when the commit changes implementation status. Do not create a change retroactively for a simple commit.
2. Let Codex native memory retain useful user preferences and project context; put required repository rules in checked-in guidance instead of relying on recall.
3. Apply the Skill Authoring section in `.codex/AGENTS.md` to user corrections, non-obvious techniques, reusable workflows, or corrected skill guidance.
4. Do not preserve commit narration, duplicate plan content, or transient failures as durable knowledge.
