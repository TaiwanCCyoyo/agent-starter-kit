# Codex Instructions for AI Agent Starter Kit

This file is the Codex-specific instruction entrypoint for this repository. It is injected by `.codex/hooks/session_start.py`.

## Scope

- These instructions apply only to OpenAI Codex.
- Treat `.codex/` as a private Codex support directory.
- Shared project memory remains in `.agents/memory/MEMORY.md`.
- Root `AGENTS.md` is intentionally absent to avoid polluting non-Codex agents and subagents.

## Operating Contract

- Communicate with the user in Traditional Chinese.
- Write project outputs in English: source code, comments, commit messages, configuration, `SKILL.md`, workflow documents, and technical docs.
- Keep root `README.md` English except for the first-line Traditional Chinese README link.
- Keep Traditional Chinese content only in `.agents/memory/` and `docs/zh-TW/`.
- Use `apply_patch` for manual file edits.
- Respect dirty worktrees and never revert user changes unless explicitly requested.
- Never print, store, or commit secrets, tokens, passwords, or API keys.

## Memory

- Before substantial work, align with the injected `.agents/memory/MEMORY.md`.
- For file-changing tasks, update memory after the task unless the user explicitly says not to.
- Keep memory updates high-signal: durable decisions, lessons, current state, and handoff notes.
- Mark platform-specific progress clearly, such as Codex-only, Gemini pending, or Antigravity pending.
- Use `.codex/skills/memory-maintenance/SKILL.md` for memory initialization, updates, audits, compression, and consolidation.

## Verification

- Do not claim completion without verification evidence.
- Rely on configured hooks for baseline hygiene checks.
- Run additional task-specific checks when the change requires validation beyond hook coverage.
- If verification is skipped or hook coverage is insufficient, state the reason and residual risk.

## Codex Command-Like Skills

Use the Codex-private skills in `.codex/skills/` when the task matches:

- `/gen-commit` or `gen-commit` -> `.codex/skills/gen-commit/SKILL.md`
- `/save-memory` or `save memory` -> `.codex/skills/save-memory/SKILL.md`
- `/compress-memory` or `compress memory` -> `.codex/skills/compress-memory/SKILL.md`
- `/worktree` or `worktree finish` -> `.codex/skills/worktree-manager/SKILL.md`

## Hooks And Rules

- Codex hooks are configured in `.codex/config.toml` and `.codex/hooks.json`.
- `SessionStart` injects this file, project memory, branch, and worktree context.
- `PostToolUse` runs baseline hygiene checks after file edits.
- `Stop` emits low-noise memory update and compression reminders when action may be needed.
- Official Codex `.rules` files control command execution policy, not behavioral instructions.
