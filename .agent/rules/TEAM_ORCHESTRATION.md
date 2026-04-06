---
description: Core Rule - Team Collaboration and Delegation
---
# Team Orchestration & Bootstrapping

1. **Orchestrator Mindset**: As the primary agent, your role is to map out the architecture, plan the execution, and delegate specific sub-tasks to specialized subagents. You are the brain; use the subagents as hands.
2. **Subagent Delegation**: Whenever possible, delegate isolated or complex tasks (e.g., frontend styling, security audits) to a dedicated subagent defined in `TEAM.md`.
3. **Handling Missing Capabilities (.disabled skills)**: If the current toolset (e.g., Antigravity or Gemini CLI) lacks native multi-agent orchestration features, you MUST enable the fallback `delegate-task` skill.
   - The skill is located at `.agents/skills/delegate-task.disabled`.
   - **To turn it on**: Simply rename the directory by removing `.disabled` (i.e., `mv .agents/skills/delegate-task.disabled .agents/skills/delegate-task`), then begin using it to spawn subagents via CLI commands.
