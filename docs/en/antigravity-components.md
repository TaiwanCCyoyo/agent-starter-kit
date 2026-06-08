# Antigravity Components Reference

This document outlines the components of the Antigravity engineering assistant infrastructure within this repository.

## Rules

Rules (`.agent/rules/`) act as constant, active constraints.

- **`WORKSPACE_SCOPE.md`**: Defines boundaries for temporary (`.tmp/`) and read-only (`.references/`) directories, and enforces respect for existing worktrees.
- **`PROMPT_DEFENSE.md`**: Enforces role integrity and prevents prompt injection and setting leaks.
- **`MEMORY_RULES.md`**: Defines the shared `.memories/` architecture, separating hot memory (`MEMORY.md`), user preferences (`USER.md`), and the persistent SQLite database (`memory_store.db`).
- **`COLLABORATIVE_DEBUGGING.md`**: The 3-Strike resilient try and explicit escalation protocol.
- **`LANGUAGE_RULES.md`**: Enforces Traditional Chinese for communication and English for source files.
- **`PREVENT_FEATURE_DELETION.md`**: Requires surgical editing and prevents arbitrary code removal.
- **`SECURITY_RULES.md`**: Enforces immutable pre-commit secret scanning and environment isolation.
- **`TDD_RULES.md`**: The Test-Driven Development cycle constraint.
- **`VERIFICATION_RULES.md`**: Requires verifiable terminal evidence before claiming a task is done.
- **`REUSE_PRINCIPLES.md`**: Emphasizes leveraging existing patterns over reinventing the wheel.

## Skills

Skills (`.agent/skills/`) are invoked to provide robust procedures and specific architectural patterns.

- **`brainstorming`**: For refining requirements and presenting options before creating implementation plans.
- **`coding-standards`**: Baseline cross-project conventions for naming, immutability, and readability.
- **`github-ops`**: Operations for triage, PR reviews, CI/CD checking, and release management.
- **`memory-manager`**: Manages `.memories/memories/MEMORY.md`, `USER.md`, and SQLite facts.
- **`memory-sql`**: Query and store facts into `memory_store.db` via the MCP server.
- **`test-driven-development`**: A rigid workflow requiring a failing test before implementation code.
- **`verification-before-completion`**: A checklist to force manual verification output before task closure.
- **`systematic-debugging`**: A scientific method approach to squashing bugs.
- **`using-superpowers`**: Enforces the invocation of skills prior to acting.
- **`commit-helper`**, **`worktree-manager`**, etc.: Tools for handling Git hygiene and isolated branches.

## Hooks

Antigravity 2.0 supports lifecycle hooks via `.agent/hooks.json`.

- **`SessionStart`** (`session_start.py`): Initializes the bounded files and SQLite schema, copies missing worktree memory, and injects memory context.
- **`PostToolUse`** (`post_tool_use_hygiene.py`): Runs targeted Ruff, mypy, and file-hygiene checks after file-modifying tool calls.
- **`Stop`** (`stop_memory_check.py`): Verifies bounded-file limits and the strict memory taxonomy.

## Workflows

Workflows (`.agent/workflows/`) are high-level user slash commands or macros for administrative tasks.

- **`/compress-memory`**: Proactively compresses project memory.
- **`/consolidate-memory`**: Merges memory from multiple branches/worktrees.
- **`/gen-commit`**: Generates a high-quality Git commit message.
- **`/save-memory`**: Commits project facts into the local SQLite store.
- **`/worktree`**: Manages isolated Git worktrees.

## Note on Subagents

Currently, the Antigravity infrastructure in this repository relies on the main agent invoking native capabilities (such as the `browser_subagent` tool) and following skills. **Custom text-based subagents (similar to those in Claude Code's `.claude/agents/`) are not currently supported.** Any complex multi-step delegation should be managed via implementation plans and systematic debugging.
