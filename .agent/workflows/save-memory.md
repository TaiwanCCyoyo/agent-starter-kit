---
description: Read and record specific thoughts or facts into the appropriate place within memory.
---

# Save Memory Sop

When the User runs `/save-memory [text]`, follow these precise steps:

**Goal**: Accurately persist the user's provided information into the correct section of the project's memory.

1. **Read Current State**:
   - Use the file reading tool to read `MEMORY.md` located in `.agents/memory/` and ANY OTHER auxiliary markdown files located in the same directory (excluding `MEMORY.example.md`).
2. **Analyze the Input**:
   - Analyze the raw `[text]` provided by the User.
   - Determine which section of memory it best belongs to (e.g., *Project Mission & Long-term Goals*, *Lessons Learned*, *Session Handover*, etc.).
3. **Write and Update**:
   - Use your file editing tools to append or insert the information into the appropriate section.
   - Refine the text to be clear, concise, and written in the established voice of the memory files.
4. **Report Back**:
   - Briefly respond to the User confirming what was saved and where it was saved (including specific file links if it was diverted to a sub-file).
