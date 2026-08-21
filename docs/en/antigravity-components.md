# Antigravity Components Reference

This document outlines the Antigravity engineering assistant infrastructure in this repository. Antigravity does not use a repository-provided cross-session memory store; durable project knowledge belongs in checked-in rules, skills, documentation, and Git history.

## Rules

Rules (`.agent/rules/`) act as constant, active constraints.

- **`WORKSPACE_SCOPE.md`**: Defines boundaries for temporary (`.tmp/`) and read-only (`.references/`) directories, and enforces respect for existing worktrees.
- **`PROMPT_DEFENSE.md`**: Enforces role integrity and prevents prompt injection and setting leaks.
- **`COLLABORATIVE_DEBUGGING.md`**: The 3-Strike resilient try and explicit escalation protocol.
- **`LANGUAGE_RULES.md`**: Enforces Traditional Chinese for communication and English for source files.
- **`PREVENT_FEATURE_DELETION.md`**: Requires surgical editing and prevents arbitrary code removal.
- **`SECURITY_RULES.md`**: Enforces immutable pre-commit secret scanning and environment isolation.
- **`TDD_RULES.md`**: The Test-Driven Development cycle constraint.
- **`VERIFICATION_RULES.md`**: Requires verifiable terminal evidence before claiming a task is done.
- **`REUSE_PRINCIPLES.md`**: Emphasizes leveraging existing patterns over reinventing the wheel.

## Skills

Skills (`.agent/skills/`) provide reusable procedures and architectural patterns.

- **`brainstorming`**: Refines requirements and presents options before implementation planning.
- **`coding-standards`**: Defines baseline conventions for naming, immutability, and readability.
- **`github-ops`**: Covers repository triage, PR reviews, CI/CD checks, and release management.
- **`test-driven-development`**: Requires a failing test before implementation code.
- **`verification-before-completion`**: Requires verification evidence before task closure.
- **`systematic-debugging`**: Provides an evidence-driven debugging workflow.
- **`using-superpowers`**: Routes tasks through relevant skills before acting.
- **`commit-helper`**, **`worktree-manager`**, and related skills: Handle Git hygiene and isolated branches.

## Hooks

Antigravity supports lifecycle hooks through `.agent/hooks.json`.

- **`SessionStart`** (`session_start.py`): Reports the active branch and whether the workspace is a Git worktree.
- **`PostToolUse`** (`post_tool_use_hygiene.py`): Runs targeted Ruff, mypy, and file-hygiene checks after file-modifying tool calls.

## Workflows

Workflows (`.agent/workflows/`) are high-level slash commands or macros.

- **`/gen-commit`**: Generates a high-quality Git commit message.
- **`/worktree`**: Manages isolated Git worktrees with baseline verification and explicit merge or cleanup authorization.

## Note on Subagents

The Antigravity infrastructure relies on the main agent invoking native capabilities and following skills. Custom text-based subagents similar to Claude Code's `.claude/agents/` are not currently supported. Manage complex multi-step delegation through implementation plans and systematic debugging.
