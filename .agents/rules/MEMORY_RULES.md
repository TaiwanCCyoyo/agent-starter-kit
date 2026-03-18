---
description: Core Rule - Memory Management
---
# Memory Rules

1. **Persistent Context**: You MUST utilize `.agents/memory/MEMORY.md` to maintain the project's long-term memory across sessions.
2. **Proactive Logging**: Whenever you make a significant architectural decision, configure a new Git Hook, determine a user preference, or solve a complex project-specific bug, you MUST append this information to `memory/MEMORY.md`.
3. **No Initialization Scripts Needed**: Do not rely on external scripts to clear or manage memory for new cloned environments. Your behavior should solely consist of reading and updating `memory/MEMORY.md` accurately based on the current state of the repository.
