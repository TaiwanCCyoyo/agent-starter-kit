---
name: compress-memory
description: Use when bounded memory files are too large, duplicated, stale, or poorly routed.
---

# Compress Memory

1. Preserve only stable high-frequency project facts in `MEMORY.md`.
2. Preserve only stable user preferences in `USER.md`.
3. Keep each entry atomic and separate entries with `§`.
4. Remove duplicates and superseded statements.
5. Move searchable lower-frequency knowledge into `facts` after a deduplication query.
6. Preserve recurring-problem evidence and verified resolutions in their structured tables.
7. Do not move plans or raw transcripts into memory.
8. Run `skill-review` when compression reveals reusable procedural guidance.
