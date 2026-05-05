---
name: memory-maintenance
description: Guide for high-quality, high-signal, and sustainable layered project memory maintenance under `.agents/memory/`.
---

# Memory Maintenance Skill

This skill keeps project memory structured, token-efficient, and readable across Hot, Warm, and Cold memory layers.

## Core Rules

- Treat `.agents/memory/MEMORY.md` as Hot Memory: a concise boot index, mission/constraints summary, compact current-state summary, and map to deeper memory.
- Keep `.agents/memory/` fully ignored as instantiated project memory. Commit rules and automation, not local memory content.
- Prefer durable facts, architectural decisions, and lessons learned over task narration.
- Treat repeated blockers, workarounds, mistaken assumptions, hidden tradeoffs, and recurring user-assistance needs as memory-worthy process signals.
- Treat OpenSpec as the model for plan lifecycle: active changes are self-contained folders, completed changes are archived, and permanent knowledge is consolidated into durable memory.
- Treat retrieval, search, RAG, or Graphify output as context until explicitly curated into the memory taxonomy.

## Core Principles

### 1. High-Signal vs. Noise
- **Avoid**: "I fixed the bug where the user was seeing a weird error message in the console." (Too verbose)
- **Prefer**: "Fixed: Regex greedy matching in `system-safe.toml`." (Concise & Direct)
- **Tone**: Use imperative/infinitive forms. Focus on *what* and *why*, not the narrative.

### 2. Sync Strategies (The "Signal-to-Noise" Filter)
- **Standard Sync (Full Ritual)**:
  - **Applicability**: Mandatory for all **Directive** tasks (any file modification, code fix, or infrastructure change).
  - **Action**: Follow all 3 phases (Pre-Task, Plan-Phase, Post-Task).
- **Lightweight Sync (Read-Only)**:
  - **Applicability**: Recommended for **Inquiry** tasks (pure consultation, log retrieval, codebase exploration without modification).
  - **Action**: Perform **Pre-Task only** (read Hot Memory to stay aligned). Skip writing unless a critical lesson, decision, or handoff is produced.
  - **Goal**: Minimize noise in `MEMORY.md` and save context tokens.

### 3. Progressive Disclosure
- **Hot Memory**: Keep `MEMORY.md` limited to mission, constraints, compact current-state summary, and memory map.
- **Warm Memory**: Store durable decisions, lessons, current-state detail, user preferences, workflows, and active changes in dedicated files/directories.
- **Cold Memory**: Store archived changes, run evidence, references, and evolution candidates under approved Cold directories.
- **Links**: Use Markdown links to point from Hot/Warm memory to detailed Cold files.

## Memory Layers

- **Hot**: `.agents/memory/MEMORY.md` plus the last 50 lines of `lessons.md` when present.
- **Warm**: `decisions.md`, `lessons.md`, `lessons-archive.md`, `current-state.md`, `user-preferences.md`, `workflows.md`, and active `changes/`.
- **Cold**: `archive/`, `runs/`, `candidates/`.

## Routing Rules

- Mission, constraints, memory map, and compact current-state summary -> `MEMORY.md`.
- Durable architectural decisions -> `decisions.md`.
- Concise recurring lessons -> `lessons.md`.
- Older or lower-frequency lessons -> `lessons-archive.md` or `archive/`.
- Active handoff detail -> `current-state.md` or a short `MEMORY.md` pointer.
- Stable user/project preferences -> `user-preferences.md`.
- Reusable workflow notes not yet promoted to skills -> `workflows.md`.
- Active change plans requiring user alignment -> `changes/<change-id>/proposal.md`, with optional `design.md`, `tasks.md`, and `specs/`.
- Completed, rejected, or superseded change plans -> `archive/changes/YYYY-MM-DD-<change-id>/`.
- Long-form reference material -> `archive/references/`.
- Important session evidence -> `runs/`, preferably Markdown plus JSONL when useful.
- Draft future rules, skills, docs, or hooks -> `candidates/`.

## Change Plan Lifecycle

```text
.agents/memory/changes/<change-id>/
├── proposal.md
├── design.md
├── tasks.md
└── specs/
```

1. Create a change folder only when the work needs user alignment, multi-step design, or survives beyond one turn.
2. Keep small active handoff notes in `current-state.md` instead of creating a change.
3. During implementation, update `tasks.md` if it exists and keep `current-state.md` as the compact pointer.
4. On completion, rejection, or supersession, consolidate durable facts into `decisions.md`, `lessons.md`, `workflows.md`, or `current-state.md`.
5. Move the whole change folder to `archive/changes/YYYY-MM-DD-<change-id>/`.
6. Do not leave top-level `*_PLAN.md`, `PROPOSAL_*.md`, `SESSION_LOG.md`, or ad hoc reference files in `.agents/memory/`.

## Graphify Cold Retrieval

- Index archive, runs, candidates, and selected archived changes when memory archaeology is needed.
- Prefer output under `.agents/memory/runs/graphify-cold/` or an external `GRAPHIFY_OUT` path.
- Read `GRAPH_REPORT.md` before deep Cold Memory searches when available.
- Use graph queries for relationships and discovery, then curate confirmed insights into Hot or Warm memory.
- Never let Graphify, RAG, or search output automatically overwrite `MEMORY.md`, `decisions.md`, `lessons.md`, or `current-state.md`.

## 4. The Sync Protocol (The 3-Phase Ritual)

### I. Pre-Task: Loading the Soul
- **Action**: Read `.agents/memory/MEMORY.md` and relevant Warm files when needed.
- **Goal**: Align with the project's mission and pick up where the last session left off.
- **Output**: Choose a short, distinct **Session Name**.

### II. Plan-Phase: Signaling Intent
- **Action**: Keep compact active detail in `current-state.md`; create `changes/<change-id>/` only for plans that need user alignment or cross-session continuity.

### III. Post-Task: Harvesting Wisdom
- **Action**:
  1. Route durable decisions, lessons, handoff, run evidence, and plan updates into the correct memory layer.
  2. Keep `lessons.md` terse and recurring-risk oriented.
  3. Archive completed or superseded `changes/<change-id>/` folders after durable knowledge is consolidated.

## 5. Specialized Subagents (Specialized Intelligence)

This architecture leverages specialized subagents to ensure high-quality memory operations without overloading the main session context.

- **`memory-auditor`**: Used during `save-memory` or worktree teardown to analyze diffs and identify durable decisions, lessons, and handoff notes.
- **`memory-compressor`**: Used during `compress-memory` to draft concise memory blocks and identify repetitive patterns for skill evolution.
- **`repo-explorer`**: Used to map architectural boundaries and dependencies before proposing significant state changes.
- **`implementation-reviewer`**: Used to audit memory update scripts and validation logic for correctness and protocol compliance.

## 6. Automated Lifecycle & Nudge Response

This section defines how the Agent interacts with system-level hooks for seamless memory management.

### I. SessionStart: Context Alignment
- **Behavior**: Upon startup, check for injected `additionalContext` containing Git branch, Hot Memory, and lesson tail content.
- **Action**: Immediately validate if the current `Doing` task aligns with the detected branch mission. If in a new Worktree, propose a goal alignment to the user.
- **Goal**: Zero-manual loading of memory.

### II. AfterAgent: The Nudge Response
- **Trigger**: System emits a nudge: `Detected changes. Please run save-memory`.
- **Response Protocol**:
    1. **Acknowledge**: Briefly confirm the system's detection.
    2. **Summarize**: Extract key completed work, durable lessons, decisions, and handoff from the *current* turn only.
    3. **Execute**: Call the `save-memory` command or update the correct `.agents/memory/` target file.
- **Priority**: System nudges are high-priority; do not ignore them unless there's a critical error.

### III. Intelligent Compression & Skill Evolution
- **Thresholds**:
    - Total `MEMORY.md` size > 2000 tokens or 100 lines.
    - `lessons.md` exceeds the auto-loaded 50-line tail budget.
    - Top-level `.agents/memory/` contains unexpected ad hoc Markdown files.
- **Compression Strategy**:
    - **Protect**: Mission, constraints, current-state summary, active handoff, and recent high-signal work.
    - **Route**: Move durable decisions, lessons, active handoff, historical detail, references, runs, and plans into their approved files/directories.
- **Skill Evolution Candidates (Active Discovery)**:
    - **Detection**: During compression or explicit audits, scan lessons, handoff, workflows, and archived changes for repeated memory patterns (e.g., the same operational sequence appears 3+ times, or a lesson describes a stable decision rule).
    - **Classification**: Classify the recurring pattern as one of:
      - `skill`: a repeatable task workflow with steps, inputs, outputs.
      - `rule`: an always-on behavior constraint (update `GEMINI.md`).
      - `doc`: stable explanatory material for architecture.
      - `hook`: deterministic lifecycle automation.
    - **Drafting (Active)**: Use the `memory-compressor` subagent to draft a candidate file (e.g., `SKILL_CANDIDATE.md` or `RULE_CANDIDATE.md`) capturing the wisdom.
    - **Staging**: Save the candidate to `.agents/memory/candidates/` and propose it to the user for review. Report to the user in this format:
      ```text
      Potential evolution candidate drafted:
      - Topic: <short name>
      - Type: <skill|rule|doc|hook>
      - Draft Location: <path to candidate file>
      - Next action: <ask user to review or activate skill-creator>
      ```

## 7. Git Worktree Sync (Contextual Mobility)
- **Objective**: Ensure intelligence flows between parallel development environments.
- **Action**: When tasking in a Worktree, keep compact branch status in Hot/Warm memory and branch-specific plans under `changes/<change-id>/`. Upon merging/closing, use `consolidate-memory` to backfill durable decisions, lessons, handoff, and meaningful milestones to the main branch memory.
