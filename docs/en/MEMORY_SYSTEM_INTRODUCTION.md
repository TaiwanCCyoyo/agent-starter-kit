# Memory System Introduction

The memory system keeps long-running agent work aligned across sessions, supported agents, and Git worktrees.

It is designed for project state that should outlive a single chat: project goals, durable decisions, lessons learned, active handoff notes, and unfinished
follow-up work.

## Mental Model

The system has three layers:

1. `.agents/memory/MEMORY.md` is the durable project memory.
2. Agent hooks load, remind, and validate memory-related state at lifecycle boundaries.
3. Agent skills or commands provide controlled workflows for saving, compressing, and consolidating memory.

Memory is intentionally git-ignored by default. It is local project state, not template source code.

## Components

| Component | Purpose |
| :--- | :--- |
| `.agents/memory/MEMORY.md` | Shared long-term project state. |
| SessionStart hooks | Inject project memory, branch context, and worktree context before work starts. |
| Stop/AfterAgent reminders | Nudge agents to update memory after sustained work with pending changes. |
| `save-memory` | Persist completed work, decisions, and handoff notes. |
| `compress-memory` | Summarize historical detail when memory becomes verbose. |
| `memory-maintenance` | Defines how to initialize, audit, update, and consolidate memory. |
| Worktree sync | Copies useful memory context into new worktrees before the first session starts. |

## Agent Integration

### Codex

Codex uses:

- `.codex/hooks/session_start.py` to inject `.codex/AGENTS.md`, branch context, and `.agents/memory/MEMORY.md`.
- `.codex/hooks/stop_memory_check.py` to issue low-noise memory update and compression reminders.
- `.codex/skills/save-memory/SKILL.md`, `.codex/skills/compress-memory/SKILL.md`, and `.codex/skills/memory-maintenance/SKILL.md`.

Codex-specific progress should be recorded as Codex-specific when the matching Gemini or Antigravity behavior has not been updated.

### Gemini CLI

Gemini uses:

- `.gemini/scripts/session_start.py` for startup memory context.
- `.gemini/scripts/memory_nudger.py` for memory update reminders.
- `.gemini/scripts/memory_compressor.py` for memory size checks.
- `.gemini/commands/save-memory.toml`, `.gemini/commands/compress-memory.toml`, and `.gemini/skills/memory-maintenance/SKILL.md`.

Gemini behavior may intentionally lag Codex behavior during Codex-only experiments. Mark that explicitly in memory.

### Antigravity

Antigravity uses `.agent/workflows/` and `.agent/rules/` as its primary instruction and workflow layer.

When Codex or Gemini changes introduce new memory behavior, mirror the concept into Antigravity only after the design is stable.

## Copy Checklist For New Projects

When reusing this starter kit, copy only the agent layers you need.

| Path | Copy When | Customize |
| :--- | :--- | :--- |
| `.agents/memory/` | You want shared memory state. | Replace `MEMORY.md` with the target project mission. |
| `.codex/` | You want Codex support. | Review hooks, skills, and `.codex/AGENTS.md`. |
| `.gemini/` | You want Gemini CLI support. | Review settings, commands, and scripts. |
| `.agent/` | You want Antigravity support. | Review rules, skills, and workflows. |
| `scripts/` | You want repository-level hygiene scripts. | Keep Git-facing baseline scripts and route agent-specific logic through agent adapters. |
| `.pre-commit-config.yaml` | You want repository-level checks. | Install with `uv run pre-commit install`. |

After copying:

1. Define the new project mission in `.agents/memory/MEMORY.md`.
2. Remove unsupported agent layers.
3. Install hooks where needed.
4. Run the repository verification command, usually `uv run ruff check .`.

## Operating Rules

- Save memory after meaningful file-changing work.
- Record durable decisions, lessons learned, and handoff notes.
- Do not store secrets, tokens, API keys, or user-private data.
- Do not store low-value narration such as every command attempted.
- Compress memory when historical detail starts hiding current state.
- Mark platform-specific progress clearly, such as `Codex-only`, `Gemini pending`, or `Antigravity pending`.

## Reminder Behavior

Memory update reminders and compression reminders are separate.

Update reminders should appear only when repository changes are pending for several agent responses and memory has not been updated.

Compression reminders should appear only when memory is large enough to need action, or during explicit memory audit/compression workflows.

The GUI should not show repeated "no compression needed" messages after every response.

## Troubleshooting

If memory is not injected:

- Confirm the agent-specific SessionStart hook is enabled.
- Confirm `.agents/memory/MEMORY.md` exists.
- Confirm the project-local agent configuration layer is trusted.

If reminders are noisy:

- Check whether the Stop or AfterAgent hook prints lean/healthy memory reports.
- Prefer silent state updates unless action is needed.

If worktree memory diverges:

- Consolidate only durable lessons, decisions, and current handoff state.
- Avoid copying stale task narration back to the main workspace.

If encoding looks wrong:

- Confirm files are UTF-8 without BOM.
- Avoid using shell output as proof of file corruption on legacy Windows consoles; validate with the repository file hygiene script.
