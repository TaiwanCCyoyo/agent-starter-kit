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

### 3. The Sync Protocol (The 3-Phase Ritual)

#### I. Pre-Task: Loading the Soul
- **Action**: Read `.agents/memory/MEMORY.md` (and `MEMORY.example.md` if needed).
- **Goal**: Align with the project's mission and pick up where the last session left off.
- **Output**: Choose a short, distinct **Session Name**.

#### II. Plan-Phase: Signaling Intent
- **Action**: Update the `Doing` section.
- **Format**: `- **[Session Name]**: [Action-led intent]`.
- **Purpose**: Prevent conflict between concurrent sessions and establish presence.

#### III. Post-Task: Harvesting Wisdom
- **Action**:
  1. Move your entry from `Doing` to `Done`.
  2. Update `Lessons Learned` with high-signal insights to prevent regression.
  3. Explicitly delegate unfinished sub-tasks in the `Handover` section.

## Best Practices for Tables and Lists
- **Consistency**: Keep tables (like Testing Status) updated and aligned.
- **Evidence**: Always include evidence or notes (e.g., `[Verified]`, `[Blocked]`).
- **Hierarchy**: Use Markdown headers to maintain a clear visual structure for the next Agent.

## Maintenance Checklist
- [ ] Is the Mission statement up to date?
- [ ] Are the Tech Stack constraints (Ruff, uv, etc.) accurately reflected?
- [ ] Does `Lessons Learned` contain fluff or repetitive history? (If so, prune/archive).
- [ ] Is the `Done` list getting too long? (Keep only the last ~5-10 entries).
