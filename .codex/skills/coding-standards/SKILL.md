---
name: coding-standards
description: Apply Codex-native engineering standards for scoped implementation, architecture judgment, review readiness, and project conventions.
---

# Coding Standards

Use this skill when a task touches shared behavior, architectural shape, or recurring implementation conventions.

## Core Practice

- Start from the existing codebase shape and use local helpers before adding new abstractions.
- Keep changes scoped to the requested behavior and its direct verification.
- Prefer boring, explicit code over cleverness.
- Add abstractions only when they remove real duplication or clarify a repeated concept.
- Keep generated outputs, config, comments, commit messages, and technical docs in English.

## Architecture Judgment

- Use Codex Plan Mode for large design choices instead of delegating to a standing planner or architect agent.
- Record decisions only when they create durable project constraints.
- Keep agent-specific adapters thin; move shared logic into `scripts/` or normal project modules.
- Treat hooks as fast feedback and pre-commit/CI as repository gates.

## Review Readiness

- Before asking for review, make sure the diff is intentionally scoped.
- Run task-specific verification when behavior changes.
- Use specialist reviewers only for real risk areas: Python, security, performance, or implementation correctness.
