---
name: memory-sql
description: Use when querying or writing to the project's SQLite cold memory database (.agents/memory/memory.db) via the memory-db MCP server. Covers schema setup, session recording, FTS5 search, and the relationship to file-based memory layers.
---

# Memory SQL

The `memory-db` MCP server exposes `.agents/memory/memory.db` (SQLite with FTS5) as the **Cold Memory** layer. Unlike the file-based Hot/Warm layers (loaded at session start), this database is queried on demand and never auto-loaded into context — making it suitable for high-volume historical data.

The MCP server is launched via `.claude/scripts/start_memory_mcp.py` which resolves the project root and starts `uvx mcp-server-sqlite --db-path` at the correct database path.

---

## Layer Relationship

```
HOT   MEMORY.md (≤2,200 chars)   ← injected at session start (frozen snapshot)
      USER.md (≤500 chars)        ← cross-agent user preferences
WARM  decisions.md, lessons.md, changes/<id>/
COLD  memory.db (SQLite FTS5)    ← query on demand via memory-db MCP
      archive/
```

**Write to `memory.db` when:**
- Graduating a stale lesson or decision out of the Warm layer
- Recording a skill candidate for later `/learn-eval` review
- Closing out a session record (session_id + cwd)

**Do NOT duplicate** content already in MEMORY.md or active Warm files into the database.

---

## Schema Setup

Run these once to initialize the database (use `create_table` or `write_query` via the MCP):

```sql
-- Searchable memory entries archived from the file layer
CREATE TABLE IF NOT EXISTS memory_entries (
    id          INTEGER PRIMARY KEY,
    session_id  TEXT NOT NULL,
    cwd         TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    type        TEXT NOT NULL CHECK(type IN ('lesson','decision','workflow','run-note','candidate')),
    tags        TEXT,           -- comma-separated keywords
    summary     TEXT NOT NULL,  -- one-liner title / tl;dr
    body        TEXT NOT NULL   -- full markdown content
);

-- FTS5 virtual table (searches summary + body)
CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
    summary,
    body,
    content='memory_entries',
    content_rowid='id'
);

-- Triggers keep FTS index in sync automatically
CREATE TRIGGER IF NOT EXISTS memory_ai AFTER INSERT ON memory_entries BEGIN
    INSERT INTO memory_fts(rowid, summary, body)
    VALUES (new.id, new.summary, new.body);
END;

CREATE TRIGGER IF NOT EXISTS memory_ad AFTER DELETE ON memory_entries BEGIN
    INSERT INTO memory_fts(memory_fts, rowid, summary, body)
    VALUES ('delete', old.id, old.summary, old.body);
END;

CREATE TRIGGER IF NOT EXISTS memory_au AFTER UPDATE ON memory_entries BEGIN
    INSERT INTO memory_fts(memory_fts, rowid, summary, body)
    VALUES ('delete', old.id, old.summary, old.body);
    INSERT INTO memory_fts(rowid, summary, body)
    VALUES (new.id, new.summary, new.body);
END;

-- Session metadata (Stop hook has session_id + cwd)
CREATE TABLE IF NOT EXISTS sessions (
    session_id  TEXT PRIMARY KEY,
    cwd         TEXT NOT NULL,
    started_at  TEXT NOT NULL DEFAULT (datetime('now')),
    stopped_at  TEXT
);
```

---

## Core Operations

### Record a session (Stop hook prompt → Claude writes)

```sql
-- Open or upsert session record
INSERT INTO sessions (session_id, cwd)
VALUES ('<session_id>', '<cwd>')
ON CONFLICT(session_id) DO NOTHING;

-- Close session at end
UPDATE sessions SET stopped_at = datetime('now')
WHERE session_id = '<session_id>';
```

### Archive a memory entry

```sql
INSERT INTO memory_entries (session_id, cwd, type, tags, summary, body)
VALUES (
    '<session_id>',
    '<cwd>',
    'lesson',                        -- lesson | decision | workflow | run-note | candidate
    'hook,stop,memory',              -- comma-separated tags
    'Stop hook fires per-response, not once at session end',
    'The Claude Code Stop hook fires after every Claude response (each turn), not once when the session closes. Use response_count in state to throttle reminders.'
);
```

### FTS5 full-text search

```sql
-- Find entries mentioning a topic
SELECT e.created_at, e.type, e.summary, e.body
FROM memory_fts f
JOIN memory_entries e ON f.rowid = e.id
WHERE memory_fts MATCH 'FTS5 OR sqlite OR search'
ORDER BY e.created_at DESC
LIMIT 20;
```

### Structured filters

```sql
-- All decisions for this repo
SELECT created_at, summary FROM memory_entries
WHERE type = 'decision' AND cwd = '<repo_root>'
ORDER BY created_at DESC;

-- Skill candidates not yet promoted
SELECT created_at, summary, body FROM memory_entries
WHERE type = 'candidate'
ORDER BY created_at ASC;

-- Entries tagged 'hook' from last 30 days
SELECT created_at, type, summary FROM memory_entries
WHERE tags LIKE '%hook%'
  AND created_at >= datetime('now', '-30 days')
ORDER BY created_at DESC;

-- Sessions with the most entries
SELECT s.session_id, s.cwd, COUNT(e.id) AS entries
FROM sessions s
LEFT JOIN memory_entries e USING (session_id)
GROUP BY s.session_id
ORDER BY entries DESC
LIMIT 10;
```

### Deduplication check before inserting

```sql
-- Check if a near-identical lesson already exists before writing
SELECT id, summary FROM memory_entries
WHERE type = 'lesson'
  AND id IN (SELECT rowid FROM memory_fts WHERE memory_fts MATCH '<keyword>')
LIMIT 5;
```

---

## When to Use (vs File Layer)

| Situation | Use SQL | Use file layer |
|-----------|---------|----------------|
| Need to search across months of sessions | ✓ | |
| Loading context at session start | | ✓ MEMORY.md |
| Archiving an old lesson out of lessons.md | ✓ | |
| Active handoff note for current task | | ✓ changes/<id>/ or MEMORY.md |
| Storing a skill candidate for /learn-eval | ✓ type='candidate' | |
| Durable architectural decision | ✓ (archive copy) | ✓ decisions.md (active) |

---

## MCP Tool Reference

The `memory-db` MCP server exposes these tools:

| Tool | Use |
|------|-----|
| `read_query` | SELECT queries |
| `write_query` | INSERT / UPDATE / DELETE |
| `create_table` | CREATE TABLE / virtual table |
| `list_tables` | See all tables |
| `describe_table` | Get column schema |

The database is auto-created at `.agents/memory/memory.db` when the MCP server starts. Schema must be initialized manually (see **Schema Setup** above) on first use.
