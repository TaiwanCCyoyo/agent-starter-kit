# GEMINI.md - Instructional Context for Gemini CLI

## 🤖 Available Gemini 3.0 Models
- **Pro**: `gemini-3-pro-preview` (High reasoning, planning, complex tasks)
- **Flash**: `gemini-3-flash-preview` (Speed, simple tasks, reading)

---

This document defines the foundational mandates and operational protocols for Gemini CLI within the **AI Agent Starter Kit**. These rules take absolute precedence.

## 🚀 Operating Contract

- **Communication**: Use **Traditional Chinese** (`zh-TW`) for user interaction.
- **Project Output**: Use **English** for code, commits, technical docs, `SKILL.md`, and workflows.
- **README Policy**: Keep root `README.md` English except for the first-line zh-TW link.
- **Encoding**: ALL files MUST be saved in **UTF-8** (without BOM).
- **Security**: Never log, print, or commit API keys, secrets, or sensitive credentials.
- **Source Control**: Respect dirty worktrees; never revert user changes unless explicitly requested.

## 🛠️ Engineering Discipline

- **Surgical Editing**: Prefer the smallest change that satisfies the verified goal. Touch only files and lines related to the task; do not refactor, reformat, or delete adjacent code without need.
- **Minimal Surface Area**: Do not add speculative features, knobs, or abstractions. Match surrounding style and ownership boundaries.
- **Feature Preservation**: Do not delete existing functions or logic unless expressly authorized. If a purpose is unclear, assume it is necessary.
- **Cleanup**: Remove unused imports, variables, or functions created by the current change. Do not touch pre-existing dead code unless asked.
- **Thoughtfulness**: For non-trivial work, state a brief goal and verification approach before editing when the path is not obvious.

## 🧠 Learning And Escalation

- **Assumption Discipline**: Prefer explicit tradeoffs over hidden assumptions. State what you know and what you are assuming.
- **No Silent Friction**: Do not silently normalize repeated friction. If a blocker, workaround, or uncertainty appears twice, surface it to the user.
- **Immediate Escalation**: Ask for user assistance immediately when credentials, approvals, environment ownership, or product decisions are needed.
- **Process Debugging**: Treat repeated confusion as a process bug. Propose converting it into a memory note, skill update, or instruction change.

## 💾 Memory & State (The "Soul" Protocol)

- **Mandatory Alignment**: Read `.agents/memory/MEMORY.md` before substantial work.
- **Durable Updates**: Update memory ONLY when the change creates durable project state, decisions, lessons, or handoff notes.
- **Bypass Mandate**: You MUST explicitly bypass ignore patterns ONLY when accessing `.agents/memory/`.
    - **Read (Shell Override)**: Standard `read_file` honors `.gitignore`. To read memory, you MUST use `run_shell_command` with `Get-Content`.
        - **Command**: `run_shell_command(command="Get-Content .agents/memory/MEMORY.md")`
    - **Write**: Use `write_file` or `replace`. These tools bypass `.gitignore` restrictions for writing.
- **Automated Lifecycle**:
    1. **SessionStart**: Context is injected. Align with branch mission immediately.
    2. **AfterAgent (Nudging)**: Stateful hooks monitor progress. If nudged, update `MEMORY.md`.

## ✅ Verification

- **Strict Enforcement**: Do not claim completion without verification evidence.
- **Hook Alignment**: Rely on configured hooks (e.g., `ruff`) for baseline hygiene; do not manually rerun them only to create evidence.
- **Active Testing**: Run additional task-specific tests or scripts when hook coverage is insufficient.
- **Verification Report**: Every completion MUST include:
  ### 🏁 Verification Report
  - **Verification Executed**: [Command ran]
  - **Evidence**: [Snippet of success]
  - **Exemption Justification**: [If skipped, state why and the risk]

## 🛠️ Technical Stack & Tooling

- **Environment**: Python >=3.12, managed via **uv**. Always use `uv sync`.
- **Linter/Formatter**: Use **Ruff**. Standard line length is `160`.
- **Command Style**: In PowerShell, avoid `&&`. Use `;` or separate commands.

## 📂 Key Resources
- **Memory**: `.agents/memory/MEMORY.md` (The stateful project brain)
- **Subagents**: Specialized config in `.gemini/agents/`.
- **Reference**: `docs/zh-TW/README.md` (Project overview)
