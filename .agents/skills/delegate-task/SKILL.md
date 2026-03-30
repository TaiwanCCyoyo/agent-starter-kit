---
name: delegate-task
description: A skill to spawn a subagent by invoking the Python orchestration script (delegate.py). Use this to safely delegate tasks to specialized subroles.
---
# Delegate Task (Orchestrated Subagent)

## Intent
Use this skill to create and dispatch a new subagent process. By using the `delegate.py` script, the subagent is automatically seeded with project memory, restricted to a specific role's allowed skills (defined in `TEAM.yaml`), and provided with a strict task protocol.

## Usage
When delegating a task, invoke the Python coordinator script using `uv run`. You must explicitly pass the target role defined in `TEAM.yaml` and detail the specific task boundary.

### Delegation Command
```powershell
uv run .agents/skills/delegate-task/delegate.py --role QA_Auditor --task "Analyze the login code in src/ and write tests."
```

## How It Works
1. **Dynamic Prompt Assembly**: The script reads `TEAM.yaml` and extracts the specific role's description and `permissions` (Allowed Skills).
2. **Memory Injection**: It reads the project `MEMORY.md` to ensure the subagent complies with global architectural constraints.
3. **Execution**: It compiles all this into `.agents/temp/task_prompt.md` and spins up the AI CLI as a subagent using the standard `gemini` command parsing.

## Constraints & Best Practices
1. **Target Selection**: Pick the most appropriate role from `TEAM.yaml` based on the task type to reduce hallucination and ensure the right skills are locked in.
2. **Explicit Task Scope**: When providing the `--task` argument, be very specific about what directories or files you want the subagent to focus on.
3. **Handover Validation**: Check `.agents/temp/handover.md` (which the subagent is instructed to create) to verify the results when the script finishes executing.
