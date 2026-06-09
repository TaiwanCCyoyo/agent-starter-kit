---
description: Create, manage, finish, merge, or clean up Git worktrees while preserving project memory. Use when asked to create a branch worktree, consolidate worktree memory, or finish a worktree.
---

# Worktree Manager

Follow `.claude/skills/worktree-memory-sync/SKILL.md` for the repository-specific `.memories/` synchronization rules. Worktree lifecycle (creation, branching, setup, finish, cleanup) is provided by Superpowers.

## Creation

Use the Superpowers worktree workflow for detection, consent, creation, setup, and baseline verification. After creation, copy only missing `.memories/` items and never overwrite worktree-local `MEMORY.md`, `USER.md`, or `memory_store.db`.

## Active Development

- Keep durable memory within the approved `.memories/` taxonomy.
- Keep approved cross-session plans under `.references/plans/`.
- Use `/memory-sql` for searchable facts and recurring-problem history.

## Finish

Before removing a worktree:

1. Verify the definition of done.
2. Run relevant tests or checks.
3. Read the worktree memory and main repository memory.
4. Consolidate durable, non-duplicate memory into the current main-workspace state.
5. Follow Superpowers for merge, PR, preservation, or cleanup.

## Consolidation

When consolidating worktree memory:

1. Identify source and destination `.memories/` directories.
2. Compare bounded files and query structured memory before writes.
3. Transfer only durable, non-duplicate facts and verified resolutions.
4. Preserve newer main-workspace entries.
5. Update the related `.references/plans/*.plan.md` with status, verification, and commit when relevant.
6. Report consolidated items and skipped duplicates.

## Safety

- Do not delete a worktree with uncommitted work unless the user explicitly authorizes it.
- Do not discard branch-specific memory before consolidation.
- Do not force-delete branches unless explicitly requested.
