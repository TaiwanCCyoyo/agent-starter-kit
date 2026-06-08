---
name: memory-manager
description: Use when initializing, reading, updating, auditing, or compressing shared project memory.
---

# Memory Manager

This is the Claude Code source of truth for `.memories/`.

## Storage

- `.memories/memories/MEMORY.md`: stable project, environment, and tool facts needed in most sessions; <= 2,200 chars.
- `.memories/memories/USER.md`: stable user preferences; <= 500 chars.
- `.memories/memory_store.db`: SQLite structured memory queried on demand.

The Markdown files use Hermes-compatible atomic entries separated by `§` on its own line. Treat their session-start content as a frozen snapshot.

## Database Routing

Use Holographic-compatible `facts` for searchable decisions, lessons, workflows, tool facts, and environment facts. Use:

- `problem_patterns` for stable recurring-problem identities.
- `problem_occurrences` for evidence each time a problem appears.
- `resolutions` for root causes, fixes, verification, and related skill or instruction changes.

Query for equivalent facts or patterns before every write.

## Repeated Problems

When the same blocker, workaround, mistaken assumption, or confusion appears twice:

1. Query existing patterns and resolutions.
2. Record the new occurrence and evidence.
3. Stop repeating an unverified workaround.
4. Investigate the root cause.
5. Record a verified resolution or explicit external blocker.
6. Update an existing skill, instruction, or regression test when the resolution reveals reusable guidance.

## Boundaries

- Keep plans outside memory: agent-native planning state, `.tmp/`, or maintained `docs/`.
- Never save secrets, credentials, private user data, raw transcripts, or command-by-command narration.
- Treat retrieved results as context until explicitly curated.
- The main agent owns final memory writes.
