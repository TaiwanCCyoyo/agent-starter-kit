---
description: Initialize, read, update, audit, or compress .memories/ for this repository. Follows the shared storage, loading, size, and searchable-history rules.
---

# Memory Maintenance

Follow `.claude/skills/memory-manager/SKILL.md` for the full routing rules and lifecycle.

## Storage And Loading

### Session-start context
- `.memories/memories/MEMORY.md` — stable project, environment, and tool facts (≤ 2,200 chars)
- `.memories/memories/USER.md` — stable user preferences (≤ 500 chars)

### Search or inspect when needed
- `.memories/memory_store.db` — SQLite via `/memory-sql` (Claude Code MCP)

## Routing Rules

- Stable project facts needed in most sessions → `.memories/memories/MEMORY.md`
- Stable user preferences → `.memories/memories/USER.md`
- Searchable facts, decisions, lessons, workflows → `facts` table in `memory_store.db`
- Recurring problem patterns and occurrences → `problem_patterns` / `problem_occurrences`
- Verified root causes and fixes → `resolutions`
- Skill candidate → `/learn-eval` or `facts` (`category='candidate'`)

## Compression

When MEMORY.md exceeds ~2,200 chars, use `/compress-memory`. Move searchable lower-frequency knowledge into `facts` after a deduplication query rather than accumulating more file content.
