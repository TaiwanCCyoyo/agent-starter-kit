---
name: compress-memory
description: Use when bounded memory files are too large, duplicated, stale, or poorly routed.
---

# Compress Memory

This skill owns bounded-file compression. Use `save-memory` to persist any graduated fact and `memory-sql` for database deduplication or writes.

When the user explicitly requests delegated analysis, `memory_compressor` may return a patch-ready draft and graduation recommendations. The main agent must review and apply every final write through the owning skills.

1. Preserve only stable high-frequency project facts in `MEMORY.md`.
2. Preserve only stable user preferences in `USER.md`.
3. Keep each entry atomic and separate entries with `§`.
4. Remove duplicates and superseded statements.
5. Before removing useful lower-frequency knowledge, use `save-memory` to graduate it after a `memory-sql` deduplication search.
6. Preserve recurring-problem evidence and verified resolutions in their structured tables.
7. Do not move plans or raw transcripts into memory.
8. Recheck bounded-file limits and report what was preserved, graduated, merged, or dropped.
9. Run `skill-review` when compression reveals reusable procedural guidance.
