---
description: Manage Git worktrees while preserving project memory and context.
---

# Git Worktree Management SOP

When the User runs `/worktree [action] [arguments]` (or asks you to manage worktrees), follow these precise steps, leveraging the `worktree-manager` skill.

## Step 1: Parse requested Action
Analyze the user command to determine the operation:
*   **Create**: Parse the target path and branch name (e.g., `/worktree create <path> <branch>`).
*   **Finish**: Parse the worktree path to teardown (e.g., `/worktree finish <path>`).

## Step 2: Execute Create Action (Phase 1)
If the action is `create`:
1.  **Create Worktree**: Run `git worktree add <path> <branch>` to set up the physical environment.
2.  **Inject Memory taxonomy**: Copy the entire contents of the main repository's `.agents/memory/` directory to the newly created worktree path's `.agents/memory/` directory.
3.  **Define Goals**: Immediately open the `.agents/memory/MEMORY.md` (or `current-state.md`) in the **new worktree** and append:
    -   **Branch Goal**: Specify the exact mission for this branch.
    -   **Definition of Done (DoD)**: List the requirements for completing this branch.
4.  **Confirm**: Report the successful creation and branch goal configuration to the user in **Traditional Chinese (zh-TW)**.

## Step 3: Execute Finish Action (Phase 3)
If the action is `finish`:
1.  **Validate DoD**: Navigate to the worktree path, inspect the local `current-state.md` and check if all Definition of Done items are met.
2.  **Consolidate Memory**:
    -   Invoke the **consolidate-memory** workflow to merge the worktree's lessons learned, decisions, and completed tasks into the main repository's memory files.
3.  **Merge Branch**:
    -   Checkout the main branch.
    -   Merge the worktree's branch: `git merge <branch_name>`.
4.  **Remove Worktree**: Run `git worktree remove <worktree_path>`.
5.  **Delete Branch**: Run `git branch -d <branch_name>`.
6.  **Confirm**: Report the consolidation details, merged branch, and cleanup status to the user in **Traditional Chinese (zh-TW)**.
