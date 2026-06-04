# Claude Code Components Reference

This document lists all agents, commands, skills, hooks, and rules active in the `.claude/` directory.
Intended for Python and SystemVerilog/UVM developers.

**ECC source version**: v2.0.0-rc.1
**Integration date**: 2026-06-02

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
| `/memory-maintenance` | Initialize, update, audit, or consolidate project memory |
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
| `/learn`, `/skill-create`, `/evolve` | Depend on full ECC installation |
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
| `memory-maintenance` | Full procedure for reading, updating, compressing project memory |
| `worktree-manager` | Worktree create/finish/merge with memory consolidation |

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
| `session_start.py` | Session start | Injects `CLAUDE.md` and `.agents/memory/MEMORY.md` into context |
| `post_tool_use_hygiene.py` | After Edit or Write | For `.py`: runs `ruff format`, `ruff check`, `mypy`, warns on `print()`; for `.md/.py/.toml/.json/.yaml/.yml`: runs `file_hygiene.py` |
| `stop_memory_check.py` | Session end | Nudges memory update if significant work was done |

### ECC hook concepts noted but not ported

| Concept | Why noted |
|---|---|
| PostToolUse continuous learning | ECC automatically generates skills from session observations — aligns with our `lessons.md` approach; future inspiration for more structured `stop_memory_check.py` prompts |
| Stop governance capture | ECC logs security events at session end — relevant if project grows to include autonomous trading agents |

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
| `deep-research` skill | ECC port | Configure firecrawl + exa MCP first |
| `marketing-agent` agent | ECC port | Short-form video planning confirmed |
| `uvm-patterns` skill | Custom build | UVM project starts |
| `rules/systemverilog/` | Custom build | UVM project starts |
| CI/CD guidance in README | Docs update | After integration stabilises |
