# Agent Orchestration

## Available Agents

Located in `.claude/agents/`:

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| architect | System design | Architectural decisions |
| tdd-guide | Test-driven development | New features, bug fixes |
| code-reviewer | Code review | After writing code |
| code-simplifier | Simplify and refine code | After implementation |
| python-reviewer | Python-specific review | Python code changes |
| security-reviewer | Read-only security analysis | Auth, input, data, filesystem, network, crypto, payment changes |
| performance-optimizer | Read-only performance analysis | Measured bottlenecks or tooling cost |
| silent-failure-hunter | Swallowed errors, bad fallbacks | Reliability concerns |
| loop-operator | Autonomous loop monitoring | Long-running agent loops |
| repo-explorer | Codebase exploration | Finding files and patterns |
| plan-reviewer | Plan quality critique (read-only) | After Native Plan Mode planning, before approving complex features |
| implementation-reviewer | Read-only code review | Pre-commit correctness check |
| commit-specialist | Commit message drafting | Generating Conventional Commits |
| doc-translator | EN→zh-TW translation | `docs/en/` → `docs/zh-TW/` |
| memory-auditor | Memory audit (read-only) | After meaningful sessions |
| memory-compressor | Memory compression drafts | When bounded files are too large |

## When to Use Agents

- Complex feature or refactor → use **Native Plan Mode**, not an agent
- Code just written → **code-reviewer**
- New feature or bug fix → **tdd-guide**
- Architectural decision → **architect**
- Security-sensitive change → **security-reviewer**

`architect`, reviewers, explorers, and memory analysts are read-only. `code-simplifier`, `tdd-guide`, and `loop-operator` may write only when explicitly delegated a bounded implementation task. `performance-optimizer` and `security-reviewer` report findings but do not edit.

## Parallel Execution

Run independent agents in parallel (single message, multiple Agent tool calls):

```
# GOOD: parallel
Agent 1: security analysis of auth module
Agent 2: performance review of cache layer

# BAD: sequential when not needed
First agent 1, then agent 2
```
