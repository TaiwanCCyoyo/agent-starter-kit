---
trigger: always_on
description: Core Rule - Memory & State Management
---

# Memory Rules

Memory is the **Soul** of your AI session. You must rely on it to understand the project and pass context to future sessions.

1. **Initialize**: If `.agents/memory/MEMORY.md` does not exist, copy it from `.agents/memory/MEMORY.example.md`. **CRITICAL**: Immediately after copying, you MUST actively analyze the project's current state, codebase structure, READMEs, and configurations. Use this analysis to comprehensively populate the new `MEMORY.md` (including Project Mission, Tech Stack, and User Preferences) to establish a solid contextual foundation for future operations. Do not leave placeholder texts.
2. **Pre-Task Sync**: BEFORE starting any work, you MUST read `.agents/memory/MEMORY.md`. Update it with what you are about to do so that if the session is interrupted, the next session knows what is unfinished.
3. **Post-Task Sync**: AFTER finishing a task, you MUST update `.agents/memory/MEMORY.md` with what was done.
4. **Learn and Delegate**: You MUST record things in Memory to:
   - Remember the long-term goals of the project.
   - Avoid making the same mistakes in the next session (Lessons Learned).
   - Delegate tasks that need to be picked up by other sessions.
5. **Memory Compression**: If you notice that `.agents/memory/MEMORY.md` is becoming too long or disorganized, or if the user requests it, you MUST run the `/compress-memory` workflow to categorize, summarize, and link out content to sub-files.