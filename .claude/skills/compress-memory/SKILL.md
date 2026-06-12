---
name: compress-memory
description: Use when bounded memory files are too large, duplicated, stale, or poorly routed.
---

# Compress Memory

This skill owns bounded-file compression. Use `save-memory` to persist graduated facts and `memory-sql` for database deduplication or writes.

1. Preserve only stable high-frequency project facts in `MEMORY.md`.
2. Preserve only stable user preferences in `USER.md`.
3. Keep each entry atomic and preserve the `§` separator.
4. Remove duplicate, stale, and superseded statements.
5. Before removing useful lower-frequency knowledge, use `save-memory` to graduate it after a `memory-sql` deduplication search.
6. Preserve recurring-problem evidence and verified resolutions in structured tables.
7. Recheck bounded-file limits and report what was preserved, graduated, merged, or dropped.
8. Run `/learn-eval` when compression reveals reusable procedural guidance.

When the user explicitly requests delegated analysis, `memory-compressor` may draft a proposal. The main agent owns final `.memories/` writes.
