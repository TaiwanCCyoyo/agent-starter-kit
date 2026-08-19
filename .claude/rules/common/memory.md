---
paths:
    - "*"
---

# Memory Routing

Claude's only durable memory in this repository is Claude Code's built-in memory
(`~/.claude/projects/<project>/memory/`). `.memories/` is shared state owned by Codex and
Antigravity, not a Claude write target.

- Route stable user habits and preferences (`type: user` / `feedback`) and durable project
  facts (`type: project`) to built-in memory.
- Route facts that belong to the repository itself — conventions, invariants, routing —
  into `CLAUDE.md`, `.claude/rules/`, or a skill instead of memory. Pairs with
  `skill-authoring`.
- Claude may create the `.memories/` skeleton and sync it into new worktrees so Codex and
  Antigravity sessions find their state, but must not read `.memories/` as session context
  and must not modify content that already exists there.
