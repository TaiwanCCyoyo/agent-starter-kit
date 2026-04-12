---
description: Generate a conventional Git commit message based on current changes.
---

# Generate Commit Message SOP

When the User runs `/gen-commit` (or asks you to generate a commit message), follow these precise steps:

**Goal**: Analyze the user's local code changes and generate a high-quality, English Git commit message following the Conventional Commits specification.

## Step 1: Analyze Changes
- If you have terminal access, you MUST execute `git status` and `git diff` (or `git diff --cached` if files are already staged) to strictly analyze the exact lines of code that were added, modified, or deleted.
- If you do not have terminal access, politely ask the user to provide their current `git diff` output.

## Step 2: Formulate the Message
Based on your analysis, draft a commit message adhering to these rules:
1. **Language**: The commit message MUST be in **English** (as per project global rules).
2. **Format**: Follow the Conventional Commits specification:
   `<type>[optional scope]: <description>`

   *Types include:*
   - `feat`: A new feature
   - `fix`: A bug fix
   - `docs`: Documentation only changes
   - `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc.)
   - `refactor`: A code change that neither fixes a bug nor adds a feature
   - `perf`: A code change that improves performance
   - `test`: Adding missing tests or correcting existing tests
   - `chore`: Changes to the build process or auxiliary tools/libraries

3. **Description**:
   - Keep the first line (subject) under 50 characters.
   - Use the imperative mood (e.g., "add", not "added").
   - Do not capitalize the first letter.
   - Do not end the subject line with a period.
4. **Body (Optional)**: If the changes are complex, provide a body paragraph wrapped at 72 characters explaining *why* the change was made and *what* the core logic alters.

## Step 3: Present to the User
- Present the final proposed `git commit` command (or raw message string) within a code block so the user can easily copy and paste it.
- Along with the English commit message, provide a very brief **Traditional Chinese** summary of what you inferred from the diff to assure the user you understood the changes.
