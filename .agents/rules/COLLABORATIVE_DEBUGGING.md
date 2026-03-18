---
description: Core Rule - Collaborative Debugging & Enablement
---
# Collaborative Debugging Rules

When you encounter errors, blocked APIs, or missing permissions, you must operate under the philosophy of **"Ask for Enablement, Not Completion"**. Do not ask the user to do your job for you. Ask them for the tools, access, or environment setup so you can solve it yourself.

## 1. Ask for Enablement, Not Completion
- ❌ **BAD**: "The [Service/API] failed to perform [Task]. Please do [Task] for me manually."
- ✅ **GOOD**: "The [Service/API] failed due to [Error/Permission/Block]. Please provide me with [Credentials/Browser Login/Access] so that I can use my tools to debug and complete the task myself."

## 2. The 3-Strike Resilient Try
Once the user has provided the required access or tool, you must demonstrate persistence.
- You **MUST** attempt to resolve the issue yourself (e.g., inspecting the environment, trying alternative parameters, searching for similar errors) at least 2 to 3 times using different methods.
- Document your failed attempts internally so you don't repeat the same logic.

## 3. Structured Escalation
If you have exhausted at least 3 distinct approaches and remain blocked, or if the roadblock is fundamentally external (e.g., Upstream Server 500 Error, 2FA required), you may escalate to the user.
Your escalation must be professional and include:
1. **The Block**: The specific error or limitation encountered.
2. **Efforts Made**: A summary of the 3 approaches you already attempted.
3. **The Root Cause**: Your technical analysis of why these attempts failed.
4. **Proposed Pivot**: A recommendation for a different approach or a specific request for human intervention if truly unsolvable.
