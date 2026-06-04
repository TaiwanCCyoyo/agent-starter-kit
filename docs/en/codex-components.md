# Codex Components Reference

This document describes the Codex-specific layer in this starter kit. Codex does not mirror Claude Code slash commands one-to-one; it uses native planning, repo-scoped skills, specialist reviewer agents, and lightweight hooks.

## Native Planning

Codex planning is handled by the main agent through Plan Mode and `<proposed_plan>` output. This repository intentionally does not define a separate `planner` agent or a Claude-style command layer for Codex.

Use planning when the task needs product intent, architecture tradeoffs, migration shape, or a decision-complete implementation handoff.

## Agents

| Agent | Purpose |
| :--- | :--- |
| `repo_explorer` | Read-only repository orientation and codebase discovery. |
| `implementation_reviewer` | General correctness, regression, test coverage, and unintended-diff review. |
| `python_reviewer` | Python typing, ruff, logging, tests, and maintainability review. |
| `security_reviewer` | Secrets, unsafe commands, injection risks, dependency surfaces, and permission boundaries. |
| `performance_reviewer` | Targeted latency, throughput, memory, algorithmic, and tooling-cost review. |
| `commit_specialist` | Staged-change review, Conventional Commit drafting, and explicit commit execution. |
| `doc_translator` | Bounded translation edits for explicit target documents. |
| `memory_auditor` / `memory_compressor` | Read-only memory maintenance analysis and compression drafts. |

Specialist reviewers are optional analysis tools. They supplement the main Codex agent and do not replace Codex's implementation or planning flow.

## Skills

| Skill | Purpose |
| :--- | :--- |
| `coding-standards` | Codex-native architecture judgment, scoped implementation, and review readiness. |
| `python-testing` | Focused Python test and static-check strategy. |
| `verification-loop` | Concise implement-check-fix workflow without a separate loop operator agent. |
| `gen-commit` | Commit review and Conventional Commit workflow. |
| `memory-maintenance`, `save-memory`, `compress-memory` | Shared memory lifecycle operations. |
| `worktree-manager` | Worktree creation, finish, and memory consolidation workflow. |

## Hooks And Gates

| Layer | Responsibility |
| :--- | :--- |
| `.codex/hooks/session_start.py` | Injects Codex instructions, memory, branch, and worktree context. |
| `.codex/hooks/post_tool_use_hygiene.py` | Fast targeted feedback after edits. Python files are formatted, linted, checked for file hygiene, and warned on `print()` calls. Text/config files run file hygiene only. |
| `.codex/hooks/stop_memory_check.py` | Nudges memory updates and checks memory size after sustained work. |
| `.pre-commit-config.yaml` | Repository-level commit gate for file hygiene, secrets, ruff, no-print Python hygiene, and full-project mypy. |

Shared hygiene logic belongs in `scripts/` so it works from PowerShell, Bash, Git Bash, and CI.

## Design Notes

- No Codex `planner` agent: native Plan Mode owns planning.
- No Codex `loop-operator` agent: iterative verification lives in the `verification-loop` skill.
- No Codex slash-command layer: command-like behavior is represented by skills and natural-language triggers.
- Full-project `mypy .` belongs in pre-commit and CI, not the post-edit hook.
