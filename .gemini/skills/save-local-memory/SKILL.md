---
name: save-local-memory
description: Persist project-specific facts, architectural decisions, and lessons learned into the local repository's memory (.agents/memory/MEMORY.md). Use to prevent context amnesia within this specific project.
---

# Skill: Save Local Memory

This skill is used to persist project-specific facts, architectural decisions, and lessons learned into the local repository's memory.

## 🎯 Purpose
To prevent "context amnesia" within this specific project without polluting the global `save_memory` space. This ensures that every new session starts with a clear understanding of the project's current state and history.

## 🛠️ Operational Protocol

1. **Identify Project Fact**: When a new piece of information is discovered that is specific to **this project** (e.g., a bug fix, a new dependency, a design decision), activate this skill.
2. **Read Current Memory**: Read `.agents/memory/MEMORY.md` and any auxiliary files in that directory.
3. **Categorize**:
   - **Project Mission**: High-level goals.
   - **Tech Stack**: Specific versions or libraries used.
   - **Lessons Learned**: Avoid repeating mistakes.
   - **Current State**: What is being worked on now.
4. **Update**: Use `replace` or `write_file` to append the new fact to the relevant section. Ensure the language is concise and professional.
5. **Verify**: Confirm the update was successful and remains well-formatted Markdown.

## ⚠️ Guidelines
- Use the global `save_memory` tool ONLY for user-wide preferences (e.g., language preference, general coding style).
- Use this `save-local-memory` skill for anything that belongs strictly to this repository.
