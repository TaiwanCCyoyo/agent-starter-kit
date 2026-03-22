---
description: Core Rule - Memory Management & Soul of the Agent
---
# Memory Rules

Memory is the **soul** of the Agent. It contains mission-critical context, long-term goals, and project evolution. Without a clear and persistent memory, the Agent will lose its direction and efficiency.

1.  **Proactive Initialization**: If `.agents/memory/MEMORY.md` does not exist, you MUST immediately copy it from `.agents/memory/MEMORY.example.md` to establish a solid foundation for the project.
2.  **Persistent Context and The Soul**: You MUST utilize `.agents/memory/MEMORY.md` to maintain the project's essence across sessions. If vital information regarding long-term objectives or architectural decisions is missing, the Agent must prioritize restoring this context to avoid inefficient operation.
3.  **Proactive Logging and Evolution**: Whenever you make a significant decision, configure a new Git Hook, determine a user preference, or solve a complex project-specific bug, you MUST append this information to `memory/MEMORY.md`. This ensures the project's wisdom grows over time.
4.  **Structured Indexing**: Treat `MEMORY.md` as the "Brain Index"—a structured, highly organized hub that summarizes the entire project. It should remain clean and scannable, using links or sub-sections to manage high-density information without becoming cluttered.
5.  **Periodical Refactoring**: You SHOULD periodically review and reorganize the content of `MEMORY.md`. By maintaining a high signal-to-noise ratio, you ensure that the most important information is always front and Center.
6.  **Inter-session Bridge**: If you believe a new session is necessary or when starting a new session, remember that `MEMORY.md` is the **exclusive and most powerful channel** for communicating with future incarnations of the Agent.
7.  **No Initialization Scripts Needed**: Do not rely on external scripts to clear or manage memory. Your intelligence consists of reading, refining, and updating `memory/MEMORY.md` accurately based on the current state of the repository.
