---
name: compress-memory
description: Reorganize, summarize, and compress the project's local memory files when they become too verbose or disorganized. Use when MEMORY.md grows too large (>2000 tokens) or contains redundant historical data.
---

# Skill: Compress Memory

This skill is used to reorganize, summarize, and compress the project's local memory files when they become too verbose or disorganized.

## 🎯 Purpose
To maintain a high-signal-to-noise ratio in the project's context window. As `MEMORY.md` grows, it can become expensive and distracting; this skill extracts details into sub-files and keeps the main memory file concise.

## 🛠️ Operational Protocol

1. **Scan & Analyze**: Read `.agents/memory/MEMORY.md` and all related files in that directory. Identify redundant information, resolved tasks, or overly detailed sections.
2. **Summarize**: Condense historical data (e.g., old session handovers) into single-sentence summaries.
3. **Extract to Sub-files**:
   - If a section (e.g., Architecture, Troubleshooting) exceeds 50 lines, move it to a new file (e.g., `.agents/memory/ARCHITECTURE.md`).
   - Leave a clear summary and a Markdown link in the main `MEMORY.md`.
4. **Clean Up**: Remove duplicated facts and irrelevant "in-progress" notes that are now completed.
5. **Update Index**: Ensure the main `MEMORY.md` acts as a clean entry point to the project's state.

## ⚠️ Guidelines
- Never delete "Lessons Learned" unless they are truly redundant.
- Ensure all links between memory files are valid relative paths.
- Perform compression only when requested by the user or when the memory files exceed a manageable size (e.g., >2000 tokens).
