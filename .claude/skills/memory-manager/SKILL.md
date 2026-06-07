---
name: memory-manager
description: Use when initializing, reading, updating, auditing, or compressing `.agents/memory/` for this repository. Governs the Hermes-aligned Hot/Warm/Cold memory structure shared across all agents.
---

# Memory Manager

The `.agents/memory/` directory is **cross-agent shared state** — Gemini, Codex, Claude Code, and Antigravity all read from it. Keep files small and high-signal so every agent can load them cheaply.

---

## Memory Structure

### Hot Memory — injected at session start

| File | Purpose | Size target |
|------|---------|-------------|
| `MEMORY.md` | Project mission, constraints, current state, memory map | ≤ 2,200 chars |
| `USER.md` | User preferences, communication language, working style | ≤ 500 chars |

`MEMORY.md` follows the frozen-snapshot pattern: injected once when the session starts, not re-read mid-session. Writes take effect at the next session start. **Note**: this is a convention enforced by Claude's self-discipline, not a technical lock — the hook injects the file once and does not re-read it, but there is no runtime enforcement preventing mid-session reads.

### Warm Memory — read on demand

| File / Dir | Purpose |
|-----------|---------|
| `decisions.md` | Durable architectural decisions (graduate old ones to `memory.db`) |
| `lessons.md` | Concise recurring lessons — tail auto-loaded by Claude at session start |
| `changes/<id>/` | Active change plans: `proposal.md`, optional `design.md`, `tasks.md` |

### Cold Memory — never auto-loaded

| Path | Purpose |
|------|---------|
| `memory.db` | SQLite FTS5 — graduated lessons, decisions, session metadata (Claude Code MCP only) |
| `archive/` | Completed change plans; long-form historical reference |

---

## Routing Rules

| Content | Destination |
|---------|-------------|
| Mission, constraints, current state summary | `MEMORY.md` |
| User communication style, working preferences | `USER.md` |
| Durable architectural decision (active) | `decisions.md` |
| Durable decision (old, inactive) | `memory.db` (`type='decision'`) then remove from `decisions.md` |
| Concise recurring lesson | `lessons.md` |
| Stale lesson | `memory.db` (`type='lesson'`) then remove from `lessons.md` |
| Active multi-step change plan | `changes/<id>/proposal.md` |
| Completed or superseded change plan | `archive/` after consolidating durable knowledge |
| Skill candidate from session | `/learn-eval` → `.claude/skills/learned/` or `memory.db` (`type='candidate'`) |

**Do not** create new Warm files for edge cases — route to `memory.db` or `archive/` instead.

---

## Change Plan Lifecycle

```
changes/<id>/
├── proposal.md   # why, what, scope, success criteria
├── design.md     # optional: technical approach and tradeoffs
└── tasks.md      # implementation checklist
```

1. Create a change plan only when work needs user alignment or spans multiple sessions.
2. On completion: consolidate durable facts into `decisions.md` or `memory.db`, then move the folder to `archive/`.

---

## Memory Health

**MEMORY.md** is healthy when:
- Under 2,200 chars
- Current state is one paragraph, not a list of past tasks
- Memory Map is accurate

**USER.md** is healthy when:
- Under 500 chars
- Contains cross-agent stable preferences, not session notes

**lessons.md** is healthy when:
- Under 50 lines (session start auto-loads only the tail)
- Each entry is a concise, actionable, recurring signal

When files grow past these limits: graduate old entries to `memory.db` via `/memory-sql`, or archive to `archive/`.

---

## Subagents

- `memory_auditor`: delegated analysis of what to save after meaningful work.
- `memory_compressor`: delegated compression drafts when Hot/Warm memory is verbose.

Both agents analyze and draft — the main agent owns final edits.
