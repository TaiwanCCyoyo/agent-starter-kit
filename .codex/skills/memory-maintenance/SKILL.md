---
name: memory-maintenance
description: Use when initializing, reading, updating, auditing, compressing, or consolidating `.agents/memory/MEMORY.md` for this repository.
---

# Memory Maintenance

This is a Codex-private skill. It is intentionally stored in `.codex/skills` and loaded through `.codex/AGENTS.md`, not through the default `.agents/skills` discovery path.

## Core Rules

- Treat `.agents/memory/MEMORY.md` as Hot Memory: a concise boot index, mission/constraints summary, compact current-state summary, and map to deeper memory.
- Keep `.agents/memory/MEMORY.md` concise, current, and project-specific.
- Keep `.agents/memory/` fully ignored as instantiated project memory. Commit the rules and automation that manage memory, not local memory content.
- Prefer durable facts, architectural decisions, and lessons learned over task narration.
- Do not save secrets or user-private data.
- Use English for technical memory entries unless the existing section explicitly uses Traditional Chinese.
- Treat repeated blockers, repeated workarounds, mistaken assumptions, hidden tradeoffs, and recurring user-assistance needs as memory-worthy process signals when they can prevent future recurrence.
- Treat retrieval, search, RAG, or Graphify output as context until it is explicitly curated into the memory taxonomy.

## Memory Layers

### Hot Memory

Always loaded or injected at session start:

- `.agents/memory/MEMORY.md`
- Tail of `.agents/memory/lessons.md` when present

Use Hot Memory for:

- Mission and non-negotiable constraints.
- Compact current-state summary and handoff.
- Official memory map.
- Recent or frequently repeated lessons that prevent recurring mistakes.

Keep auto-loaded lessons extremely concise. The bottom of `lessons.md` is highest priority because hooks may load only the last 50 lines.

### Warm Memory

Loaded on demand:

- `.agents/memory/decisions.md`
- `.agents/memory/lessons.md`
- `.agents/memory/lessons-archive.md`
- `.agents/memory/current-state.md`
- `.agents/memory/user-preferences.md`
- `.agents/memory/workflows.md`

Use Warm Memory for curated durable knowledge that is useful but not always needed in the prompt.

### Cold Memory

Never loaded by default:

- `.agents/memory/archive/`
- `.agents/memory/runs/`
- `.agents/memory/candidates/`

Use Cold Memory for historical summaries, run evidence, detailed logs, and draft evolution candidates. Important run evidence may use both Markdown and JSONL.

## Routing Rules

- Mission, constraints, memory map, and compact current-state summary -> `MEMORY.md`.
- Durable architectural decisions -> `decisions.md`.
- Concise recurring lessons that should reduce repeated mistakes -> `lessons.md`.
- Older or lower-frequency lessons -> `lessons-archive.md` or `archive/`.
- Active handoff detail -> `current-state.md` or a short `MEMORY.md` pointer.
- Stable user/project preferences -> `user-preferences.md`.
- Reusable workflow notes not yet promoted to skills -> `workflows.md`.
- Historical details -> `archive/`.
- Important session evidence -> `runs/`, preferably Markdown plus JSONL when useful.
- Draft future rules, skills, docs, or hooks -> `candidates/`.
- Future user-facing plans requiring alignment -> `.agents/memory/*_PLAN.md`.

## Three-Phase Ritual

### 1. Pre-task

Read `.agents/memory/MEMORY.md` before substantial work. Align with the mission, current-state summary, auto-loaded lessons, and relevant Warm files.

### 2. During Work

For file-changing tasks, maintain a compact session intent in `MEMORY.md` or detailed active handoff in `current-state.md` when the task is large or likely to span turns.

Escalate instead of normalizing friction:

1. Ask for user help immediately when the next step needs user authority, credentials, global settings, external accounts, environment ownership, a product decision, or an irreversible tradeoff.
2. If a workaround is needed once, keep the task moving and note the risk.
3. If the same workaround or confusion repeats, tell the user the pattern and recommend the durable fix.
4. If the lesson should survive the session, add it to `Lessons Learned` or `Session Handover`.

### 3. Post-task

After file-changing work:

1. Move completed session intent from active state to completed state.
2. Add high-signal lessons to `lessons.md` only when they are concise and recurring-risk oriented.
3. Put older or lower-frequency lessons in `lessons-archive.md` or `archive/`.
4. Put durable decisions in `decisions.md`.
5. Put unresolved follow-up in `current-state.md` or a compact `MEMORY.md` summary.
6. Keep the last entries readable and short.

## Memory Subagents

Codex provides read-only memory support agents under `.codex/agents/`:

- `memory_auditor`: use for delegated analysis of what should be saved after meaningful work.
- `memory_compressor`: use for delegated compression drafts when Hot or Warm memory becomes verbose.

These agents may recommend or draft memory changes, but the main agent owns the final decision and file edits under `.agents/memory/`.

## Compression

When memory exceeds roughly 2000 tokens or the `Done` list becomes noisy:

- Preserve project mission, tech stack, current state, and recent high-signal work.
- Merge duplicate lessons.
- Move historical detail to `archive/` when useful.
- Move stale or low-frequency lessons out of `lessons.md` so the auto-loaded tail stays high-signal.
- During compression, identify repeated workflows that should become skills.

## Skill Evolution Candidates (Active Discovery)

During compression or explicit memory audits, look for repeated memory patterns that should be promoted out of memory.

Classify candidates as:

- `skill`: a repeatable task workflow with steps, inputs, outputs, and verification.
- `rule`: an always-on behavior constraint that should apply across tasks.
- `doc`: stable explanatory material that helps onboarding or architecture understanding.
- `hook`: deterministic lifecycle automation that should run without agent judgment.
- `none`: project state or a one-time lesson that should stay in memory.

Use these signals:

- The same operational sequence appears across multiple memory entries (3+ times).
- A lesson describes a stable decision rule rather than a single completed task.
- A handoff item keeps recurring because no reusable workflow exists.
- Compression needs to preserve long procedural detail that would be better as a skill or doc.

**Drafting (Active)**: If a pattern is identified (excluding `none`), use the `memory-compressor` subagent to physically draft a candidate file (e.g., `SKILL_CANDIDATE.md` or `RULE_CANDIDATE.md`) capturing the wisdom. Save this candidate to `.agents/memory/candidates/`.

Report to the user in this compact format:

```text
Potential evolution candidate drafted:
- Topic: <short name>
- Type: <skill|rule|doc|hook>
- Reason: <why memory should not remain the only home>
- Draft Location: <path to candidate file>
- Next action: <ask user to review or formally adopt>
```

If there are no meaningful candidates, say so briefly instead of inventing one.

## Worktree Consolidation

When finishing a worktree:

- Read the worktree memory and the main memory.
- Transfer only durable lessons, decisions, and meaningful milestones.
- Avoid duplicates.
- Prefix branch context when it matters.
