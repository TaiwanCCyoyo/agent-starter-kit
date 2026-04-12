---
trigger: always_on
description: Core Rule - Memory & State Management
---

# Memory Rules

Memory is the **Soul** of your AI session. You must rely on it to understand the project and pass context to future sessions. Failure to sync with memory guarantees context amnesia and mission failure. UNLESS a task is a one-time minor matter ENTIRELY UNRELATED to the current project (e.g., general knowledge questions, greetings), you MUST follow the **Sync Protocol**.

1. **Initialize**: If `.agents/memory/MEMORY.md` does not exist, copy it from `.agents/memory/MEMORY.example.md`. **CRITICAL**: Immediately after copying, you MUST actively analyze the project's current state, codebase structure, READMEs, and configurations. Use this analysis to comprehensively populate the new `MEMORY.md` (including Project Mission, Tech Stack, and User Preferences) to establish a solid contextual foundation for future operations. Do not leave placeholder texts.

2. **Sync Protocol (The 3-Phase Sync)**:
   - **Pre-Task Sync**: BEFORE starting any work, you MUST read `.agents/memory/MEMORY.md`. You must understand the project's current "Soul" to act correctly.
   - **Plan-Phase Sync**: After research and planning, and before modifying files, update the `Doing` section in `MEMORY.md` with your specific intent. **You MUST choose a short, distinct Session Name for yourself and prefix your entry.** (e.g., `- **[Session Name]**: ...`). This allows multiple sessions to work concurrently without confusion.
   - **Post-Task Sync**: AFTER finishing a task and successful verification, you MUST move your entry from `Doing` to the `Done` section (keeping your Session Name prefix), and record `Lessons Learned` to avoid repeating mistakes.

3. **Learn and Delegate**: You MUST record things in Memory to:
   - Remember the long-term goals of the project.
   - Avoid making the same mistakes in the next session (Lessons Learned).
   - Delegate tasks that need to be picked up by other sessions.

4. **Memory Compression**: If you notice that `.agents/memory/MEMORY.md` is becoming too long or disorganized, or if the user requests it, you MUST run the `/compress-memory` workflow to categorize, summarize, and link out content to sub-files.

5. **Tooling & Bypassing**: Always assume memory files in `.agents/memory/` are crucial. If regular file-reading tools fail, immediately use shell commands (`cat`, `Get-Content`) as a fallback to ensure the "Soul" is accessible.