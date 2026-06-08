---
name: save-memory
description: Use when the user asks Codex to save durable project facts, user preferences, recurring problems, or verified resolutions.
---

# Save Memory

1. Read the current bounded files and query `memory_store.db` for duplicates.
2. Route stable project facts needed in most sessions to `MEMORY.md`.
3. Route stable user preferences to `USER.md`.
4. Route searchable facts and decisions to Holographic-compatible `facts`.
5. Route repeated blockers and evidence to `problem_patterns` and `problem_occurrences`.
6. Save root causes and fixes to `resolutions`; use `verified` only after concrete checks pass.
7. Keep plans, transcripts, and task narration outside memory.
8. Recheck file limits and database consistency.
