---
trigger: always_on
description: Prevent the AI from indiscriminately deleting functions or features without explicit intent to do so.
---

# Prevent Feature Deletion

When modifying code, do not delete existing functions or features simply because they seem unused or their purpose is currently unclear.

Unless there is an explicit decision or request in the current task to remove a specific functionality, you must suspect that its original purpose might be forgotten. It could be an undocumented feature, a specific bug fix, or intended for future use where the documentation or memory has not been properly preserved.

Always verify and preserve existing logic unless expressly authorized or required by the current task to remove it.
