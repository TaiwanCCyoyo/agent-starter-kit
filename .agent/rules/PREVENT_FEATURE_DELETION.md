---
trigger: always_on
description: Prevent the AI from indiscriminately deleting functions or features without explicit intent to do so.
---

# Code Modification & Engineering Discipline

## 1. Prevent Feature Deletion
When modifying code, do not delete existing functions or features simply because they seem unused or their purpose is currently unclear.

Unless there is an explicit decision or request in the current task to remove a specific functionality, you must suspect that its original purpose might be forgotten. It could be an undocumented feature, a specific bug fix, or intended for future use where the documentation or memory has not been properly preserved.

Always verify and preserve existing logic unless expressly authorized or required by the current task to remove it.

## 2. Surgical Editing
Prefer the smallest change that satisfies the verified goal. Touch only files and lines related to the task; do not refactor, reformat, rename, or delete adjacent code without need. Match the surrounding style and ownership boundaries before introducing new patterns.

## 3. Cleanup Boundaries
Clean up unused imports, variables, functions, or files created by the current change. Do not touch or delete pre-existing unrelated dead code; instead, report it to the user if noticed.
