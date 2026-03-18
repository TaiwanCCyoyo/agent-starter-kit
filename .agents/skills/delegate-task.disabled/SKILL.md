---
name: delegate-task
description: A fallback skill to spawn a subagent by invoking the internal CLI (e.g., Gemini CLI) with a specific prompt and context. Use this when native subagent tools are unavailable.
---
# Delegate Task (CLI Wrapper Subagent)

## Intent
Use this skill to create and dispatch a new subagent process. It passes a specialized system prompt (persona) and a specific task to a separate CLI instance.

## Usage
When deciding to delegate a task, you must use shell commands to invoke the AI CLI again, passing the target role from `TEAM.md` and the isolated task scope.

Example Shell Execution:
```bash
# This is a conceptual format. Adapt to the specific CLI tool available in the environment (e.g., gemini --prompt "...")
gemini --prompt "You are a QA_Auditor. Analyze the code in src/ and write tests that cover the recent login changes."
```

## Constraints
1. **Isolation**: Only provide the subagent with context relevant to its specific domain. Do not overwhelm it with the main project's long-term plan.
2. **Return Delivery**: Request that the subagent output its findings (e.g., test results or modified code paths) straight to the console or a specific temp file so you (the orchestrator) can read and verify them.
