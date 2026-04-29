# Codex Instructions for AI Agent Starter Kit

This file is the Codex-specific instruction layer for this repository. It translates the Gemini CLI configuration into Codex-native behavior.

## Scope

- These instructions apply only to OpenAI Codex.
- Treat `.codex/` as a private Codex support directory.
- Do not assume `.codex/skills` is an official Codex skill discovery location. Use it because this file explicitly points Codex to it.
- Shared project memory remains in `.agents/memory/MEMORY.md`.

## Operating Rules

### Language and Encoding

- Communicate with the user in Traditional Chinese.
- Write project outputs in English: source code, comments, commit messages, configuration, `SKILL.md`, workflow documents, and technical docs.
- Save files as UTF-8 without BOM.
- Root `README.md` must remain English, except for the first-line link to the Traditional Chinese README.
- Traditional Chinese content is allowed only in `.agents/memory/` and `docs/zh-TW/`.

### Memory Protocol

- Before substantial work, read `.agents/memory/MEMORY.md` to align with the project mission and active handoff.
- For any task that modifies files, update `.agents/memory/MEMORY.md` after the task unless the user explicitly says not to.
- Keep memory updates high-signal and concise.
- Use `.codex/skills/memory-maintenance/SKILL.md` for memory initialization, updates, audits, compression, and consolidation.
- If `.agents/memory/MEMORY.md` is missing, run `uv run python .codex/hooks/session_start.py` or initialize it from that script's template.

### Verification

- Do not claim completion without tangible verification.
- For Python changes, run `uv run ruff check .` and relevant script checks.
- For Codex configuration changes, validate TOML, JSON, and required `SKILL.md` frontmatter.
- If verification is skipped, state the exact reason. Documentation-only changes may use a clear exemption.

### Security

- Never print, store, or commit secrets, tokens, passwords, or API keys.
- Keep `.env` and `.env.local` untracked.
- Do not disable secret scanning, pre-commit checks, or file hygiene checks without explicit user authorization.
- Use Codex sandbox approvals for privileged or networked operations. Ask for enablement, not for the user to complete the task manually.

### Editing Discipline

- Use `apply_patch` for manual file edits.
- Do not delete existing features or rules unless the user explicitly requests removal.
- Prefer existing scripts, skills, and workflow patterns over new abstractions.
- Keep changes scoped to the current request.

### Git and Worktrees

- Respect dirty worktrees. Never revert user changes unless explicitly requested.
- Use `.codex/skills/gen-commit/SKILL.md` when generating commits.
- Use `.codex/skills/worktree-manager/SKILL.md` when creating, finishing, or consolidating Git worktrees.

## Codex Private Skills

The Codex-private skills for this repository live under `.codex/skills/`.

Use these files when the task matches their descriptions:

- `.codex/skills/compress-memory/SKILL.md`
- `.codex/skills/gen-commit/SKILL.md`
- `.codex/skills/memory-maintenance/SKILL.md`
- `.codex/skills/save-memory/SKILL.md`
- `.codex/skills/worktree-manager/SKILL.md`

## Codex Command-Like Skills

Codex does not register repository slash commands from files. Use command-like skills instead:

- `/gen-commit` or `gen-commit` triggers `.codex/skills/gen-commit/SKILL.md`.
- `/save-memory` or `save memory` triggers `.codex/skills/save-memory/SKILL.md`.
- `/compress-memory` or `compress memory` triggers `.codex/skills/compress-memory/SKILL.md`.
- `/worktree` or `worktree finish` triggers `.codex/skills/worktree-manager/SKILL.md`.

## Hooks

Codex hooks are configured in `.codex/config.toml` and `.codex/hooks.json`.

- `SessionStart` injects `.codex/AGENTS.md`, project memory, branch, and worktree context through `.codex/hooks/session_start.py`.
- `PostToolUse` for file edits runs Codex hygiene checks.
- `Stop` emits memory maintenance reminders after several Codex response rounds with pending changes, and runs memory size checks.

Project-local hooks require the `.codex/` project layer to be trusted by Codex.
