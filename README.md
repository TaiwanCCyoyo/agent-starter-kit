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

## 🧠 Memory Management Workflow

This project uses a proactive memory system to maintain long-term context across sessions and worktrees.

### 1. Daily Usage
- **Save Memory**: When you finish a sub-task, use `/save-memory`. The agent will automatically update the `Done` section.
- **Auto-Nudge**: If the agent modifies files but forgets to update `MEMORY.md`, a system hook will automatically remind them.

### 2. Multi-Worktree Consolidation
When working with multiple worktrees, your memories will naturally diverge. To bring insights back to the main repository:
1. Run the consolidation tool:
   ```bash
   uv run python .gemini/skills/worktree-manager/scripts/memory_consolidator.py /path/to/worktree
   ```
2. Follow the tool's suggestions to merge high-signal `Lessons Learned` and `Done` items into your primary `MEMORY.md`.

### 3. Memory Compression
If `MEMORY.md` becomes too large (over 2000 tokens), the system will suggest compression. Run:
- `/compress-memory`: Summarizes old `Done` items into a single historical entry to keep the context lean.

## 🪝 Automated Hooks & Lifecycle

This repository utilizes several hooks to maintain system integrity:

| Hook Type | Name | Purpose | Script |
| :--- | :--- | :--- | :--- |
| **Git** | `pre-commit` | Lints, formats, and scans for secrets. | `.pre-commit-config.yaml` |
| **Git** | `post-checkout` | Initializes memory and hooks in new worktrees. | `scripts/git_post_checkout.py` |
| **Gemini CLI** | `SessionStart` | Loads project memory and branch context. | `scripts/session_start.py` |
| **Gemini CLI** | `AfterTool` | Formats code and validates file hygiene. | `scripts/file_hygiene.py` |
| **Gemini CLI** | `AfterAgent` | Nudges the agent to update memory after file changes. | `scripts/memory_nudger.py` |
| **Gemini CLI** | `AfterAgent` | Checks memory file size and warns if compression is needed. | `scripts/memory_compressor.py` |

### Troubleshooting Hooks
If hooks are not firing:
1. Ensure you have run `uv run pre-commit install --hook-type pre-commit --hook-type pre-push`.
2. Check `.git/hooks/post-checkout` exists and is executable.
3. Verify `.gemini/settings.json` has the correct `matcher` and `command` paths.

## 🛠️ How to Initialize
...

**For Humans**:
Prompt your AI Assistant: *"Please follow the README to initialize this repository."*

**For Agents**:
1. **Initialize Memory**:
   - **Gemini CLI**: Accessing the codebase for the first time will automatically trigger `scripts/session_start.py`, creating `.agents/memory/MEMORY.md` if it doesn't exist.
   - **Other Agents (e.g., Antigravity)**: You must manually create `.agents/memory/MEMORY.md` using the template found in `scripts/session_start.py` or ask a Gemini CLI session to initialize it for you, as these agents do not support the `SessionStart` hook.
   - **Crucial**: You MUST immediately populate the **Mission** section in the newly created `MEMORY.md` based on the current `README.md` and project context to establish the session's "Soul."
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
