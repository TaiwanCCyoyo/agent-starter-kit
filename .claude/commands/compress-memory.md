---
description: Compress .memories/ when bounded memory files are too large, duplicated, stale, or poorly routed.
---

# Compress Memory

Follow `.claude/skills/memory-manager/SKILL.md` for routing rules and health targets.

When the user explicitly asks for delegated memory compression analysis, use the read-only `memory_compressor` subagent to draft a compression proposal. The main agent must review and apply any final `.memories/` edits.

## Workflow

1. Preserve only stable high-frequency project facts in `MEMORY.md`.
2. Preserve only stable user preferences in `USER.md`.
3. Keep each entry atomic and separate entries with `§`.
4. Remove duplicates and superseded statements.
5. Move searchable lower-frequency knowledge into `facts` after a deduplication query.
6. Preserve recurring-problem evidence and verified resolutions in their structured tables.
7. Do not move plans or raw transcripts into memory.
8. Run `/learn-eval` when compression reveals reusable procedural guidance.
9. Report what was preserved, graduated, merged, or dropped.
