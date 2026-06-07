# Claude Code Components Reference

This document lists all agents, commands, skills, hooks, and rules active in the `.claude/` directory.
Intended for Python and SystemVerilog/UVM developers.

**ECC source**: [affaan-m/ECC](https://github.com/affaan-m/ECC) v2.0.0-rc.1
**ECC integration date**: 2026-06-02
**Memory taxonomy**: [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) Hot/Warm/Cold model

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
| `memory-compressor` | sonnet | Read, Grep, Glob | Draft compression proposals for Hot/Warm memory |
| `repo-explorer` | sonnet | Read, Grep, Glob, Bash | Locate files, trace execution paths, map dependencies |

### Development (ported from ECC v2.0.0-rc.1)

| Agent | Model | Tools | Purpose |
|---|---|---|---|
| `architect` | opus | Read, Grep, Glob | System design, trade-off analysis, ADRs |
| `code-reviewer` | sonnet | Read, Grep, Glob, Bash | General code review across all languages |
| `code-simplifier` | sonnet | Read, Write, Edit, Bash, Grep, Glob | Simplify code structure while preserving behavior |
| `loop-operator` | sonnet | Read, Grep, Glob, Bash, Edit | Monitor and safely intervene in autonomous loops |
| `performance-optimizer` | sonnet | Read, Write, Edit, Bash, Grep, Glob | Identify bottlenecks, optimize algorithms and queries |
| `planner` | opus | Read, Grep, Glob | Create detailed implementation plans; waits for confirmation before coding |
| `python-reviewer` | sonnet | Read, Grep, Glob, Bash | Python-specific review: type hints, security, Pythonic idioms |
| `security-reviewer` | sonnet | Read, Write, Edit, Bash, Grep, Glob | OWASP Top 10, secrets detection, trading security |
| `silent-failure-hunter` | sonnet | Read, Grep, Glob, Bash | Find swallowed exceptions, bad fallbacks, missing error propagation |
| `tdd-guide` | sonnet | Read, Write, Edit, Bash, Grep | Enforce Red-Green-Refactor; target 80%+ coverage |

### Not ported from ECC (with reasons)

| Agent | Reason |
|---|---|
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
| `/compress-memory` | Compress `.agents/memory/` when it grows too large |
| `/gen-commit` | Generate a Conventional Commit message via `commit-specialist` |
| `/learn-eval` | Evaluate session patterns through a holistic quality gate; extract as skills after approval |
| `/memory-maintenance` | Initialize, update, audit, or consolidate project memory |
| `/memory-sql` | Query or write to `.agents/memory/memory.db` (SQLite FTS5) via the memory-db MCP server |
| `/save-memory` | Save lessons, decisions, or handoff notes to `.agents/memory/` |
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
| `/sessions`, `/save-session`, `/resume-session` | Replaced by `.agents/memory/` system |
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
| `memory-sql` | SQLite FTS5 cold memory: schema, session recording, search queries, and layer routing rules |
| `skill-curator` | Session extraction quality gate (holistic verdict), skill lifecycle (active/stale/archived), save-location guidance |
| `worktree-manager` | Worktree create/finish/merge with memory consolidation; dual-mode: Mode A uses built-in `EnterWorktree`/`ExitWorktree`, Mode B uses git worktree with full lifecycle |

### Development (ported from ECC v2.0.0-rc.1)

| Skill | Purpose |
|---|---|
| `coding-standards` | Cross-language baseline: KISS/DRY/YAGNI, naming, error handling |
| `cost-aware-llm-pipeline` | LLM cost control: model routing, budget tracking, prompt caching |
| `eval-harness` | Formal evaluation framework for Claude Code sessions |
| `git-workflow` | Branching strategies, commit conventions, conflict resolution |
| `github-ops` | CI/CD debugging, release management, Dependabot monitoring |
| `llm-trading-agent-security` | Trading agent security: spend limits, circuit breakers, key handling |
| `python-testing` | pytest, fixtures, mocking, parametrization, coverage |
| `tdd-workflow` | Red-Green-Refactor cycle, 80%+ coverage target |
| `verification-loop` | Run → analyze → fix iteration |

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
| `session_start.py` | Session start | Injects `CLAUDE.md` and `.agents/memory/MEMORY.md` into context once (frozen snapshot — system prompt is not re-read mid-session). Copies memory taxonomy into new worktrees. |
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
| **Cold memory search (SQLite FTS5)** | Hermes port | See below |
| `deep-research` skill | ECC port | Configure firecrawl + exa MCP first |
| `marketing-agent` agent | ECC port | Short-form video planning confirmed |
| `uvm-patterns` skill | Custom build | UVM project starts |
| `rules/systemverilog/` | Custom build | UVM project starts |
| CI/CD guidance in README | Docs update | After integration stabilises |

### Cold Memory Search — SQLite FTS5 (Deferred)

**[Hermes](https://github.com/NousResearch/hermes-agent)** stores all session messages in a local SQLite database (`~/.hermes/state.db`) with FTS5 full-text search, enabling ~20ms recall of any past conversation without LLM summarization.

**Why not implemented yet**: Claude Code's Stop hook receives only a session_id event — it does not receive conversation messages directly. Implementing session recording would require:
1. Intercepting every PostToolUse event to capture tool input/output.
2. Writing a persistent SQLite writer at `.agents/memory/sessions.db` (or a user-level path to avoid git exposure).
3. A `/session-search <query>` slash command backed by an FTS5 query.

**What would change when implemented**:
- Cold memory layer gains a searchable session corpus (complements the existing `runs/` markdown approach).
- Stop hook gains a session archival step.
- `/memory-maintenance` audit workflow gains a "search sessions" step.
- A new `session-search` command would be added to the commands table.

**Status: Implemented.** The `memory-db` MCP server (`uvx mcp-server-sqlite`) is configured in `.claude/mcp.json` (launched via `uv run python .claude/scripts/start_memory_mcp.py`). Claude writes to the database explicitly via MCP `write_query` calls — the Stop hook prompts Claude to upsert the session record and archive graduated entries. See `.claude/skills/memory-sql/SKILL.md` for schema and query examples.
