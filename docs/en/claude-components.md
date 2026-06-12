# Claude Code Components Reference

This document lists all agents, commands, skills, hooks, and rules active in the `.claude/` directory.
Intended for Python and SystemVerilog/UVM developers.

**ECC source**: [affaan-m/ECC](https://github.com/affaan-m/ECC) v2.0.0-rc.1
**ECC integration date**: 2026-06-02
**Memory design influence**: [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent); this project adapts bounded session context, searchable SQLite history, and a learning review loop

---

## Agents

Agents are specialized subagents invoked by the main Claude session for focused tasks.

### Memory & Workflow (original — not from ECC)

| Agent | Model | Tools | Purpose |
|---|---|---|---|
| `commit-specialist` | sonnet | Bash, Read | Review staged changes and draft commit messages |
| `doc-translator` | sonnet | Read, Write, Edit | Translate `docs/en/` files to `docs/zh-TW/` |
| `implementation-reviewer` | opus | Read, Grep, Glob, Bash | Read-only code review: correctness, style, security |
| `memory-auditor` | haiku | Read, Grep, Glob | Classify save candidates and Do Not Save items; never writes memory |
| `memory-compressor` | sonnet | Read, Grep, Glob | Draft bounded-file compression and graduation proposals; never writes memory |
| `plan-reviewer` | sonnet | Read, Grep, Glob, Bash | Pre-implementation plan critique: completeness, scope creep, step sequencing, repo alignment, testability |
| `repo-explorer` | sonnet | Read, Grep, Glob, Bash | Locate files, trace execution paths, map dependencies |

### Development (ported from ECC v2.0.0-rc.1)

| Agent | Model | Tools | Purpose |
|---|---|---|---|
| `architect` | opus | Read, Grep, Glob | System design, trade-off analysis, ADRs |
| `code-reviewer` | sonnet | Read, Grep, Glob, Bash | General code review across all languages |
| `code-simplifier` | sonnet | Read, Write, Edit, Bash, Grep, Glob | Simplify code structure while preserving behavior |
| `loop-operator` | sonnet | Read, Grep, Glob, Bash, Edit | Monitor and safely intervene in autonomous loops |
| `performance-optimizer` | sonnet | Read, Grep, Glob, Bash | Read-only review of measured bottlenecks, I/O, memory, complexity, and tooling cost |
| `python-reviewer` | sonnet | Read, Grep, Glob, Bash | Python-specific review: type hints, security, Pythonic idioms |
| `security-reviewer` | sonnet | Read, Grep, Glob, Bash | Read-only secrets, injection, dependency, permission, auth, and sensitive-data review |
| `silent-failure-hunter` | sonnet | Read, Grep, Glob, Bash | Find swallowed exceptions, bad fallbacks, missing error propagation |
| `tdd-guide` | sonnet | Read, Write, Edit, Bash, Grep | Delegatable bounded TDD implementation following `superpowers:test-driven-development`; coverage is optional |

### Not ported from ECC (with reasons)

| Agent | Reason |
|---|---|
| `planner` | Removed 2026-06-08 — superseded by Native Plan Mode (`EnterPlanMode`/`ExitPlanMode`) |
| `refactor-cleaner` | Depends on Node.js tools (knip, depcheck, ts-prune); Python project |
| `harness-optimizer` | Requires ECC-internal `/harness-audit`; not portable |
| All `*-build-resolver` (11 agents) | Non-Python languages not in use |
| Language reviewers (non-Python) | Unused languages |
| `gan-*`, `seo-specialist` | Out of scope |
| `homelab-*`, `network-*`, `healthcare-reviewer` | Domain mismatch |
| `marketing-agent` | Deferred — add when short-form video planning starts |

---

## Commands (Slash Commands)

### Memory & Workflow (original — not from ECC)

| Command | Purpose |
|---|---|
| `/compress-memory` | Compress bounded memory when it grows too large |
| `/gen-commit` | Generate a Conventional Commit message via `commit-specialist` |
| `/learn-eval` | Evaluate session patterns through a holistic quality gate; extract as skills after approval |
| `/memory-maintenance` | Initialize, update, audit, or consolidate project memory |
| `/memory-sql` | Query or write to `.memories/memory_store.db` via the memory-db MCP server |
| `/save-memory` | Save durable facts to the appropriate bounded file or SQLite store |
| `/worktree` | Create, manage, and merge Git worktrees with memory preservation |

### Removed (2026-06-10 cleanup — agents, Superpowers, and built-in `/code-review` now cover these)

| Command | Replacement |
|---|---|
| `/build-fix` | Superpowers systematic debugging + `python-testing` skill |
| `/code-review` | Built-in `/code-review` (incl. `ultra` cloud review) + `code-reviewer` / `implementation-reviewer` agents |
| `/feature-dev` | Native Plan Mode + Superpowers TDD + `repo-explorer` agent |
| `/python-review` | `python-reviewer` agent |
| `/security-scan` | `security-reviewer` agent + `detect-secrets` gate |
| `/test-coverage` | `python-testing` skill (`pytest --cov`) |

### Not ported from ECC (with reasons)

| Command | Reason |
|---|---|
| `/pr`, `/review-pr` | PR workflow not needed |
| `/multi-*` (5 commands) | Multi-agent orchestration premature |
| `/learn`, `/skill-create` | Depend on ECC observation hooks and full instinct pipeline; replaced by `/learn-eval` |
| `/evolve` | Replaced by skill-curator lifecycle in `/learn-eval` |
| `/hookify-*` (4 commands) | ECC-internal hook management |
| `/sessions`, `/save-session`, `/resume-session` | Replaced by the `.memories/` system |
| Language-specific build/test/review | Go/Rust/Kotlin/Java etc. not in use |
| `/cost-report`, `/model-route` | Add later if needed |
| `/jira`, `/prp-*`, `/plan-prd` | No PM integration planned |

---

## Skills

Skills are internal workflow documents loaded when a matching command or agent needs them.

### Memory & Workflow (original — not from ECC)

| Skill | Purpose |
|---|---|
| `commit-helper` | Conventional Commits format, pre-commit checklist |
| `memory-manager` | Memory initialization, reading, audits, taxonomy, health checks, and operation routing |
| `save-memory` | Explicit durable writes, classification, bounded-file limits, and deduplication handoff |
| `compress-memory` | Bounded-file cleanup, deduplication, and graduation of lower-frequency knowledge |
| `memory-sql` | Exclusive SQLite owner for schema discovery, reads, writes, recurring problems, and verified resolutions |
| `skill-curator` | Session extraction quality gate (holistic verdict), skill lifecycle (active/stale/archived), save-location guidance |
| `worktree-memory-sync` | Repository-specific `.memories/` synchronization for worktrees — copy missing items, never overwrite local bounded files or SQLite, merge only durable non-duplicate facts. Worktree lifecycle is provided by Superpowers. |
| `plan-artifact` | Durable cross-session/cross-agent plan artifacts — PRD ingestion, pattern grounding, structured `.references/plans/` output. Native Plan Mode handles interactive planning; this skill is for the persistent structured output. |

### Development (ported from ECC v2.0.0-rc.1)

| Skill | Purpose |
|---|---|
| `cost-aware-llm-pipeline` | LLM cost control: model routing, budget tracking, prompt caching |
| `github-ops` | CI/CD debugging, release management, Dependabot monitoring |
| `llm-trading-agent-security` | Trading agent security: spend limits, circuit breakers, key handling |
| `python-testing` | Repository-specific test requirements only: `uv run python -m pytest`, ruff, mypy, hook JSON fixtures, Windows path behavior. General TDD provided by Superpowers. |

### Removed (2026-06-08 cleanup — Superpowers now covers these)

| Skill | Reason |
|---|---|
| `coding-standards` | Superpowers + narrowed `coding-style` rule cover this |
| `tdd-workflow` | Replaced by `superpowers:test-driven-development` |
| `verification-loop` | Replaced by Superpowers TDD/debugging/completion-verification |
| `git-workflow` | 716-line Git textbook; repo commit policy is now solely in the `commit-helper` skill (the `git-workflow` rule was also removed in the 2026-06-13 cleanup) |

### Not ported from ECC (with reasons)

| Skill | Reason |
|---|---|
| `python-patterns` | PEP 8 formatting handled by ruff; idioms covered by `python-reviewer` agent |
| `deep-research` | Requires firecrawl + exa MCP — deferred until MCP configured |
| `api-design`, `backend-patterns` | Stock project is not a web backend |
| `security-review` | Covered by `security-reviewer` agent + `llm-trading-agent-security` |
| Non-Python language patterns | Unused languages |
| `homelab-*`, `network-*`, `healthcare-*` | Domain mismatch |
| `angular-developer`, `react-*`, `nextjs-*` | No frontend planned |
| `eval-harness` | Removed 2026-06-09: referenced nonexistent `/eval` commands and had no runner, graders, baseline format, Python commands, or CI integration. Restore only after those capabilities exist. |

---

## Hooks

Hooks are Python scripts executed automatically by the Claude Code harness.

| Hook | Trigger | What it does |
|---|---|---|
| `session_start.py` | Session start | Injects `CLAUDE.md`, `.memories/memories/MEMORY.md`, and `USER.md` into context once (frozen snapshot — system prompt is not re-read mid-session). Copies the approved memory layout into new worktrees. |
| `post_tool_use_hygiene.py` | After Edit or Write | For `.py`: runs `ruff format`, `ruff check --fix`, `mypy`, warns on `print()`; for `.md/.py/.toml/.json/.yaml/.yml`: runs `file_hygiene.py` |
| `stop_memory_check.py` | After each response | Nudges memory update if significant work was done; prompts skill review via `/learn-eval` after 5+ responses with code changes (once per session) |

### ECC hook concepts noted but not ported

| Concept | Status | Why |
|---|---|---|
| PostToolUse continuous learning | **Partially implemented** | Skill review trigger added to `stop_memory_check.py`; full hook-based observation pipeline (instinct YAML, background Haiku agent) not ported — too heavyweight without a persistent process |
| Stop governance capture | Deferred | ECC logs security events at session end — relevant if project grows to include autonomous trading agents |

---

## Rules

Rules are path-scoped markdown files loaded when Claude works with matching file types.

| Rule set | Paths | Source | Notes |
|---|---|---|---|
| `rules/common/` | All files | ECC v2.0.0-rc.1 (narrowed, 2026-06-13 cleanup) | Routing layer only: security triggers, review severity, reviewer routing, phase routing map, risk-based testing baseline, and coding style heuristics. `git-workflow` and `agents` rules removed; detail lives in `commit-helper`, `github-ops`, `superpowers:finishing-a-development-branch`, and CLAUDE.md `Subagents`. |
| `rules/memory/` | `.memories/**` | Custom | Path-scoped storage safety: ignored-state protection, bounded-file limits, atomic separators, deduplication, frozen snapshots, prohibited content, and SQLite MCP-only access. |
| `rules/python/` | `**/*.py`, `**/*.pyi` | ECC v2.0.0-rc.1 (modified) | Type annotations, Ruff, logging, repository hooks, pytest, and risk-based security review |

### Removed (2026-06-13 cleanup — owned by skills and CLAUDE.md)

| Rule | Reason |
|---|---|
| `rules/common/git-workflow` | Commit format owned by `commit-helper`; PR preparation owned by `github-ops` (full history, `base...HEAD` diff, summary, test plan); push and creation owned by `superpowers:finishing-a-development-branch` |
| `rules/common/agents` | Agent index owned by CLAUDE.md `Subagents`; parallel-execution guidance migrated there |

### Not ported from ECC (with reasons)

| Rule set | Reason |
|---|---|
| `rules/typescript/`, `rules/react/` etc. | Unused languages |
| `rules/cpp/` | SV/UVM differs too much from C++; deferred — create `rules/systemverilog/` when UVM project starts |

---

## Deferred Items

| Item | Type | Condition |
|---|---|---|
| **Automatic transcript capture + FTS5 session search** | Hermes port | Claude Code Stop hook receives only session_id, not conversation content |
| `deep-research` skill | ECC port | Configure firecrawl + exa MCP first |
| `marketing-agent` agent | ECC port | Short-form video planning confirmed |
| `uvm-patterns` skill | Custom build | UVM project starts |
| `rules/systemverilog/` | Custom build | UVM project starts |
| CI/CD guidance in README | Docs update | After integration stabilises |
| Eval-driven development harness | Workflow infrastructure | Add a real runner, deterministic graders, baselines, repeated-run metrics, Python commands, and CI integration |

### Shared Plans

Approved plans that need cross-agent or cross-session visibility live under `.references/plans/{kebab-name}.plan.md`. This is the only writable exception under the otherwise read-only `.references/` tree. Plans remain git-ignored and outside durable memory.

### Searchable Memory — SQLite FTS5

**What is implemented**: The `memory-db` MCP server is configured at `.mcp.json` and launched directly with `uvx mcp-server-sqlite`, using `${CLAUDE_PROJECT_DIR:-.}` to resolve the database path from any project subdirectory. Claude writes curated entries — graduated lessons, decisions, and session metadata — explicitly via MCP `write_query` calls. The Stop hook prompts Claude to upsert session records and archive graduated entries. See `.claude/skills/memory-sql/SKILL.md` for schema and query examples.

**What remains deferred — automatic transcript search**: [Hermes](https://github.com/NousResearch/hermes-agent) stores all session messages automatically in a local SQLite database with FTS5 full-text search, enabling ~20ms recall of any past conversation without LLM summarization. This project provides curated entries only — automatic capture remains deferred because Claude Code's Stop hook receives only a session_id event, not conversation content. Implementing automatic recording would require:
1. Intercepting every PostToolUse event to capture tool input/output.
2. Writing session records to a dedicated table or database under the git-ignored `.memories/` root.
3. A `/session-search <query>` slash command backed by an FTS5 query.
