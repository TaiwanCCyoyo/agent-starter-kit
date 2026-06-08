---
description: Save completed work, lessons learned, decisions, current state, plans, or handoff notes to .agents/memory/.
---

# Save Memory

Follow `.claude/skills/memory-manager/SKILL.md` for routing rules and quality standards.

## Workflow

1. Read `.agents/memory/MEMORY.md` and any existing on-demand file that matches the update type.
2. Extract only project-specific facts, decisions, completed work, lessons learned, and unresolved follow-up.
3. Route the update to the exact destination defined by the approved memory layout:
   - Mission, constraints, memory map, and compact current-state summary → `.agents/memory/MEMORY.md` (≤ 2,200 chars).
   - Cross-agent user preferences and working style → `.agents/memory/USER.md` (≤ 500 chars).
   - Durable architectural decisions → `.agents/memory/decisions.md`.
   - Concise recurring lessons → `.agents/memory/lessons.md` (≤ 50 lines).
   - Active change plans → `.agents/memory/changes/<change-id>/proposal.md`.
   - Completed or superseded change plans → `.agents/memory/archive/`.
   - Stale lessons or decisions → `memory.db` via `/memory-sql` (`type='lesson'|'decision'`).
   - Skill candidates → `memory.db` (`type='candidate'`) or run `/learn-eval`.
4. Keep entries concise and high-signal.
5. Keep `lessons.md` especially terse because session start auto-loads only its last 50 lines.
6. Use English unless the target section already uses Traditional Chinese.
7. Avoid secrets, private user data, and low-value turn narration.
8. Do not create top-level ad hoc plan files such as `*_PLAN.md`, `PROPOSAL_*.md`, or `SESSION_LOG.md`.
9. Report the saved location to the user in Traditional Chinese.
