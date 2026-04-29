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

## Three-Phase Ritual

### 1. Pre-task

Read `.agents/memory/MEMORY.md` before substantial work. Align with the mission, active `Doing` items, and handoff notes.

### 2. During Work

For file-changing tasks, maintain a short session intent in `Doing` when the task is large or likely to span turns.

### 3. Post-task

After file-changing work:

1. Move completed session intent from `Doing` to `Done`.
2. Add high-signal lessons to `Lessons Learned`.
3. Put unresolved follow-up in `Session Handover`.
4. Keep the last entries readable and short.

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
