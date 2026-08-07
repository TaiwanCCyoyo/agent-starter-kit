# Codex Components Reference

Codex uses Native Plan Mode, repo-scoped skills, specialist subagents, project hooks, installed plugins, and a project-scoped memory MCP server. Its `.codex/AGENTS.md` is semantically aligned with the shared policy in `CLAUDE.md` plus `.claude/rules/common/`, while retaining Codex-specific approval and tool constraints.

## Native And Plugin Equivalents

| Capability                                          | Codex implementation                                           |
| :-------------------------------------------------- | :------------------------------------------------------------- |
| Planning                                            | Native Plan Mode and `<proposed_plan>`                         |
| Plan quality review                                 | Read-only `plan_reviewer` agent                                |
| TDD, debugging, worktrees, completion verification  | Native Codex capabilities, project skills, and explicit checks |
| GitHub issues, PRs, CI, review comments, publishing | Installed GitHub plugin                                        |
| Slash commands                                      | Natural-language skill triggers                                |
| Cross-session planning                              | Native planning plus optional project-owned OpenSpec files     |
| Searchable memory                                   | Project-scoped `memory-db` MCP server                          |

Codex keeps planning and implementation authority in the main agent. Read-only agents provide critique, security review, verification feedback, and context-isolated evidence summaries from broad searches, logs, test output, diffs, or commands whose stdout would overwhelm the main context; they do not replace Codex Native Plan Mode or take over commits, pushes, merges, or pull requests without explicit user authorization.

## Agents

| Agent                                  | Access        | Purpose                                                                                                                                                                                         |
| :------------------------------------- | :------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `signal_miner`                         | Read-only     | Lowest-cost mechanical exploration and pre-execution routing for commands expected to produce large logs or stdout; returns concise signal instead of raw output                                |
| `task_worker`                          | Bounded write | Implement explicit low-to-medium-risk tasks with acceptance criteria and verification; stop when scope or risk expands                                                                          |
| `plan_reviewer`                        | Read-only     | Plan completeness, scope, sequencing, repository alignment, testability, and risk                                                                                                               |
| `implementation_reviewer`              | Read-only     | Correctness, regression, test coverage, and unintended-diff review                                                                                                                              |
| `security_reviewer`                    | Read-only     | Secrets, injection, dependencies, permissions, auth, and sensitive data                                                                                                                         |
| `memory_auditor` / `memory_compressor` | Read-only     | Advisory layer for save classification and compression drafts; final writes remain with the main agent and memory skills                                                                        |
| `doc_translator`                       | Bounded write | Low-tier translator and synchronizer for any file-based translation into one explicit non-canonical target; the main agent selects source and target, and its canonical document wins conflicts |
| `commit_specialist`                    | Bounded write | Reviews staged changes and commits only on explicit request                                                                                                                                     |

### Model routing

| Tier                        | Model                        | Roles                                                                            |
| --------------------------- | ---------------------------- | -------------------------------------------------------------------------------- |
| High-confidence review      | `gpt-5.6` / high             | Plan, implementation, and security review                                        |
| Balanced judgment           | `gpt-5.6-terra` / low-medium | Memory compression                                                               |
| Bounded implementation      | `gpt-5.6-terra` / medium     | Routine, explicitly scoped implementation through `task_worker`                  |
| High-volume mechanical work | `gpt-5.6-luna` / medium      | Signal mining, commits, documentation synchronization, and memory classification |

`plan_reviewer` critiques plans and never replaces Native Plan Mode. `signal_miner` is the lowest-cost read-only utility for mechanical exploration and bounded high-output commands. When tests, benchmarks, broad searches, verbose diagnostics, dependency traces, or large diff/log inspections are expected to produce substantial output, delegate before running them in the main context. `task_worker` is a mid-cost option only for a higher-tier main agent to downshift bounded edits with an explicit goal, scope, acceptance criteria, and verification. A lowest-cost main agent handles simple work directly or uses an appropriate native low-cost route; it does not escalate to `task_worker`. Ambiguous, cross-cutting, security-sensitive, architectural, and planning work stays with the main agent or a suitable built-in agent. Security review is expected for authentication, authorization, untrusted input, database, filesystem, external API, cryptography, payment, and sensitive-data changes.

## Skills

| Skill                  | Purpose                                                                                                           |
| :--------------------- | :---------------------------------------------------------------------------------------------------------------- |
| `python-development`   | Python coding, typing, logging, secrets, security routing, Codex hook ownership, and conditional FastAPI guidance |
| `python-testing`       | Exact pytest, optional coverage, Ruff, mypy, hook fixture, and Windows-path requirements                          |
| `gen-commit`           | Commit review, Conventional Commits, post-commit plan update, memory routing, and skill review                    |
| `memory-manager`       | Memory initialization, reading, audits, taxonomy, health checks, and operation routing                            |
| `save-memory`          | Explicit durable writes, classification, bounded-file limits, and deduplication handoff                           |
| `compress-memory`      | Bounded-file cleanup, deduplication, and graduation of lower-frequency knowledge                                  |
| `memory-sql`           | Exclusive SQLite owner for schema discovery, reads, writes, recurring problems, and verified resolutions          |
| `skill-review`         | Manual reusable-pattern quality gate and skill candidate routing                                                  |
| `worktree-memory-sync` | Ignored memory initialization and consolidation across worktrees                                                  |

## Claude Capability Decisions

| Claude capability                                            | Codex decision                       | Reason                                                                                                                                                                                                   |
| :----------------------------------------------------------- | :----------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/plan`                                                      | Native/optional artifact replacement | Conversational planning is provided by native Plan Mode. Durable PRD-based or cross-session planning handoff may use project-owned OpenSpec files when present.                                          |
| `plan-reviewer`                                              | Ported                               | Independent plan critique is useful and does not duplicate plan creation.                                                                                                                                |
| `/feature-dev`                                               | Native replacement                   | Brainstorming, Plan Mode, test-first development, verification, and review already form the workflow.                                                                                                    |
| `/build-fix`                                                 | Native replacement                   | Evidence-driven debugging plus repository verification covers incremental diagnosis and repair.                                                                                                          |
| `/code-review`                                               | Native/plugin replacement            | Local review uses Codex review stance and agents; PR review uses the GitHub plugin.                                                                                                                      |
| `/python-review`                                             | Skill replacement                    | `python-testing` provides repository-supported Ruff, mypy, pytest, and optional coverage commands.                                                                                                       |
| `/security-scan`                                             | Agent and gate replacement           | `security_reviewer`, detect-secrets, hooks, and pre-commit are installed; AgentShield is not.                                                                                                            |
| `/test-coverage`                                             | Skill replacement                    | Optional coverage is part of `python-testing`; Codex does not need a command wrapper.                                                                                                                    |
| `github-ops`                                                 | Plugin replacement                   | The GitHub plugin supplies repository, issue, PR, CI, comment, and publishing workflows with current connector semantics.                                                                                |
| `cost-aware-llm-pipeline`                                    | Not ported                           | It is application-domain guidance with provider-specific model names and volatile pricing, not a Codex workflow. Create a shared, vendor-verified skill when this repository builds an LLM API pipeline. |
| `eval-harness`                                               | Removed/deferred                     | It referenced nonexistent `/eval` commands and lacked a runner, grader implementation, baseline format, Python commands, and CI integration. Restore only after those capabilities exist.                |
| `llm-trading-agent-security`                                 | Not ported                           | It is domain-specific to transaction-signing or wallet-authorized agents. Share it when the repository contains that execution surface.                                                                  |
| `architect`, `code-simplifier`, `loop-operator`, `tdd-guide` | Not mirrored                         | Codex keeps planning and implementation in the main agent and uses project-scoped skills; duplicating write-capable specialists would add overlapping authority.                                         |
| `code-reviewer`, `silent-failure-hunter`, `python-reviewer`  | Consolidated                         | `implementation_reviewer`, `security_reviewer`, Python skills, and systematic debugging cover the useful review dimensions.                                                                              |
| `performance-optimizer`                                      | Main-agent review                    | Require a measured bottleneck before requesting targeted performance analysis.                                                                                                                           |

## Shared Policy Alignment

| Shared behavior                                                   | Codex owner                                               |
| :---------------------------------------------------------------- | :-------------------------------------------------------- |
| Operating contract, prompt defense, scoped changes                | `.codex/AGENTS.md`                                        |
| Research and reuse before implementation                          | `.codex/AGENTS.md` engineering discipline                 |
| Review severity and CRITICAL/HIGH completion policy               | `.codex/AGENTS.md` review and security section            |
| Security triggers and secret handling                             | `.codex/AGENTS.md` plus `security_reviewer`               |
| Risk-based test scope                                             | `.codex/AGENTS.md` verification section                   |
| Python development rules                                          | `python-development`                                      |
| Repository Python verification                                    | `python-testing`                                          |
| Planning, TDD, debugging, review, verification, branch completion | Native Codex, project agents, and repository verification |

Shared development behavior now mirrors the Claude common-rule routing layer: plan through Native Plan Mode or optional project-owned OpenSpec files; test and debug through native workflows, task-specific tests, and project skills; review through `implementation_reviewer` plus targeted specialists; prepare PRs through the GitHub plugin when available; and finish branches through explicit native Git operations within Codex approval rules.

## Plans, Memory, And Commits

- `.references/` is read-only local reference storage for upstream clones and comparison material.
- OpenSpec specs, changes, and tasks are regular project files when present; commit them when they are part of the project record.
- After a commit, update the related OpenSpec change when one exists, then route only durable facts, decisions, lessons, recurring problems, or verified resolutions into memory.
- Reusable corrections and workflows go through `skill-review`; immature ideas may become low-trust `candidate` facts.

## Hooks And Gates

| Layer                                   | Responsibility                                                                        |
| :-------------------------------------- | :------------------------------------------------------------------------------------ |
| `.codex/hooks/session_start.py`         | Initializes `.memories/`, SQLite schema, and bounded session context                  |
| `.codex/hooks/post_tool_use_hygiene.py` | Read-only targeted Ruff `F` diagnostics for edited Python files                       |
| `.codex/hooks/memory_health_check.py`   | Memory limits, taxonomy, and planning-location guidance                               |
| `.pre-commit-config.yaml`               | Formatting, file hygiene, detect-secrets, Ruff including T201, and targeted mypy      |
| `.vscode/settings.json`                 | Final-newline and trailing-whitespace hygiene plus Ruff formatter defaults for Python |

Python verification uses targeted `uv run python -m pytest` commands while developing and pre-commit against changed files before completion. If formatters modify files, the agent inspects the diff and reruns the relevant checks. Coverage is optional through `uv run python -m pytest --cov --cov-report=term-missing`; there is no universal percentage gate.

## Deferred Capabilities

- Automatic transcript capture and transparent recall.
- Persistent asynchronous memory or background skill curation.
- Eval-driven development infrastructure until a real runner, deterministic graders, baselines, repeated-run metrics, and CI integration exist.
- Domain skills for LLM API cost routing or transaction-authorized agents until the repository adopts those application surfaces.
