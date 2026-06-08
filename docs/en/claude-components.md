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
| `memory-auditor` | sonnet | Read, Grep, Glob | Recommend memory updates after significant work |
| `memory-compressor` | sonnet | Read, Grep, Glob | Draft compression proposals for automatically loaded and on-demand memory |
| `plan-reviewer` | sonnet | Read, Grep, Glob, Bash | Pre-implementation plan critique: completeness, scope creep, step sequencing, repo alignment, testability |
| `repo-explorer` | sonnet | Read, Grep, Glob, Bash | Locate files, trace execution paths, map dependencies |

### Development (ported from ECC v2.0.0-rc.1)

| Agent | Model | Tools | Purpose |
|---|---|---|---|
| `architect` | opus | Read, Grep, Glob | System design, trade-off analysis, ADRs |
| `code-reviewer` | sonnet | Read, Grep, Glob, Bash | General code review across all languages |
| `code-simplifier` | sonnet | Read, Write, Edit, Bash, Grep, Glob | Simplify code structure while preserving behavior |
| `loop-operator` | sonnet | Read, Grep, Glob, Bash, Edit | Monitor and safely intervene in autonomous loops |
| `performance-optimizer` | sonnet | Read, Write, Edit, Bash, Grep, Glob | Identify bottlenecks, optimize algorithms and queries |
| `python-reviewer` | sonnet | Read, Grep, Glob, Bash | Python-specific review: type hints, security, Pythonic idioms |
| `security-reviewer` | sonnet | Read, Write, Edit, Bash, Grep, Glob | OWASP Top 10, secrets detection, trading security |
| `silent-failure-hunter` | sonnet | Read, Grep, Glob, Bash | Find swallowed exceptions, bad fallbacks, missing error propagation |
| `tdd-guide` | sonnet | Read, Write, Edit, Bash, Grep | Delegatable TDD subagent; follows `superpowers:test-driven-development` workflow; targets 80%+ coverage |

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

### Development (ported from ECC v2.0.0-rc.1)

| Command | Purpose |
|---|---|
| `/build-fix` | Detect build system and incrementally fix build/type errors |
| `/code-review` | Review local diff |
| `/feature-dev` | Structured feature development: understand first, then write |
| `/plan` | Create implementation plan; waits for user confirmation before coding |
| `/python-review` | Invoke `python-reviewer` agent on Python changes |
| `/security-scan` | Run security review across agent, hook, MCP, permission surfaces |
| `/test-coverage` | Analyze coverage gaps and generate missing tests |

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
| `memory-manager` | Full procedure for reading, updating, compressing project memory; includes frozen snapshot model, Hermes-aligned routing rules, and size health criteria |
| `memory-sql` | SQLite FTS5 searchable history: schema, session recording, search queries, and routing rules |
| `skill-curator` | Session extraction quality gate (holistic verdict), skill lifecycle (active/stale/archived), save-location guidance |
| `worktree-memory-sync` | Repository-specific `.memories/` synchronization for worktrees — copy missing items, never overwrite local bounded files or SQLite, merge only durable non-duplicate facts. Worktree lifecycle is provided by Superpowers. |

### Development (ported from ECC v2.0.0-rc.1)

| Skill | Purpose |
|---|---|
| `cost-aware-llm-pipeline` | LLM cost control: model routing, budget tracking, prompt caching |
| `eval-harness` | Formal evaluation framework for Claude Code sessions (EDD, pass@k) |
| `github-ops` | CI/CD debugging, release management, Dependabot monitoring |
| `llm-trading-agent-security` | Trading agent security: spend limits, circuit breakers, key handling |
| `python-testing` | Repository-specific test requirements only: `uv run python -m pytest`, ruff, mypy, hook JSON fixtures, Windows path behavior. General TDD provided by Superpowers. |

### Removed (2026-06-08 cleanup — Superpowers now covers these)

| Skill | Reason |
|---|---|
| `coding-standards` | Superpowers + narrowed `coding-style` rule cover this |
| `tdd-workflow` | Replaced by `superpowers:test-driven-development` |
| `verification-loop` | Replaced by Superpowers TDD/debugging/completion-verification |
| `git-workflow` | 716-line Git textbook; repo commit policy is in the `git-workflow` rule + `commit-helper` skill |

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

---

## Hooks

Hooks are Python scripts executed automatically by the Claude Code harness.

| Hook | Trigger | What it does |
|---|---|---|
| `session_start.py` | Session start | Injects `CLAUDE.md`, `.memories/memories/MEMORY.md`, and `USER.md` into context once (frozen snapshot — system prompt is not re-read mid-session). Copies the approved memory layout into new worktrees. |
| `post_tool_use_hygiene.py` | After Edit or Write | For `.py`: runs `ruff format`, `ruff check`, `mypy`, warns on `print()`; for `.md/.py/.toml/.json/.yaml/.yml`: runs `file_hygiene.py` |
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
| `rules/common/` | All files | ECC v2.0.0-rc.1 | Universal principles: KISS/DRY/YAGNI, naming, error handling, immutability, file size limits |
| `rules/python/` | `**/*.py`, `**/*.pyi` | ECC v2.0.0-rc.1 (modified) | Type annotations on all function signatures; formatter changed from black to **ruff**; logging required (no `print()`) |

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

### Searchable Memory — SQLite FTS5

**What is implemented**: The `memory-db` MCP server is configured at `.mcp.json` and launched directly with `uvx mcp-server-sqlite`, using `${CLAUDE_PROJECT_DIR:-.}` to resolve the database path from any project subdirectory. Claude writes curated entries — graduated lessons, decisions, and session metadata — explicitly via MCP `write_query` calls. The Stop hook prompts Claude to upsert session records and archive graduated entries. See `.claude/skills/memory-sql/SKILL.md` for schema and query examples.

**What remains deferred — automatic transcript search**: [Hermes](https://github.com/NousResearch/hermes-agent) stores all session messages automatically in a local SQLite database with FTS5 full-text search, enabling ~20ms recall of any past conversation without LLM summarization. This project provides curated entries only — automatic capture remains deferred because Claude Code's Stop hook receives only a session_id event, not conversation content. Implementing automatic recording would require:
1. Intercepting every PostToolUse event to capture tool input/output.
2. Writing session records to a dedicated table or database under the git-ignored `.memories/` root.
3. A `/session-search <query>` slash command backed by an FTS5 query.
