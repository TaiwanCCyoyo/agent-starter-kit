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
**STRICT ENFORCEMENT**: Do not claim completion without verification evidence.
- **Hook Alignment**: Rely on configured hooks (e.g., `scripts/file_hygiene.py`, `ruff`) for baseline hygiene. Do not manually rerun baseline checks only to create evidence.
- **Active Testing**: Run additional task-specific tests or scripts when the change requires validation beyond hook coverage.
- **Verification Report**: Every completion MUST include the following format:
  ### 🏁 Verification Report
  - **Verification Executed**: [Command ran, e.g., `uv run pytest`]
  - **Evidence**: [Snippet of output proving success]
  - **Exemption Justification**: [If verification is skipped, state why and the residual risk]

### 3. Long-Term Memory & State (The "Soul" Protocol)
**CRITICAL**: Failure to sync with memory guarantees context amnesia.
- **Mandatory Alignment**: Follow the **`memory-maintenance` skill** for updates and audits.
- **Automated Lifecycle**:
    1.  **SessionStart**: System injects Git context and `MEMORY.md`. Align with branch mission immediately.
    2.  **AfterAgent (Nudging)**: Stateful hooks monitor progress. If nudged, update `MEMORY.md`.
- **Command-Like Skills**:
    - `save-memory` -> Update `MEMORY.md` with Done & Lessons.
    - `compress-memory` -> Archive historical details to keep memory lean.
- **Bypass Rule**: Always bypass `.gitignore` for `.agents/memory/`.

### 4. Learning And Escalation
- **No Silent Friction**: Do not silently normalize repeated friction. If a blocker, workaround, or uncertainty appears more than once, pause and surface it to the user.
- **Explicit Tradeoffs**: Prefer explicit tradeoffs over hidden assumptions. State what you know and what you are assuming.
- **Process Debugging**: Treat repeated confusion as a process bug. Convert it into an instruction, skill update, or memory lesson.
- **Immediate Escalation**: Ask for user assistance immediately when credentials, approvals, environment ownership, or irreversible tradeoffs are needed.

### 5. Surgical Editing & Feature Preservation
- **Minimal Surface Area**: Prefer the smallest change that satisfies the verified goal. Do not rewrite adjacent code or formatting without need.
- **Prevent Feature Deletion**: Do not delete existing functions or logic unless expressly authorized. If a purpose is unclear, assume it is necessary.

### 6. Security & Secrets
- **No Secrets Policy**: Never log, print, or commit API keys or sensitive credentials.
- **Pre-commit Integrity**: Ensure hooks are installed (`uv run pre-commit install`). Do not bypass.

### 7. Language & Encoding Mandates
- **Communication**: Use **Traditional Chinese** (`zh-TW`) for user interaction.
- **Project Output**: Use **English** for code, commits, and technical docs.
- **Encoding**: ALL files MUST be saved in **UTF-8** (without BOM).

## 🛠️ Technical Stack & Tooling

- **Environment**: Python >=3.12, managed via **uv**.
- **Sync**: Always use `uv sync` to ensure dependency alignment.
- **Linter/Formatter**: Use **Ruff**. Standard line length is `160` (defined in `ruff.toml`).
- **Command Style**: In PowerShell, avoid `&&`. Use `;` or separate commands.

## 📂 Key Resources
- **Memory**: `.agents/memory/MEMORY.md` (The stateful project brain)
- **Skills**: `.gemini/skills/` (Gemini-specific capabilities)
- **Reference**: `docs/zh-TW/README.md` (Project overview in Traditional Chinese)
