---
description: Intelligently merge memory from multiple branches or worktrees.
---

# Consolidate Memory SOP

When the User runs `/consolidate-memory [source_path]` (or asks you to merge, sync, or consolidate memory from a worktree/branch), follow these precise steps.

## Step 1: Read Source Context
1.  **Locate Memory**: Locate the `.agents/memory/` directory in the specified `[source_path]`.
2.  **Read Files**: Load the source `MEMORY.md`, and any modified Warm files (e.g., `decisions.md`, `lessons.md`, `current-state.md`, and active folders in `changes/`).

## Step 2: Quality Filtering & Semantic Merge
1.  **Extract High-Signal Info**: Analyze the source memory to identify new lessons learned, architectural decisions, and completed change milestones.
2.  **Compare and Filter**: Avoid duplicates. Filter out low-value turn narration or branch-specific temporary debug logs.
3.  **Synthesize**: Combine overlapping lessons into clear, reusable, and generalized lessons.

## Step 3: Route to Target Layers
Following the **memory-maintenance** skill routing rules, merge the extracted insights into the MAIN repository's memory files:
1.  **Durable Decisions** ➡️ Merged into `.agents/memory/decisions.md`.
2.  **Lessons** ➡️ Merged into `.agents/memory/lessons.md` (place high-impact, active lessons near the tail).
3.  **Milestones / Done Items** ➡️ Merged into `.agents/memory/MEMORY.md` (Done list), prefixing the items with the branch/session context if relevant.
4.  **Completed/Superseaded Change Plans** ➡️ Move the change plan folders from the source path's `changes/` to the main repository's `.agents/memory/archive/changes/YYYY-MM-DD-<change-id>/`.

## Step 4: Report Back
Report the consolidation results back to the user in **Traditional Chinese (zh-TW)**. Specify:
1.  Which target memory files were updated.
2.  What lessons or decisions were successfully merged.
3.  What change folders were archived.
4.  What duplicate or low-signal entries were skipped.
