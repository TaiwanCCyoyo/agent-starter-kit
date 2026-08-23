# Codex Components Reference

Codex uses Native Plan Mode, native local memories, repo-scoped skills, specialist subagents, project hooks, and installed plugins. Its `.codex/AGENTS.md` is semantically aligned with the shared policy in `CLAUDE.md`, while retaining Codex-specific approval and tool constraints.

## Native And Plugin Equivalents

| Capability                                          | Codex implementation                                           |
| :-------------------------------------------------- | :------------------------------------------------------------- |
| Planning                                            | Native Plan Mode and `<proposed_plan>`                         |
| Plan quality review                                 | Read-only `plan_reviewer` agent                                |
| TDD, debugging, worktrees, completion verification  | Native Codex capabilities, project skills, and explicit checks |
| GitHub issues, PRs, CI, review comments, publishing | Installed GitHub plugin                                        |
| Slash commands                                      | Natural-language skill triggers                                |
| Cross-session planning                              | Native planning plus optional project-owned OpenSpec files     |
| Cross-session recall                                | Native Codex local memories, enabled by project configuration  |

Codex keeps planning and implementation authority in the main agent. Read-only agents provide critique, security review, verification feedback, and context-isolated evidence summaries from broad searches, logs, test output, diffs, or commands whose stdout would overwhelm the main context; they do not replace Codex Native Plan Mode or take over commits, pushes, merges, or pull requests without explicit user authorization.

## Agents

| Agent                     | Access        | Purpose                                                                                                                                                                                         |
| :------------------------ | :------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `signal_miner`            | Read-only     | Lowest-cost high-output command utility; when delegation is authorized, returns concise signal instead of raw output                                                                            |
| `task_worker`             | Bounded write | Implement explicit low-to-medium-risk tasks with acceptance criteria and verification; stop when scope or risk expands                                                                          |
| `plan_reviewer`           | Read-only     | Plan completeness, scope, sequencing, repository alignment, testability, and risk                                                                                                               |
| `implementation_reviewer` | Read-only     | Correctness, regression, test coverage, and unintended-diff review                                                                                                                              |
| `security_reviewer`       | Read-only     | Secrets, injection, dependencies, permissions, auth, and sensitive data                                                                                                                         |
| `doc_translator`          | Bounded write | Low-tier translator and synchronizer for any file-based translation into one explicit non-canonical target; the main agent selects source and target, and its canonical document wins conflicts |
| `commit-specialist`       | Bounded write | Reviews staged changes and commits only on explicit request                                                                                                                                     |

### Model routing

| Tier                        | Model                    | Roles                                                           |
| --------------------------- | ------------------------ | --------------------------------------------------------------- |
| High-confidence review      | `gpt-5.6-sol` / high     | Plan and implementation review                                  |
| Security review             | `gpt-5.6-luna` / xhigh   | Security review                                                 |
| Bounded implementation      | `gpt-5.6-terra` / medium | Routine, explicitly scoped implementation through `task_worker` |
| High-volume mechanical work | `gpt-5.6-luna` / medium  | Signal mining, commits, and documentation synchronization       |

`plan_reviewer` critiques plans and never replaces Native Plan Mode. Use `explorer` for ordinary code location. When Antigravity CLI is available, `antigravity-subagent` is the preferred low-cost external route for bounded, read-only research, inspection, concise review, or mechanical analysis: invoke `agy -p --mode plan --sandbox` with explicit scope and acceptance criteria, then review its response. Do not use it for ambiguous, architectural, security-sensitive, or final integration judgment, and stop rather than retry if it reports `RESOURCE_EXHAUSTED` or `Individual quota reached`. When delegation is authorized and tests, benchmarks, broad searches, verbose diagnostics, dependency traces, or large diff/log inspections are expected to produce substantial output, use `signal_miner` before running them in the main context. `task_worker` is a mid-cost option only for a higher-tier main agent to downshift bounded edits with an explicit goal, scope, acceptance criteria, and verification. A lowest-cost main agent handles simple work directly or uses an appropriate native low-cost route; it does not escalate to `task_worker`. Ambiguous, cross-cutting, security-sensitive, architectural, and planning work stays with the main agent or a suitable built-in agent. Security review is expected for authentication, authorization, untrusted input, database, filesystem, external API, cryptography, payment, and sensitive-data changes.

## Skills

| Skill                  | Purpose                                                                                                   |
| :--------------------- | :-------------------------------------------------------------------------------------------------------- |
| `python-development`   | Python coding, logging, secrets, security routing, Codex hook ownership, and conditional FastAPI guidance |
| `python-testing`       | Exact pytest, optional coverage, Ruff, mypy, hook fixture, and Windows-path requirements                  |
| `gen-commit`           | Commit review, Conventional Commits, post-commit plan updates, and durable-guidance checks                |
| `antigravity-subagent` | Low-cost, bounded read-only delegation to Antigravity CLI through headless `agy -p`                       |

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

## Plans, Native Memory, And Commits

- `.references/` is read-only local reference storage for upstream clones and comparison material.
- OpenSpec specs, changes, and tasks are regular project files when present; commit them when they are part of the project record.
- Codex native local memories live under the user's Codex home outside the repository and provide optional recall; required repository rules remain in checked-in guidance.
- After a commit, update a related OpenSpec change when one exists and apply the always-loaded Skill Authoring rules in `.codex/AGENTS.md`.

## Hooks And Gates

| Layer                                   | Responsibility                                                                        |
| :-------------------------------------- | :------------------------------------------------------------------------------------ |
| `.codex/hooks/session_start.py`         | Reports branch/worktree context and injects `.codex/AGENTS.md`                        |
| `.codex/hooks/post_tool_use_hygiene.py` | Read-only targeted Ruff `F` diagnostics for edited Python files                       |
| `.pre-commit-config.yaml`               | Formatting, file hygiene, detect-secrets, Ruff including T201, and targeted mypy      |
| `.vscode/settings.json`                 | Final-newline and trailing-whitespace hygiene plus Ruff formatter defaults for Python |

Python verification uses targeted `uv run python -m pytest` commands while developing and pre-commit against changed files before completion. If formatters modify files, the agent inspects the diff and reruns the relevant checks. Coverage is optional through `uv run python -m pytest --cov --cov-report=term-missing`; there is no universal percentage gate.

## Deferred Capabilities

- Background skill curation beyond native memory extraction and explicit skill authoring.
- Eval-driven development infrastructure until a real runner, deterministic graders, baselines, repeated-run metrics, and CI integration exist.
- Domain skills for LLM API cost routing or transaction-authorized agents until the repository adopts those application surfaces.
