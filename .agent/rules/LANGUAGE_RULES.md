---
trigger: always_on
description: Rules for language preferences (Traditional Chinese for collaboration, English for project output) and I18N documentation requirements.
---

# Language and I18N Documentation Rules

## 1. Language Preferences

- **[MANDATORY] Collaboration & Communication**: When interacting with the USER outside of source code modifications, you **MUST** use **Traditional Chinese** (`zh-TW`) by default. This strictly applies to:
    - Dialogue responses
    - Implementation Plans
    - Task summaries & Walkthroughs
    - All artifacts generated during Planning Mode
      _(Note: Technical terms, technical comments, and variable names may remain in English.)_
- **Project Output**: All project-related files (source code, git commit messages, `SKILL.md` files, configuration files, etc.) must be in **English**.

## 2. I18N Documentation (README) Rules

- **Default README**: The root `README.md` must be in **English**.
- **Multilingual Support**: If a Traditional Chinese version is required, it must be placed at `docs/zh-TW/README.md`.
- **Linking**: The English `README.md` should contain a link to the Traditional Chinese version at the top of the file for easy navigation.

## 3. Encoding and File Path Integrity

- **Encoding**: Save all repository files in **UTF-8 without BOM**.
- **Chinese Content Boundary**: Traditional Chinese content is strictly restricted to `.memories/`, `docs/zh-TW/`, `legacy/`, ignored local `tasks/` logs, and the Traditional Chinese translation link in the root `README.md`. No Chinese files or comments should be created in other code development paths.
