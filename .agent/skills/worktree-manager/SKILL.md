---
name: worktree-manager
description: Manage Git worktrees while preserving project memory and context. Defines branch creation injection and teardown consolidation.
---

# Skill: Worktree Manager

This skill defines the rigorous lifecycle protocols for managing Git worktrees within the project ecosystem. It ensures that memory (context, goals, and lessons learned) is proactively injected during creation and safely consolidated during teardown, preventing context amnesia and orphaned knowledge.

---

## 🧬 1. Lifecycle Protocols

### Phase 1: Creation (Splitting a Worktree)
When instructed to create a new worktree (e.g., for a new feature or bugfix), the Agent MUST follow these steps BEFORE declaring the task complete:
1.  **Branch Creation**: Create the new branch and worktree using `git worktree add <path> <branch_name>`.
2.  **Proactive Memory Injection**: Copy the official memory taxonomy from the main branch into the new worktree: `.agents/memory/MEMORY.md`, Warm files, `changes/`, `archive/`, `runs/`, and `candidates/`.
3.  **Explicit Goal Definition**: The Agent creating the worktree MUST immediately edit the worktree's local memory:
    - Update Hot Memory or `current-state.md` with the specific **Branch Goal** and **Definition of Done (DoD)** based on the user's initial request.
    - *Rationale*: The next Agent booting up in that worktree will instantly know its exact mission without needing to ask the user.

### Phase 2: Active Development
- Normal development occurs within the worktree.
- The `memory-maintenance` skill applies locally to that worktree's layered `.agents/memory/`.
- Keep branch-specific multi-step plans under `changes/<change-id>/` and consolidate/archive them before worktree removal.

### Phase 3: Teardown (Finishing a Worktree)
When a worktree's mission is accomplished, the Agent MUST execute the "Closing Ritual" BEFORE removing the worktree:
1.  **Validation**: Ensure all items in the worktree's `Definition of Done` are met and tests pass.
2.  **AI Semantic Consolidation**:
    - Read `MEMORY.md` plus relevant Warm files and active `changes/` from both the worktree path and the MAIN repository.
    - Perform semantic merge of layered memory files:
        - **Lessons Learned**: Merge overlapping insights and keep high-signal discoveries.
        - **Change Plans**: Move completed, rejected, or superseded plans to `archive/changes/` after consolidation.
        - **Done Items**: Transfer completed milestones to the correct Warm/Cold memory file, prefixing them with the branch/session context if relevant.
    - Apply updates to the MAIN repository's `.agents/memory/` targets.
3.  **Branch Merge**: Merge the worktree's branch into the main development branch (e.g., `main`).
4.  **Cleanup**: Execute `git worktree remove <worktree_path>`.
5.  **Branch Deletion**: Delete the merged branch using `git branch -d <branch_name>`.

---

## 🛠️ 2. Tooling & Automation
- **AI Semantic Engine**: Primary tool for memory consolidation during Phase 3 (semantic merging of layered memory files).
- **`git worktree` commands**: For physical environment management.
