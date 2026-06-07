---
description: Compress .agents/memory/ when Hot/Warm memory is too large. Preserves mission and current state while consolidating noisy or duplicated memory.
---

# Compress Memory

Follow `.claude/skills/memory-manager/SKILL.md` for routing rules and health targets.

When the user explicitly asks for delegated memory compression analysis, use the read-only `memory_compressor` subagent to draft a compression proposal. The main agent must review and apply any final `.agents/memory/` edits.

## Workflow

1. Read `.agents/memory/MEMORY.md`, `USER.md`, `decisions.md`, and `lessons.md`.
2. Preserve the project mission, constraints, and compact current-state summary.
3. Compress `MEMORY.md` into a Hot Memory boot index (≤ 2,200 chars) instead of a full history file.
4. Merge duplicate lessons into generalized, reusable lessons in `lessons.md` (≤ 50 lines).
5. Graduate stale lessons and old decisions to `memory.db` via `/memory-sql` rather than leaving them in Warm files.
6. Move active multi-step plans into `changes/<change-id>/`; archive completed or superseded plans under `archive/` after consolidating durable knowledge.
7. Report what was compressed, what was preserved, target files changed, and any follow-up recommendations.
