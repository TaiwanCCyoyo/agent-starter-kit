---
paths:
    - ".memories/**"
---

# Memory Storage Safety

`.memories/` is Codex/Antigravity-owned shared state, not a Claude memory target — see
`common/memory.md` for where Claude's own durable memory lives.

- Never stage or commit `.memories/` contents; it is git-ignored.
- Never edit `MEMORY.md`, `USER.md`, or `memory_store.db` beyond the initial skeleton
  Claude's SessionStart hook creates when they do not yet exist.
- Never edit `memory_store.db` as a regular file.
- Content ownership (routing, compression, database writes) belongs to Codex and
  Antigravity, not Claude.
