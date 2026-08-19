[繁體中文](docs/zh-TW/README.md)

# AI Agent Starter Kit

A standardized, frictionless engineering infrastructure for Codex, Claude Code, and Antigravity. Use this repository as a project template when you want every supported agent to discover the project mission, memory, rules, skills, workflows, and verification expectations quickly.

## Core Philosophy

1. **Long-Term Memory Persistence**: Codex uses bounded files under `.memories/memories/` plus a Holographic-compatible SQLite `memory_store.db`.
2. **Optional OpenSpec Planning Handoff**: Downstream projects may initialize OpenSpec and treat its specs, changes, and tasks as regular project files.
3. **Agent-Specific Bootstrap**: Each agent owns its native instruction and hook layer. Codex and Antigravity share `.memories/` project memory; Claude Code uses its own built-in memory and stays custodian-only for `.memories/` (skeleton creation, worktree sync).
4. **Automated Maintenance**: Formatting, linting, file hygiene, and memory nudges are enforced through agent hooks and repository verification scripts.
5. **Native Security**: Secret scanning is integrated into the pre-commit workflow through `detect-secrets`.
6. **Encoding & Language Integrity**: UTF-8 without BOM and language boundaries are validated for repository files.
7. **Verification-First Execution**: Agents state a verification plan before making non-trivial changes, run those checks after editing, and provide evidence before marking tasks complete.

## Current Defaults

- **Shared development rules**: Codex and Claude Code use the same phase routing model: native planning for in-session plans, optional downstream OpenSpec files for durable planning handoff, repository-owned skills and direct verification for implementation work, dedicated reviewers for quality and security, and explicit commit/PR workflow owners.
- **OpenSpec CLI dependency**: Spec-driven planning expects the OpenSpec CLI to be installed by the user. Run `openspec init` in each downstream project or workspace that wants OpenSpec planning, then treat the generated specs, changes, and tasks as normal project files and commit them when they are part of the project record.
- **Layered verification**: Claude Code uses the official Pyright LSP plugin plus a read-only Ruff check for `E722,F601,F602,F634`; Codex uses a broader read-only `F` check because it has no Python LSP. Both use pre-commit before completion for authoritative formatting, linting, type checking, and file validation.
- **Security review contract**: Security-sensitive changes route to dedicated security reviewers, and any `CRITICAL` security or data-loss risk blocks completion until fixed.
- **Editor hygiene**: `.vscode/settings.json` trims trailing whitespace, keeps exactly one final newline, enables Ruff formatting for Python, and hides generated caches and local agent state from search/watchers.

## Memory Management Workflow

Codex and Antigravity use a proactive `.memories/` system to maintain long-term context across sessions and worktrees. Claude Code uses its own built-in memory instead and only acts as custodian of `.memories/` (skeleton creation, worktree sync) — see [Claude Code Components Reference](docs/en/claude-components.md).

For a detailed architecture, setup model, and copy checklist, see [Memory System Introduction](docs/en/memory-system-introduction.md).

### 1. Daily Usage (Codex, Antigravity)

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
- **Claude Code**: Uses registered slash commands in `.claude/commands/` (e.g. `/gen-commit`, `/worktree`). Subagents live in `.claude/agents/`. Path-scoped coding rules live in `.claude/rules/`. Durable memory is Claude Code's built-in memory, not `.memories/` — see `rules/common/memory.md`. For a full list of available agents, commands, skills, hooks, and rules, see [Claude Code Components Reference](docs/en/claude-components.md).
- **Antigravity**: Uses `.agent/workflows/`, `.agent/rules/`, and `.agent/skills/`. For a full list of available components and hooks, see [Antigravity Components Reference](docs/en/antigravity-components.md).

## Automated Hooks & Lifecycle

This repository uses agent-native hooks to maintain system integrity:

| Agent           | Hook Type      | Purpose                                                                                                                 | Script                                   |
| :-------------- | :------------- | :---------------------------------------------------------------------------------------------------------------------- | :--------------------------------------- |
| **Codex**       | `SessionStart` | Injects `.codex/AGENTS.md`, project memory, branch, and worktree context.                                               | `.codex/hooks/session_start.py`          |
| **Codex**       | `PostToolUse`  | Reports targeted Ruff `F` diagnostics for edited Python files without modifying them.                                   | `.codex/hooks/post_tool_use_hygiene.py`  |
| **Codex**       | `Stop`         | Checks memory size limits and taxonomy.                                                                                 | `.codex/hooks/memory_health_check.py`    |
| **Claude Code** | `SessionStart` | Injects `CLAUDE.md`, branch, and worktree context; creates/syncs the `.memories/` skeleton without reading its content. | `.claude/hooks/session_start.py`         |
| **Claude Code** | `PostToolUse`  | Reports Ruff `E722,F601,F602,F634` diagnostics that complement Pyright without modifying files.                         | `.claude/hooks/post_tool_use_hygiene.py` |
| **Antigravity** | `SessionStart` | Initializes SQLite, copies missing worktree memory, and injects the bounded files.                                      | `.agent/hooks/session_start.py`          |
| **Antigravity** | `PostToolUse`  | Runs targeted Ruff, mypy, and file-hygiene checks.                                                                      | `.agent/hooks/post_tool_use_hygiene.py`  |
| **Antigravity** | `Stop`         | Checks bounded-file limits and rejects legacy memory taxonomy.                                                          | `.agent/hooks/stop_memory_check.py`      |

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
              run: uv run ruff check --fix .

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

| Task                    | Command                                         |
| :---------------------- | :---------------------------------------------- |
| View failed run logs    | `gh run view <run-id> --log-failed`             |
| Re-run failed steps     | `gh run rerun <run-id> --failed`                |
| List recent failures    | `gh run list --status failure --limit 10`       |
| Check Dependabot alerts | `gh api repos/{owner}/{repo}/dependabot/alerts` |

Requires `gh` CLI installed and authenticated (`gh auth login`).

### Troubleshooting CI Failures

1. **Reproduce locally first** — run the same commands the workflow runs (`ruff check --fix .`, `mypy .`, `pytest`) before investigating remotely.
2. **Read the full log** — `gh run view <run-id> --log-failed` shows only the failing step output.
3. **Check for environment differences** — Python version, missing env vars, or missing `uv sync` are the most common causes.
4. **Distinguish flaky from real** — if the same test passes locally and fails remotely consistently, it is usually an environment issue, not a flaky test.

## Template Usage

When applying this starter kit to a new project, copy the agent infrastructure that matches your supported tools:

| Path                      | Purpose                                                                                       |
| :------------------------ | :-------------------------------------------------------------------------------------------- |
| `.memories/`              | Git-ignored instantiated memory: bounded files and SQLite store.                              |
| `.agent/`                 | Antigravity rules, skills, and workflows.                                                     |
| `.codex/`                 | Codex instructions, hooks, private command-like skills, and specialist agents.                |
| `.claude/`                | Claude Code settings, hooks, slash commands, subagents, skills, and path-scoped coding rules. |
| `.vscode/`                | Workspace editor defaults that match file hygiene and Python Ruff workflows.                  |
| `scripts/`                | Repository-level hygiene and formatting scripts used by Git and agent adapters.               |
| `.pre-commit-config.yaml` | Repository-level verification hooks.                                                          |

After copying, replace `.memories/memories/MEMORY.md` with the target project's durable facts, review agent-specific rules, install hooks with `uv run pre-commit install`, initialize OpenSpec with `openspec init` when spec-driven planning is desired, treat that project's OpenSpec artifacts as regular project files, and verify with `uv run ruff check --fix .`.

### Agent Workflow Plugin And Skill Integration

This repository integrates native capabilities, project-owned skills, and selected plugins differently per agent:

- **Claude Code**: The project settings intentionally disable the Superpowers, Ponytail, and Karpathy plugins. Native Claude capabilities, project-owned `.claude/` agents, commands, skills, rules, and hooks provide the workflow; GitHub, skill-creator, and Pyright LSP remain enabled.
- **Codex**: Does not depend on Superpowers, Ponytail, or external Karpathy skills. Native Codex capabilities, project-scoped agents and skills provide the workflow; GitHub integration is supplied by the available GitHub plugin when installed.
- **Antigravity**: Uses the existing `.agent/skills/`, `.agent/rules/`, and `.agent/workflows/` content. Its plugin and skill set is not aligned with the Claude Code and Codex plugin layers.

## Design Influences

This starter kit is shaped by two open-source projects:

- **[Everything Claude Code (ECC)](https://github.com/affaan-m/ECC)** — Production-ready agents, skills, hooks, commands, and rules for Claude Code. The specialist agents (`code-reviewer`, `tdd-guide`, `security-reviewer`, etc.), coding rules, and the Prompt Defense Baseline in `CLAUDE.md` are ported or adapted from ECC v2.0.0-rc.1. Most development slash commands have since been retired in favour of native Plan Mode and autoloaded project skills.

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
    uv run ruff check --fix .
    ```
4. **Initialize OpenSpec When Needed**

    Install the OpenSpec CLI in your user environment, then initialize planning state per project or workspace:

    ```bash
    openspec init
    ```

    This starter kit does not commit the `openspec/` directory created by initializing the template repository itself. Downstream projects should treat their own OpenSpec specs, changes, and tasks as regular project files and commit them when those artifacts define project planning or requirements.

5. **Antigravity MCP Setup**

    If you are using Antigravity, note that it requires MCP servers to be configured globally. Please configure your SQLite memory-db MCP server in your home directory (e.g., `~/.mcp.json`).

### Initializing Memory for New Projects

Once the repository is initialized:

1. Ensure `.memories/memories/MEMORY.md` contains the target project's stable mission and constraints.

---

This project enforces UTF-8 without BOM and English for source code, technical documentation, workflows, and configuration. Traditional Chinese content belongs in `docs/zh-TW/` and `.memories/`.
