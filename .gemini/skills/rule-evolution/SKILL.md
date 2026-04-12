---
name: rule-evolution
description: Automatically evolve and refine project rules through a "Test-Check-Refine" closed-loop system using subagents. Use this when a rule in .agent/rules/ needs to be strengthened, validated against edge cases, or evolved to handle new failure modes.
---

# Skill: Rule Evolution

This skill automates the evolution of project rules by challenging them with simulated scenarios and refining them based on failure analysis.

## 🎯 Purpose
To transform loose guidelines into robust, "fail-proof" mandates by systematically identifying loopholes and patching them through iterative testing with subagents.

## 🛠️ Operational Protocol

### 1. Variables & Initial Analysis
- **`{TargetRule}`**: The path to the rule file (e.g., `.agent/rules/MEMORY_RULES.md`).
- **`{MaxAttempts}`**: Maximum refinement iterations (Default: 3-5).
- **Initial Read**: Analyze the target rule to understand its current constraints, required outputs, and intended behavior.

### 2. Orchestration Planning
- **Scenario Design**: Design a specific test case or "trap" that challenges the rule's current wording.
- **Mock Data Synthesis**: Identify necessary mock files (Markdown, code, or data) to simulate the environment.
- **Subagent Roles**:
    - **Tester**: Acts as an agent trying to follow the rule.
    - **Checker**: Acts as a compliance expert evaluating the Tester's performance.

### 3. Test Environment Setup
- **Directory**: Ensure `.agent/rule-testbed/` exists.
- **Initialization**: Create the planned mock files in the testbed using `write_file`.

### 4. Iterative Evolution Loop
For each attempt up to `{MaxAttempts}`:

#### Step A: Tester Execution
Invoke the `generalist` subagent:
- **Prompt**: `You are the Tester. Follow the rule defined in {TargetRule} strictly. Execute the assigned task in .agent/rule-testbed/ and report your tool calls and final output. [Task Description]`
- **Wait**: For the subagent to complete the task.

#### Step B: Checker Verification
Invoke the `generalist` subagent:
- **Prompt**: `You are the Rule Compliance Expert. Evaluate the Tester's output and tool calls against the constraints in {TargetRule}.
    - If compliant, output TEST_PASSED.
    - If non-compliant, explain exactly which constraint was violated and provide a "fix and strengthen" suggestion for the rule.`

#### Step C: Feedback & Patching
- **If TEST_PASSED**: The rule is robust for this scenario. Exit or proceed to the next scenario.
- **If TEST_FAILED**:
    - Analyze the Checker's feedback.
    - Apply a "Failure-Driven Patch" to `{TargetRule}` (e.g., changing "SHOULD" to "MUST", adding specific formatting requirements).
    - Clear the testbed and repeat from Step A.

## ⚠️ Core Evolution Principles
- **Constraint Escalation**: Move from suggestions to mandatory requirements.
- **Structural Integrity**: Mandate specific outputs (tables, tags, or headers) to ensure consistency.
- **Defensive Writing**: Add clauses that explicitly forbid known failure modes identified during testing.

## 🏁 Verification
- Every refinement must be followed by a successful `TEST_PASSED` or reach `{MaxAttempts}` with a detailed failure report.
- Ensure the final rule remains idiomatically consistent with the project's standards.
