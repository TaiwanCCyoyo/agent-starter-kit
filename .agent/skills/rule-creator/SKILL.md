---
name: rule-creator
description: Create a new project rule (Policy). Use this for defining mandatory behaviors, constraints, or non-negotiable standards.
---

# Skill: Rule-Creator (Defining Policy)

This skill provides a high-quality template for defining project policies—the "Laws" that all agents must obey.

## 🎯 Purpose
To ensure all project rules follow a consistent structure, including clear triggers and enforcement mechanisms, making them machine-readable and human-verifiable.

## 🛠️ Operational Protocol

1. **Identify the Mandate**: Determine what *must* or *must not* happen (e.g., "Always use Traditional Chinese for UI").
2. **Standard Naming**: Rule files must be named in `UPPERCASE_WITH_UNDERSCORES.md` inside `.agent/rules/`.
3. **Template Application**: Use this strict structure:

   ```markdown
   ---
   trigger: [always_on | manual | model_decision | glob]
   globs: [optional: required if trigger is glob]
   description: [Mandatory: Concise summary of the policy's intent]
   ---

   # [Rule Name]

   1. **[Core Mandate]**: Define the primary requirement clearly.
   2. **[Constraints]**: List what is explicitly forbidden or required to support the mandate.
   3. **[Enforcement]**: Define how this rule is verified (e.g., "Run file_hygiene.py").

   ## 🏁 Mandatory Verification Format
   If this rule requires a specific reporting format (like a Verification Report), specify it here.
   ```

4. **Validation**: Verify that the YAML frontmatter is valid and the file is correctly placed.

## ⚠️ Guidelines
- **Policy over Procedure**: Rules define *what* the result must be, not *how* to do it.
- **Conciseness**: One rule should cover one domain.
- **Verification-First**: A rule without an enforcement method is just a suggestion.
