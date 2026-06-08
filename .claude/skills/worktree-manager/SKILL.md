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
| **Memory** | No dedicated memory needed | Scoped `MEMORY.md` plus bounded memory layout |
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

### Start

1. Identify the main repository and target worktree.
2. Copy missing `.memories/` items from the main workspace without overwriting worktree-local memory.
3. Ensure `memories/MEMORY.md`, `memories/USER.md`, and `memory_store.db` exist.
4. Confirm the branch goal through user alignment before starting implementation.

### During Work

- Keep stable cross-session facts in the bounded files.
- Query and update structured facts or recurring-problem history through `/memory-sql`.
- Keep plans in agent-native planning state, `.tmp/`, or maintained `docs/`.

### Finish

1. Verify the branch changes and run relevant checks.
2. Consolidate only durable, non-duplicate facts and verified problem resolutions.
3. Do not overwrite newer main-workspace memory.
4. Merge the branch, then remove the worktree only when explicitly requested.
5. Delete the branch only after the merge succeeds.
6. Run `/learn-eval` — check whether patterns from this branch deserve skill extraction.

---

## Safety (Both Modes)

- Do not delete a worktree with uncommitted work unless the user explicitly authorizes it.
- Do not discard branch-specific memory before consolidation (Mode B).
- Do not force-delete branches unless explicitly requested.
- Never treat ignored memory as Git merge content.
