---
name: plan-artifact
description: Use when a plan needs durable cross-agent/cross-session visibility, when
  planning from a PRD (.prd.md), or before implementing a non-trivial feature — produces
  a structured .references/plans/{name}.plan.md artifact. Native Plan Mode handles
  interactive/conversational planning; this skill is for the persistent structured output.
---

# Plan Artifact

Native Plan Mode owns interactive planning and approval. Use this skill only to produce or update the durable, structured plan artifact that Plan Mode does not standardize.

## When

- Plan must survive across agents or sessions (cross-agent visibility).
- Planning from a `.prd.md` file.
- A non-trivial feature or refactor where a written, reviewable artifact adds value.

## Input Modes

| Input | Mode | Behavior |
|---|---|---|
| `path/to/name.prd.md` | PRD mode | Read the PRD, pick the next pending milestone, write the artifact, update only that row pending→in-progress and set its Plan cell. |
| Other markdown path | Reference mode | Read the file as context and produce the artifact. |
| Free-form text | Inline mode | Only when durable persistence is wanted; otherwise use Native Plan Mode directly. |

## Pattern Grounding

Before writing the artifact, search the codebase for conventions the implementation should mirror. Capture one top example per relevant category with file references:

| Category | What to capture |
|---|---|
| Naming | File, function, type, command, or script naming in the affected area |
| Error handling | How failures are raised, returned, logged, or handled gracefully |
| Logging | Levels, format, and what gets logged |
| Data access | Repository, service, query, or filesystem patterns |
| Tests | Test file location, framework, fixtures, and assertion style |

State "none" if no example exists. Do not invent a pattern.

## Artifact: `.references/plans/{kebab-name}.plan.md`

Create `.references/plans/` if needed. Use this structure:

````markdown
# Plan: {Feature Name}

**Source PRD**: {path or "none"}
**Selected Milestone**: {milestone or phase name, or "n/a"}
**Complexity**: {Small | Medium | Large}
**Updated**: {ISO 8601 timestamp}
**Related Commit**: pending

## Summary
{2-3 sentences}

## Patterns to Mirror
| Category | Source | Pattern |
|---|---|---|
| Naming | `path:line` | {short description} |
| Errors | `path:line` | {short description} |
| Tests | `path:line` | {short description} |

## Files to Change
| File | Action | Why |
|---|---|---|
| `path` | CREATE / UPDATE / DELETE | {reason} |

## Tasks
### Task 1: {name}
- **Action**: {what to do}
- **Mirror**: {pattern to follow}
- **Validate**: {runnable command that proves correctness}

## Validation
```bash
{project-specific validation commands}
```

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|

## Acceptance
- [ ] All tasks complete
- [ ] Validation passes
- [ ] Patterns mirrored, not reinvented

## Completion
- **Status**: approved | in-progress | completed | blocked
- **Verification**: pending
- **Commit**: pending
````

## After Writing

Report the artifact path and WAIT for user confirmation before writing any code. Use `plan-reviewer` for complex or high-risk plans. Implement via `superpowers: test-driven-development`.
