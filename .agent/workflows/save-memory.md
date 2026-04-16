---
description: Persist project-specific facts and lessons learned into the local memory following the Soul Protocol.
---

# Save Memory SOP

When the User runs `/save-memory [text]` (or asks you to save information), follow these precise steps, leveraging the `memory-maintenance` skill for quality standards.

## Step 1: Analyze Input
- **Extract Essence**: Identify the core fact, lesson learned, or architectural decision within the provided `[text]`.
- **Project Specificity**: Ensure the information is relevant to **this project**.

## Step 2: Soul Protocol (Consult Skill)
You MUST use the **memory-maintenance** skill for all decisions regarding:
- **The 3-Phase Ritual**: Follow the "Read, Update, Report" cycle.
- **High-Signal vs. Noise**: Ensure the entry is concise and avoids narrative fluff.
- **Formatting**: Use table formatting or structured lists as defined in the skill.

## Step 3: Execution Plan
1.  **Read**: Load `.agents/memory/MEMORY.md` and any relevant auxiliary files.
2.  **Identify**: Find the most appropriate section (e.g., *Lessons Learned*, *Current State*).
3.  **Update**: Use your file editing tools to append or insert the new fact.
4.  **Refine**: Ensure the text matches the project's established voice.

## Step 4: Report Back
- Briefly respond to the User in **Traditional Chinese**, confirming exactly what was saved and which file was modified.
