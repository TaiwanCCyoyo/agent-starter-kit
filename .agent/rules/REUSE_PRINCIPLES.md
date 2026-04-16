---
trigger: always_on
description: Core Rule - Reuse Existing Implementations
---
# Reuse Principles

1. **Don't Reinvent the Wheel**: For complex tasks, significant features, or MCP server setups, always check reference open-source projects (e.g., `everything-claude-code`, `oh-my-openagent`) first.
2. **Copy and Adapt**: Prioritize copying existing, proven implementations (skills, prompts, configurations) and adapting them to the current project's needs.
3. **Simple Tasks Exception**: If a task is trivial or requires a tiny script, write it directly to prioritize speed over searching for an existing solution.
4. **Traceability and Attribution**: When proposing significant architectural changes or reusing external patterns, always explicitly state the source of the inspiration (e.g., specific industry standards, relevant open-source projects, or established design patterns). This provides technical weight, ensures transparency, and allows for a deeper understanding of the "why" behind the design without limiting the scope of research.
