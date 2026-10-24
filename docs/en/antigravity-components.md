# Antigravity Components Reference

Antigravity uses built-in planning and conversation artifacts, repo-scoped skills in `.agents/skills/`, built-in subagents (`self` and `research`), lifecycle hooks in `.agents/hooks.json`, and terminal sandboxing. It reads the shared root `AGENTS.md`, which Antigravity discovers natively alongside any nested `AGENTS.md` or `GEMINI.md` files.

## Native And Built-in Equivalents

| Capability                                          | Antigravity implementation                                                               |
| :-------------------------------------------------- | :--------------------------------------------------------------------------------------- |
| Planning                                            | Built-in `/plan` and `/grill-me` slash commands plus conversation artifacts              |
| TDD, debugging, worktrees, completion verification  | Native Antigravity capabilities, project skills, and explicit checks                     |
| GitHub issues, PRs, CI, review comments, publishing | Authenticated `gh` CLI (with `permissioned-github` grants when restricted)               |
| Slash commands                                      | `.agents/skills/<name>/SKILL.md` (first-class `/<name>` trigger and semantic discovery)  |
| Cross-session planning                              | Maintained repository plan documents (with conversation artifacts for in-session review) |
| Cross-session recall                                | Antigravity durable memory and global user rules (`~/.gemini/config/`)                   |

Antigravity keeps planning and implementation authority in the main agent. Read-only `research` subagents and bounded `self` subagents provide context-isolated evidence summaries from broad searches, logs, test output, diffs, or repetitive edits; they do not replace main-session architectural judgment or own publication and integration. The main agent follows the [shared Git workflow contract](git-workflow.md).

## Delegation

Use the built-in `self` subagent for bounded implementation or verification work and `research` for read-only codebase or web discovery. This project defines no custom subagent types (`define_subagent` is unnecessary for ordinary work). `AGENTS.md` owns the shared delegation principles; skills retain task-specific workflow details.

`invoke_subagent` exposes `Model` (`"inherit"`, `"flash_lite"`, `"flash"`, `"pro"`) and `Workspace` (`"inherit"`, `"branch"`, `"share"`):

- Prefer `"flash_lite"` or `"flash"` for straightforward work with substantial input, output, noise, or repetitive cycles: long translations, documentation synchronization, large diff/log inspection, and mechanical hook fixes.
- Preserve `"inherit"` (or select `"pro"` when required) for bounded implementation that needs higher judgment, and respect runtime instructions when the user explicitly locks model selection. If only parent-model inheritance is permitted in the active session, report that limit and run directly, or delegate only for a concrete context-isolation or parallelism benefit without claiming model or cost reduction.
- Always pass `Workspace: "inherit"` for repository work so subagents operate inside the parent-assigned checkout; task worktrees are managed explicitly under `.worktrees/<name>/` via `scripts/worktree_inventory.py`, not through unmanaged `branch` or `share` subagent clones.
- Subagents and background tasks wake the parent conversation reactively on completion. Never poll status in a loop or run shell sleep timers.
- Treat terminal sandbox or permission failures (`BypassSandbox: true` required for `.git` writes or network access, `EPERM`, or `permissioned-github` blocks) as immediate execution-boundary handoffs: subagents must stop and return the exact error, attempted step, and affected paths to the parent without retrying or seeking escalated access.

For document translation or synchronization, the main agent selects the authoritative source and explicit target. Preserve structure, links, code, and identifiers; report source conflicts or ambiguous terminology.

## Skills

Antigravity discovers workspace skills under `.agents/skills/<name>/SKILL.md` using progressive disclosure (only `name` and `description` are loaded into context until activated). Legacy `.agents/workflows/*.md` files are deprecated in Antigravity and are not used here.

| Skill                    | Purpose                                                                                                 |
| :----------------------- | :------------------------------------------------------------------------------------------------------ |
| `python-development`     | Python logging and log-driven debugging                                                                 |
| `gen-commit`             | Scoped local commits, built-in delegation for substantial diff reading and hook recovery, and reporting |
| `dependabot-remediation` | Read-only alert retrieval, minimum-safe upgrades, and completion evidence                               |

## Claude Capability Decisions

| Claude capability                                                | Antigravity decision              | Reason                                                                                                                                                               |
| :--------------------------------------------------------------- | :-------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/plan`                                                          | Built-in slash command / artifact | Antigravity provides `/plan`, `/grill-me`, and conversation artifacts for interactive planning; durable cross-session plans live in repository docs.                 |
| `plan-reviewer`, `implementation-reviewer`, `security-reviewer`  | Not mirrored                      | Current model capability, hosted Codex PR review, and pre-commit gates cover them; delegation uses built-in `self` and `research` subagents.                         |
| `/feature-dev`, `/build-fix`, `/python-review`, `/test-coverage` | Native replacement                | Evidence-driven debugging, test-first development, and repository verification cover these workflows without wrapper commands.                                       |
| `/code-review`, `/security-scan`                                 | Native and gate replacement       | Local review follows `AGENTS.md` severity rules; `detect-secrets`, pre-commit, and hosted PR review enforce repository gates.                                        |
| `/worktree`                                                      | Contract replacement              | Worktree lifecycle is governed directly by `docs/en/git-workflow.md` and `scripts/worktree_inventory.py`.                                                            |
| `github-ops`                                                     | Built-in / CLI replacement        | Authenticated `gh` CLI (and Antigravity's built-in `permissioned-github` skill when restricted) plus `dependabot-remediation` cover GitHub and Dependabot workflows. |
| `cost-aware-llm-pipeline`, `llm-trading-agent-security`          | Not ported                        | Domain-specific skills omitted from the meta-tooling starter template until a downstream project adopts those execution surfaces.                                    |
| `eval-harness`                                                   | Deferred                          | Restore only after a real runner, deterministic graders, baselines, and CI integration exist.                                                                        |

## Shared Policy Alignment

| Shared behavior                                                   | Antigravity owner                                                 |
| :---------------------------------------------------------------- | :---------------------------------------------------------------- |
| Operating contract, scoped changes                                | `AGENTS.md`                                                       |
| Project conventions and tool preferences                          | `AGENTS.md` project conventions                                   |
| Review severity and CRITICAL/HIGH completion policy               | `AGENTS.md` review and security section                           |
| Verification scope                                                | `AGENTS.md` verification section                                  |
| Python development rules                                          | `python-development`                                              |
| Scratch files and disposable diagnostics                          | `.tmp/` in the workspace (takes precedence over brain `scratch/`) |
| Planning, TDD, debugging, review, verification, branch completion | Native Antigravity, built-in subagents, and repository gates      |

## Hooks And Gates

| Layer                                                | Responsibility                                                                        |
| :--------------------------------------------------- | :------------------------------------------------------------------------------------ |
| `.agents/hooks/antigravity_post_tool_use_hygiene.py` | Read-only targeted Ruff `F` diagnostics for edited Python files                       |
| `.pre-commit-config.yaml`                            | Formatting, file hygiene, detect-secrets, Ruff including T201, mypy, and pyright      |
| `.vscode/settings.json`                              | Final-newline and trailing-whitespace hygiene plus Ruff formatter defaults for Python |

Local Python verification targets changed behavior. Installed commit hooks and PR CI own automated checks; skills and reviewers do not request a separate manual pass.

## Runtime Verification

Antigravity configures workspace hooks in `.agents/hooks.json`, where top-level keys are hook group names (`python-hygiene`) mapping to lifecycle events (`PostToolUse` with matcher `edit_file|write_file`). Unlike Claude Code, Antigravity's agent tool harness does not attach a Pyright LSP plugin to `edit_file` or `write_file` tool steps, so the hook runs Ruff `F` checks excluding `F401,F841,F842` (`--no-fix --select F --ignore F401,F841,F842 --output-format concise`), matching Codex.

Antigravity runs no `SessionStart`, `PreInvocation`, or `PostInvocation` hook here: root `AGENTS.md` is discovered natively, and avoiding per-invocation hooks prevents spawning Python on read-only turns. Hook commands execute with the working directory set to `.agents/` (via `cmd /c` on Windows and `sh -c` on Unix), so `.agents/hooks.json` invokes `uv run --no-sync --project .. python hooks/antigravity_post_tool_use_hygiene.py` without POSIX-only `$(...)` command substitution.

Per Antigravity's `PostToolUse` protojson contract, the hook reads `workspacePaths` and `toolCall.args.Path` from `stdin`, always emits `{}` on `stdout`, and logs any Ruff diagnostics to `stderr` via Python's `logging` module without modifying files.
