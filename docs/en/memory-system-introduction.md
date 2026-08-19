# Memory System Introduction

The project memory system separates tracked agent infrastructure from local instantiated memory.

## Layout

```text
.memories/                       # Fully git-ignored instantiated memory
├── memories/
│   ├── MEMORY.md
│   └── USER.md
└── memory_store.db
```

`MEMORY.md` and `USER.md` follow Hermes's bounded atomic-entry format. Entries are separated by `§` on its own line and are injected as frozen session-start snapshots.

`memory_store.db` is SQLite. It uses the Hermes Holographic fact-store schema plus project-specific recurring-problem tables.

## Responsibilities

| Store                                                    | Purpose                                                                                    |
| :------------------------------------------------------- | :----------------------------------------------------------------------------------------- |
| `MEMORY.md`                                              | Stable project, environment, and tool facts needed in most future sessions; <= 2,200 chars |
| `USER.md`                                                | Stable user preferences and collaboration expectations; <= 500 chars                       |
| `facts`                                                  | Searchable decisions, lessons, workflows, tool facts, and environment facts                |
| `entities`, `fact_entities`, `memory_banks`, `facts_fts` | Holographic-compatible entity, retrieval, and FTS5 support                                 |
| `problem_patterns`                                       | Stable identities for recurring blockers, workarounds, mistaken assumptions, or confusion  |
| `problem_occurrences`                                    | Concrete evidence each time a problem recurs                                               |
| `resolutions`                                            | Root causes, fixes, verification evidence, and related skill or instruction changes        |

Plans, completed plans, raw transcripts, and arbitrary historical documents are not long-term memory. Use agent-native planning state for in-session work, optional project-owned OpenSpec files for durable planning handoff, `.tmp/`, maintained `docs/`, and Git history.

## Repeated-Problem Loop

When a problem appears twice:

1. Query existing facts, patterns, occurrences, and resolutions.
2. Record the new occurrence and evidence.
3. Stop repeating an unverified workaround.
4. Investigate the root cause.
5. Record a verified resolution or explicit external blocker.
6. Update an existing skill, instruction, or regression test when needed.

## Hermes Compatibility

The bounded file format is compatible with Hermes `memories/MEMORY.md` and `memories/USER.md`. The SQLite schema begins with the Holographic provider tables, so a future Hermes integration can point Holographic at the same `memory_store.db`.

Hermes `SOUL.md` and `state.db` are intentionally outside this contract. Agent identity remains in native instruction files, and current hooks do not expose the complete message lifecycle required for reliable transcript persistence.

## Current Platform Status

- **Codex**: migrated to `.memories/` and `memory_store.db`.
- **Claude Code**: withdrawn (2026-08-20) — Claude uses Claude Code's built-in memory
  instead. It stays custodian-only for `.memories/` (skeleton creation, worktree sync) so
  Codex and Antigravity sessions still find their state; see `Claude Code Lifecycle` below
  and `.claude/rules/common/memory.md`.
- **Antigravity**: adapter implemented; runtime validation pending.

## Codex Lifecycle

- `.codex/hooks/session_start.py` initializes the bounded files and SQLite schema, copies missing memory into worktrees, and injects `MEMORY.md` plus `USER.md`.
- `.codex/hooks/memory_health_check.py` validates limits and taxonomy.
- `.codex/skills/memory-manager/SKILL.md` defines routing.
- `.codex/skills/memory-sql/SKILL.md` defines SQLite query and write workflows.
- `.codex/config.toml` exposes `.memories/memory_store.db` through `mcp-server-sqlite`.

## Claude Code Lifecycle (custodian only — see Current Platform Status)

- `.claude/hooks/session_start.py` creates the bounded files and SQLite schema if missing
  and copies missing memory into worktrees, but does not read or inject their content.
- Claude has no memory-content skill, agent, MCP server, or Stop-hook reminder — durable
  facts and preferences route to Claude Code's built-in memory instead
  (`.claude/rules/common/memory.md`).
- `.claude/rules/memory/storage.md` is a hands-off guard: never stage/commit
  `.memories/`, never edit its content beyond initial skeleton creation.

## Antigravity Lifecycle

- `.agent/hooks/session_start.py` initializes the bounded files and SQLite schema, copies missing memory into worktrees, and injects `MEMORY.md` plus `USER.md`.
- `.agent/hooks/stop_memory_check.py` validates bounded-file limits and the strict taxonomy.
- `.agent/skills/memory-manager/SKILL.md` defines routing.
- `.agent/skills/memory-sql/SKILL.md` defines SQLite query and write workflows.
- Antigravity requires its `memory-db` MCP server to be configured in the platform-supported global configuration.

Retrieved database output is context until explicitly curated. Never store secrets, private credentials, or raw task narration.
