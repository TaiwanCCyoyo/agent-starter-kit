---
name: compress-memory
description: Use when the user says /compress-memory, compress-memory, compress memory, shrink memory, audit memory size, or when hooks recommend reducing Hot/Warm memory; preserves project mission and current state while consolidating noisy or duplicated memory.
---

# Compress Memory

This is a command-like Codex skill. It replaces Gemini-style `/compress-memory` with a skill trigger that can be invoked by plain text.

Follow `.codex/skills/memory-maintenance/SKILL.md` for quality rules.

When the user explicitly asks for delegated memory compression analysis, use the read-only `memory_compressor` subagent to draft a compression proposal. The main
agent must review and apply any final `.agents/memory/` edits.

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
11. Preserve important run evidence under `runs/`, using Markdown plus JSONL when useful.
12. Treat Graphify cold-memory output as retrieval context; store any graph reports under `runs/graphify-cold/` or an external `GRAPHIFY_OUT` path.
13. Apply the "Skill Evolution Candidates" section from `memory-maintenance` to report repeated memory patterns that may deserve a future skill, rule, doc, or hook.
14. Report what was compressed, what was preserved, target files changed, and any follow-up recommendations.
