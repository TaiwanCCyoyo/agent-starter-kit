---
description: Create, manage, finish, merge, or clean up Git worktrees while preserving project memory. Use when asked to create a branch worktree, consolidate worktree memory, or finish a worktree.
---

# Worktree Manager

Use the `worktree-memory-sync` skill for the full worktree lifecycle: creation, active development, finish, consolidation, and safety rules. Worktree lifecycle mechanics (creation, branching, setup, finish, cleanup) use native Git worktree operations; the skill owns only the repository-specific `.memories/` synchronization that Git cannot provide.
