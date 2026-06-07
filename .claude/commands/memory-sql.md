---
description: Query or write to the project's SQLite cold memory database (.agents/memory/memory.db) via the memory-db MCP server. Use for FTS5 full-text search across archived sessions, archiving graduated entries, and recording session metadata.
---

# /memory-sql

Follow `.claude/skills/memory-sql/SKILL.md` for schema reference, core operations, and when to use SQL vs file-based memory.

Before issuing any write_query, verify the target table exists with list_tables. If the schema is not initialized, run the CREATE TABLE statements from the skill document first.
