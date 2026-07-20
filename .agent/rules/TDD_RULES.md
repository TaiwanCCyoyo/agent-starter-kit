---
trigger: always_on
description: Test-Driven Development (TDD) Enforcement Rule (MIT Licensed, adapted from obra/superpowers)
---

# Test-Driven Development (TDD) Rules

> [!NOTE]
> This rule is adapted from the `test-driven-development` skill in the `obra/superpowers` project (Copyright (c) 2026 Jesse Vincent, licensed under the MIT License).

1. **TEST FIRST**: You are strictly forbidden from writing or modifying any implementation/production code before writing a corresponding failing test.
2. **RED PHASE (Verify Failure)**: Run the test suite to verify that the newly written test indeed fails. Output the test failure logs in your response as evidence.
3. **GREEN PHASE (Write Minimal Code)**: Implement the minimum amount of production code necessary to make the failing test pass.
4. **REFACTOR PHASE**: Clean up the implementation code while ensuring all tests continue to pass.
5. **EXEMPTION**: The only exceptions are documentation-only updates, structural refactoring (where tests already exist), or initial project scaffolding.
