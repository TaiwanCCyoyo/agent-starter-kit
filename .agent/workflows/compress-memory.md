---
description: Reorganize and compress the project memory files to maintain high signal-to-noise ratio and trigger active discovery.
---

# Compress Memory SOP

When the User runs `/compress-memory` (or when memory size warnings are triggered), follow these precise steps to condense the project memory and extract valuable rules or skills.

## Step 1: Evaluate & Prune Hot Memory
1.  **Analyze Size**: Read all files in `.agents/memory/` (mainly `.agents/memory/MEMORY.md`).
2.  **Verify Threshold**: Compression is recommended if `MEMORY.md` exceeds roughly 2000 tokens or if the `Done` list contains more than 10 entries.
3.  **Preserve Core**: Always preserve the project mission statement, non-negotiable tech stack constraints, and current core task context.
4.  **Condense Done List**: Move older entries from the `Done` list to the `archive/` folder, leaving only the last ~5 entries in the active list.

## Step 2: Route & Consolidate Warm/Cold Layers
1.  **Extract Decisions**: Move long-form architectural decisions out of `MEMORY.md` into `decisions.md`.
2.  **Consolidate Lessons**:
    -   Merge duplicate or overlapping lessons into single, generalized lessons.
    -   Keep `lessons.md` concise and focused on recurring high-impact risks.
    -   Move stale or low-frequency lessons to `lessons-archive.md` or `.agents/memory/archive/`.
3.  **Clean Change Folders**: Move completed, rejected, or superseded change plans from `changes/` to `archive/changes/`.

## Step 3: Active Discovery (Skill/Rule Identification)
During consolidation, actively scan memory files for repeated workflows or rules:
1.  **Check Frequency**: Look for any operational sequence, workaround, or instruction that appears **3 or more times** in memory.
2.  **Assess Typology**: Decide if it should become a `skill` (repeatable workflow), a `rule` (behavior constraint), a `doc` (architecture description), or a `hook` (automation script).
3.  **Draft Candidates**: If a candidate is identified, create a draft (e.g., `RULE_CANDIDATE.md`) and save it to `.agents/memory/candidates/`.

## Step 4: Report Back
Report the results to the user in **Traditional Chinese (zh-TW)**. Your report must contain:
1.  What files were compressed or reorganized.
2.  What information was preserved in Hot memory.
3.  Details of any **Skill Evolution Candidates** drafted under `.agents/memory/candidates/` (topic, type, reason, and location). If none were found, state so briefly.
