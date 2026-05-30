---
description: Save completed work, lessons learned, decisions, current state, plans, or handoff notes to .agents/memory/.
---

# Save Memory

Follow `.claude/commands/memory-maintenance.md` for quality rules.

## Workflow

1. Read `.agents/memory/MEMORY.md` and any existing Warm file that matches the update type.
2. Extract only project-specific facts, decisions, completed work, lessons learned, and unresolved follow-up.
3. Route the update to the best memory layer:
   - Mission, constraints, memory map, and compact current-state summary → `.agents/memory/MEMORY.md`.
   - Durable architectural decisions → `.agents/memory/decisions.md`.
   - Concise recurring lessons → `.agents/memory/lessons.md`.
   - Older or lower-frequency lessons → `.agents/memory/lessons-archive.md` or `.agents/memory/archive/`.
   - Active handoff detail → `.agents/memory/current-state.md` or a compact `MEMORY.md` pointer.
   - Stable user/project preferences → `.agents/memory/user-preferences.md`.
   - Reusable workflow notes not yet promoted to commands → `.agents/memory/workflows.md`.
   - Active change plans → `.agents/memory/changes/<change-id>/proposal.md`.
   - Historical details → `.agents/memory/archive/`.
   - Completed, rejected, or superseded change plans → `.agents/memory/archive/changes/YYYY-MM-DD-<change-id>/`.
   - Long-form reference material → `.agents/memory/archive/references/`.
   - Important session evidence → `.agents/memory/runs/`.
   - Draft future rules, commands, docs, or hooks → `.agents/memory/candidates/`.
4. Keep entries concise and high-signal.
5. Keep `lessons.md` especially terse because session start may auto-load only its last 50 lines.
6. Use English unless the target section already uses Traditional Chinese.
7. Avoid secrets, private user data, and low-value turn narration.
8. Do not create top-level ad hoc plan files such as `*_PLAN.md`, `PROPOSAL_*.md`, or `SESSION_LOG.md`.
9. Report the saved location to the user in Traditional Chinese.
