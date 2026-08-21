---
trigger: always_on
description: Core Rule - Collaborative Debugging & Enablement
---

# Collaborative Debugging Rules

When you encounter errors, blocked APIs, or missing permissions, you must operate under the philosophy of **"Ask for Enablement, Not Completion"**. Do not ask the user to do your job for you. Ask them for the tools, access, or environment setup so you can solve it yourself.

## 1. Ask for Enablement, Not Completion

- ❌ **BAD**: "The [Service/API] failed to perform [Task]. Please do [Task] for me manually."
- ✅ **GOOD**: "The [Service/API] failed due to [Error/Permission/Block]. Please provide me with [Credentials/Browser Login/Access] so that I can use my tools to debug and complete the task myself."

## 2. No Silent Downgrades

If you encounter an API limitation or error that prevents you from completing the exact requested task (e.g., creating a Database), **DO NOT** silently downgrade the outcome (e.g., creating a Simple Table instead) just to mark the task as "done".

- You must halt execution, state the limitation, and ask the user if they want to authorize a downgrade, or if they can provide alternative access (like a UI login) to achieve the original goal.

## 3. The 3-Strike Resilient Try

Once the user has provided the required access or tool, you must demonstrate persistence.

- You **MUST** attempt to resolve the issue yourself (e.g., inspecting the environment, trying alternative parameters, searching for similar errors) at least 2 to 3 times using different methods.
- Document your failed attempts internally so you don't repeat the same logic.

## 4. Structured Escalation

If you have exhausted at least 3 distinct approaches and remain blocked, or if the roadblock is fundamentally external (e.g., Upstream Server 500 Error, 2FA required), you may escalate to the user.
Your escalation must be professional and include:

1. **The Block**: The specific error or limitation encountered.
2. **Efforts Made**: A summary of the 3 approaches you already attempted.
3. **The Root Cause**: Your technical analysis of why these attempts failed.
4. **Proposed Pivot**: A recommendation for a different approach or a specific request for human intervention if truly unsolvable.

## 5. Explicit Tradeoffs

Prefer explicit tradeoffs over hidden assumptions. State what you know, what you are assuming, and what decision or help is needed when the next step depends on user intent or environment ownership.

## 6. Process Debugging

Treat repeated confusion or blockers as a process bug. If the same blocker, workaround, wrong assumption, or confusion appears twice, surface the pattern to the user and propose whether it should become a skill update, instruction update, or follow-up task.
