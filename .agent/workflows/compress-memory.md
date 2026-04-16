---
description: Reorganize and compress the project memory files to maintain high signal-to-noise ratio.
---

# Compress Memory SOP

When the User runs `/compress-memory`, follow these precise steps to maintain a clean and performant memory footprint.

## Step 1: Evaluate Threshold
- **Analyze Length**: Read all files in `.agents/memory/` (excluding `.example.md`).
- **Check Threshold**: Only proceed with compression if the main `MEMORY.md` is too verbose (approx. >2000 tokens) or contains redundant historical data.

## Step 2: Quality Standards (Consult Skill)
You MUST use the **memory-maintenance** skill for guidelines on:
- **Progressive Disclosure**: Keep critical insights in the main file; extract details to sub-files.
- **High-Signal Extraction**: Condense historical logs into single-sentence summaries.

## Step 3: Execution Plan
1.  **Extract**: Identify categories (e.g., ARCHIVE, ARCHITECTURE) for extraction.
2.  **Move**: Create or update auxiliary files in `.agents/memory/` and move the relevant content there.
3.  **Link**: In `MEMORY.md`, leave a concise summary and a standard link pointing to the new sub-file.
4.  **Prune**: Delete redundant facts and resolved tasks that are no longer useful.

## Step 4: Report Back
- Report back with a summary of the changes (what was compressed, what was moved) in **Traditional Chinese**.
