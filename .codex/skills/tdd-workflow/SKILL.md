---
name: tdd-workflow
description: Use when a behavior change benefits from a reproducible RED-GREEN-REFACTOR cycle and focused regression coverage.
---

# TDD Workflow

This is a Codex-native adaptation of the ECC TDD workflow.

1. Describe the behavior and acceptance criteria.
2. Add the smallest regression test that exercises the missing or broken behavior.
3. Run that exact test and confirm RED for the intended reason, not setup failure.
4. Apply the smallest production change that can make it pass.
5. Rerun the same test and confirm GREEN.
6. Refactor only if it reduces real complexity; keep the focused test green.
7. Broaden verification according to blast radius, then run repository lint and type gates.

Do not create checkpoint commits unless the user explicitly asks for them. Do not impose a universal coverage percentage; use risk, shared behavior, and repository policy to choose coverage.
