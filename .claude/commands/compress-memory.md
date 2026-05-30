---
description: Compress .agents/memory/ when Hot/Warm memory is too large. Preserves mission and current state while consolidating noisy or duplicated memory.
---

# Compress Memory

Follow `.claude/commands/memory-maintenance.md` for quality rules.

When the user explicitly asks for delegated memory compression analysis, use the read-only `memory_compressor` subagent to draft a compression proposal. The main agent must review and apply any final `.agents/memory/` edits.

## Workflow

1. Read relevant files in `.agents/memory/`.
2. Preserve the project mission, constraints, compact current-state summary, active handoff notes, and recent high-signal completed work.
3. Compress `MEMORY.md` into a Hot Memory boot index instead of a full history file.
4. Merge duplicate lessons into generalized, reusable lessons.
5. Keep `lessons.md` short and recurring-risk oriented; move stale or lower-frequency lessons to `lessons-archive.md` or `archive/`.
6. Move durable decisions into `decisions.md`.
7. Move active but non-boot handoff detail into `current-state.md`.
8. Move active multi-step plans into `changes/<change-id>/`; archive completed, rejected, or superseded plans under `archive/changes/` after consolidating durable knowledge.
9. Summarize older completed work into `archive/` when useful.
10. Move long-form references into `archive/references/` unless they should become committed docs.
11. Preserve important run evidence under `runs/`.
12. Apply the "Skill Evolution Candidates" section from `memory-maintenance` to report repeated memory patterns that may deserve a future command, rule, doc, or hook.
13. Report what was compressed, what was preserved, target files changed, and any follow-up recommendations.
