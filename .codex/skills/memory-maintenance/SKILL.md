---
name: memory-maintenance
description: Use when initializing, reading, updating, auditing, compressing, or consolidating `.agents/memory/MEMORY.md` for this repository.
---

# Memory Maintenance

This is a Codex-private skill. It is intentionally stored in `.codex/skills` and loaded through `.codex/AGENTS.md`, not through the default `.agents/skills` discovery path.

## Core Rules

- Keep `.agents/memory/MEMORY.md` concise, current, and project-specific.
- Prefer durable facts, architectural decisions, and lessons learned over task narration.
- Do not save secrets or user-private data.
- Use English for technical memory entries unless the existing section explicitly uses Traditional Chinese.
- Treat repeated blockers, repeated workarounds, mistaken assumptions, hidden tradeoffs, and recurring user-assistance needs as memory-worthy process signals when they can prevent future recurrence.

## Three-Phase Ritual

### 1. Pre-task

Read `.agents/memory/MEMORY.md` before substantial work. Align with the mission, active `Doing` items, and handoff notes.

### 2. During Work

For file-changing tasks, maintain a short session intent in `Doing` when the task is large or likely to span turns.

Escalate instead of normalizing friction:

1. Ask for user help immediately when the next step needs user authority, credentials, global settings, external accounts, environment ownership, a product decision, or an irreversible tradeoff.
2. If a workaround is needed once, keep the task moving and note the risk.
3. If the same workaround or confusion repeats, tell the user the pattern and recommend the durable fix.
4. If the lesson should survive the session, add it to `Lessons Learned` or `Session Handover`.

### 3. Post-task

After file-changing work:

1. Move completed session intent from `Doing` to `Done`.
2. Add high-signal lessons to `Lessons Learned`.
3. Put unresolved follow-up in `Session Handover`.
4. Keep the last entries readable and short.

## Memory Subagents

Codex provides read-only memory support agents under `.codex/agents/`:

- `memory_auditor`: use for delegated analysis of what should be saved after meaningful work.
- `memory_compressor`: use for delegated compression drafts when `MEMORY.md` becomes verbose.

These agents may recommend or draft memory changes, but the main agent owns the final decision and file edit for `.agents/memory/MEMORY.md`.

## Compression

When memory exceeds roughly 2000 tokens or the `Done` list becomes noisy:

- Preserve project mission, tech stack, current state, and recent high-signal work.
- Merge duplicate lessons.
- Move historical detail to an archive file under `.agents/memory/` when useful.
- During compression, identify repeated workflows that should become skills.

## Skill Evolution Candidates

During compression or explicit memory audits, look for repeated memory patterns that should be promoted out of memory. This is suggestion-only: do not create
skills, rules, docs, hooks, or scripts unless the user explicitly asks.

Classify candidates as:

- `skill`: a repeatable task workflow with steps, inputs, outputs, and verification.
- `rule`: an always-on behavior constraint that should apply across tasks.
- `doc`: stable explanatory material that helps onboarding or architecture understanding.
- `hook`: deterministic lifecycle automation that should run without agent judgment.
- `none`: project state or a one-time lesson that should stay in memory.

Use these signals:

- The same operational sequence appears across multiple memory entries.
- A lesson describes a stable decision rule rather than a single completed task.
- A handoff item keeps recurring because no reusable workflow exists.
- Compression needs to preserve long procedural detail that would be better as a skill or doc.
- A reminder or validation pattern is deterministic enough to become a hook.

Report candidates in this compact format:

```text
Potential evolution candidate:
- Topic: <short name>
- Type: <skill|rule|doc|hook>
- Reason: <why memory should not remain the only home>
- Suggested target: <path or surface>
- Next action: <ask user approval, draft proposal, or keep in memory>
```

If there are no meaningful candidates, say so briefly instead of inventing one.

## Worktree Consolidation

When finishing a worktree:

- Read the worktree memory and the main memory.
- Transfer only durable lessons, decisions, and meaningful milestones.
- Avoid duplicates.
- Prefix branch context when it matters.
