---
description: Generate a high-quality Git commit message using commit-helper standards.
---

# Generate Commit Message SOP

When the User runs `/gen-commit` (or asks you to generate a commit message), follow these precise steps, leveraging the `commit-helper` skill for quality standards.

## Step 1: Analyze Context
1.  **Current Status**: Execute `git status` to check staged and unstaged changes.
2.  **Staged Changes**: Execute `git diff --cached` to analyze the exact lines of code to be committed.
3.  **User Input**: Incorporate any additional context or instructions provided by the user.

## Step 2: Quality Standards (Consult Skill)
You MUST use the **commit-helper** skill for all decisions regarding:
-   **Conventional Commits** format.
-   **English language** usage.
-   **Imperative mood** and formatting rules.
-   **Security Check**: Ensure no sensitive data (like `.env`) is staged.

## Step 3: Execution Plan
1.  **Draft Message**: Based on the analysis, draft a commit message in English.
2.  **Present Draft**: Show the draft to the user in a code block.
3.  **Summary**: Provide a brief **Traditional Chinese** summary of the changes.
4.  **Confirm/Execute**:
    -   If the user specifically requested an autonomous commit, add the trailer `Agent-Status: autonomous` and execute `git commit -m "..."`.
    -   Otherwise, wait for the user to confirm the message before executing.

## Step 4: Handle Failures
If `git commit` is blocked by pre-commit hooks (e.g., Ruff linting error), address the errors:
1.  Analyze the terminal output to identify the failing files/lines.
2.  Fix the issues directly.
3.  Re-stage the fixed files.
4.  Retry the commit.
