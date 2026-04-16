---
name: skill-creator
description: Create a new skill (Expertise). Use this for defining specialized workflows, SOPs, or deep knowledge on HOW to perform specific tasks.
---

# Skill: Skill-Creator (Defining Expertise)

This skill provides a structured framework for creating specialized agent expertise. It follows the principles of "High-Signal" and "Progressive Disclosure."

## 🎯 Purpose
To transform general-purpose agents into specialists by providing them with procedural knowledge, reusable scripts, and domain-specific references.

## 🛠️ Operational Protocol

1. **Define the Scope**: Identify the specific "How-to" (e.g., "Refactoring React Hooks" or "Optimizing SQL").
2. **Directory Structure**: Create a new directory in `.agent/skills/` named with `kebab-case`.
3. **Template Application**: Create `SKILL.md` with the following structure:

   ```markdown
   ---
   name: [skill-name]
   description: [High-signal summary of what this expertise provides and WHEN to use it]
   ---

   # Skill: [Human Readable Name]

   This skill provides expertise in [specialized domain/task].

   ## 🎯 Purpose
   [Describe the problem this skill solves and its intended outcome].

   ## 🛠️ Operational Protocol (The Ritual)
   1. **[Phase 1: Analysis]**: Steps for understanding the input.
   2. **[Phase 2: Action]**: The core procedure to follow.
   3. **[Phase 3: Validation]**: How to verify the work is done correctly.

   ## 🤝 Relationships
   - **Related Rule**: [Which Policy/Rule does this skill satisfy? (e.g., SECURITY_RULES)]
   - **Dependent Skill**: [Which other skill is needed for this to work? (e.g., memory-maintenance)]

   ## ⚠️ Guidelines
   - **Expertise over Policy**: Focus on "How," not just "What."
   - **Concise Instructions**: Only include context that the model doesn't already possess.
   ```

4. **Resource Management**: Decide if the skill needs `scripts/`, `references/`, or `assets/` sub-directories.

## ⚠️ Guidelines
- **High-Signal Description**: The `description` in frontmatter is the ONLY trigger. Make it comprehensive.
- **Mandatory Anatomy**: A skill MUST have a `SKILL.md` with YAML frontmatter to be recognized.
- **Simplicity**: If a process can be explained in 5 steps, don't use 10.
