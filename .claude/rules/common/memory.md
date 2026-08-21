---
paths:
    - "*"
---

# Memory Routing

Claude's only durable memory in this repository is Claude Code's built-in memory
(`~/.claude/projects/<project>/memory/`).

- Route stable user habits and preferences (`type: user` / `feedback`) and durable project
  facts (`type: project`) to built-in memory.
- Route repository conventions, invariants, and workflows into `CLAUDE.md`,
  `.claude/rules/`, checked-in documentation, or a skill instead of memory.
- Never store secrets, credentials, private user data, raw transcripts, or task narration.
