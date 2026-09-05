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
| `signal_miner`            | Read-only     | Low-cost utility for substantial output isolation; returns concise evidence when delegation has a concrete benefit                                                                              |
| `task_worker`             | Bounded write | Implement explicit low-to-medium-risk tasks with acceptance criteria and verification; stop when scope or risk expands                                                                          |
| `plan_reviewer`           | Read-only     | Plan completeness, scope, sequencing, repository alignment, testability, and risk                                                                                                               |
| `implementation_reviewer` | Read-only     | Correctness, regression, test coverage, and unintended-diff review                                                                                                                              |
| `security_reviewer`       | Read-only     | Secrets, injection, dependencies, permissions, auth, and sensitive data                                                                                                                         |
| `doc_translator`          | Bounded write | Low-tier translator and synchronizer for any file-based translation into one explicit non-canonical target; the main agent selects source and target, and its canonical document wins conflicts |
| `commit-specialist`       | Bounded write | Optional delegate for mode-dependent staged review, pre-commit and commits; sandbox failures return to the main agent                                                                           |

### Model routing

| Tier                        | Model                    | Roles                                                           |
| --------------------------- | ------------------------ | --------------------------------------------------------------- |
| High-confidence review      | `gpt-5.6-sol` / high     | Plan and implementation review                                  |
| Security review             | `gpt-5.6-sol` / high     | Security review                                                 |
| Bounded implementation      | `gpt-5.6-terra` / medium | Routine, explicitly scoped implementation through `task_worker` |
| High-volume mechanical work | `gpt-5.6-luna` / medium  | Signal mining, commits, and documentation synchronization       |

`plan_reviewer` critiques plans and never replaces Native Plan Mode. Use `explorer` for ordinary code location and `signal_miner` when substantial output isolation saves context. Run short checks locally; avoid same-tier handoffs without a concrete benefit. `task_worker` lets a higher-tier main agent downshift bounded implementation to Terra, while Luna handles mechanical work. Keep ambiguous, architectural, and security-sensitive judgment with the main agent or designated reviewer. Security review applies to changed trust boundaries, permissions, secrets, untrusted input handling, and sensitive data flows; routine file access alone does not require delegation.

The seven roles plus the built-in explorer cover current recurring work. Add a role only for a demonstrated gap. The main model remains user-selected; role model defaults do not establish measured cost savings or quality. Keep the bounded concurrency and depth defaults unless actual workloads justify changing them.

## Skills

| Skill                | Purpose                                                                                                   |
| :------------------- | :-------------------------------------------------------------------------------------------------------- |
| `python-development` | Python coding, logging, secrets, security routing, Codex hook ownership, and conditional FastAPI guidance |
| `python-testing`     | Exact pytest, optional coverage, Ruff, mypy, hook fixture, and Windows-path requirements                  |
| `gen-commit`         | Scoped local commits, optional specialist review and execution, sandbox handoff, and reporting            |

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
- Include applicable OpenSpec status and workflow corrections in the verified commit when possible. Standing authorization permits project-local skills, hooks, rules, and agent configuration improvements without repeated approval: validate, commit locally, and report what changed and why. External actions, global settings, and platform permissions are outside that authorization.
- Native memory writes require an explicit user request under the active storage rules.

## Hooks And Gates

| Layer                                   | Responsibility                                                                        |
| :-------------------------------------- | :------------------------------------------------------------------------------------ |
| `.codex/hooks/session_start.py`         | Reports branch/worktree context and injects `.codex/AGENTS.md`                        |
| `.codex/hooks/post_tool_use_hygiene.py` | Read-only targeted Ruff `F` diagnostics for edited Python files                       |
| `.pre-commit-config.yaml`               | Formatting, file hygiene, detect-secrets, Ruff including T201, and targeted mypy      |
| `.vscode/settings.json`                 | Final-newline and trailing-whitespace hygiene plus Ruff formatter defaults for Python |

Python verification uses targeted `uv run python -m pytest` commands while developing and pre-commit against changed files before completion. If formatters modify files, the agent inspects the diff and reruns the relevant checks. Coverage is optional through `uv run python -m pytest --cov --cov-report=term-missing`; there is no universal percentage gate.

`gen-commit` uses `commit-specialist` for substantial review, rough or missing messages, and explicitly requested independent checks. The main agent may commit small verified agent-owned changes directly with a complete message and no unrelated staged files, using the same verification and normal hooks. If a delegated step fails on a sandbox or cache permission boundary, the specialist returns the exact error without retries or environment changes; the main agent resumes only the blocked step in its authorized context.

Diff inspection is mode-dependent rather than automatic. Missing or rough intent asks the specialist to inspect the staged diff and write the message. A complete message for a clean, well-understood scope skips diff inspection and focuses the specialist on pre-commit and commit execution. A complete message receives an additional diff check only when the main agent explicitly requests it for a concrete concern; the specialist cannot promote itself into that review mode.

## Deferred Capabilities

- Unattended background curation or changes outside the active project; project-local improvements during authorized work use the standing authorization above.
- Eval-driven development infrastructure until a real runner, deterministic graders, baselines, repeated-run metrics, and CI integration exist.
- Domain skills for LLM API cost routing or transaction-authorized agents until the repository adopts those application surfaces.

## Runtime Verification

The edit hook retains only Ruff `F` diagnostics excluding `F401,F841,F842`, limited to Python files named by that event. Full linting and formatting remain in pre-commit; this hook does not auto-fix or expand the lint rule set.

SessionStart retains instruction injection because `.codex/AGENTS.md` is not a root instruction filename in the default discovery chain. It reports checkout metadata without inferring a task from branch names or commit messages. Hooks use the prepared environment with `uv run --no-sync`; set up dependencies before use. PostToolUse runs Ruff once per edit event with `--no-fix` and a timeout, and reports warnings without replacing the original tool result.

Entrypoint tests verify protocol output and real Ruff execution, not dispatch from every desktop tool path. Live matcher coverage must be checked in the target runtime before treating hooks as enforcement. Pre-commit remains the completion gate.

The [official model guidance](https://developers.openai.com/api/docs/guides/latest-model) recommends auditing conflicting skill instructions. The [hook reference](https://learn.chatgpt.com/docs/hooks) documents that `continue: false` replaces the normal PostToolUse result; diagnostic-only feedback here uses `systemMessage`.
