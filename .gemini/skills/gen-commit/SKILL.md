---
name: gen-commit
description: Generate Conventional Git commit messages with dual-mode support (Inspection and Autonomous). Use when staging changes, finalizing a task, or when the user asks for a commit message or automated commit.
---

# Skill: Gen-Commit

This skill automates the generation of high-quality Git commit messages following the Conventional Commits specification, with clear markers for autonomous agent actions.

## 🎯 Purpose
To ensure consistent, professional commit history while maintaining transparency about which commits were autonomously performed by the agent versus those manually reviewed by the user.

## 🛠️ Operational Protocol

### Step 1: Analyze Changes
- Execute `git status` and `git diff --cached` (or `git diff HEAD` if nothing is staged) to analyze exact changes.
- Identify the core intent of the changes (feature, fix, refactor, etc.).

### Step 2: Determine Mode
- **Inspection Mode**: Triggered when the user asks to "generate a commit message", "write a commit", or uses `/gen-commit`.
    - Focus on draft quality and providing a summary for user review.
- **Autonomous Mode**: Triggered when the user explicitly says "just commit it", "you handle the commit", or "go ahead and commit everything".
    - Focus on speed and adding the `Agent-Status` trailer.

### Step 3: Formulate the Message
1. **Language**: **English** only for the commit message.
2. **Format**: `<type>[optional scope]: <description>`
    - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`.
    - Description: Imperative mood, no capitalization of first letter, no trailing period, < 50 chars.
3. **Body (Optional)**: Explain *why* and *what* changed (wrapped at 72 chars).
4. **Agent Footer (Autonomous Mode Only)**:
    - Add a blank line after the body/subject.
    - Append: `Agent-Status: autonomous`

### Step 4: Execution & Feedback
- **In Inspection Mode**:
    - Present the message in a code block.
    - Provide a brief **Traditional Chinese** summary of the changes.
    - Wait for user approval or command: `git commit -m "..."`.
- **In Autonomous Mode**:
    - State clearly that you are committing autonomously.
    - Execute `git commit -m "..."` directly.
    - Confirm success with the user.

## ⚠️ Guidelines
- **No Silent Commits**: Never commit without at least stating you are doing so.
- **English-Only Messages**: Technical metadata (commits) must be in English.
- **Trailer Consistency**: The `Agent-Status: autonomous` trailer is mandatory for all commits executed without manual user review of the message content.

## 🏁 Verification
- Run `git log -n 1` after committing to ensure the format and trailers are correct.
- Ensure the Conventional Commits `type` accurately reflects the change.
