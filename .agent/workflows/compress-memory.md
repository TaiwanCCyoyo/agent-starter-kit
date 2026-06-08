---
description: Compress bounded memory files and route searchable knowledge into SQLite.
---

# Compress Memory

When the user runs `/compress-memory` or a size warning is triggered:

1. Preserve only stable, high-frequency project facts in `.memories/memories/MEMORY.md`.
2. Preserve only stable user preferences in `.memories/memories/USER.md`.
3. Keep each entry atomic and preserve the established memory delimiter.
4. Remove duplicates and superseded statements.
5. Move searchable lower-frequency knowledge into `facts` after a deduplication query.
6. Preserve recurring-problem evidence and verified resolutions in their structured tables.
7. Keep plans and raw transcripts outside memory.
8. Review reusable procedural guidance for promotion into a rule, skill, hook, or regression test.

Report what was preserved, moved, or removed in Traditional Chinese.
