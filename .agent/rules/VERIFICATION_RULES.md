---
trigger: always_on
description: Core Rule - Verification-First Approach
---

# Verification Rules

1. **Verification is Mandatory**: Never claim a task is complete without evidence from actual terminal output, test results, logs, or API responses.
2. **Active Verification Execution**: You MUST actively execute tests using tools like `run_command` (e.g. running scripts, unit tests, or syntax checkers) BEFORE marking the task as complete. Do NOT rely solely on visual inspection.
3. **Plan-Phase Alignment**: Your verification actions must closely follow the Verification Plan established during the Planning Phase.
4. **Mandatory Completion Format [STRICT]**:
   Every time you declare a task "completed" or "finished" in your response to the user, you MUST include a section titled `### 🏁 Verification Report` using the exact format below:

   ### 🏁 Verification Report
   - **Verification Executed**: [Describe the exact command you ran (e.g., `uvx ruff check .`) and a brief summary of the result. If none, write "None".]
   - **Evidence**: [Provide the key terminal output, log snippet, or reference the specific test result that proves success. If none, write "None".]
   - **Exemption Justification**: [If and ONLY IF no verification was executed, you must explicitly state the reason here. Acceptable reasons: "purely markdown/documentation updates". UNACCEPTABLE reasons: "the code change was simple/minor".]
