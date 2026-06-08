# Workspace Scope & Boundaries

## 1. Respect Existing Worktrees and Context
- **Never discard or overwrite** uncommitted user changes or dirty worktrees unless explicitly instructed by the user or an approved Verification Plan.
- Always observe and match the existing architectural patterns and surrounding style before introducing new ones.

## 2. Directory Access Restrictions
- **`.tmp/`**: Treated as a scratchpad or temporary workspace. You may create, read, and delete files here without explicit permission.
- **`.references/`**: Treated as **Read-Only**. Never modify or delete documentation or examples found in this directory. If a reference is outdated, notify the user.

## 3. Explicit File Boundaries
- Do not modify files outside the immediate scope of the user's requested task unless it is directly required to fix a compilation or test error caused by your primary edits.
- Ensure that you clean up any unused variables, functions, or temporary files generated *during* your own execution flow.
