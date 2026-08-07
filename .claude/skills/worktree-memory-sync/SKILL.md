---
name: worktree-memory-sync
description: Use when the user says /worktree, worktree create, worktree finish, create branch worktree, merge worktree, consolidate worktree memory, or asks Claude to create, manage, finish, merge, or clean up Git worktrees while preserving project memory.
---

# Worktree Memory Sync

Worktree lifecycle (creation, branching, setup, baseline verification, finish, cleanup) uses native Git operations. This skill contains the repository-specific `.memories/` synchronization behavior that Git cannot provide for this project's git-ignored memory state.

## Starting a Worktree (Memory Setup)

After the native Git workflow creates the worktree:

1. Copy only **missing** `.memories/` items from the main workspace into the worktree.
2. Never overwrite worktree-local bounded files (`memories/MEMORY.md`, `memories/USER.md`) or SQLite state (`memory_store.db`) if they already exist.
3. Verify that `memories/MEMORY.md`, `memories/USER.md`, and `memory_store.db` are present before starting work.

## During Work

- Keep stable cross-session facts in the bounded files.
- Query and update structured facts through `/memory-sql`.
- Keep plans in agent-native planning state, `.tmp/`, or maintained `docs/`.

## Finishing a Worktree (Memory Consolidation)

Before the native Git workflow removes the worktree:

1. Compare worktree memory against the current main-workspace versions.
2. Merge only **durable, non-duplicate** facts and verified resolutions into the main workspace.
3. Preserve newer main-workspace entries — never overwrite them with older worktree content.
4. Never treat `.memories/` as Git merge content; it is git-ignored and must be synchronized manually.

## Safety Rules

- Do not delete a worktree with uncommitted work unless the user explicitly authorizes it.
- Do not discard branch-specific memory before consolidation.
- Never force-delete branches unless explicitly requested.
- Never treat ignored memory as Git merge content.
