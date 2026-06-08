---
name: memory-manager
description: Use when initializing, reading, updating, auditing, compressing, or consolidating shared project memory.
---

# Memory Manager

This is the Codex source of truth for `.agents/memory/`.

## Storage And Loading

- Session start: `MEMORY.md` (mission/current state, <= 2,200 chars) and `USER.md` (stable preferences, <= 500 chars).
- On demand: `decisions.md`, `lessons.md` (<= 50 lines), and active `changes/<id>/`.
- History: `memory.db` (searchable SQLite FTS5) and `archive/` (non-searchable files).

Only `MEMORY.md`, `USER.md`, and the lesson tail are injected at session start. Treat them as frozen snapshots for the running session.

## Routing

- Mission, constraints, compact current state -> `MEMORY.md`.
- Communication and collaboration preferences -> `USER.md`.
- Active durable decisions -> `decisions.md`.
- Concise recurring lessons -> `lessons.md`.
- Active multi-step work -> `changes/<id>/proposal.md`, optionally `design.md` and `tasks.md`.
- Graduated searchable lessons, decisions, workflows, run notes, and candidates -> `memory.db` through `memory-sql`.
- Completed plans and non-searchable history -> `archive/`.

Do not create additional top-level memory files or directories outside this approved taxonomy.

## Lifecycle

1. Read the injected project context before substantial work.
2. Load on-demand or historical memory only when relevant.
3. During work, keep current state compact; use a change folder for detailed multi-step plans.
4. After work, save only durable state, decisions, recurring lessons, and unresolved follow-up.
5. Before writing SQL, search for equivalent entries and avoid duplicating active file content.
6. On completion, consolidate durable knowledge and move historical plan material to `archive/`.

## Safety

- Never save secrets, credentials, private user data, raw transcripts, or command-by-command narration.
- Retrieval and SQL results are context, not canonical memory, until curated.
- Keep platform-specific status explicit.
- The main agent owns final memory edits even when subagents provide recommendations.

## Skill Evolution

After a meaningful session, use `skill-review` when the work produced a reusable correction, technique, or workflow. Prefer updating an existing skill over creating a new one.
