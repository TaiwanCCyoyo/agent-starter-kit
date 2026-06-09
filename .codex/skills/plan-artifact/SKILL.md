---
name: plan-artifact
description: Use when a plan needs durable cross-session or cross-agent visibility,
  when planning from a PRD (.prd.md), or when a non-trivial feature benefits from a
  reviewable written artifact — produces a .references/plans/{name}.plan.md file.
  Codex native planning flow handles interactive planning; this skill is for persistent structured output.
---

# Plan Artifact

Codex native planning flow handles interactive planning and approval. Use this skill only to produce or update the durable structured artifact that native planning does not standardize.

## When

- Plan must persist across sessions or agents.
- Working from a `.prd.md` file.
- A non-trivial feature or refactor where a written artifact adds review value.

## Input Modes

- `path/to/name.prd.md` → PRD mode: pick the next pending milestone, write the artifact, update only that row pending→in-progress and set its Plan cell.
- Other markdown path → read as reference context.
- Free-form → only when persistent output is wanted; otherwise use native planning directly.

## Pattern Grounding

Search the codebase for naming, error-handling, logging, data-access, and test conventions in the affected area. Capture one example with a file reference per relevant category. State "none" if absent; never invent.

## Artifact: `.references/plans/{kebab-name}.plan.md`

Create `.references/plans/` if needed. Include: Summary · Patterns to Mirror · Files to Change · Tasks (Action/Mirror/Validate) · Validation · Risks · Acceptance · Completion (status/verification/commit).

After writing the artifact, report its path and WAIT for user confirmation before coding. Use `plan_reviewer` for complex or high-risk plans.
