---
description: Query or write to the project's searchable SQLite memory database (.memories/memory_store.db) via the memory-db MCP server. Use for full-text search across facts, recording structured facts and decisions, and managing recurring-problem history.
---

# /memory-sql

Follow `.claude/skills/memory-sql/SKILL.md` for schema reference, core operations, and when to use SQL vs file-based memory.

Before issuing any write_query, verify the target table exists with list_tables. If the schema is not initialized, it is set up automatically by the session_start hook.
