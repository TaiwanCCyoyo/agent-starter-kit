---
description: Manage Git worktrees while preserving shared project memory.
---

# Git Worktree Management

Use the `worktree-manager` skill for `/worktree [action] [arguments]`.

## Create

1. Create the branch and worktree with `git worktree add`.
2. Copy only missing `.memories/` items from the main workspace.
3. Ensure `memories/MEMORY.md`, `memories/USER.md`, and `memory_store.db` exist.
4. Confirm the branch goal and definition of done through planning or user alignment.
5. Report the created path and branch in Traditional Chinese.

## Finish

1. Verify the branch changes and definition of done.
2. Consolidate only durable, non-duplicate facts and verified problem resolutions.
3. Do not overwrite newer main-workspace memory.
4. Merge the branch only when requested.
5. Remove the worktree and delete the branch only when requested.
6. Report verification, consolidation, merge, and cleanup results in Traditional Chinese.

Ignored memory is local state and must not be treated as Git merge content.
