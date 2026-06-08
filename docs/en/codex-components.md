# Codex Components Reference

This document describes the Codex-specific layer. Codex uses native Plan Mode, repo-scoped skills, specialist subagents, project hooks, plugins, and project-scoped MCP servers rather than mirroring Claude Code slash commands.

## Native Equivalents

| Claude/ECC concept | Codex implementation |
| :--- | :--- |
| `/plan` and planner agent | Native Plan Mode and `<proposed_plan>` |
| Loop operator | `verification-loop` skill |
| GitHub operations skill | Installed GitHub plugin |
| Slash commands | Natural-language skill triggers |
| `memory-db` MCP | Project-scoped `.codex/config.toml` server |

## Agents

| Agent | Purpose |
| :--- | :--- |
| `repo_explorer` | Read-only repository orientation and dependency tracing |
| `implementation_reviewer` | Correctness, regression, test coverage, and unintended-diff review |
| `python_reviewer` | Python typing, ruff, logging, tests, and maintainability review |
| `security_reviewer` | Secrets, unsafe commands, injection, dependency, and permission review |
| `performance_reviewer` | Targeted latency, throughput, memory, complexity, and tooling-cost review |
| `commit_specialist` | Staged-change review and explicit commit execution from the repository root |
| `doc_translator` | Bounded translation edits |
| `memory_auditor` / `memory_compressor` | Read-only memory recommendations and compression drafts |

## Skills

| Skill | Purpose |
| :--- | :--- |
| `coding-standards` | Codex-native architecture and scoped implementation judgment |
| `python-testing` | Focused Python regression and static-check strategy |
| `tdd-workflow` | Risk-based RED-GREEN-REFACTOR workflow adapted from ECC |
| `verification-loop` | Concise implement-check-fix workflow |
| `gen-commit` | Commit review and Conventional Commit workflow |
| `memory-manager`, `save-memory`, `compress-memory` | Shared project memory lifecycle |
| `memory-sql` | Holographic-compatible SQLite fact and recurring-problem workflows |
| `skill-review` | ECC-style extraction quality gate and manual Hermes-style curation |
| `worktree-manager` | Worktree lifecycle with memory consolidation |

## Hooks And Gates

| Layer | Responsibility |
| :--- | :--- |
| `.codex/hooks/session_start.py` | Initializes `.memories/`, the SQLite schema, and injects `MEMORY.md` plus `USER.md` |
| `.codex/hooks/post_tool_use_hygiene.py` | Runs targeted formatting, lint, file hygiene, and Python print checks |
| `.codex/hooks/stop_memory_check.py` | Enforces memory limits, strict taxonomy, session-scoped reminders, SQL graduation guidance, and one-time skill review |
| `.pre-commit-config.yaml` | Repository commit gate for hygiene, secrets, ruff, no-print checks, and mypy |

## Searchable Memory MCP

`.codex/config.toml` defines `memory-db` as a project-scoped stdio MCP server:

- Command: `uvx mcp-server-sqlite`
- Database: `.memories/memory_store.db`
- Working directory: repository root through `cwd = ".."`
- Read tools: automatic approval
- Schema and write tools: prompt for approval
- Startup failure: non-fatal (`required = false`)

The current migration is Codex-specific. Claude Code, Gemini CLI, and Antigravity still require separate adapter migrations.

## ECC Adaptation

Ported or adapted:

- Coding, Python testing, TDD, verification, security, performance, and review principles.
- Prompt Defense baseline.
- Functional-test requirement for hook or script changes.
- Session skill-review quality gate.

Replaced by Codex-native capability:

- Planner agent and `/plan` command.
- Loop operator.
- GitHub operations workflow.
- Claude slash-command wrappers.

Not ported:

- ECC observation/instinct pipeline and background learning process.
- Hookify and harness-internal tooling.
- Language/domain workflows not used by this starter kit.

## Hermes Adaptation

Implemented:

- Bounded `MEMORY.md` and `USER.md`.
- Frozen session-start snapshots.
- Hermes-compatible bounded files and frozen session-start snapshots.
- Holographic-compatible SQLite facts, FTS5, entities, trust metadata, recurring problem occurrences, and verified resolutions.
- Manual skill review and lifecycle decisions.

Not implemented:

- Automatic capture of every conversation message.
- Transparent transcript recall.
- Hermes background skill curator.
- A persistent asynchronous memory process.
