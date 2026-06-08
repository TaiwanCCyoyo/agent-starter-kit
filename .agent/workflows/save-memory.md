---
description: Persist durable project facts, user preferences, recurring problems, or verified resolutions.
---

# Save Memory

When the user runs `/save-memory [text]` or asks to save durable memory:

1. Read `.memories/memories/MEMORY.md` and `USER.md`.
2. Query `memory_store.db` for equivalent facts or recurring-problem patterns.
3. Route stable project facts needed in most sessions to `MEMORY.md`.
4. Route stable user preferences to `USER.md`.
5. Route searchable facts and decisions to the `facts` table.
6. Route repeated blockers and evidence to `problem_patterns` and `problem_occurrences`.
7. Save root causes and fixes to `resolutions`; use `verified` only after concrete checks pass.
8. Keep plans, transcripts, and task narration outside memory.
9. Recheck bounded-file limits and database consistency.

Report the updated stores and a concise summary in Traditional Chinese.
