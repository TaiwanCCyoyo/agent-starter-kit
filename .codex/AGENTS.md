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
- Respect dirty worktrees and never revert user changes unless explicitly requested.
- Never print, store, or commit secrets, tokens, passwords, or API keys.

## Engineering Discipline

- Prefer the smallest change that satisfies the verified goal; do not add speculative features, knobs, abstractions, or error handling beyond the request.
- Match the surrounding style and ownership boundaries before introducing new patterns.
- Touch only files and lines related to the task; do not refactor, reformat, rename, or delete adjacent code unless needed for the current request.
- Clean up unused imports, variables, functions, or files created by the current change, but only mention pre-existing unrelated dead code unless asked to remove it.
- For non-trivial implementation work, state a brief goal and verification approach before editing when the path is not obvious.

## Learning And Escalation

- Prefer explicit tradeoffs over hidden assumptions: state what you know, what you are assuming, and what decision or help is needed when the next step depends on user intent or environment ownership.
- Ask for user assistance immediately when credentials, global settings, approvals, environment ownership, external accounts, product decisions, or irreversible tradeoffs are needed. Do not wait for repeated failures before asking.
- If the same blocker, workaround, wrong assumption, or confusion appears twice, surface the pattern to the user and propose whether it should become a memory note, skill update, instruction update, or follow-up task.

## Memory

- Before substantial work, align with the injected `.agents/memory/MEMORY.md`.
- After file-changing tasks, update memory only when the change creates durable project state, decisions, lessons, constraints, or handoff notes.
- Keep memory updates high-signal: durable decisions, lessons, current state, and handoff notes.
- Record durable lessons when repeated blockers, mistaken assumptions, hidden tradeoffs, or user-assistance patterns affect the work, even if the code change itself is small.
- Mark platform-specific progress clearly, such as Codex-only, Gemini pending, or Antigravity pending.
- Use `.codex/skills/memory-maintenance/SKILL.md` for memory initialization, updates, audits, compression, and consolidation.
- When explicitly delegating memory analysis, use `memory_auditor` for save recommendations and `memory_compressor` for compression drafts; the main agent remains responsible for final `.agents/memory/MEMORY.md` edits.

## Verification

- Do not claim completion without verification evidence.
- Rely on configured hooks for baseline hygiene checks; do not manually rerun hook-backed checks only to create evidence.
- Run additional task-specific checks when the change affects behavior, generated output, hooks, skills, documentation links, or user-facing workflows.
- Manually rerun hook-backed checks only when changing hook scripts, validating hook behavior, debugging an uncertain or failed hook, or performing an explicit commit/pre-commit workflow.
- If verification is skipped or hook coverage is insufficient, state the reason and residual risk.

## Skills

- Keep Codex-specific reusable workflows in `.codex/skills/`; workflow-specific instructions belong in each skill's `SKILL.md`, not in this file.
- Revisit the official repo-scoped `.agents/skills` path before adding skills meant to be shared outside Codex.

## Subagents

- Codex project custom agents live in `.codex/agents/*.toml`.
- Read-only subagents: `repo_explorer`, `implementation_reviewer`, `memory_auditor`, and `memory_compressor`.
- Write-capable subagents: `doc_translator` may edit only the explicit target translation file; `commit_specialist` may review staged changes, draft commit messages, and commit only when explicitly requested.
- Translation subagents must not modify the source document unless the user explicitly asks for source edits.
- Subagents may analyze and draft, but they must not directly mutate durable memory unless the main agent explicitly integrates the result.
