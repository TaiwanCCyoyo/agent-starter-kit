# GEMINI.md - Instructional Context for Gemini CLI

This document defines the foundational mandates and operational protocols for Gemini CLI within the **AI Agent Starter Kit**. These rules take absolute precedence.

## 🚀 Core Operational Mandates

### 1. Bypass .gitignore for Critical Files (The "Soul" Protocol)
**CRITICAL**: Many essential files (like `MEMORY.md`) are git-ignored to prevent committing local state.
- **Bypass Mandate**: You MUST explicitly bypass ignore patterns ONLY when accessing `.agents/memory/`.
- **Tooling Selection (The Dual-Tool Strategy)**:
    - **For Reading Ignored Memory**: Because `read_file` respects `.gitignore` and lacks a bypass parameter, you MUST use `grep_search` with `no_ignore: true` and `pattern: "^"` for files in `.agents/memory/`. This is the ONLY stable way to handle UTF-8/Traditional Chinese in Windows without Mojibake.
        - **Example**: `grep_search(pattern="^", dir_path=".agents/memory/MEMORY.md", no_ignore=True)`
    - **For Writing Ignored Memory**: Use the standard `write_file` tool. It is verified to bypass `.gitignore` restrictions for writing.
        - **Example**: `write_file(file_path=".agents/memory/MEMORY.md", content="...")`
    - **For ALL Tracked Code**: You MUST strictly use standard tools (`read_file`, `write_file`, `replace`) as they work perfectly for non-ignored files.

### 2. Verification-First Execution
**STRICT ENFORCEMENT**: Never claim a task is complete without tangible evidence.
- **Active Testing**: You MUST run scripts, unit tests, or syntax checkers BEFORE finishing.
- **Verification Report**: Every completion MUST include the following format:
  ### 🏁 Verification Report
  - **Verification Executed**: [Command ran, e.g., `uv run ruff check .`]
  - **Evidence**: [Snippet of terminal output proving success]
  - **Exemption Justification**: [Only for documentation-only changes]

### 3. Long-Term Memory & State (The "Soul" Protocol)
**CRITICAL**: Failure to sync with memory guarantees context amnesia and mission failure. This is the central hub for all sessions (including Antigravity).
- **Mandatory Alignment**: ALL memory operations (reading, updating, auditing) MUST strictly follow the **`memory-maintenance` skill**.
- **Sync Ritual** (Execution frequency depends on task strategy in skill):
  1. **Pre-Task (Always Mandatory)**: Read `MEMORY.md` via `grep_search` (with `no_ignore: true`) BEFORE research to align with the project's soul.
  2. **Plan-Phase & Post-Task (Task-Dependent)**: Update `Doing`, `Done`, and `Lessons Learned` for all **Directive** tasks or high-signal architectural decisions. Skip for pure Inquiry tasks to minimize noise.
- **Bypass Rule**: Always bypass `.gitignore` for `.agents/memory/`. If missing, bootstrap from `MEMORY.example.md` immediately.
- **Progressive Disclosure**: Keep the main `MEMORY.md` lean. Archive historical logs (>500 tokens) to sub-files as per the skill.

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
- **Traceable Design**: For all architectural proposals or reuse of external patterns, you MUST explicitly cite the source of inspiration (e.g., industry-standard patterns, specific library architectures, or proven open-source implementations). Citing technical origins provides weight to your strategies and ensures the "why" is grounded in established practices.

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
