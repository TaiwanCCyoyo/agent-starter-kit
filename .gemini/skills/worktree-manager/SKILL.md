# Worktree Manager Skill

## 1. Description
This skill defines the rigorous lifecycle protocols for managing Git worktrees within the project ecosystem. It ensures that memory (context, goals, and lessons learned) is proactively injected during creation and safely consolidated during teardown, preventing context amnesia and orphaned knowledge.

## 2. Lifecycle Protocols

### Phase 1: Creation (Splitting a Worktree)
When instructed to create a new worktree (e.g., for a new feature or bugfix), the Agent MUST follow these steps BEFORE declaring the task complete:
1. **Branch Creation**: Create the new branch and worktree using `git worktree add <path> <branch_name>`.
2. **Proactive Memory Injection**: Do NOT rely solely on the `post-checkout` hook to leave an empty `[MISSION REQUIRED]` prompt.
3. **Explicit Goal Definition**: The Agent creating the worktree MUST immediately edit the `MEMORY.md` inside the newly created worktree path.
   - Update the `Doing` section with the specific **Branch Goal** and **Definition of Done** based on the user's initial request.
   - *Rationale*: The next Agent booting up in that worktree will instantly know its exact mission without needing to ask the user.

### Phase 2: Active Development
- Normal development occurs within the worktree.
- The `memory-maintenance` skill applies locally to that worktree's `MEMORY.md`.

### Phase 3: Teardown (Finishing a Worktree)
When a worktree's mission is accomplished, the Agent MUST execute the "Closing Ritual" BEFORE removing the worktree:
1. **Validation**: Ensure all items in the worktree's `Definition of Done` are met and tests pass.
2. **AI Semantic Consolidation**:
   - Read the `MEMORY.md` from the worktree path and the MAIN repository.
   - Use LLM reasoning to synthesize a unified memory.
   - **Lessons Learned**: Merge overlapping insights and keep high-signal discoveries.
   - **Done Items**: Transfer completed milestones to the main memory, prefixing them with the branch/session context if relevant.
   - **Action**: Use the `replace` or `write_file` tool to update the MAIN repository's `.agents/memory/MEMORY.md`.
3. **Branch Merge**: Merge the worktree's branch into the main development branch (e.g., `main`).
4. **Cleanup**: Execute `git worktree remove <worktree_path>`.
5. **Branch Deletion**: Delete the merged branch using `git branch -d <branch_name>`.

## 3. Relationship with System Hooks (Automated Infrastructure)

This skill operates on top of the project's automated infrastructure. The following hooks are active and provide "Safe Defaults":

| Hook | Type | Automation Provided |
| :--- | :--- | :--- |
| **`post-checkout`** | Git Hook | Automatically copies `MEMORY.md` and installs basic hooks (`pre-commit`) into the new worktree upon creation. |
| **`session_start.py`** | Gemini Hook | Automatically alerts the Agent if a branch mission (`[MISSION REQUIRED]`) is uninitialized during session startup. |
| **`.gemini/scripts/memory_nudger.py`** | Gemini Hook | Reminds the Agent to update `MEMORY.md` after any file modifications within the worktree. |

**Important**: While the `post-checkout` hook provides the **scaffolding** (files and basic prompts), the Agent exercising this skill is RESPONSIBLE for the **intellectual injection** (defining the actual branch-specific mission).

## 4. Tooling
- **AI Semantic Engine**: Primary tool for memory consolidation during Phase 3 (Semantic merging of `MEMORY.md` files).
- **`git worktree` commands**: For physical environment management.
- **`scripts/git_post_checkout.py`**: Automated safety net for basic worktree scaffolding.
