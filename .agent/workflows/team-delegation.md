---
description: SOP for Delegating Tasks to Subagents
---
# Team Delegation SOP

1. **Task Breakdown**: Decompose the user request into smaller, isolated components.
2. **Role Assignment**: Check `TEAM.md` for the appropriate role (e.g., `QA_Expert`, `Frontend_Dev`).
3. **Context Preparation**: Gather only the necessary codebase context and instructions for the specific sub-task.
4. **Dispatch**: Invoke the subagent using the available tool (or the custom bootstrapped CLI script) with the prepared context.
5. **Collection & Verification**: Wait for the subagent to report back with evidence. Verify their claim. If satisfactory, integrate their work.
