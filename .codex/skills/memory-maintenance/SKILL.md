---
name: memory-maintenance
description: Use when initializing, reading, updating, auditing, compressing, or consolidating `.agents/memory/MEMORY.md` for this repository.
---

# Memory Maintenance

This is a Codex-private skill. It is intentionally stored in `.codex/skills` and loaded through `.codex/AGENTS.md`, not through the default `.agents/skills` discovery path.

## Core Rules

- Keep `.agents/memory/MEMORY.md` concise, current, and project-specific.
- Prefer durable facts, architectural decisions, and lessons learned over task narration.
- Do not save secrets or user-private data.
- Use English for technical memory entries unless the existing section explicitly uses Traditional Chinese.
- Treat repeated blockers, repeated workarounds, mistaken assumptions, hidden tradeoffs, and recurring user-assistance needs as memory-worthy process signals when they can prevent future recurrence.

## Three-Phase Ritual

### 1. Pre-task

Read `.agents/memory/MEMORY.md` before substantial work. Align with the mission, active `Doing` items, and handoff notes.

### 2. During Work

For file-changing tasks, maintain a short session intent in `Doing` when the task is large or likely to span turns.

Escalate instead of normalizing friction:

1. Ask for user help immediately when the next step needs user authority, credentials, global settings, external accounts, environment ownership, a product decision, or an irreversible tradeoff.
2. If a workaround is needed once, keep the task moving and note the risk.
3. If the same workaround or confusion repeats, tell the user the pattern and recommend the durable fix.
4. If the lesson should survive the session, add it to `Lessons Learned` or `Session Handover`.

### 3. Post-task

After file-changing work:

1. Move completed session intent from `Doing` to `Done`.
2. Add high-signal lessons to `Lessons Learned`.
3. Put unresolved follow-up in `Session Handover`.
4. Keep the last entries readable and short.

## Memory Subagents

Codex provides read-only memory support agents under `.codex/agents/`:

- `memory_auditor`: use for delegated analysis of what should be saved after meaningful work.
- `memory_compressor`: use for delegated compression drafts when `MEMORY.md` becomes verbose.

These agents may recommend or draft memory changes, but the main agent owns the final decision and file edit for `.agents/memory/MEMORY.md`.

## Compression

When memory exceeds roughly 2000 tokens or the `Done` list becomes noisy:

- Preserve project mission, tech stack, current state, and recent high-signal work.
- Merge duplicate lessons.
- Move historical detail to an archive file under `.agents/memory/` when useful.
- During compression, identify repeated workflows that should become skills.

## Worktree Consolidation

When finishing a worktree:

- Read the worktree memory and the main memory.
- Transfer only durable lessons, decisions, and meaningful milestones.
- Avoid duplicates.
- Prefix branch context when it matters.
