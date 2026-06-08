---
name: memory-sql
description: Use when querying or writing the Holographic-compatible SQLite store at .memories/memory_store.db.
---

# Memory SQL

Codex accesses `.memories/memory_store.db` through the `memory-db` SQLite MCP server.

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
3. Ask for approval before database writes when tool policy requires it.
4. Store one concise fact per row with an accurate category, tags, and trust score.
5. Use a stable semantic fingerprint for recurring problems, not a raw error string.
6. On recurrence, insert an occurrence, update the pattern count and timestamps, then investigate root cause.
7. Mark a resolution `verified` only with concrete verification evidence.

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
