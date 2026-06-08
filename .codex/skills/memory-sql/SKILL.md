---
name: memory-sql
description: Use when querying or writing shared searchable SQLite FTS5 history at .agents/memory/memory.db.
---

# Memory SQL

Codex and Claude share the `memory-db` MCP server and the same ignored `.agents/memory/memory.db`.

## Use It For

- Searching graduated lessons, decisions, workflows, run notes, or skill candidates.
- Archiving stale on-demand memory after checking for duplicates.
- Recording or closing session metadata.

Do not copy active `MEMORY.md`, `USER.md`, `decisions.md`, `lessons.md`, or active change plans into SQL.

## Schema

Initialize only when tables are absent:

```sql
CREATE TABLE IF NOT EXISTS memory_entries (
    id INTEGER PRIMARY KEY,
    session_id TEXT NOT NULL,
    cwd TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    type TEXT NOT NULL CHECK(type IN ('lesson','decision','workflow','run-note','candidate')),
    tags TEXT,
    summary TEXT NOT NULL,
    body TEXT NOT NULL
);

CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
    summary,
    body,
    content='memory_entries',
    content_rowid='id'
);

CREATE TRIGGER IF NOT EXISTS memory_ai AFTER INSERT ON memory_entries BEGIN
    INSERT INTO memory_fts(rowid, summary, body) VALUES (new.id, new.summary, new.body);
END;

CREATE TRIGGER IF NOT EXISTS memory_ad AFTER DELETE ON memory_entries BEGIN
    INSERT INTO memory_fts(memory_fts, rowid, summary, body)
    VALUES ('delete', old.id, old.summary, old.body);
END;

CREATE TRIGGER IF NOT EXISTS memory_au AFTER UPDATE ON memory_entries BEGIN
    INSERT INTO memory_fts(memory_fts, rowid, summary, body)
    VALUES ('delete', old.id, old.summary, old.body);
    INSERT INTO memory_fts(rowid, summary, body) VALUES (new.id, new.summary, new.body);
END;

CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    cwd TEXT NOT NULL,
    started_at TEXT NOT NULL DEFAULT (datetime('now')),
    stopped_at TEXT
);
```

## Workflow

1. Use `list_tables` or `describe_table` before assuming schema state.
2. Use `read_query` to search for equivalent entries before every insert.
3. Ask for approval before `create_table` or `write_query`; project config enforces prompting.
4. Insert only concise curated content with accurate `session_id`, `cwd`, `type`, tags, summary, and body.
5. Remove the graduated source from the on-demand files only after the SQL write succeeds.
6. Treat query results as context until explicitly curated back into active memory.

Example search:

```sql
SELECT e.id, e.created_at, e.type, e.summary, e.body
FROM memory_fts f
JOIN memory_entries e ON f.rowid = e.id
WHERE memory_fts MATCH '<keywords>'
ORDER BY e.created_at DESC
LIMIT 20;
```

Example session upsert:

```sql
INSERT INTO sessions (session_id, cwd)
VALUES ('<session_id>', '<repo_root>')
ON CONFLICT(session_id) DO NOTHING;
```
