# GEMINI.md - Instructional Context for Gemini CLI

This document defines the foundational mandates and operational protocols for Gemini CLI within the **AI Agent Starter Kit**. These rules take absolute precedence.

## 🚀 Core Operational Mandates

### 1. Bypass .gitignore for Critical Files
**CRITICAL**: Many essential files (like `MEMORY.md`) are git-ignored to prevent committing local state.
- You MUST explicitly bypass ignore patterns when accessing `.agents/memory/`.
- **Tooling**:
  - `glob`: Set `respect_git_ignore: false`.
  - `list_directory`: Set `file_filtering_options: { respect_git_ignore: false }`.
  - `grep_search`: Set `no_ignore: true`.
- **Fallback**: `read_file` LACKS ignore-bypass parameters. If blocked, you MUST use `run_shell_command` (e.g., `Get-Content` or `cat`) to read the file.

### 2. Verification-First Execution
**STRICT ENFORCEMENT**: Never claim a task is complete without tangible evidence.
- **Active Testing**: You MUST run scripts, unit tests, or syntax checkers BEFORE finishing.
- **Verification Report**: Every completion MUST include the following format:
  ### 🏁 Verification Report
  - **Verification Executed**: [Command ran, e.g., `uv run ruff check .`]
  - **Evidence**: [Snippet of terminal output proving success]
  - **Exemption Justification**: [Only for documentation-only changes]

### 3. Long-Term Memory & State (The "Soul" Protocol)
**CRITICAL**: Failure to sync with memory guarantees context amnesia and mission failure. UNLESS a task is a one-time minor matter ENTIRELY UNRELATED to the current project (e.g., general knowledge questions, greetings), you MUST follow the **Sync Protocol**.
- **Sync Protocol**:
  1. **Pre-Task Sync**: Read `MEMORY.md` (and related sub-files) BEFORE any research or planning. You must understand the project's current "Soul" to act correctly.
  2. **Plan-Phase Sync**: After research and planning, update the `Doing` section in `MEMORY.md` with your specific intent BEFORE you start modifying files. **You MUST choose a short, distinct Session Name for yourself and prefix your entry.** (e.g., `- **[Session Name]**: ...`).
  3. **Post-Task Sync**: After successful validation, update the `Done` section (keeping your Session Name prefix) and record `Lessons Learned` to avoid repeating mistakes.
- **Bypass Rule**: Always use `respect_git_ignore: false` or shell commands to access `.agents/memory/`. If missing, bootstrap from `MEMORY.example.md` immediately.

### 4. Collaborative Debugging & Enablement
- **Ask for Enablement, Not Completion**: If blocked (permissions, API keys), ask for the **tools or access** to solve it yourself. Do not ask the user to do the manual work for you.
- **No Silent Downgrades**: If a task cannot be completed as requested, halt and consult the user. Do not unilaterally simplify the task.
- **3-Strike Persistence**: Attempt at least 3 distinct debugging approaches before escalating.

### 5. Security & Secrets
- **No Secrets Policy**: Never log, print, or commit API keys or sensitive credentials.
- **Pre-commit Integrity**: Git `pre-commit` hooks are mandatory. Ensure they are installed (`uv run pre-commit install`). Do not bypass them.

### 6. Reuse & Efficiency
- **Don't Reinvent the Wheel**: Check existing patterns in the codebase or reference open-source implementations before writing complex logic from scratch.
- **Copy and Adapt**: Prioritize adapting proven configurations and scripts.

### 7. Prevent Feature Deletion
**CRITICAL**: Do not delete existing functions or features without explicit intent or request.
- **Suspect Utility**: If a purpose is unclear, assume it is necessary (e.g., undocumented feature, bug fix, or future-use).
- **Verification**: Always verify and preserve existing logic unless expressly authorized or required by the current task to remove it.

### 8. Language & Encoding Mandates
- **Communication**: Use **Traditional Chinese** (`zh-TW`) for all user-facing communication (responses, plans, walkthroughs).
- **Project Output**: Use **English** for all technical outputs (code, commit messages, `SKILL.md`, config files, comments).
- **Encoding**: ALL files MUST be saved in **UTF-8** (without BOM). Avoid Mojibake by ensuring consistent encoding across tools.
- **Validation Hook**: A mandatory `AfterTool` hook runs `scripts/file_hygiene.py` to enforce these rules.
    - **Exception Paths**: `.agents/memory/`, `docs/zh-TW/`, and the first line of `README.md` are allowed to contain Traditional Chinese.
- **Documentation**: Root `README.md` MUST be in English and link to the Traditional Chinese version at `docs/zh-TW/README.md`.

## 🛠️ Technical Stack & Tooling

- **Environment**: Python >=3.12, managed via **uv**.
- **Sync**: Always use `uv sync` to ensure dependency alignment.
- **Linter/Formatter**: Use **Ruff**. Standard line length is `160` (defined in `ruff.toml`).
- **Command Style**: In PowerShell, avoid `&&`. Use `;` or separate commands.

## 📂 Key Resources
- **Memory**: `.agents/memory/MEMORY.md` (The stateful project brain)
- **Skills**: `.gemini/skills/` (Gemini-specific capabilities)
- **Reference**: `docs/zh-TW/README.md` (Project overview in Traditional Chinese)
