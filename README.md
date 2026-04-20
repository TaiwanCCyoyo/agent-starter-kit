[繁體中文版本 (Traditional Chinese)](docs/zh-TW/README.md)
# AI Agent Starter Kit

A standardized, friction-less engineering infrastructure for multi-agent ecosystems (Gemini CLI, Antigravity, and more).

## 🚀 Core Philosophy

1. **Long-Term Memory Persistence**: The agent tracks project goals and lessons learned in `.agents/memory/MEMORY.md`, eliminating context amnesia.
2. **Automated Maintenance**: Python formatting (`ruff`) and file hygiene (UTF-8, English constraints) are **completely automatic** via Gemini CLI `AfterTool` hooks and Git `pre-commit` hooks.
3. **Native Security**: Security scanning (`detect-secrets`) is integrated into the pre-commit workflow.
4. **Auto-Approval Policies**: Standardized tasks (like memory updates in `.agents/memory/`) are auto-approved for Gemini CLI to minimize interruptions.
5. **Encoding & Language Integrity**: Mandatory validation (UTF-8 and English) for core logic, enforced via Gemini CLI hooks and `pre-commit`.
6. **Verification-First Execution**: Agents must provide tangible validation evidence before marking tasks as complete.

## 🏗️ Architecture

Agent-specific protocols are isolated:

* **`.agent/`**: **Antigravity-specific** rules and workflows.
* **`.gemini/`**: **Gemini CLI-specific** policies, skills, and hooks.
* **`.agents/memory/`**: **Shared** stateful brain (Git-ignored).

## 🛠️ How to Initialize

**For Humans**:
Prompt your AI Assistant: *"Please follow the README to initialize this repository."*

**For Agents**:
1. **Bootstrap Memory**: Copy `.agents/memory/MEMORY.example.md` to `.agents/memory/MEMORY.md`.
   - **Crucial**: You MUST immediately populate the **Mission** section in `MEMORY.md` based on the current `README.md` and project context to establish the session's "Soul."
2. **Install Hooks**: Run the following to install standard and custom hooks:
   ```bash
   uv run pre-commit install
   # Register sync protocol (Linux/macOS)
   printf "#!/bin/bash\nuv run python scripts/git_post_checkout.py \"\$@\"" > .git/hooks/post-checkout
   chmod +x .git/hooks/post-checkout
   ```
3. **Verify Setup**: Run `uv run ruff check .` to ensure the environment is ready.

---
*Note: This project enforces **UTF-8 (without BOM)** encoding and **English** for technical documentation/code.*
