---
name: compress-memory
description: Use when the user says /compress-memory, compress-memory, compress memory, shrink memory, audit memory size, or when hooks recommend reducing `.agents/memory/MEMORY.md`; preserves project mission and current state while consolidating noisy or duplicated memory.
---

# Compress Memory

This is a command-like Codex skill. It replaces Gemini-style `/compress-memory` with a skill trigger that can be invoked by plain text.

Follow `.codex/skills/memory-maintenance/SKILL.md` for quality rules.

When the user explicitly asks for delegated memory compression analysis, use the read-only `memory_compressor` subagent to draft a compression proposal. The main
agent must review and apply any final `.agents/memory/MEMORY.md` edits.

## Workflow

1. Read relevant files in `.agents/memory/`.
2. Preserve the project mission, tech stack, current `Doing` items, active handoff notes, and recent high-signal `Done` entries.
3. Merge duplicate lessons into generalized, reusable lessons.
4. Summarize older completed work into a compact historical entry or move historical detail to an auxiliary memory file under `.agents/memory/` when useful.
5. Apply the "Skill Evolution Candidates" section from `memory-maintenance` to report repeated memory patterns that may deserve a future skill, rule, doc, or hook.
6. Report what was compressed, what was preserved, and any follow-up recommendations.
