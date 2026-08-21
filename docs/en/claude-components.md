# Claude Code Components Reference

This document lists all agents, commands, skills, hooks, and rules active in the `.claude/` directory.
Intended for Python and SystemVerilog/UVM developers.

**ECC source**: [affaan-m/ECC](https://github.com/affaan-m/ECC) v2.0.0-rc.1
**ECC integration date**: 2026-06-02
**Memory**: Claude uses Claude Code's built-in memory only; required repository guidance remains checked in — see `rules/common/memory.md`.

The project settings intentionally disable the external Superpowers, Ponytail, and Karpathy plugins. This reference describes the repository-owned Claude components plus native Claude capabilities; GitHub, skill-creator, and Pyright LSP remain enabled in `.claude/settings.json`.

---

## Agents

Agents are specialized subagents invoked by the main Claude session for focused tasks.

Claude auto-delegation is primarily guided by each agent's description and the current task context. `signal-miner` is the lowest-cost read-only utility for mechanical exploration and bounded high-output commands. When tests, benchmarks, broad searches, verbose diagnostics, dependency traces, or large diff/log inspections are expected to produce substantial output, delegate before running them in the main context. `task-worker` is a mid-cost option only for a higher-tier main session to downshift bounded implementation with an explicit goal, scope, acceptance criteria, and verification. A lowest-cost main session handles simple work directly or uses built-in Explore or general-purpose as appropriate; it does not escalate to `task-worker`. Keep ambiguous, cross-cutting, security-sensitive, architectural, and planning work with the main session or a suitable built-in agent.

Claude keeps `model: "opusplan"` in `.claude/settings.json`: native Plan Mode uses `opus`, and execution uses `sonnet`. Custom agents are not used to transfer plans back to the main session.

### Workflow (original — not from ECC)

| Agent                     | Model           | Tools                               | Purpose                                                                                                                                                                                           |
| ------------------------- | --------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `commit-specialist`       | haiku           | Bash, Read                          | Review staged changes and draft commit messages                                                                                                                                                   |
| `doc-translator`          | haiku           | Read, Write, Edit                   | Low-tier translator and synchronizer for any file-based translation into one explicit non-canonical target; the main session selects source and target, and its canonical document wins conflicts |
| `implementation-reviewer` | opus            | Read, Grep, Glob, Bash              | Read-only code review: correctness, style, security                                                                                                                                               |
| `plan-reviewer`           | opus (high)     | Read, Grep, Glob, Bash              | Pre-implementation plan critique: completeness, scope creep, step sequencing, repo alignment, testability                                                                                         |
| `signal-miner`            | haiku           | Read, Grep, Glob, Bash              | Lowest-cost mechanical exploration and pre-execution routing for commands expected to produce large logs or stdout; returns concise signal instead of raw output                                  |
| `task-worker`             | sonnet (medium) | Read, Grep, Glob, Write, Edit, Bash | Implement explicit low-to-medium-risk tasks with acceptance criteria and verification; stop when scope or risk expands                                                                            |
| `security-reviewer`       | opus (high)     | Read, Grep, Glob, Bash              | Read-only secrets, injection, dependency, permission, auth, and sensitive-data review                                                                                                             |

### Not ported from ECC (with reasons)

| Agent                                                                                                                                              | Reason                                                                                                                             |
| -------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `planner`                                                                                                                                          | Removed 2026-06-08 — superseded by Native Plan Mode (`EnterPlanMode`/`ExitPlanMode`)                                               |
| `architect`, `code-reviewer`, `code-simplifier`, `loop-operator`, `performance-optimizer`, `python-reviewer`, `silent-failure-hunter`, `tdd-guide` | Removed 2026-07-13 — native Claude capabilities and focused reviewers cover their responsibilities without overlapping delegation. |
| `refactor-cleaner`                                                                                                                                 | Depends on Node.js tools (knip, depcheck, ts-prune); Python project                                                                |
| `harness-optimizer`                                                                                                                                | Requires ECC-internal `/harness-audit`; not portable                                                                               |
| All `*-build-resolver` (11 agents)                                                                                                                 | Non-Python languages not in use                                                                                                    |
| Language reviewers (non-Python)                                                                                                                    | Unused languages                                                                                                                   |
| `gan-*`, `seo-specialist`                                                                                                                          | Out of scope                                                                                                                       |
| `homelab-*`, `network-*`, `healthcare-reviewer`                                                                                                    | Domain mismatch                                                                                                                    |
| `marketing-agent`                                                                                                                                  | Deferred — add when short-form video planning starts                                                                               |

---

## Interactive, Automated, and Company Use

- Interactive work: enter Native Plan Mode, optionally use `plan-reviewer` for complex or high-risk plans, approve the plan, then return to execution mode.
- Unattended work: use separate planning and execution sessions. The planning session writes an OpenSpec or maintained plan artifact; the execution session reads the approved artifact. Do not use a planner subagent as the main-session handoff.
- Claude-only company copy: retain instructions, rules, agents, skills, and hygiene hooks as-is. Use organization-approved model IDs or alias mappings rather than this repository's personal-Pro defaults.

`REVIEW.md` is not part of the local baseline. Add it only when the repository is enrolled in Claude's managed Team or Enterprise Code Review service.

---

## Commands (Slash Commands)

### Workflow (original — not from ECC)

| Command       | Purpose                                                        |
| ------------- | -------------------------------------------------------------- |
| `/gen-commit` | Generate a Conventional Commit message via `commit-specialist` |
| `/worktree`   | Create, verify, manage, merge, and clean up Git worktrees      |

Claude Code PR preparation is owned by the `github-ops` skill: inspect full branch history, compare `base...HEAD`, write the PR summary, and include a fresh test plan. Publishing, pushing, and final branch completion use native Git/GitHub operations and explicit user authorization.

### Removed (2026-06-10 cleanup — agents and built-in `/code-review` now cover these)

| Command          | Replacement                                                                            |
| ---------------- | -------------------------------------------------------------------------------------- |
| `/build-fix`     | Native evidence-driven debugging + `python-testing` skill                              |
| `/code-review`   | Built-in `/code-review` (incl. `ultra` cloud review) + `implementation-reviewer` agent |
| `/feature-dev`   | Native Plan Mode + native test-first workflow + `signal-miner` agent                   |
| `/python-review` | `python-testing` skill and `implementation-reviewer`                                   |
| `/security-scan` | `security-reviewer` agent + `detect-secrets` gate                                      |
| `/test-coverage` | `python-testing` skill (`pytest --cov`)                                                |

### Not ported from ECC (with reasons)

| Command                                         | Reason                                                                                                                            |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `/pr`, `/review-pr`                             | PR workflow not needed                                                                                                            |
| `/multi-*` (5 commands)                         | Multi-agent orchestration premature                                                                                               |
| `/learn`, `/skill-create`                       | Depend on ECC observation hooks and full instinct pipeline; replaced by the `skill-authoring` rule and the `skill-creator` plugin |
| `/evolve`                                       | Replaced by the `skill-authoring` rule and the `skill-creator` plugin                                                             |
| `/hookify-*` (4 commands)                       | ECC-internal hook management                                                                                                      |
| `/sessions`, `/save-session`, `/resume-session` | Replaced by Claude Code's built-in memory and session history                                                                     |
| Language-specific build/test/review             | Go/Rust/Kotlin/Java etc. not in use                                                                                               |
| `/cost-report`, `/model-route`                  | Add later if needed                                                                                                               |
| `/jira`, `/prp-*`, `/plan-prd`                  | No PM integration planned                                                                                                         |

---

## Skills

Skills are internal workflow documents loaded when a matching command or agent needs them.

### Workflow (original — not from ECC)

| Skill           | Purpose                                           |
| --------------- | ------------------------------------------------- |
| `commit-helper` | Conventional Commits format, pre-commit checklist |

### Development (ported from ECC v2.0.0-rc.1)

| Skill            | Purpose                                                                                                                                                                            |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `github-ops`     | CI/CD debugging, release management, Dependabot monitoring                                                                                                                         |
| `python-testing` | Repository-specific test requirements only: `uv run python -m pytest`, ruff, mypy, hook JSON fixtures, Windows path behavior. Test-first decisions use native Claude capabilities. |

### Removed (2026-08-19 cleanup — `/learn-eval` never triggered in practice)

| Skill / Command                | Reason                                                                                                                                                                                                                                                                                                                                                               |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `skill-curator`, `/learn-eval` | The manual port of ECC's holistic verdict gate and Hermes' curator lifecycle went untriggered — the only prompt was a weekly Stop-hook reminder. Replaced by the always-loaded `rules/common/skill-authoring.md` rule stating the durable intent (write a project skill when a task class will recur) plus the already-enabled `skill-creator` plugin for authoring. |

### Removed (2026-08-07 cleanup — dormant-by-design ECC demo skills, no downstream usage)

| Skill                        | Reason                                                                                                                                                                                                                                                                                                                     |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `cost-aware-llm-pipeline`    | This repo never calls an LLM API (meta-tooling only), so the skill only matched by description in a downstream project; it hardcoded a stale model ID (`claude-sonnet-4-6`) and a 2025-2026 price table that would leak into generated code. Re-add from ECC when a project built from this kit actually calls an LLM API. |
| `llm-trading-agent-security` | No trading-agent functionality in this repo. Removing it narrows the `security-review` coverage claim below — restore if trading-agent work begins.                                                                                                                                                                        |

### Removed (2026-06-08 cleanup — native Claude verification now covers these)

| Skill               | Reason                                                                                                                                                    |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `coding-standards`  | Native guidance plus the narrowed `coding-style` rule cover this                                                                                          |
| `tdd-workflow`      | Replaced by the native test-first workflow                                                                                                                |
| `verification-loop` | Replaced by native testing, review, and pre-commit verification                                                                                           |
| `git-workflow`      | 716-line Git textbook; repo commit policy is now solely in the `commit-helper` skill (the `git-workflow` rule was also removed in the 2026-06-13 cleanup) |

### Not ported from ECC (with reasons)

| Skill                                      | Reason                                                                                                                                                                                    |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `python-patterns`                          | PEP 8 formatting handled by ruff; idioms covered by `python-reviewer` agent                                                                                                               |
| `deep-research`                            | Requires firecrawl + exa MCP — deferred until MCP configured                                                                                                                              |
| `api-design`, `backend-patterns`           | Stock project is not a web backend                                                                                                                                                        |
| `security-review`                          | Covered by `security-reviewer` agent; trading-specific patterns (spend limits, circuit breakers) no longer covered since `llm-trading-agent-security` was removed 2026-08-07              |
| Non-Python language patterns               | Unused languages                                                                                                                                                                          |
| `homelab-*`, `network-*`, `healthcare-*`   | Domain mismatch                                                                                                                                                                           |
| `angular-developer`, `react-*`, `nextjs-*` | No frontend planned                                                                                                                                                                       |
| `eval-harness`                             | Removed 2026-06-09: referenced nonexistent `/eval` commands and had no runner, graders, baseline format, Python commands, or CI integration. Restore only after those capabilities exist. |

---

## Hooks

Hooks are Python scripts executed automatically by the Claude Code harness.

| Hook                       | Trigger                 | What it does                                                                                                       |
| -------------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `session_start.py`         | Session start           | Injects git branch, worktree, goal-alignment, and last-commit context once.                                        |
| `post_tool_use_hygiene.py` | After Python Edit/Write | Runs read-only Ruff `E722,F601,F602,F634` diagnostics that complement Pyright; it does not format or modify files. |

Workspace editor defaults live in `.vscode/settings.json`: trim trailing whitespace, keep one final newline, use Ruff for Python formatting and explicit code actions, and exclude generated caches plus local agent state from search, watchers, and local history.

Claude Code uses the official Pyright plugin for immediate type-aware navigation and diagnostics. Its PostToolUse hook adds a read-only targeted Ruff check for `E722,F601,F602,F634`, which complements Pyright without repeating its common undefined-name and unused-symbol diagnostics. Complete Ruff linting and formatting are deferred to pre-commit, so normal edits do not trigger repository-wide formatting. Before completion, the agent runs pre-commit against changed files, and pre-commit owns formatting and validation.

### ECC hook concepts noted but not ported

| Concept                         | Status              | Why                                                                                                                                      |
| ------------------------------- | ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| PostToolUse continuous learning | **Not implemented** | The hook-based observation pipeline (instinct YAML, background Haiku agent) is not ported — too heavyweight without a persistent process |
| Stop governance capture         | Deferred            | ECC logs security events at session end — relevant if project grows to include autonomous trading agents                                 |

---

## Rules

Rules are path-scoped markdown files loaded when Claude works with matching file types.

| Rule set        | Paths                 | Source                                         | Notes                                                                                                                                                                                                                                                                                                                                                                   |
| --------------- | --------------------- | ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `rules/common/` | All files             | ECC v2.0.0-rc.1 (narrowed, 2026-08-07 cleanup) | Routing layer only: security triggers, review severity, reviewer routing, structural review heuristics, phase routing map, skill authoring, memory routing, and the risk-based testing baseline. `git-workflow`, `agents`, and `coding-style` rules removed; detail lives in `commit-helper`, `github-ops`, native Git operations, CLAUDE.md, and the applicable skill. |
| `rules/python/` | `**/*.py`, `**/*.pyi` | ECC v2.0.0-rc.1 (modified)                     | Type annotations, Ruff, logging, repository hooks, pytest, and risk-based security review                                                                                                                                                                                                                                                                               |

The common rules intentionally stay small and carry only decisions a model cannot derive on its own. Security triggers are centralized in `rules/common/security.md`, severity handling and review heuristics in `rules/common/code-review.md`, and phase ownership in `rules/common/development-workflow.md`; detailed procedures live in skills or agent definitions.

### Removed (2026-06-13 cleanup — owned by skills and CLAUDE.md)

| Rule                        | Reason                                                                                                                                                                                                              |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `rules/common/git-workflow` | Commit format owned by `commit-helper`; PR preparation owned by `github-ops` (full history, `base...HEAD` diff, summary, test plan); push and creation use native Git/GitHub operations with explicit authorization |
| `rules/common/agents`       | Agent index owned by CLAUDE.md `Subagents`; parallel-execution guidance migrated there                                                                                                                              |

### Removed (2026-08-07 cleanup — model priors and CLAUDE.md already cover these)

Because every `rules/common/` file matches `paths: "*"`, the set is injected on the first file access of any session, so its content competes with CLAUDE.md rather than deferring cost. Generic craft guidance was dropped and only non-derivable routing decisions were kept.

| Rule                                      | Reason                                                                                                                                       |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `rules/common/coding-style`               | Generic craft guidance duplicated CLAUDE.md `Engineering Discipline`; the structural review heuristic moved to `rules/common/code-review.md` |
| `development-workflow` §Research & Reuse  | Verbatim duplicate of CLAUDE.md `Engineering Discipline`                                                                                     |
| `development-workflow` §Pre-Review Checks | Generic pre-merge hygiene; CI and `github-ops` own it                                                                                        |
| `testing` §AAA and §Test Naming           | Generic pytest structure and naming examples; owned by `skill: python-testing`                                                               |
| `code-review` §Security Review Triggers   | Pointer-only section; the reviewer routing list already links `security.md`                                                                  |

### Not ported from ECC (with reasons)

| Rule set                                 | Reason                                                                                             |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `rules/typescript/`, `rules/react/` etc. | Unused languages                                                                                   |
| `rules/cpp/`                             | SV/UVM differs too much from C++; deferred — create `rules/systemverilog/` when UVM project starts |

---

## Deferred Items

| Item                            | Type                    | Condition                                                                                                      |
| ------------------------------- | ----------------------- | -------------------------------------------------------------------------------------------------------------- |
| `deep-research` skill           | ECC port                | Configure firecrawl + exa MCP first                                                                            |
| `marketing-agent` agent         | ECC port                | Short-form video planning confirmed                                                                            |
| `uvm-patterns` skill            | Custom build            | UVM project starts                                                                                             |
| `rules/systemverilog/`          | Custom build            | UVM project starts                                                                                             |
| Eval-driven development harness | Workflow infrastructure | Add a real runner, deterministic graders, baselines, repeated-run metrics, Python commands, and CI integration |

### OpenSpec Planning Handoff

OpenSpec is optional project state, not starter-kit committed content. Its specs, changes, and tasks are regular project files when present; commit them when they are part of the project record. Plans remain outside durable memory.
