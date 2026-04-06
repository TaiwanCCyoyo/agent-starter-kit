---
name: create-skill
description: Create a new skill structure automatically, ensuring the skill is in its own directory and includes a properly formatted SKILL.md with frontmatter.
---

# Skill: Create Skill

This skill automates the creation of new skills, adhering to the standard structure and formatting required by the agent system.

## 🎯 Purpose
To provide a fast and standardized way to scaffold new skills. It ensures every new skill is placed in its own dedicated directory and contains a `SKILL.md` file with the mandatory YAML frontmatter.

## 🛠️ Operational Protocol

1. **Information Gathering**: Collect the desired `name` (e.g., `my-cool-skill`) and a brief `description` for the new skill from the user or the current task context.
2. **Scaffold Directory**: Create a new folder matching the skill name inside `.agent/skills/`.
3. **Create SKILL.md**: Inside the new folder, create a file named exactly `SKILL.md`.
4. **Apply Template**: Populate `SKILL.md` with the following standard structure:

   ```markdown
   ---
   name: [skill-name]
   description: [Brief description of what the skill does]
   ---

   # Skill: [Human Readable Skill Name]

   This skill is used to [brief explanation].

   ## 🎯 Purpose
   [Describe the specific goal or problem this skill addresses]

   ## 🛠️ Operational Protocol
   1. [First operational step]
   2. [Second operational step]

   ## ⚠️ Guidelines
   - [Key constraint or best practice to follow]
   ```

5. **Final Review**: Validate that the file was created successfully and the YAML frontmatter is well-formed.

## ⚠️ Guidelines
- The folder name should ideally be lowercase with hyphens (kebab-case).
- The definition file **must** be strictly named `SKILL.md`.
- The YAML frontmatter (`name` and `description`) is **mandatory** for the system to recognize the skill.
