---
name: memory-maintenance
description: Use when initializing, reading, updating, auditing, compressing, or consolidating `.agents/memory/` for this repository. Enforces memory layers, OpenSpec lifecycle, and active discovery.
---

# Skill: Memory Maintenance

This skill transforms the project's memory into a structured, token-efficient, and highly readable "Soul" of the project. It defines memory layers, routing rules, plan lifecycles, and guidelines for active discovery of rules and skills.

---

## 🧬 1. Memory Layers (記憶分層)

### Hot Memory (熱記憶 - 啟動即載入)
*   **Files**: `.agents/memory/MEMORY.md` (and the tail of `lessons.md` when configured).
*   **Purpose**: Contains the project mission, non-negotiable tech stack constraints, current state summary, active handoff, and the official memory map. Keep it extremely concise (target < 1000 tokens).

### Warm Memory (溫記憶 - 按需主動載入)
*   **Files**:
    *   `.agents/memory/decisions.md` (Durable architectural decisions)
    *   `.agents/memory/lessons.md` (踩坑紀錄 - Concise recurring lessons)
    *   `.agents/memory/lessons-archive.md` (Older lessons archive)
    *   `.agents/memory/current-state.md` (Detailed active handoff notes)
    *   `.agents/memory/user-preferences.md` (Stable user/project preferences)
    *   `.agents/memory/workflows.md` (Temporary workflows not yet promoted to skills)
    *   `.agents/memory/changes/` (Active change proposals)
*   **Purpose**: Curated durable knowledge that is essential for task execution but doesn't need to bloat the initial session context.

### Cold Memory (冷記憶 - 不會自動載入)
*   **Files**: `.agents/memory/archive/`, `.agents/memory/runs/`.
*   **Purpose**: Contains historical logs, archived design proposals, run evidence, and detailed task execution records.

---

## 🗺️ 2. Routing Rules (記憶路由表)

When updating the repository memory, route information to the correct layer:
1.  **Mission & Constraints** ➡️ `MEMORY.md`
2.  **Durable Architectural Decisions** ➡️ `decisions.md`
3.  **Concise & Recurring Lessons (踩坑點)** ➡️ `lessons.md`
4.  **Historical/Low-Frequency Lessons** ➡️ `lessons-archive.md`
5.  **Active Turn Handoff Detail** ➡️ `current-state.md`
6.  **User Preferences & Stylistic Guidelines** ➡️ `user-preferences.md`
7.  **Temporary SOPs** ➡️ `workflows.md`
8.  **Multi-step Plans requiring Alignment** ➡️ `changes/<change-id>/proposal.md`
9.  **Completed/Rejected Change Plans** ➡️ `archive/changes/YYYY-MM-DD-<change-id>/`

---

## 📋 3. Change Plan Lifecycle (變更計畫生命週期)

For significant, multi-step engineering tasks, structure plans under `.agents/memory/changes/<change-id>/`:
*   `proposal.md` (Goal, scope, background, success criteria)
*   `design.md` (Technical architecture, API changes, tradeoffs)
*   `tasks.md` (Detailed task checklist)

### Lifecycle Flow:
1.  **Creation**: Create a change folder when work spans multiple turns or needs explicit user alignment.
2.  **Tracking**: Update `tasks.md` during execution, keeping `current-state.md` pointing to it.
3.  **Completion**: Upon completion, extract durable decisions and lessons into `decisions.md`/`lessons.md`.
4.  **Archive**: Move the entire change folder to `archive/changes/YYYY-MM-DD-<change-id>/`.

---

## 🔍 4. Active Discovery (技能/規則主動發現)

During memory audits or compression, monitor patterns to detect reusable knowledge:
*   **Detection Signal**:
    *   A specific execution pattern or workaround appears across memory entries **3 or more times**.
    *   A lesson defines a general behavioral constraint rather than a project-specific task fact.
*   **Action**: Draft a candidate file and place it in `.agents/memory/candidates/` (e.g., `RULE_CANDIDATE.md` or `SKILL_CANDIDATE.md`).
*   **Report**: Inform the user using the following format:
    ```text
    Potential evolution candidate drafted:
    - Topic: <short name>
    - Type: <skill | rule | doc | hook>
    - Reason: <why memory should not remain the only home>
    - Draft Location: <path to candidate file>
    - Next action: <ask user to review or formally adopt>
    ```

---

## 🔄 5. The 3-Phase Ritual

### Phase 1: Pre-task (Read)
*   Read `.agents/memory/MEMORY.md` before substantial work. Align with the mission, tech constraints, and relevant Warm memory files (such as `decisions.md` or `lessons.md`).

### Phase 2: Plan-Phase (Do)
*   Update your active status. For tasks spanning multiple sessions, log your intent in `current-state.md`.

### Phase 3: Post-task (Harvest)
*   Harvest wisdom after file-changing work:
    1. Update the `Done` list and clear your entry from `Doing`.
    2. Route new lessons to `lessons.md` (high-signal, short) and architectural decisions to `decisions.md`.
    3. Document handovers in `current-state.md`.

---

## 📦 6. Compression & Worktree Consolidation
*   **Compression**: When `MEMORY.md` exceeds ~2000 tokens, prune redundant task narration, compress the `Done` list to the last ~5 entries, merge duplicate lessons, and move older records to the `archive/`.
*   **Worktree Consolidation**: When finishing a branch/worktree, transfer only durable lessons and decisions back to the main memory, avoiding duplicate entries.
