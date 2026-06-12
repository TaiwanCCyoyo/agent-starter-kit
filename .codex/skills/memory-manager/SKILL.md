---
name: memory-manager
description: Use when initializing, reading, auditing, or deciding how to route shared project memory operations.
---

# Memory Manager

This skill owns memory taxonomy, lifecycle boundaries, health checks, and operation routing. It does not own detailed writes, compression, or SQL procedures.

## Storage

- `.memories/memories/MEMORY.md`: stable project, environment, and tool facts needed in most sessions; <= 2,200 chars.
- `.memories/memories/USER.md`: stable user preferences; <= 500 chars.
- `.memories/memory_store.db`: SQLite structured memory queried on demand.

The Markdown files use Hermes-compatible atomic entries separated by `§` on its own line. Treat their session-start content as a frozen snapshot.

## Operation Routing

- Use `save-memory` for explicit durable writes.
- Use `compress-memory` when bounded files are too large, duplicated, stale, or poorly routed.
- Use `memory-sql` for database schema discovery, searches, inserts, recurring-problem history, and resolutions.
- Use `worktree-memory-sync` for ignored memory state across Git worktrees.
- When the user explicitly requests delegation, use `memory_auditor` for read-only save recommendations or `memory_compressor` for a read-only compression draft. Route their output back through the owning skill; subagents never write memory.

## Repeated Problems

When the same blocker, workaround, mistaken assumption, or confusion appears twice, route to `memory-sql` for the recurring-problem workflow and stop repeating the unverified approach.

## Boundaries

- Keep plans outside memory: Codex planning state, `.tmp/`, or maintained `docs/`.
- Never save secrets, credentials, private user data, raw transcripts, or command-by-command narration.
- Treat retrieved results as context until explicitly curated.
- The main agent owns final memory writes.
