---
description: Initialize, read, update, audit, or compress .agents/memory/ for this repository. Follows the Hermes-aligned Hot/Warm/Cold structure shared across all agents.
---

# Memory Maintenance

Follow `.claude/skills/memory-manager/SKILL.md` for the full routing rules and lifecycle.

## Memory Structure (Hermes-aligned)

### Hot (injected at session start)
- `MEMORY.md` — mission, constraints, current state (≤ 2,200 chars)
- `USER.md` — cross-agent user preferences (≤ 500 chars)

### Warm (on demand)
- `decisions.md` — durable architectural decisions
- `lessons.md` — concise recurring lessons (tail auto-loaded)
- `changes/<id>/` — active change plans

### Cold (never auto-loaded)
- `memory.db` — SQLite FTS5 via `/memory-sql` (Claude Code MCP)
- `archive/` — completed plans, historical reference

## Routing Rules

- Mission, constraints, current state summary → `MEMORY.md`
- User preferences, working style → `USER.md`
- Durable decisions (active) → `decisions.md`
- Stale decisions / lessons → `memory.db` then remove from source file
- Active multi-step change plan → `changes/<id>/`
- Completed change → `archive/` after consolidation
- Skill candidate → `/learn-eval` or `memory.db` (`type='candidate'`)
- User collaboration preferences → `CLAUDE.md` Operating Contract or `~/.claude/CLAUDE.md` (not in `.agents/memory/`)

## Compression

When MEMORY.md exceeds ~2,200 chars or lessons.md exceeds 50 lines, use `/compress-memory`. Graduate stale entries to `memory.db` via `/memory-sql` rather than adding more files.
