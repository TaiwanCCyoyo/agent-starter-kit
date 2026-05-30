---
name: memory-maintenance
description: Use when initializing, reading, updating, auditing, compressing, or consolidating `.agents/memory/MEMORY.md` for this repository.
---

# Memory Maintenance

This is a Claude Code agent-internal skill. It is invoked through the `/memory-maintenance` slash command in `.claude/commands/memory-maintenance.md`.

## Core Rules

- Treat `.agents/memory/MEMORY.md` as Hot Memory: a concise boot index, mission/constraints summary, compact current-state summary, and map to deeper memory.
- Keep `.agents/memory/MEMORY.md` concise, current, and project-specific.
- Keep `.agents/memory/` fully ignored as instantiated project memory. Commit the rules and automation that manage memory, not local memory content.
- Prefer durable facts, architectural decisions, and lessons learned over task narration.
- Do not save secrets or user-private data.
- Use English for technical memory entries unless the existing section explicitly uses Traditional Chinese.
- Treat repeated blockers, repeated workarounds, mistaken assumptions, hidden tradeoffs, and recurring user-assistance needs as memory-worthy process signals when they can prevent future recurrence.
- Treat OpenSpec as the model for plan lifecycle: active changes are self-contained folders, completed changes are archived, and permanent knowledge is consolidated into durable memory.

## Memory Layers

### Hot Memory

Always loaded or injected at session start:

- `.agents/memory/MEMORY.md`
- Tail of `.agents/memory/lessons.md` when present

### Warm Memory

Loaded on demand:

- `.agents/memory/decisions.md`
- `.agents/memory/lessons.md`
- `.agents/memory/lessons-archive.md`
- `.agents/memory/current-state.md`
- `.agents/memory/user-preferences.md`
- `.agents/memory/workflows.md`
- `.agents/memory/changes/`

### Cold Memory

Never loaded by default:

- `.agents/memory/archive/`
- `.agents/memory/runs/`
- `.agents/memory/candidates/`

## Routing Rules

- Mission, constraints, memory map, and compact current-state summary → `MEMORY.md`.
- Durable architectural decisions → `decisions.md`.
- Concise recurring lessons → `lessons.md`.
- Older or lower-frequency lessons → `lessons-archive.md` or `archive/`.
- Active handoff detail → `current-state.md` or a short `MEMORY.md` pointer.
- Stable user/project preferences → `user-preferences.md`.
- Reusable workflow notes not yet promoted to skills → `workflows.md`.
- Active change plans → `changes/<change-id>/proposal.md`, with optional `design.md`, `tasks.md`, and `specs/`.
- Historical details → `archive/`.
- Completed, rejected, or superseded change plans → `archive/changes/YYYY-MM-DD-<change-id>/`.
- Long-form reference material → `archive/references/`.
- Important session evidence → `runs/`.
- Draft future rules, skills, docs, or hooks → `candidates/`.

## Change Plan Lifecycle

```text
.agents/memory/changes/<change-id>/
├── proposal.md      # why, what, scope, success criteria
├── design.md        # optional technical approach and tradeoffs
├── tasks.md         # implementation checklist
└── specs/           # optional capability deltas or requirements
```

1. Create a change folder only when the work needs user alignment, multi-step design, or survives beyond one turn.
2. Keep small active handoff notes in `current-state.md` instead of creating a change.
3. During implementation, update `tasks.md` if it exists and keep `current-state.md` as the compact pointer.
4. On completion, rejection, or supersession, consolidate durable facts into `decisions.md`, `lessons.md`, `workflows.md`, or `current-state.md`.
5. Move the whole change folder to `archive/changes/YYYY-MM-DD-<change-id>/`.

## Three-Phase Ritual

### 1. Pre-task
Read `.agents/memory/MEMORY.md` before substantial work. Align with the mission, current-state summary, auto-loaded lessons, and relevant Warm files.

### 2. During Work
For file-changing tasks, maintain a compact session intent in `MEMORY.md` or detailed active handoff in `current-state.md`.

### 3. Post-task
1. Move completed session intent from active state to completed state.
2. Add high-signal lessons to `lessons.md` only when concise and recurring-risk oriented.
3. Put older or lower-frequency lessons in `lessons-archive.md` or `archive/`.
4. Put durable decisions in `decisions.md`.
5. Put unresolved follow-up in `current-state.md` or a compact `MEMORY.md` summary.
6. Archive completed or superseded `changes/<change-id>/` folders after durable knowledge is consolidated.

## Memory Subagents

- `memory_auditor`: use for delegated analysis of what should be saved after meaningful work.
- `memory_compressor`: use for delegated compression drafts when Hot or Warm memory becomes verbose.

These agents may recommend or draft memory changes, but the main agent owns the final decision and file edits under `.agents/memory/`.

## Compression

When memory exceeds roughly 2000 tokens or the `Done` list becomes noisy, use `/compress-memory`.

## Skill Evolution Candidates (Active Discovery)

During compression or explicit memory audits, look for repeated memory patterns that should be promoted out of memory. Classify as `skill`, `rule`, `doc`, `hook`, or `none`. Use the `memory_compressor` subagent to draft candidate files into `.agents/memory/candidates/`.
