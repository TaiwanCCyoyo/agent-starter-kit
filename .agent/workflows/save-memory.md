---
description: Persist project-specific facts and lessons learned into the local memory following the Soul Protocol.
---

# Save Memory SOP

When the User runs `/save-memory [text]` (or asks you to save information, decisions, or lessons), follow these precise steps to record it, leveraging the **memory-maintenance** skill for quality and routing rules.

## Step 1: Analyze Input & Classify
1.  **Extract Essence**: Identify the core fact, architectural decision, lesson learned, or active handoff details.
2.  **Filter Noise**: Ignore low-value turn narration, emotional feedback, or temporary debug outputs. Keep the text concise and project-specific.

## Step 2: Query Memory Layer Routing
Consult the **memory-maintenance** skill routing rules to determine where to save the data:
*   Project mission, constraints, core status ➡️ `.agents/memory/MEMORY.md` (Hot)
*   Durable architectural decisions ➡️ `.agents/memory/decisions.md` (Warm)
*   Concise, recurring lessons learned ➡️ `.agents/memory/lessons.md` (Warm)
*   Detailed active handoff notes ➡️ `.agents/memory/current-state.md` (Warm)
*   User preferences or code style guidelines ➡️ `.agents/memory/user-preferences.md` (Warm)
*   Active change plan ➡️ `.agents/memory/changes/<change-id>/proposal.md` (Warm)
*   Historical logs or references ➡️ `.agents/memory/archive/` (Cold)

## Step 3: Execution Plan
1.  **Read Target File**: Load the specific memory file (and create it if it does not exist).
2.  **Verify Language**: Use English for all database design, code facts, and architectural decisions, unless the existing file/section explicitly uses Traditional Chinese.
3.  **Perform Update**: Write the structured fact or lesson into the target file. Keep entries clean, formatting as bullet points or tables.
4.  **Security Sweep**: Double-check that no API keys or local settings credentials are being written.

## Step 4: Report Back
Report back to the user in **Traditional Chinese (zh-TW)**. Your report must contain:
1.  Which memory file was updated.
2.  A brief summary of what information was saved.
