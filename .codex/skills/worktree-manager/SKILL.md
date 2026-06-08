---
name: worktree-manager
description: Use when creating, managing, finishing, merging, or cleaning up Git worktrees while preserving shared project memory.
---

# Worktree Manager

## Start

1. Identify the main repository and target worktree.
2. Copy missing `.memories/` items from the main workspace without overwriting worktree-local memory.
3. Ensure `memories/MEMORY.md`, `memories/USER.md`, and `memory_store.db` exist.
4. Confirm the branch goal through Codex native planning or user alignment.

## During Work

- Keep stable cross-session facts in the bounded files.
- Query and update structured facts or recurring-problem history through `memory-sql`.
- Keep plans in Codex planning state, `.tmp/`, or maintained `docs/`.

## Finish

1. Verify the branch changes.
2. Consolidate only durable, non-duplicate facts and verified problem resolutions.
3. Do not overwrite newer main-workspace memory.
4. Merge or clean up the worktree only when explicitly requested.

Never treat ignored memory as Git merge content.
