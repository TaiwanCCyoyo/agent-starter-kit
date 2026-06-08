---
name: worktree-manager
description: Use when the user says /worktree, worktree create, worktree finish, create branch worktree, merge worktree, consolidate worktree memory, or asks Claude to create, manage, finish, merge, or clean up Git worktrees while preserving project memory.
---

# Worktree Manager

Two modes serve different needs. Choose based on task duration and memory requirements.

## Mode Selection

| Dimension | Mode A: Quick Isolation | Mode B: Feature Branch |
|-----------|------------------------|----------------------|
| **Duration** | Single session, hours | Multi-session, days |
| **Memory** | No dedicated memory needed | Scoped `MEMORY.md` plus the approved memory layout |
| **Branching** | Auto (built-in tool manages) | Manual branch strategy |
| **Cleanup** | `ExitWorktree(remove)` | Full finish workflow |
| **Use when** | Experiments, isolated fixes, subagent tasks | Features, refactors requiring handoff |

---

## Mode A: Quick Isolation

Uses Claude Code's built-in `EnterWorktree` / `ExitWorktree` tools. The built-in tool creates the worktree inside `.claude/worktrees/` and switches the session CWD automatically.

### Start

```
EnterWorktree(name="<task-slug>")
```

- Creates a new branch and worktree at `.claude/worktrees/<task-slug>/`.
- Session CWD switches to the worktree; system prompt, memory files, and plans reload from the new CWD.
- `worktree.baseRef` in settings controls branching: `fresh` (from origin default branch) or `head` (from current HEAD).

### Work

- Make changes in the isolated environment.
- No separate memory management needed — keep notes in the conversation or in temporary files.

### Finish

```
ExitWorktree(action="keep")    # keep branch and files for later review
ExitWorktree(action="remove")  # discard worktree (confirm no needed changes first)
```

`action: "remove"` with `discard_changes: true` force-removes even with uncommitted work — use only when explicitly authorized.

After exit, run `/learn-eval` if the session produced non-obvious techniques worth saving.

---

## Mode B: Feature Branch

Uses `git worktree add` directly for long-lived branches with dedicated memory and formal handoff.

### Creation

1. Create the branch and worktree: `git worktree add <path> <branch>`.
2. Ensure `.agents/memory/MEMORY.md` exists in the worktree (the `session_start.py` hook copies it automatically on first open).
3. Immediately define the worktree mission in the session-start project context:
   - Branch goal.
   - Definition of done.
   - Any constraints from the user request.
4. Do not leave `[MISSION REQUIRED]` in the new worktree memory.

### Active Development

- Use the local worktree memory for task progress.
- Mark entries with the branch name when needed.
- Keep compact branch status in `MEMORY.md`.
- Keep compact branch status in `MEMORY.md`; put detailed handoff in an active `changes/<id>/` plan.
- Keep recurring branch lessons concise in `lessons.md`; graduate stale lessons to `memory.db` via `/memory-sql` or `archive/`.
- Keep branch-specific multi-step plans under `changes/<change-id>/` and consolidate/archive them before worktree removal.

### Finish

Before removing a worktree:

1. Verify the definition of done.
2. Run relevant tests or checks.
3. Read the worktree memory and main repository memory.
4. Consolidate durable lessons and meaningful completed milestones into the main memory.
5. Run `/learn-eval` — check whether patterns from this branch deserve skill extraction.
6. Merge the branch into the target branch.
7. Remove the worktree: `git worktree remove <path>`.
8. Delete the branch only after the merge succeeds.

### Consolidation

When consolidating worktree memory:

1. Identify source and destination memory directories.
2. Read `MEMORY.md` plus relevant on-demand files from both locations.
3. Transfer only high-signal lessons, architectural decisions, active handoff, and meaningful completed milestones.
4. Route consolidated items to the correct destination file instead of forcing everything into `MEMORY.md`.
5. Move completed, rejected, or superseded worktree change plans to `archive/changes/` after consolidation.
6. Avoid duplicate entries.
7. Prefix branch-specific milestones when context matters.
8. Report consolidated items, target files, archived change folders, and skipped duplicates.

---

## Safety (Both Modes)

- Do not delete a worktree with uncommitted work unless the user explicitly authorizes it.
- Do not discard branch-specific memory before consolidation (Mode B).
- Do not force-delete branches unless explicitly requested.
- For Mode A with `ExitWorktree(remove)`: confirm no changes are needed before removing.
