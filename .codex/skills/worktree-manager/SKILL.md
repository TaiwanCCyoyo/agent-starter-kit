---
name: worktree-manager
description: Use when the user says /worktree, worktree, worktree create, worktree finish, create branch worktree, merge worktree, consolidate worktree memory, or asks Codex to create, manage, finish, merge, or clean up Git worktrees while preserving project memory.
---

# Worktree Manager

This is a Codex-private skill. It is intentionally stored in `.codex/skills` and loaded through `.codex/AGENTS.md`, not through the default `.agents/skills` discovery path.

This is also a command-like Codex skill. It replaces Gemini-style `/worktree` with a skill trigger that can be invoked by plain text.

## Creation

When creating a worktree:

1. Create the branch and worktree with `git worktree add <path> <branch>`.
2. Ensure `.agents/memory/MEMORY.md` exists in the worktree.
3. Immediately define the worktree mission in the `Doing` section:
   - Branch goal.
   - Definition of done.
   - Any constraints from the user request.
4. Do not leave `[MISSION REQUIRED]` in the new worktree memory.

## Active Development

- Use the local worktree memory for task progress.
- Mark entries with the branch name when needed.
- Keep unfinished work in `Session Handover`.

## Finish

Before removing a worktree:

1. Verify the definition of done.
2. Run relevant tests or checks.
3. Read the worktree memory and main repository memory.
4. Consolidate durable lessons and meaningful completed milestones into the main memory.
5. Merge the branch into the target branch.
6. Remove the worktree.
7. Delete the branch only after the merge succeeds.

## Consolidation

When consolidating worktree memory:

1. Identify the source memory file and destination `.agents/memory/MEMORY.md`.
2. Read both files.
3. Transfer only high-signal lessons, architectural decisions, and completed milestones.
4. Avoid duplicate entries.
5. Prefix branch-specific milestones when context matters.
6. Report consolidated items and skipped duplicates.

## Safety

- Do not delete a worktree with uncommitted work unless the user explicitly authorizes it.
- Do not discard branch-specific memory before consolidation.
- Do not force-delete branches unless explicitly requested.
