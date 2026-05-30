---
description: Initialize, read, update, audit, compress, or consolidate .agents/memory/MEMORY.md for this repository.
---

# Memory Maintenance

Follow the Hot/Warm/Cold taxonomy for all memory operations.

## Core Rules

- Treat `.agents/memory/MEMORY.md` as Hot Memory: a concise boot index, mission/constraints summary, compact current-state summary, and map to deeper memory.
- Keep `.agents/memory/MEMORY.md` concise, current, and project-specific.
- Keep `.agents/memory/` fully ignored as instantiated project memory. Commit the rules and automation that manage memory, not local memory content.
- Prefer durable facts, architectural decisions, and lessons learned over task narration.
- Do not save secrets or user-private data.
- Use English for technical memory entries unless the existing section explicitly uses Traditional Chinese.
- Treat repeated blockers, repeated workarounds, mistaken assumptions, hidden tradeoffs, and recurring user-assistance needs as memory-worthy process signals when they can prevent future recurrence.

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
- Draft future rules, commands, docs, or hooks → `candidates/`.

## Three-Phase Ritual

### 1. Pre-task
Read `.agents/memory/MEMORY.md` before substantial work. Align with the mission, current-state summary, auto-loaded lessons, and relevant Warm files.

### 2. During Work
For file-changing tasks, maintain a compact session intent in `MEMORY.md` or detailed active handoff in `current-state.md` when the task is large or likely to span turns.

### 3. Post-task
After file-changing work:
1. Move completed session intent from active state to completed state.
2. Add high-signal lessons to `lessons.md` only when they are concise and recurring-risk oriented.
3. Put older or lower-frequency lessons in `lessons-archive.md` or `archive/`.
4. Put durable decisions in `decisions.md`.
5. Put unresolved follow-up in `current-state.md` or a compact `MEMORY.md` summary.
6. Archive completed or superseded `changes/<change-id>/` folders after durable knowledge is consolidated.

## Compression

When memory exceeds roughly 2000 tokens or the `Done` list becomes noisy, use `/compress-memory`.

## Skill Evolution Candidates (Active Discovery)

During compression or explicit memory audits, look for repeated memory patterns that should be promoted out of memory. Classify candidates as `skill`, `rule`, `doc`, `hook`, or `none`. Use the `memory_compressor` subagent to draft candidate files into `.agents/memory/candidates/`.
