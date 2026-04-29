[繁體中文](docs/zh-TW/README.md)
# AI Agent Starter Kit

A standardized, frictionless engineering infrastructure for multi-agent ecosystems such as Gemini CLI, Codex, and Antigravity. Use this repository as a project template when you want every supported agent to discover the project mission, memory, rules, skills, workflows, and verification expectations quickly.

## Core Philosophy

1. **Long-Term Memory Persistence**: Agents track project goals and lessons learned in `.agents/memory/MEMORY.md`, reducing context loss across sessions.
2. **Agent-Specific Bootstrap**: Each agent owns its native instruction and hook layer while sharing the same project memory.
3. **Automated Maintenance**: Formatting, linting, file hygiene, and memory nudges are enforced through agent hooks and repository verification scripts.
4. **Native Security**: Secret scanning is integrated into the pre-commit workflow through `detect-secrets`.
5. **Encoding & Language Integrity**: UTF-8 without BOM and language boundaries are validated for repository files.
6. **Verification-First Execution**: Agents must provide tangible validation evidence before marking tasks as complete.

## Memory Management Workflow

This project uses a proactive memory system to maintain long-term context across sessions and worktrees.

### 1. Daily Usage

- **Save Memory**: When you finish a meaningful sub-task, update `.agents/memory/MEMORY.md` through the relevant agent workflow.
- **Auto-Nudge**: Hooks remind agents to update memory after sustained work with pending changes.
- **Compression**: If `MEMORY.md` grows too large, the system suggests memory compression.

### 2. Multi-Worktree Consolidation

When working with multiple worktrees, memories can diverge. To bring insights back to the main repository:

1. Use the Gemini CLI command:
   ```bash
   /worktree finish <path/to/worktree>
   ```
2. The agent performs AI semantic consolidation to merge high-signal `Lessons Learned` and `Done` items into the primary `MEMORY.md`.

### 3. Agent Workflows

- **Gemini CLI**: Uses `.gemini/commands/` and `.gemini/skills/`.
- **Codex**: Uses command-like skills in `.codex/skills/`; these can be invoked with plain text such as `/gen-commit`, but they are not registered slash commands.
- **Antigravity**: Uses `.agent/workflows/` and `.agent/rules/`.

## Automated Hooks & Lifecycle

This repository uses agent-native hooks to maintain system integrity:

| Agent | Hook Type | Purpose | Script |
| :--- | :--- | :--- | :--- |
| **Gemini CLI** | `SessionStart` | Loads project memory and branch context. | `.gemini/scripts/session_start.py` |
| **Gemini CLI** | `AfterTool` | Formats code and validates file hygiene. | `scripts/auto_format.py`, `scripts/file_hygiene.py` |
| **Gemini CLI** | `AfterAgent` | Nudges the agent to update memory after file changes. | `.gemini/scripts/memory_nudger.py` |
| **Gemini CLI** | `AfterAgent` | Checks memory file size and warns if compression is needed. | `.gemini/scripts/memory_compressor.py` |
| **Codex** | `SessionStart` | Injects `.codex/AGENTS.md`, project memory, branch, and worktree context. | `.codex/hooks/session_start.py` |
| **Codex** | `PostToolUse` | Runs lint and file hygiene checks after file edits. | `.codex/hooks/post_tool_use_hygiene.py` |
| **Codex** | `Stop` | Reminds Codex to update memory after several response rounds with pending changes and checks memory size. | `.codex/hooks/stop_memory_check.py` |

### Troubleshooting Hooks

If hooks are not firing:

1. Ensure Git hooks are installed:
   ```bash
   uv run pre-commit install
   ```
2. For Gemini CLI, verify `.gemini/settings.json` has the correct matcher and command paths.
3. For Codex, verify `.codex/config.toml` enables `codex_hooks` and `.codex/hooks.json` points to `.codex/hooks/`.
4. Confirm the agent trusts the project-local configuration layer.

## Template Usage

When applying this starter kit to a new project, copy the agent infrastructure that matches your supported tools:

| Path | Purpose |
| :--- | :--- |
| `AGENTS.md` | Thin router for Codex and other agents. |
| `.agents/memory/` | Shared long-term project memory location. |
| `.agent/` | Antigravity rules, skills, and workflows. |
| `.gemini/` | Gemini CLI commands, policies, hooks, and skills. |
| `.codex/` | Codex instructions, hooks, and private command-like skills. |
| `scripts/` | Shared hygiene, formatting, and memory helper scripts. |
| `.pre-commit-config.yaml` | Repository-level verification hooks. |

After copying, replace `.agents/memory/MEMORY.md` with the target project's real mission, review agent-specific rules, install hooks with `uv run pre-commit install`, and verify with `uv run ruff check .`.

## Initialization

**For humans**:

Prompt your AI assistant: "Please follow the README to initialize this repository."

**For agents**:

1. **Initialize Memory**
   - **Gemini CLI**: First access automatically triggers `.gemini/scripts/session_start.py`, creating `.agents/memory/MEMORY.md` if it does not exist.
   - **Codex**: First trusted session triggers `.codex/hooks/session_start.py`, injecting `.codex/AGENTS.md` and `.agents/memory/MEMORY.md`.
   - **Other agents**: Manually create `.agents/memory/MEMORY.md` using the template in `.gemini/scripts/session_start.py` or ask a supported agent to initialize it.
   - Populate the **Mission** section in `MEMORY.md` based on the target project.
2. **Install Hooks**
   ```bash
   uv run pre-commit install
   ```
3. **Verify Setup**
   ```bash
   uv run ruff check .
   ```

---

This project enforces UTF-8 without BOM and English for source code, technical documentation, workflows, and configuration. Traditional Chinese content belongs in `docs/zh-TW/` and `.agents/memory/`.
