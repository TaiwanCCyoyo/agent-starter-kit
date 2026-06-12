---
name: save-memory
description: Use when the user asks to save durable project facts, user preferences, recurring problems, or verified resolutions.
---

# Save Memory

This skill owns explicit durable memory writes. Use `memory-manager` for taxonomy and `memory-sql` for every database operation.

When the user explicitly requests delegated analysis, `memory-auditor` may classify candidates and Do Not Save items. The main agent must review the recommendation and perform every final write through this skill.

1. Read the target bounded files and use `memory-sql` to search for equivalent facts or problem history.
2. Route stable high-frequency project, environment, or tool facts to `MEMORY.md`.
3. Route stable user preferences to `USER.md`.
4. Route lower-frequency searchable facts, decisions, lessons, and workflows through `memory-sql`.
5. Route recurring problems and verified resolutions through `memory-sql`; never mark a resolution verified without concrete evidence.
6. Keep each bounded entry atomic, preserve the `§` separator, and stay within file limits.
7. Do not save plans, transcripts, task narration, secrets, credentials, private user data, or uncurated retrieval output.
8. Re-read the changed destination and report where the durable information was stored in Traditional Chinese.
