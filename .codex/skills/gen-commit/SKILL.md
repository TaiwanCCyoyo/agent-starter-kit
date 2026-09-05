---
name: gen-commit
description: Prepare commit messages and create scoped local Git commits with pre-commit checks and optional specialist delegation. Use for /gen-commit, commit requests, and automatic agent-owned commits.
---

# Gen Commit

This is a command-like Codex skill that can be invoked with plain text such as `/gen-commit`.

The main agent owns scope, staging authorization, sandbox fallback, and post-commit review. Use `commit-specialist` for substantial staged-content review, rough or missing messages, or an explicitly requested independent check. For a small, verified agent-owned change with a complete message and no unrelated staged files, the main agent may run the same checks and commit directly; do not delegate merely to repeat work already completed. If delegation is unavailable, follow the same workflow locally.

## Workflow

1. Determine message-only versus commit execution from the request and standing authorization; ask only if that intent remains ambiguous.
2. Inspect staged scope at filename/status level only, such as with `git status --short` or `git diff --cached --name-status`.
3. If nothing is staged, inspect unstaged filenames/status only. Stage automatically when the operating contract authorizes a verified agent-owned commit or the user explicitly requested staging; otherwise ask first.
4. Exclude forbidden or unrelated unstaged paths. If the index already contains unrelated changes, preserve it and resolve the commit boundary before execution; ask only when ownership cannot be established from the session.
5. When the user explicitly authorizes commit execution or autonomous staging, identify intended submodule paths. Confirm each submodule has a committed `HEAD`, run `git add -- <submodule-path>` in the superproject, and record its staged gitlink state. Do not stage a submodule without that authorization.
6. If delegating, select and state the delegation mode using Mode Selection below. Do not automatically escalate to diff review merely because review could provide extra confidence: use **accept supplied message**, **review supplied message**, or **complete rough or missing message** according to what the main agent actually knows and requests. For direct execution, the main agent owns the equivalent scope checks, pre-commit, bounded recovery, and commit.
    - **Direct path:** Run pre-commit on approved paths, inspect any formatter changes, apply bounded Hook Recovery if needed, and execute the authorized commit with normal hooks. For message-only requests, return the message without committing. Skip steps 7-11 and proceed to step 12 after a commit; permission failures require the main agent's normal authorized escalation, not environment workarounds.
    - **Delegated path:** Follow steps 7-11 below.
7. When delegating, send one review objective with explicit paths, acceptance criteria, the user's intent, filename-level staged scope, delegation mode, any supplied commit message, and every staged submodule gitlink state to `commit-specialist`.
8. The specialist verifies staged filenames and each handed-off gitlink, then follows only the selected mode's diff policy. It runs pre-commit against the approved paths in every mode and prepares or accepts an English Conventional Commit message. It must not commit inside a submodule or broaden the approved scope.
9. For a simple, directly actionable formatter or hook failure, the specialist applies Hook Recovery below. If the user requested only a message, it then returns the message without committing. If a commit is authorized, it executes `git commit` with the approved message and lets normal commit-time hooks run.
10. If pre-commit, hook recovery, or commit execution fails because the sandbox cannot write `.git/index.lock`, the user-level `uv` cache, a hook cache, or another permission-constrained path, the specialist must immediately return the exact error to the main agent. It must not retry that sandbox-failed step, relocate or rebuild caches, change ACLs, alter cache-related environment variables, bypass hooks, or attempt another environment workaround.
11. The main agent decides whether the reported error is a sandbox handoff case. If so, it resumes the same verification or commit step once in its authorized execution context without duplicating the specialist's completed detailed review.
12. After a successful commit, the main agent runs the Post-Commit Review because only it has the full session context.

## Why Commit Has A Main-Agent Fallback

On Codex Desktop for Windows, delegated agents can edit workspace files but may be unable to create `.git/index.lock`; their user-level `uv` cache may also be read-only. These restrictions can change as Codex sandbox behavior evolves, so they are not grounds for permanently preventing delegated commit execution.

In the delegated path, the specialist owns the selected review and commit work. A permission or sandbox failure is a handoff signal: the specialist reports it without changing caches or permissions, and the main agent resumes the blocked step in its authorized context. Direct execution follows the same scope and verification requirements without this handoff. Neither path bypasses hooks.

## Commit Message Standard

- Use English only.
- Use Conventional Commits: `<type>[optional scope]: <description>`.
- Use imperative mood.
- Start the description with lowercase.
- Do not end the subject with a period.
- Keep the subject under 50 characters when practical.
- Use the body to explain why and how for complex changes.

## Safety

- Never stage or commit secrets.
- Respect dirty worktrees; do not revert user changes.
- Do not bypass hooks unless the user explicitly authorizes it.
- When delegating, do not duplicate the specialist's completed full staged-content review or pre-commit run unless files changed or unresolved evidence warrants it. Normal commit-time hooks still run; neither execution route bypasses them.

## Mode Selection

1. **Unknown change intent:** Use **complete rough or missing message**. The specialist inspects the staged diff and derives the message.
2. **Approximate change intent:** Use **complete rough or missing message** with the rough intent. The specialist inspects the staged diff, checks the rough intent, and writes the complete message.
3. **Exact intent in a clean, well-understood scope:** Use **accept supplied message**. The specialist must not inspect the staged diff or revise the complete supplied message; it verifies filenames, then focuses on pre-commit, bounded ordinary hook recovery, and commit execution.
4. **Exact intent but explicit double-check requested:** Use **review supplied message**. The specialist inspects only the approved staged diff, checks it against the supplied message, and still focuses on pre-commit, bounded ordinary hook recovery, and commit execution. Use this mode only when the main agent explicitly requests the extra review because of a dirty or shared worktree, unexplained state, or another concrete concern. The specialist must not promote itself into this mode merely because additional review might be useful.

## Hook Recovery

The specialist may fix one simple, directly actionable pre-commit or commit-hook failure, inspect the resulting diff, re-stage only the approved paths, and retry once. Sandbox or permission failures are excluded from recovery and must be handed off immediately under the workflow above. For any failure requiring non-trivial investigation, broader changes, or unclear ownership, stop and report the error, attempted fix, affected paths, and required user decision. Never bypass hooks without explicit authorization.

## Post-Commit Review

After a successful commit:

1. Verify the committed scope and remaining worktree status, then report the commit hash and checks. Include related OpenSpec status and reusable workflow corrections in the verified commit before execution when possible; do not create an OpenSpec change merely to commit.
2. Apply the standing workflow-improvement authorization in `.codex/AGENTS.md` to concrete reusable findings; verify and commit any necessary follow-up, then report it.
3. Put required repository guidance in checked-in files. Write native memory only on an explicit user request, following the active memory storage rules.
4. Do not preserve commit narration, duplicate plan content, or transient failures as durable knowledge.
