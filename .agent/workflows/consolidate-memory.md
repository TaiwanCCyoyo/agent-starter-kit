---
description: Consolidate durable memory from another branch or worktree without overwriting newer local facts.
---

# Consolidate Memory

When the user runs `/consolidate-memory [source_path]`:

1. Read the source and target bounded memory files.
2. Query both SQLite stores for equivalent facts, recurring patterns, and resolutions.
3. Preserve only durable, non-duplicate facts and verified resolutions.
4. Merge stable high-frequency project facts into `.memories/memories/MEMORY.md`.
5. Merge stable user preferences into `.memories/memories/USER.md`.
6. Merge searchable facts and recurring-problem history through `memory-sql`.
7. Do not overwrite newer target facts or copy agent-specific state files.
8. Keep plans, transcripts, completed-task logs, and historical artifacts outside memory.

Report the merged and skipped information in Traditional Chinese.
