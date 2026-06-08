---
name: worktree-manager
description: Use when creating, managing, finishing, merging, or cleaning up Git worktrees while preserving shared project memory.
---

# Worktree Manager

## Creation

1. Create the branch and worktree with `git worktree add`.
2. Copy missing ignored memory from the main workspace without overwriting local worktree memory.
3. Ensure the approved taxonomy exists: `MEMORY.md`, `USER.md`, `decisions.md`, `lessons.md`, `changes/`, and `archive/`.
4. Define the branch goal and definition of done in `MEMORY.md`.

## Active Work

- Keep compact branch status in `MEMORY.md`.
- Keep detailed multi-step plans under `changes/<id>/`.
- Keep active decisions and recurring lessons concise.
- Query shared searchable history with `memory-sql` when historical context is needed.

## Finish

1. Verify the definition of done and run relevant checks.
2. Compare worktree and main memory.
3. Consolidate only durable, non-duplicate state, decisions, and lessons.
4. Graduate stale searchable entries through `memory-sql`; move completed plan history to `archive/`.
5. Merge the branch, then remove the worktree.
6. Delete the branch only after the merge succeeds.

Never discard uncommitted work or branch-specific memory without explicit authorization.
