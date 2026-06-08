[繁體中文](docs/zh-TW/README.md)
# AI Agent Starter Kit

A standardized, frictionless engineering infrastructure for Codex, Claude Code, and Antigravity. Use this repository as a project template when you want every supported agent to discover the project mission, memory, rules, skills, workflows, and verification expectations quickly.

## Core Philosophy

1. **Long-Term Memory Persistence**: Codex uses bounded files under `.memories/memories/` plus a Holographic-compatible SQLite `memory_store.db`.
2. **Agent-Specific Bootstrap**: Each agent owns its native instruction and hook layer while sharing the same project memory.
3. **Automated Maintenance**: Formatting, linting, file hygiene, and memory nudges are enforced through agent hooks and repository verification scripts.
4. **Native Security**: Secret scanning is integrated into the pre-commit workflow through `detect-secrets`.
5. **Encoding & Language Integrity**: UTF-8 without BOM and language boundaries are validated for repository files.
6. **Verification-First Execution**: Agents state a verification plan before making non-trivial changes, run those checks after editing, and provide evidence before marking tasks complete.

## Memory Management Workflow

This project uses a proactive memory system to maintain long-term context across sessions and worktrees.

For a detailed architecture, setup model, and copy checklist, see [Memory System Introduction](docs/en/memory-system-introduction.md).

### 1. Daily Usage

- **Save Memory**: Curate stable high-frequency facts in `.memories/memories/MEMORY.md`; store searchable facts and recurring-problem history in `.memories/memory_store.db`.
- **Auto-Nudge**: Hooks remind agents to update memory after sustained work with pending changes.
- **Compression**: If `MEMORY.md` grows too large, the system suggests memory compression.

### 2. Multi-Worktree Consolidation

When working with multiple worktrees, memories can diverge. To bring insights back to the main repository:

1. Use the active agent's worktree workflow:
   ```bash
   /worktree finish <path/to/worktree>
   ```
2. The agent performs AI semantic consolidation to merge high-signal `Lessons Learned` and `Done` items into the primary `MEMORY.md`.

### 3. Agent Workflows

- **Codex**: Uses native Plan Mode, repo-scoped skills in `.codex/skills/`, and specialist reviewer agents in `.codex/agents/`. Command-like skills can be invoked with plain text such as `/gen-commit`, but they are not registered slash commands. For details, see [Codex Components Reference](docs/en/codex-components.md).
- **Claude Code**: Uses registered slash commands in `.claude/commands/` (e.g. `/plan`, `/code-review`, `/gen-commit`). Subagents live in `.claude/agents/`. Path-scoped coding rules live in `.claude/rules/`. For a full list of available agents, commands, skills, hooks, and rules, see [Claude Code Components Reference](docs/en/claude-components.md).
- **Antigravity**: Uses `.agent/workflows/`, `.agent/rules/`, and `.agent/skills/`. For a full list of available components and hooks, see [Antigravity Components Reference](docs/en/antigravity-components.md).

## Automated Hooks & Lifecycle

This repository uses agent-native hooks to maintain system integrity:

| Agent | Hook Type | Purpose | Script |
| :--- | :--- | :--- | :--- |
| **Codex** | `SessionStart` | Injects `.codex/AGENTS.md`, project memory, branch, and worktree context. | `.codex/hooks/session_start.py` |
| **Codex** | `PostToolUse` | Runs targeted post-edit hygiene. Python files are formatted, linted, checked for file hygiene, and warned on `print()` calls; docs and config files run file hygiene only. | `.codex/hooks/post_tool_use_hygiene.py`, `scripts/python_hygiene.py`, `scripts/file_hygiene.py` |
| **Codex** | `Stop` | Reminds Codex to update memory after several response rounds with pending changes and checks memory size. | `.codex/hooks/stop_memory_check.py` |
| **Claude Code** | `SessionStart` | Injects `CLAUDE.md`, project memory, branch, and worktree context. | `.claude/hooks/session_start.py` |
| **Claude Code** | `PostToolUse` | For `.py` files: auto-formats with `ruff format`, lints with `ruff check`, type-checks with `mypy`, and warns on `print()` usage. For config and doc files: validates file hygiene. | `.claude/hooks/post_tool_use_hygiene.py` |
| **Claude Code** | `Stop` | Reminds Claude to update memory after several response rounds with pending changes, checks memory size, and prompts skill review after substantial sessions. | `.claude/hooks/stop_memory_check.py` |
| **Antigravity** | `SessionStart` | Initializes SQLite, copies missing worktree memory, and injects the bounded files. | `.agent/hooks/session_start.py` |
| **Antigravity** | `PostToolUse` | Runs targeted Ruff, mypy, and file-hygiene checks. | `.agent/hooks/post_tool_use_hygiene.py` |
| **Antigravity** | `Stop` | Checks bounded-file limits and rejects legacy memory taxonomy. | `.agent/hooks/stop_memory_check.py` |

### Troubleshooting Hooks

If hooks are not firing:

1. Ensure Git hooks are installed:
   ```bash
   uv run pre-commit install
   ```
2. For Codex, verify `.codex/config.toml` enables `codex_hooks` and `.codex/hooks.json` points to `.codex/hooks/`.
3. For Claude Code, verify `.claude/settings.json` has the `hooks` section with correct paths; open `/hooks` in the Claude Code UI to reload config if hooks were added mid-session.
4. For Antigravity, verify `.agent/hooks.json` is correctly defining the events.
5. Confirm the agent trusts the project-local configuration layer.

## Permissions Configuration

Each agent layer ships with its own permission configuration. Rules follow a common pattern: auto-allow safe read and non-destructive operations; require confirmation for publishing (`git push`); deny destructive or `.git`-mutating commands.

### Claude Code (`.claude/settings.json`)

Permissions are declared in `.claude/settings.json` and take effect immediately without modifying global config. Key rules:

- **Auto-Allowed**: All workspace reads/writes, common CLI tools (`ls`, `cat`, `grep`, `find`, `diff`, `uv`, `ruff`, `pytest`, `npm`, `jq`, …), and safe git operations (`status`, `diff`, `log`, `add`, `commit`, `fetch`, `branch`, `merge`, …).
- **Requires Confirmation (ask)**: `git push` — prevents accidental remote publishing.
- **Blocked (deny)**: `git push --force`, `git push --force-with-lease`, any command that deletes or mutates the `.git` directory (`rm -rf .git`, `rd /s`, `Remove-Item -Recurse … .git`), and direct `powershell`/`pwsh` invocations (commands should run directly, not wrapped).

### Codex

Codex does not ship repository-local permission rules in this starter kit. Permission review is delegated to the configured approvals reviewer (for example, an auto-review / "review on my behalf" workflow) instead of `.codex/rules/`.

Codex planning is handled by the main agent through Plan Mode; this starter kit intentionally does not define a separate Codex planner agent.

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
| `.memories/` | Git-ignored instantiated memory: bounded files and SQLite store. |
| `.agent/` | Antigravity rules, skills, and workflows. |
| `.codex/` | Codex instructions, hooks, private command-like skills, and specialist agents. |
| `.claude/` | Claude Code settings, hooks, slash commands, subagents, skills, and path-scoped coding rules. |
| `scripts/` | Repository-level hygiene and formatting scripts used by Git and agent adapters. |
| `.pre-commit-config.yaml` | Repository-level verification hooks. |

After copying, replace `.memories/memories/MEMORY.md` with the target project's durable facts, review agent-specific rules, install hooks with `uv run pre-commit install`, and verify with `uv run ruff check .`.

### Superpowers Skills Integration

This repository integrates superpowers capabilities across all three agents:

- **Claude Code**: The official `superpowers@claude-plugins-official` plugin is enabled in `.claude/settings.json` and activates automatically — no manual installation required.
- **Antigravity**: A suite of skills adapted from the open-source [obra/superpowers](https://github.com/obra/superpowers) project resides under `.agent/skills/`, fully compliant with the MIT License (Copyright (c) 2026 Jesse Vincent).
- **Codex**: Superpowers is not pre-configured. Install it separately following the [obra/superpowers](https://github.com/obra/superpowers) setup instructions.

## Design Influences

This starter kit is shaped by two open-source projects:

- **[Everything Claude Code (ECC)](https://github.com/affaan-m/ECC)** — Production-ready agents, skills, hooks, commands, and rules for Claude Code. The development agents (planner, code-reviewer, tdd-guide, security-reviewer, etc.), slash commands (/plan, /build-fix, /code-review, /test-coverage), coding rules, and the Prompt Defense Baseline in `CLAUDE.md` are all ported or adapted from ECC v2.0.0-rc.1.

- **[Hermes Agent (NousResearch)](https://github.com/NousResearch/hermes-agent)** — Inspired this project's bounded `MEMORY.md` and `USER.md`, frozen prompt snapshots, SQLite FTS5 session recall, and learning-loop design. This starter kit adapts those mechanisms rather than directly porting Hermes.

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
4. **Antigravity MCP Setup**

   If you are using Antigravity, note that it requires MCP servers to be configured globally. Please configure your SQLite memory-db MCP server in your home directory (e.g., `~/.mcp.json`).

### Initializing Memory for New Projects
Once the repository is initialized:
1. Ensure `.memories/memories/MEMORY.md` contains the target project's stable mission and constraints.

---

This project enforces UTF-8 without BOM and English for source code, technical documentation, workflows, and configuration. Traditional Chinese content belongs in `docs/zh-TW/` and `.memories/`.
