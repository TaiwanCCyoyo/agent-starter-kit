[繁體中文](docs/zh-TW/README.md)
# AI Agent Starter Kit

A standardized, frictionless engineering infrastructure for multi-agent ecosystems such as Gemini CLI, Codex, Claude Code, and Antigravity. Use this repository as a project template when you want every supported agent to discover the project mission, memory, rules, skills, workflows, and verification expectations quickly.

## Core Philosophy

1. **Long-Term Memory Persistence**: Agents track project goals and lessons learned in `.agents/memory/MEMORY.md`, reducing context loss across sessions.
2. **Agent-Specific Bootstrap**: Each agent owns its native instruction and hook layer while sharing the same project memory.
3. **Automated Maintenance**: Formatting, linting, file hygiene, and memory nudges are enforced through agent hooks and repository verification scripts.
4. **Native Security**: Secret scanning is integrated into the pre-commit workflow through `detect-secrets`.
5. **Encoding & Language Integrity**: UTF-8 without BOM and language boundaries are validated for repository files.
6. **Verification-First Execution**: Agents must provide tangible validation evidence before marking tasks as complete.

## Memory Management Workflow

This project uses a proactive memory system to maintain long-term context across sessions and worktrees.

For a detailed architecture, setup model, and copy checklist, see [Memory System Introduction](docs/en/MEMORY_SYSTEM_INTRODUCTION.md).

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
- **Claude Code**: Uses registered slash commands in `.claude/commands/` (e.g. `/plan`, `/code-review`, `/gen-commit`). Subagents live in `.claude/agents/`. Path-scoped coding rules live in `.claude/rules/`. For a full list of available agents, commands, skills, hooks, and rules, see [Claude Code Components Reference](docs/en/claude-components.md).
- **Antigravity**: Uses `.agent/workflows/` and `.agent/rules/`.

## Automated Hooks & Lifecycle

This repository uses agent-native hooks to maintain system integrity:

| Agent | Hook Type | Purpose | Script |
| :--- | :--- | :--- | :--- |
| **Gemini CLI** | `SessionStart` | Loads project memory and branch context. | `.gemini/scripts/session_start.py` |
| **Gemini CLI** | `AfterTool` | Formats code and validates file hygiene. | `.gemini/scripts/auto_format.py`, `.gemini/scripts/file_hygiene.py` |
| **Gemini CLI** | `AfterAgent` | Nudges the agent to update memory after file changes. | `.gemini/scripts/memory_nudger.py` |
| **Gemini CLI** | `AfterAgent` | Checks memory file size and warns if compression is needed. | `.gemini/scripts/memory_compressor.py` |
| **Codex** | `SessionStart` | Injects `.codex/AGENTS.md`, project memory, branch, and worktree context. | `.codex/hooks/session_start.py` |
| **Codex** | `PostToolUse` | Runs lint and file hygiene checks after file edits. | `.codex/hooks/post_tool_use_hygiene.py` |
| **Codex** | `Stop` | Reminds Codex to update memory after several response rounds with pending changes and checks memory size. | `.codex/hooks/stop_memory_check.py` |
| **Claude Code** | `SessionStart` | Injects `CLAUDE.md`, project memory, branch, and worktree context. | `.claude/hooks/session_start.py` |
| **Claude Code** | `PostToolUse` | For `.py` files: auto-formats with `ruff format`, lints with `ruff check`, type-checks with `mypy`, and warns on `print()` usage. For config and doc files: validates file hygiene. | `.claude/hooks/post_tool_use_hygiene.py` |
| **Claude Code** | `Stop` | Reminds Claude to update memory after several response rounds with pending changes and checks memory size. | `.claude/hooks/stop_memory_check.py` |

### Troubleshooting Hooks

If hooks are not firing:

1. Ensure Git hooks are installed:
   ```bash
   uv run pre-commit install
   ```
2. For Gemini CLI, verify `.gemini/settings.json` has the correct matcher and command paths.
3. For Codex, verify `.codex/config.toml` enables `codex_hooks` and `.codex/hooks.json` points to `.codex/hooks/`.
4. For Claude Code, verify `.claude/settings.json` has the `hooks` section with correct paths; open `/hooks` in the Claude Code UI to reload config if hooks were added mid-session.
5. Confirm the agent trusts the project-local configuration layer.

## Permissions Configuration

Each agent layer ships with its own permission configuration. Rules follow a common pattern: auto-allow safe read and non-destructive operations; require confirmation for publishing (`git push`); deny destructive or `.git`-mutating commands.

### Claude Code (`.claude/settings.json`)

Permissions are declared in `.claude/settings.json` and take effect immediately without modifying global config. Key rules:

- **Auto-Allowed**: All workspace reads/writes, common CLI tools (`ls`, `cat`, `grep`, `find`, `diff`, `uv`, `ruff`, `pytest`, `npm`, `jq`, …), and safe git operations (`status`, `diff`, `log`, `add`, `commit`, `fetch`, `branch`, `merge`, …).
- **Requires Confirmation (ask)**: `git push` — prevents accidental remote publishing.
- **Blocked (deny)**: `git push --force`, `git push --force-with-lease`, any command that deletes or mutates the `.git` directory (`rm -rf .git`, `rd /s`, `Remove-Item -Recurse … .git`), and direct `powershell`/`pwsh` invocations (commands should run directly, not wrapped).

### Gemini CLI (`.gemini/policies/system-safe.toml`)

- **Auto-Allowed**: Basic read commands and non-destructive git operations. Memory path edits under `.agents/memory/` are also auto-approved.
- **Blocked**: `git push`, `git branch -d/-D`.

### Codex (`.codex/rules/git.rules`)

- **Requires Confirmation**: `git push`, `git branch -d/-D`.

For Codex, it is also recommended to use **Auto Mode** or auto-approval mechanisms to ensure seamless workflow execution without sacrificing safety boundaries.

## CI/CD Setup

Agents enforce quality locally via hooks, but a CI pipeline catches issues on every push and makes quality gates visible to the whole team. This section provides a minimal starting point.

### Recommended GitHub Actions Workflow

Create `.github/workflows/ci.yml` in your project:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install uv && uv sync --group dev

      - name: Lint
        run: uv run ruff check .

      - name: Type check
        run: uv run mypy .

      - name: Test
        run: uv run pytest

      - name: Secret scan
        run: uv run pre-commit run detect-secrets --all-files
```

Adjust the `pytest` step to match your project's test directory and the Python version to match `.python-version`.

### When to Use the `github-ops` Skill

Once CI is configured, use the `github-ops` skill (via Claude Code) for operational tasks:

| Task | Command |
| :--- | :--- |
| View failed run logs | `gh run view <run-id> --log-failed` |
| Re-run failed steps | `gh run rerun <run-id> --failed` |
| List recent failures | `gh run list --status failure --limit 10` |
| Check Dependabot alerts | `gh api repos/{owner}/{repo}/dependabot/alerts` |

Requires `gh` CLI installed and authenticated (`gh auth login`).

### Troubleshooting CI Failures

1. **Reproduce locally first** — run the same commands the workflow runs (`ruff check .`, `mypy .`, `pytest`) before investigating remotely.
2. **Read the full log** — `gh run view <run-id> --log-failed` shows only the failing step output.
3. **Check for environment differences** — Python version, missing env vars, or missing `uv sync` are the most common causes.
4. **Distinguish flaky from real** — if the same test passes locally and fails remotely consistently, it is usually an environment issue, not a flaky test.

## Template Usage

When applying this starter kit to a new project, copy the agent infrastructure that matches your supported tools:

| Path | Purpose |
| :--- | :--- |
| `.agents/memory/` | Shared long-term project memory location. |
| `.agent/` | Antigravity rules, skills, and workflows. |
| `.gemini/` | Gemini CLI commands, policies, hooks, and skills. |
| `.codex/` | Codex instructions, hooks, and private command-like skills. |
| `.claude/` | Claude Code settings, hooks, slash commands, subagents, skills, and path-scoped coding rules. |
| `scripts/` | Repository-level hygiene and formatting scripts used by Git and agent adapters. |
| `.pre-commit-config.yaml` | Repository-level verification hooks. |

After copying, replace `.agents/memory/MEMORY.md` with the target project's real mission, review agent-specific rules, install hooks with `uv run pre-commit install`, and verify with `uv run ruff check .`.

### Superpowers Skills Integration (for Antigravity)

To equip Antigravity agents with robust capabilities such as structured brainstorming and test-driven development, this repository has integrated a suite of skills adapted from the open-source [obra/superpowers](https://github.com/obra/superpowers) project. These copied skills reside directly under `.agent/skills/` and are fully compliant with the MIT License (Copyright (c) 2026 Jesse Vincent).

## Initialization

To initialize this repository and set up verification tools:

1. **Install Git Hooks**
   ```bash
   uv run pre-commit install
   ```
2. **Install Dev Dependencies** (includes mypy for type checking)
   ```bash
   uv sync --group dev
   ```
3. **Verify Environment**
   ```bash
   uv run ruff check .
   ```

### Initializing Memory for New Projects
Once the repository is initialized:
1. Ensure `.agents/memory/MEMORY.md` is populated with your specific project's **Mission**.

---

This project enforces UTF-8 without BOM and English for source code, technical documentation, workflows, and configuration. Traditional Chinese content belongs in `docs/zh-TW/` and `.agents/memory/`.
