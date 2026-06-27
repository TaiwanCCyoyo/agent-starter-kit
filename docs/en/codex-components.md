# Codex Components Reference

Codex uses Native Plan Mode, repo-scoped skills, specialist subagents, project hooks, installed plugins, and a project-scoped memory MCP server. Its `.codex/AGENTS.md` is semantically aligned with the shared policy in `CLAUDE.md` plus `.claude/rules/common/`, while retaining Codex-specific approval and tool constraints.

## Native And Plugin Equivalents

| Capability | Codex implementation |
| :--- | :--- |
| Planning | Native Plan Mode and `<proposed_plan>` |
| Plan quality review | Read-only `plan_reviewer` agent |
| TDD, debugging, worktrees, completion verification | Installed Superpowers plugin |
| GitHub issues, PRs, CI, review comments, publishing | Installed GitHub plugin |
| Slash commands | Natural-language skill triggers |
| Cross-session plans | Git-ignored `.references/plans/*.plan.md` |
| Searchable memory | Project-scoped `memory-db` MCP server |

Codex keeps planning and implementation authority in the main agent. Read-only agents provide critique, security review, verification feedback, and context-isolated evidence summaries from broad searches, logs, test output, diffs, or commands whose stdout would overwhelm the main context; they do not replace Codex Native Plan Mode or take over commits, pushes, merges, or pull requests without explicit user authorization.

## Agents

| Agent | Access | Purpose |
| :--- | :--- | :--- |
| `evidence_gatherer` | Read-only | Locate files, trace execution paths, map dependencies, and run high-output commands while returning concise summaries instead of raw stdout |
| `plan_reviewer` | Read-only | Plan completeness, scope, sequencing, repository alignment, testability, and risk |
| `implementation_reviewer` | Read-only | Correctness, regression, test coverage, and unintended-diff review |
| `python_reviewer` | Read-only | Python runtime, typing, Ruff, tests, logging, and maintainability |
| `security_reviewer` | Read-only | Secrets, injection, dependencies, permissions, auth, and sensitive data |
| `performance_reviewer` | Read-only | Measured latency, memory, complexity, I/O, and tooling cost |
| `memory_auditor` / `memory_compressor` | Read-only | Advisory layer for save classification and compression drafts; final writes remain with the main agent and memory skills |
| `doc_translator` | Bounded write | Edits only the explicit translation target |
| `commit_specialist` | Bounded write | Reviews staged changes and commits only on explicit request |

`plan_reviewer` critiques plans and never replaces Native Plan Mode. Prefer read-only subagents when the useful output is a compact report with file paths, command names, risk notes, and next-step recommendations rather than raw terminal or search output. Use `evidence_gatherer` for mechanical extraction of broad searches, large stdout, logs, diffs, and test output; escalate to a higher-tier reviewer when the task requires judgment over ambiguous output. Security review is expected for authentication, authorization, untrusted input, database, filesystem, external API, cryptography, payment, and sensitive-data changes.

## Skills

| Skill | Purpose |
| :--- | :--- |
| `python-development` | Python coding, typing, logging, secrets, security routing, Codex hook ownership, and conditional FastAPI guidance |
| `python-testing` | Exact pytest, optional coverage, Ruff, mypy, hook fixture, and Windows-path requirements |
| `gen-commit` | Commit review, Conventional Commits, post-commit plan update, memory routing, and skill review |
| `memory-manager` | Memory initialization, reading, audits, taxonomy, health checks, and operation routing |
| `save-memory` | Explicit durable writes, classification, bounded-file limits, and deduplication handoff |
| `compress-memory` | Bounded-file cleanup, deduplication, and graduation of lower-frequency knowledge |
| `memory-sql` | Exclusive SQLite owner for schema discovery, reads, writes, recurring problems, and verified resolutions |
| `skill-review` | Manual reusable-pattern quality gate and skill candidate routing |
| `worktree-memory-sync` | Ignored memory initialization and consolidation across worktrees |
| `plan-artifact` | Durable cross-session/cross-agent plan artifacts — PRD ingestion, pattern grounding, structured `.references/plans/` output. Native planning handles interactive planning; this skill is for persistent structured output. |

## Claude Capability Decisions

| Claude capability | Codex decision | Reason |
| :--- | :--- | :--- |
| `/plan` | Skill + native replacement | Conversational planning is provided by native Plan Mode. Durable artifact output (PRD-based or cross-session) uses the `plan-artifact` skill; no slash command needed. |
| `plan-reviewer` | Ported | Independent plan critique is useful and does not duplicate plan creation. |
| `/feature-dev` | Superpowers/native replacement | Brainstorming, Plan Mode, TDD, verification, and review already form the workflow. |
| `/build-fix` | Superpowers/native replacement | Systematic debugging plus repository verification covers incremental diagnosis and repair. |
| `/code-review` | Native/plugin replacement | Local review uses Codex review stance and agents; PR review uses the GitHub plugin. |
| `/python-review` | Agent replacement | `python_reviewer` uses repository-supported Ruff, mypy, pytest, and optional coverage commands. |
| `/security-scan` | Agent and gate replacement | `security_reviewer`, detect-secrets, hooks, and pre-commit are installed; AgentShield is not. |
| `/test-coverage` | Skill replacement | Optional coverage is part of `python-testing`; Codex does not need a command wrapper. |
| `github-ops` | Plugin replacement | The GitHub plugin supplies repository, issue, PR, CI, comment, and publishing workflows with current connector semantics. |
| `cost-aware-llm-pipeline` | Not ported | It is application-domain guidance with provider-specific model names and volatile pricing, not a Codex workflow. Create a shared, vendor-verified skill when this repository builds an LLM API pipeline. |
| `eval-harness` | Removed/deferred | It referenced nonexistent `/eval` commands and lacked a runner, grader implementation, baseline format, Python commands, and CI integration. Restore only after those capabilities exist. |
| `llm-trading-agent-security` | Not ported | It is domain-specific to transaction-signing or wallet-authorized agents. Share it when the repository contains that execution surface. |
| `architect`, `code-simplifier`, `loop-operator`, `tdd-guide` | Not mirrored | Codex keeps planning and implementation in the main agent and uses Superpowers workflows; duplicating write-capable specialists would add overlapping authority. |
| `code-reviewer`, `silent-failure-hunter` | Consolidated | `implementation_reviewer`, `python_reviewer`, `security_reviewer`, and systematic debugging cover the useful review dimensions. |
| `performance-optimizer` | Read-only equivalent | Codex uses `performance_reviewer` and requires measurement before optimization. |

## Shared Policy Alignment

| Shared behavior | Codex owner |
| :--- | :--- |
| Operating contract, prompt defense, scoped changes | `.codex/AGENTS.md` |
| Research and reuse before implementation | `.codex/AGENTS.md` engineering discipline |
| Review severity and CRITICAL/HIGH completion policy | `.codex/AGENTS.md` review and security section |
| Security triggers and secret handling | `.codex/AGENTS.md` plus `security_reviewer` |
| Risk-based test scope | `.codex/AGENTS.md` verification section |
| Python development rules | `python-development` |
| Repository Python verification | `python-testing` |
| Planning, TDD, debugging, review, verification, branch completion | Native Codex, project agents, and Superpowers phase routing |

Superpowers is active in Codex. It provides workflow guidance but cannot bypass user intent, sandbox approvals, dirty-worktree protections, repository ownership, or explicit authorization for delegation, commits, destructive actions, pushes, merges, and pull requests. GitHub plugin workflows own Codex PR preparation and publishing behavior.

Shared development behavior now mirrors the Claude common-rule routing layer: plan through Native Plan Mode or `plan-artifact`, test and debug through Superpowers, review through `implementation_reviewer` plus targeted specialists, prepare PRs through the GitHub plugin, and finish branches through Superpowers within Codex approval rules.

## Plans, Memory, And Commits

- `.references/plans/` is the only writable exception under the otherwise read-only `.references/` tree.
- Approved cross-session plans record goal, decisions, tasks, verification, update time, status, and related commit. They remain git-ignored and are not durable memory.
- After a commit, update a related plan when one exists, then route only durable facts, decisions, lessons, recurring problems, or verified resolutions into memory.
- Reusable corrections and workflows go through `skill-review`; immature ideas may become low-trust `candidate` facts.

## Hooks And Gates

| Layer | Responsibility |
| :--- | :--- |
| `.codex/hooks/session_start.py` | Initializes `.memories/`, SQLite schema, and bounded session context |
| `.codex/hooks/post_tool_use_hygiene.py` | Targeted formatting, lint, file hygiene, and Ruff-backed Python print blocking |
| `.codex/hooks/stop_memory_check.py` | Memory limits, taxonomy, plan routing, and one-time skill-review reminder |
| `.pre-commit-config.yaml` | File hygiene, detect-secrets, Ruff including T201 print blocking, and full-project mypy |
| `.vscode/settings.json` | Final-newline and trailing-whitespace hygiene plus Ruff formatter defaults for Python |

Python verification uses `uv run python -m pytest`, `uv run ruff check --fix .`, and `uv run mypy .`. Coverage is optional through `uv run python -m pytest --cov --cov-report=term-missing`; there is no universal percentage gate.

## Deferred Capabilities

- Automatic transcript capture and transparent recall.
- Persistent asynchronous memory or background skill curation.
- Eval-driven development infrastructure until a real runner, deterministic graders, baselines, repeated-run metrics, and CI integration exist.
- Domain skills for LLM API cost routing or transaction-authorized agents until the repository adopts those application surfaces.
