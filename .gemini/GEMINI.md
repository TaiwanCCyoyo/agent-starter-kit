# GEMINI.md - Instructional Context for Gemini CLI

This document defines the foundational mandates and operational protocols for Gemini CLI within the **AI Agent Starter Kit**. These rules take absolute precedence.

## 🚀 Core Operational Mandates

### 1. Bypass .gitignore for Critical Files
**CRITICAL**: Many essential files (like `MEMORY.md`) are git-ignored to prevent committing local state.
- You MUST explicitly bypass ignore patterns when accessing `.agents/memory/`.
- **Tooling**: Set `respect_git_ignore: false` for `list_directory`/`glob`, and `no_ignore: true` for `grep_search`.
- **Fallback**: Use `run_shell_command` with `Get-Content` if file-reading tools are blocked.

### 2. Verification-First Execution
**STRICT ENFORCEMENT**: Never claim a task is complete without tangible evidence.
- **Active Testing**: You MUST run scripts, unit tests, or syntax checkers BEFORE finishing.
- **Verification Report**: Every completion MUST include the following format:
  ### 🏁 Verification Report
  - **Verification Executed**: [Command ran, e.g., `uv run ruff check .`]
  - **Evidence**: [Snippet of terminal output proving success]
  - **Exemption Justification**: [Only for documentation-only changes]

### 3. Long-Term Memory & State
- **Soul of the Session**: Rely on `.agents/memory/MEMORY.md` to eliminate context amnesia.
- **Sync Protocol**: 
  - **Pre-Task**: Read `MEMORY.md` before starting; update it with your current intent.
  - **Post-Task**: Update `MEMORY.md` with results and "Lessons Learned."
- **Initialization**: If missing, bootstrap from `MEMORY.example.md` and populate it by analyzing the codebase immediately.

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

## 🛠️ Technical Stack & Tooling

- **Environment**: Python >=3.12, managed via **uv**.
- **Sync**: Always use `uv sync` to ensure dependency alignment.
- **Linter/Formatter**: Use **Ruff**. Standard line length is `160` (defined in `ruff.toml`).
- **Command Style**: In PowerShell, avoid `&&`. Use `;` or separate commands.

## 📂 Key Resources
- **Memory**: `.agents/memory/MEMORY.md` (The stateful project brain)
- **Workflows**: `.gemini/skills/` (Custom capabilities)
- **Reference**: `doc/README.zh-TW.md` (Project overview in Traditional Chinese)
