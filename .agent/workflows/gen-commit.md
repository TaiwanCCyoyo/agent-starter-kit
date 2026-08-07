---
description: Generate a high-quality Git commit message using commit-helper standards.
---

# Generate Commit Message SOP

When the User runs `/gen-commit` (or asks you to generate a commit or stage files), follow these precise steps, leveraging the `commit-helper` skill for quality standards.

## Step 1: Analyze Context & Collect Diff

1.  **Check Status**: Execute `git status` to verify staged and unstaged changes.
2.  **Verify Staging**:
    - If no changes are staged, inspect unstaged changes and ask the user before staging unless autonomous staging was explicitly requested.
    - If changes are staged, execute `git diff --cached` to analyze the exact modifications.

## Step 2: Security & Hygiene Audit

1.  **Consult Standard**: Review the `Security & Hygiene` section of the **commit-helper** skill.
2.  **Filter Secrets**: Ensure no sensitive files (e.g., `.env`, keys, credentials) are in the staged list. If found, unstage them immediately and warn the user.
3.  **Clean Junk**: Verify no temporary artifacts (like `__pycache__` or binary outputs) are staged.

## Step 3: Draft and Present Message

1.  **Generate Message**: Draft an English commit message adhering strictly to the **commit-helper** quality standards (Conventional Commits, imperative mood, lowercase subject).
2.  **Incorporate Context**: Integrate any additional instructions provided by the user in their request.
3.  **Present to User**:
    - Show the drafted commit message in an English code block.
    - Provide a brief summary of what changes are included in **Traditional Chinese (zh-TW)**.
4.  **Confirm Execution**:
    - If autonomous commit is enabled or requested, append the `Agent: Antigravity` trailer to the body and run `git commit -m "<message>"`.
    - If the user reviewed or explicitly approved the final staged diff or message, append the `Agent: Antigravity` trailer.
    - Otherwise, wait for the user to explicitly confirm before executing the commit command.

## Step 4: Handle Failure & Fix Mode

If the commit is blocked by pre-commit hooks (e.g., Ruff format checker, trailing whitespace cleaner):

1.  **Analyze Terminal Output**: Inspect the hook failure logs to identify the files and lines causing the error.
2.  **Fix Directly**: Enter "Fix Mode" to modify the files and resolve the code quality issues.
3.  **Re-stage & Retry**: Run `git add` for the modified files, and execute the commit command again.
