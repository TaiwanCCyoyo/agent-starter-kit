---
name: worktree-memory-sync
description: Preserve and consolidate shared project memory when work happens in a Git worktree.
---

# Worktree Memory Sync

Use native Git worktree operations for creation, setup, completion, and cleanup. Use this skill for the ignored `.memories/` state that Git cannot carry between worktrees.

## Initialize

1. Identify the main workspace and target worktree.
2. Copy only missing `.memories/` items from the main workspace.
3. Never overwrite worktree-local `MEMORY.md`, `USER.md`, or `memory_store.db`.
4. Ensure the bounded files and SQLite store exist before memory-dependent work.

## Consolidate

1. Compare worktree memory with the current main-workspace state.
2. Merge only durable, non-duplicate facts and verified problem resolutions.
3. Preserve newer main-workspace entries when the same fact differs.
4. Use `memory-sql` for SQLite facts and recurring-problem history.

Never treat ignored memory as Git merge content or copy it wholesale over newer state.
