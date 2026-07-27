---
trigger: always_on
description: Core Rule - Verification-First Approach
---

# Verification Rules

1. **Verification Evidence**: Base completion claims on actual test results, logs, API responses, or automated hook output.
2. **Task-Specific Verification**: Execute behavioral tests that directly cover the changed behavior.
3. **Automation Ownership**: Agent hooks own touched-file hygiene, pre-commit owns staged gates, and CI owns repository-wide gates.
4. **Targeted Verification Standards**:
    - For Python changes: Run relevant script tests.
    - For Configuration changes (TOML, JSON): Validate formatting syntax and verify required `SKILL.md` frontmatter.
5. **Plan-Phase Alignment**: Your verification actions must closely follow the Verification Plan established during the Planning Phase.
6. **Mandatory Completion Format [STRICT]**:
   Every time you declare a task "completed" or "finished" in your response to the user, you MUST include a section titled `### 🏁 Verification Report` using the exact format below:

    ### 🏁 Verification Report
    - **Verification Executed**: [Describe the exact command you ran (e.g., `uv run pytest`) and a brief summary of the result. If none, write "None".]
    - **Evidence**: [Provide the key terminal output, log snippet, or reference the specific test result that proves success. If none, write "None".]
    - **Exemption Justification**: [If and ONLY IF no verification was executed, you must explicitly state the reason here. Acceptable reasons: "purely markdown/documentation updates". UNACCEPTABLE reasons: "the code change was simple/minor".]
    - **Residual Risk**: [If verification is skipped or hook coverage is insufficient, explicitly state the residual risk here. Otherwise, write "None".]
