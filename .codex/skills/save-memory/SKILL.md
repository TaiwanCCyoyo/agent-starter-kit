---
name: save-memory
description: Use when the user says /save-memory, save-memory, save memory, update memory, persist memory, write memory, or asks Codex to record completed work, lessons learned, decisions, current state, plans, or handoff notes under `.agents/memory/`.
---

# Save Memory

This is a command-like Codex skill. It replaces Gemini-style `/save-memory` with a skill trigger that can be invoked by plain text.

Follow `.codex/skills/memory-maintenance/SKILL.md` for quality rules.

## Workflow

1. Read `.agents/memory/MEMORY.md` and any existing Warm file that matches the update type.
2. Extract only project-specific facts, decisions, completed work, lessons learned, and unresolved follow-up.
3. Route the update to the best memory layer:
   - Mission, constraints, memory map, and compact current-state summary -> `.agents/memory/MEMORY.md`.
   - Durable architectural decisions -> `.agents/memory/decisions.md`.
   - Concise recurring lessons that should reduce repeated mistakes -> `.agents/memory/lessons.md`.
   - Older or lower-frequency lessons -> `.agents/memory/lessons-archive.md` or `.agents/memory/archive/`.
   - Active handoff detail -> `.agents/memory/current-state.md` or a compact `MEMORY.md` pointer.
   - Stable user/project preferences -> `.agents/memory/user-preferences.md`.
   - Reusable workflow notes not yet promoted to skills -> `.agents/memory/workflows.md`.
   - Historical details -> `.agents/memory/archive/`.
   - Important session evidence -> `.agents/memory/runs/`, preferably Markdown plus JSONL when useful.
   - Draft future rules, skills, docs, or hooks -> `.agents/memory/candidates/`.
   - Future user-facing plans requiring alignment -> `.agents/memory/*_PLAN.md`.
4. Keep entries concise and high-signal.
5. Keep `lessons.md` especially terse because session start may auto-load only its last 50 lines.
6. Use English unless the target section already uses Traditional Chinese.
7. Avoid secrets, private user data, and low-value turn narration.
8. Treat retrieval, search, RAG, or Graphify output as context until curated into the memory taxonomy.
9. Report the saved location to the user in Traditional Chinese.
