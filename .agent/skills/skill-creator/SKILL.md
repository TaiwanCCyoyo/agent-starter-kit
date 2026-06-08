---
name: skill-creator
description: Create a new skill for a specialized workflow, procedure, or domain-specific capability.
---

# Skill Creator

Use this skill to create concise, discoverable expertise under `.agent/skills/`.

## Workflow

1. Define the task boundary and when the skill should trigger.
2. Create a kebab-case directory under `.agent/skills/`.
3. Add a `SKILL.md` with YAML frontmatter containing `name` and a high-signal `description`.
4. Describe the smallest reliable analysis, action, and validation workflow.
5. Add `scripts/`, `references/`, or `assets/` only when the skill genuinely needs them.
6. Verify that examples and dependencies reference existing project capabilities.

## Template

```markdown
---
name: skill-name
description: Explain what the skill does and when to use it.
---

# Skill Name

## Workflow

1. Analyze the input.
2. Perform the task.
3. Validate the result.

## Boundaries

- State important constraints and exclusions.
```

Prefer short, procedural instructions over broad policy or duplicated project rules.
