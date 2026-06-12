---
name: memory-sql
description: Use when querying or writing to the Holographic-compatible SQLite store at .memories/memory_store.db via the memory-db MCP server.
---

# Memory SQL

This skill is the sole owner of SQLite memory operations. Claude Code accesses `.memories/memory_store.db` through the `memory-db` SQLite MCP server configured in `.mcp.json`; never edit the database as a regular file.

## Use It For

- Searching or storing curated facts, decisions, lessons, workflows, tool facts, and environment facts.
- Recording recurring problem patterns and concrete occurrences.
- Maintaining root causes and verified resolutions.
- Reviewing trust, retrieval, and helpfulness metadata.

Do not store raw transcripts, temporary plans, task narration, secrets, or duplicate bounded file entries.

## Core Tables

Holographic-compatible tables:

- `facts`
- `entities`
- `fact_entities`
- `memory_banks`
- `facts_fts`

Starter-kit problem lifecycle tables:

- `problem_patterns`
- `problem_occurrences`
- `resolutions`

The schema is initialized by `scripts.memory_store.initialize_memory_store`.

## Workflow

1. Use `list_tables` or `describe_table` before assuming schema state.
2. Search `facts_fts` and relevant problem tables before every insert.
3. Receive write intent from `save-memory`, `compress-memory`, or an explicit user request; ask for approval when tool policy requires it.
4. Store one concise fact per row with an accurate category, tags, and trust score.
5. Use a stable semantic fingerprint for recurring problems, not a raw error string.
6. On recurrence, insert an occurrence, update the pattern count and timestamps, then investigate root cause.
7. Mark a resolution `verified` only with concrete verification evidence.
8. Return concise results to the calling workflow; retrieved rows remain context until curated.

Example fact search:

```sql
SELECT f.fact_id, f.category, f.tags, f.trust_score, f.content
FROM facts_fts x
JOIN facts f ON f.fact_id = x.rowid
WHERE facts_fts MATCH '<keywords>'
ORDER BY f.trust_score DESC, f.updated_at DESC
LIMIT 20;
```

Example problem lookup:

```sql
SELECT p.*, r.solution, r.verification, r.status AS resolution_status
FROM problem_patterns p
LEFT JOIN resolutions r ON r.resolution_id = p.resolution_id
WHERE p.fingerprint = '<stable-fingerprint>';
```
