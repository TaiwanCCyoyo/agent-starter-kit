---
trigger: always_on
description: Core Rule - Verification-First Approach
---

# Verification Rules

1. **Verification is Mandatory**: Never claim a task is complete without evidence.
2. **Active Verification Execution**: You MUST actively execute tests using tools like `run_command` (e.g. running scripts, unit tests, or syntax checkers) BEFORE marking the task as complete. Do NOT just assume the edits are correct or rely solely on visual inspection.
3. **Evidence-Based**: Use actual terminal output, test results, logs, or API responses as proof.
4. **No Blind Finishing**: If you modify code or configuration, you must verify the changes locally to ensure there are no syntax errors or breaking changes before finishing your turn.
5. **Plan-Phase Prerequisites**: If verification needs human help (e.g., login, API key), you MUST request it during the *Planning Phase*.