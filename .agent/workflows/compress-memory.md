---
description: Compress, organize, and categorize memory files when they become too large.
---

# Compress Memory SOP

When the User runs `/compress-memory`, follow these precise steps:

**Goal**: Keep the memory footprint clean, organized, and performant for the Agent's context window.

1. **Scan Memory Contents**:
   - Read `.agents/memory/MEMORY.md` and ALL other `.md` files in `.agents/memory/` (excluding `MEMORY.example.md`).
2. **Analyze Length & Redundancy**:
   - Identify duplicated facts, resolved tasks that are no longer relevant, or overly verbose explanations.
   - Summarize old "Session Handover" and "Current State" items that are already completed.
3. **Categorize and Extract (If Necessary)**:
   - If `MEMORY.md` is too long, identify distinct categories (e.g., `ARCHITECTURE.md`, `TROUBLESHOOTING.md`, `STANDARDS.md`).
   - Create these new markdown files in `.agents/memory/` and move the relevant content there.
   - In `MEMORY.md`, leave behind a concise summary and a standard markdown link (e.g., `[See Architecture Details](ARCHITECTURE.md)`) pointing to the newly created file.
4. **Apply Edits**:
   - Execute the file edits and creations.
5. **Report Back**:
   - Present a brief summary of what was compressed, what was deleted as redundant, and any new sub-files that were created.
