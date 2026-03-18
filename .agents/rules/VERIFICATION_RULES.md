---
description: Core Rule - Verification-First Approach
---
# Verification Rules

1. **Verification is Mandatory**: Never claim a task is complete without evidence.
2. **Evidence-Based**: Use terminal output, test results, logs, or API responses.
3. **Plan-Phase Prerequisites**: If verification needs human help (e.g., login, API key), you MUST request it during the *Planning Phase*. 
4. **Pre-Commit SOP Enforcement**: Verification of any commit-related task **MUST** include proof that `.agents/workflows/PRE_COMMIT_SOP.md` was executed successfully.
