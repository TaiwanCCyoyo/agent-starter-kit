---
description: Standard Operating Procedure for the Verified Loop
---
# Verified Loop SOP

When executing any assigned task, follow this strict loop:

1. **Plan & Identify Dependencies**: Analyze the goal. Define what success looks like. Immediately list any human prerequisites needed for verification (e.g., accounts, hardware access).
2. **Execute**: Write code, modify files, or run commands.
3. **Verify**: Use tools to gather evidence (test output, API responses, logs).
4. **Reflect**: Does the evidence meet the success criteria defined in Step 1?
   - If YES: Task is complete. Proceed to write to `.agents/memory/MEMORY.md` if the knowledge is reusable.
   - If NO: Analyze the failure. **DO NOT immediately ask the human to finish the task.** Refer to `COLLABORATIVE_DEBUGGING.md` to ask for missing permissions/tools, then attempt to fix the plan and go back to Step 2 yourself.
