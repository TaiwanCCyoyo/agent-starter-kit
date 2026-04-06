---
name: create-rule
description: Create a new project rule structure automatically, ensuring the rule is placed in the correct directory with the required YAML frontmatter.
---

# Skill: Create Rule

This skill automates the creation of new project-wide rules, ensuring they are correctly formatted and placed for the agent system to recognize.

## 🎯 Purpose
To provide a standardized way to add new rules to the system. It ensures every new rule is placed in the `.agent/rules/` directory and contains the mandatory YAML frontmatter with `trigger` and `description`.

## 🛠️ Operational Protocol

1. **Information Gathering**: Collect the desired `name` (e.g., `MY_NEW_RULE.md`) and a brief `description` for the new rule.
2. **Setup File**: All rules **must** be created inside the `.agent/rules/` directory. The filename should be uppercase with underscores (e.g., `LOGGING_ROUTINES.md`).
3. **Template Application**: Populate the file with the following standard structure:

   ```markdown
   ```markdown
   ---
   trigger: [always_on | manual | model_decision | glob]
   globs: [optional: required only if trigger is glob, e.g., "*.js"]
   description: [Short, clear description of the rule's purpose]
   ---

   # [Rule Name]
...
   ```

4. **Final Review**: Validate that the file was created successfully and the YAML frontmatter is well-formed.

## ⚠️ Guidelines
- Filenames in `.agent/rules/` should be `UPPERCASE_WITH_UNDERSCORES.md`.
- The YAML frontmatter is **mandatory**:
  - `trigger`: Choose from `always_on` (default), `manual`, `model_decision`, or `glob`.
  - `globs`: **Required** if `trigger` is `glob`. Specify a pattern (e.g., `*.py`, `src/**`).
  - `description`: Required summary of the rule.
- Rules should be concise and actionable.
