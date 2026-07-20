---
paths:
    - ".memories/**"
---

# Memory Storage Safety

Apply these invariants whenever reading or changing instantiated memory:

- Treat `.memories/` as git-ignored cross-agent state; never stage or commit its contents.
- Keep `MEMORY.md` at or below 2,200 characters and `USER.md` at or below 500 characters.
- Keep bounded entries atomic and preserve `§` on its own line between entries.
- Treat bounded-file writes as next-session updates because the current session snapshot is frozen.
- Search for duplicates before writing and re-read the destination after writing.
- Never store secrets, credentials, private user data, raw transcripts, plans, command narration, or uncurated retrieval output.
- Never edit `memory_store.db` as a regular file; use the `memory-sql` skill and `memory-db` MCP tools.
- The main agent owns final writes even when a memory subagent drafts recommendations.
