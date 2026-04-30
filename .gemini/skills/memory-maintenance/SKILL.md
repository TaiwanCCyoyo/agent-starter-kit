---
name: memory-maintenance
description: Guide for high-quality, high-signal, and sustainable project memory maintenance. Use when initializing, updating (BEFORE/AFTER tasks), or auditing the project's long-term memory (.agents/memory/MEMORY.md).
---

# Memory Maintenance Skill

This skill transforms the project's memory into a **Living Skill Guide**. It ensures that every session (personality) contributes to a structured, token-efficient, and highly readable "Soul" of the project.

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
  - **Action**: Perform **Pre-Task only** (Read MEMORY.md to stay aligned). **Skip** writing to `Doing`/`Done` unless a critical `Lesson Learned` or architectural decision is produced.
  - **Goal**: Minimize noise in `MEMORY.md` and save context tokens.

### 3. Progressive Disclosure
- **Main Memory**: Keep only the most recent/critical insights (Mission, Tech Stack, Current State).
- **Archive**: Move historical logs or resolved issues to sub-files (e.g., `ARCHIVE.md`) if a section exceeds 500 tokens.
- **Links**: Use Markdown links to point to detailed documentation or scripts.

## 4. The Sync Protocol (The 3-Phase Ritual)

### I. Pre-Task: Loading the Soul
- **Action**: Read `.agents/memory/MEMORY.md` (and `MEMORY.example.md` if needed).
- **Goal**: Align with the project's mission and pick up where the last session left off.
- **Output**: Choose a short, distinct **Session Name**.

### II. Plan-Phase: Signaling Intent
- **Action**: Update the `Doing` section.
- **Format**: `- **[Session Name]**: [Action-led intent]`.
- **Purpose**: Prevent conflict between concurrent sessions and establish presence.

### III. Post-Task: Harvesting Wisdom
- **Action**:
  1. Move your entry from `Doing` to `Done`.
  2. Update `Lessons Learned` with high-signal insights to prevent regression.
  3. Explicitly delegate unfinished sub-tasks in the `Handover` section.

## 5. Specialized Subagents (Specialized Intelligence)

This architecture leverages specialized subagents to ensure high-quality memory operations without overloading the main session context.

- **`memory-auditor`**: Used during `save-memory` or worktree teardown to analyze diffs and identify durable decisions, lessons, and handoff notes.
- **`memory-compressor`**: Used during `compress-memory` to draft concise memory blocks and identify repetitive patterns for skill evolution.
- **`repo-explorer`**: Used to map architectural boundaries and dependencies before proposing significant state changes.
- **`implementation-reviewer`**: Used to audit memory update scripts and validation logic for correctness and protocol compliance.

## 6. Automated Lifecycle & Nudge Response

This section defines how the Agent interacts with system-level hooks for seamless memory management.

### I. SessionStart: Context Alignment
- **Behavior**: Upon startup, check for injected `additionalContext` containing Git branch and `MEMORY.md` content.
- **Action**: Immediately validate if the current `Doing` task aligns with the detected branch mission. If in a new Worktree, propose a goal alignment to the user.
- **Goal**: Zero-manual loading of memory.

### II. AfterAgent: The Nudge Response
- **Trigger**: System emits a nudge: `Detected changes. Please run save-memory`.
- **Response Protocol**:
    1. **Acknowledge**: Briefly confirm the system's detection.
    2. **Summarize**: Extract the key `Done` items and `Lessons Learned` from the *current* turn only.
    3. **Execute**: Call the `save-memory` command (or the `write_file` equivalent) to update `.agents/memory/MEMORY.md`.
- **Priority**: System nudges are high-priority; do not ignore them unless there's a critical error.

### III. Intelligent Compression & Skill Discovery
- **Thresholds**:
    - Total `MEMORY.md` size > 2000 tokens.
    - `Done` list entries > 15.
- **Compression Strategy**:
    - **Protect**: Mission, Tech Stack, and the last 3 `Done` entries.
    - **Compress**: Summarize older `Done` entries into a "Milestones Archive" section.
- **Skill Discovery**: During compression, analyze if a repetitive workflow exists. If so, suggest activating `skill-creator` to encapsulate the wisdom.

## 7. Git Worktree Sync (Contextual Mobility)
- **Objective**: Ensure intelligence flows between parallel development environments.
- **Action**: When tasking in a Worktree, mark entries with `[Worktree: branch-name]`. Upon merging/closing, use `consolidate-memory` (or manual transfer) to backfill critical `Lessons Learned` to the main branch memory.
