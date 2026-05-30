---
description: Create, manage, finish, merge, or clean up Git worktrees while preserving project memory. Use when asked to create a branch worktree, consolidate worktree memory, or finish a worktree.
---

# Worktree Manager

## Creation

When creating a worktree:

1. Create the branch and worktree with `git worktree add <path> <branch>`.
2. Ensure `.agents/memory/MEMORY.md` exists in the worktree.
3. Copy or initialize the official memory taxonomy when relevant: `decisions.md`, `lessons.md`, `lessons-archive.md`, `current-state.md`, `user-preferences.md`, `workflows.md`, `changes/`, `archive/`, `runs/`, and `candidates/`.
4. Immediately define the worktree mission in the Hot Memory current-state summary or active state:
   - Branch goal.
   - Definition of done.
   - Any constraints from the user request.
5. Do not leave `[MISSION REQUIRED]` in the new worktree memory.

## Active Development

- Use the local worktree memory for task progress.
- Mark entries with the branch name when needed.
- Keep compact branch status in `MEMORY.md`.
- Keep detailed unfinished work in `current-state.md`.
- Keep recurring branch lessons concise in `lessons.md`; move lower-frequency detail to `lessons-archive.md` or `archive/`.
- Keep branch-specific multi-step plans under `changes/<change-id>/` and consolidate/archive them before worktree removal.

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

1. Identify source and destination memory directories.
2. Read `MEMORY.md` plus relevant Warm files from both locations.
3. Transfer only high-signal lessons, architectural decisions, active handoff, and meaningful completed milestones.
4. Route consolidated items to the correct destination file instead of forcing everything into `MEMORY.md`.
5. Move completed, rejected, or superseded worktree change plans to `archive/changes/` after consolidation.
6. Avoid duplicate entries.
7. Prefix branch-specific milestones when context matters.
8. Report consolidated items, target files, archived change folders, and skipped duplicates.

## Safety

- Do not delete a worktree with uncommitted work unless the user explicitly authorizes it.
- Do not discard branch-specific memory before consolidation.
- Do not force-delete branches unless explicitly requested.
