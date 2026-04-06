---
description: Automatically evolves and refines project rules through a "Test-Check-Refine" closed-loop system using subagents.
---
# Rule Evolution Workflow

This workflow is designed to automatically evolve and refine project rules through a "Test-Check-Refine" closed-loop system using subagents.

## 1. Variables
- **`{TargetRule}`**: The path to the rule file to be optimized (e.g., `MEMORY_RULES.md`).
- **`{MaxAttempts}`**: Maximum number of refinement iterations (Default: 5).

## 2. Iterative Evolution Steps

### Step 1: Rule Testbed Setup
- [ ] Check if the `Rule Testbed` directory exists.
- [ ] If it does not exist, create the directory.

### Step 2: Subagent Orchestration Planning
- [ ] Analyze the `{TargetRule}` to understand its constraints and expected behaviors.
- [ ] Dynamically design a specific test environment/scenario to challenge the rule.
- [ ] Synthesize any necessary mock markdown files or data required for the test.
- [ ] Prepare the **Tester Subagent** and **Checker Subagent**.
- [ ] Planning logic:
  - Initialize the environment with the synthesized files (Step 3).
  - Pass the Rule prompt to the Tester (Step 4).
  - Wait for the Tester to finish, then trigger the Checker to verify compliance (Step 5).

### Step 3: Test Environment Initialization
- [ ] Execute setup actions to initialize the planned test environment in the `Rule Testbed`.
- [ ] Create the generated mock files and ensure the environment is ready for testing.

### Step 4: Tester Execution (Agent A)
- [ ] Call the **Tester Subagent**.
- [ ] **Prompt**:
  `You are the Tester. Follow the rule defined in {TargetRule} strictly. Execute the assigned task and report your tool calls and final output.`

### Step 5: Checker Verification (Agent B)
- [ ] Call the **Checker Subagent** to evaluate the results from Step 4.
- [ ] **Prompt**:
  `You are the Rule Compliance Expert. Evaluate the Tester's output against {TargetRule}.`
  - If compliant, output `TEST_PASSED`.
  - If non-compliant, explain failures and provide specific suggestions to "fix and strengthen" the rule.

### Step 6: Feedback Loop & Rule Refinement
- [ ] **If Checker outputs `TEST_FAILED`**:
  - If attempts < `{MaxAttempts}`:
    - Modify `{TargetRule}` based on the Checker's feedback.
    - Increment attempt counter and return to **Step 3**.
  - If attempts >= `{MaxAttempts}`: Exit with failure report.
- [ ] **If Checker outputs `TEST_PASSED`**:
  - If there are remaining Rules to test, proceed to the next Rule.
  - Otherwise, exit and report success.

## 3. Core Evolution Principles
- **Constraint Escalation**: Change suggestions (SHOULD) to mandates (MUST).
- **Failure-Driven Patching**: Each failure must result in a specific rule update that prevents that specific failure mode.
- **Structural Integrity**: Enforce specific mandatory outputs (e.g., tables, tags) in rewritten rules.

