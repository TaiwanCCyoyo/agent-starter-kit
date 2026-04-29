---
name: save-memory
description: Use when the user says /save-memory, save-memory, save memory, update memory, persist memory, write memory, or asks Codex to record completed work, lessons learned, decisions, current state, or handoff notes in `.agents/memory/MEMORY.md`.
---

# Save Memory

This is a command-like Codex skill. It replaces Gemini-style `/save-memory` with a skill trigger that can be invoked by plain text.

Follow `.codex/skills/memory-maintenance/SKILL.md` for quality rules.

## Workflow

1. Read `.agents/memory/MEMORY.md`.
2. Extract only project-specific facts, decisions, completed work, lessons learned, and unresolved follow-up.
3. Update the best section:
   - `Lessons Learned` for reusable insights.
   - `Current State` or `Doing` for active work.
   - `Done` for completed tasks.
   - `Session Handover` for unfinished follow-up.
4. Keep entries concise and high-signal.
5. Use English unless the target section already uses Traditional Chinese.
6. Avoid secrets, private user data, and low-value turn narration.
7. Report the saved location to the user in Traditional Chinese.
