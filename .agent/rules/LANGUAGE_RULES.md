---
trigger: always_on
description: Rules for language preferences (Traditional Chinese for collaboration, English for project output) and I18N documentation requirements.
---

# Language and I18N Documentation Rules

## 1. Language Preferences
- **Collaboration & Communication**: When communicating with the user (e.g., in responses, implementation plans, walkthroughs), use **Traditional Chinese** (`zh-TW`) by default. Technical terms may remain in English.
- **Project Output**: All project-related files (source code, git commit messages, `SKILL.md` files, configuration files, etc.) must be in **English**.

## 2. I18N Documentation (README) Rules
- **Default README**: The root `README.md` must be in **English**.
- **Multilingual Support**: If a Traditional Chinese version is required, it must be placed at `docs/zh-TW/README.md`.
- **Linking**: The English `README.md` should contain a link to the Traditional Chinese version at the top of the file for easy navigation.
