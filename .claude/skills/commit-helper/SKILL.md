---
name: commit-helper
description: Quality standards and delegation rules for Git commits — pre-commit handoff, Conventional Commits format, and post-commit memory checks. Load this BEFORE staging, drafting a commit message, running `git commit`, or delegating to commit-specialist, for ANY commit request (not only when the user types /gen-commit) — triggers on "commit", "commit this", "commit changes", "write a commit message", or any request to record staged work as a commit.
---

# Skill: Commit-Helper

This skill is the source of truth for high-quality commits in this project. All Claude commit generation workflows must refer to this helper.

## Pre-commit Checklist

1. **Scope Verification**: The main agent performs filename-level staged-scope preflight only.
2. **Submodule Handoff**: When commit execution or autonomous staging is explicitly authorized, confirm each intended submodule has a committed `HEAD`, run `git add -- <submodule-path>` in the superproject, and give its staged gitlink state to `commit-specialist`. The specialist verifies it and must not commit inside a submodule.

## Commit Message Standard

1. **Language**: English only for the subject and body.
2. **Format**: `<type>[optional scope]: <description>`
3. **Subject Line**:
    - Use imperative mood, such as `add` instead of `added`.
    - Start with lowercase.
    - Do not end with a period.
    - Keep under 50 characters when practical.
4. **Body**:
    - Use for complex changes to explain why and how.
    - Use a simple bullet list when helpful.
    - Wrap each line at 72 characters.
    - Leave one blank line between subject and body.

## Delegation Modes

The main agent must select one mode based on its confidence in the staged changes. Do not duplicate diff review: if the main agent needs a diff review, delegate it to `commit-specialist` instead of reading the diff itself. State the selected mode and provide the commit message when it is available:

1. **Execute supplied message**: A complete commit message was supplied. Do not inspect the staged diff or revise the message; commit it directly.
2. **Review supplied message**: A complete commit message was supplied and the main agent explicitly requests review. Inspect the staged diff to validate the requested scope, then commit the supplied message unless the main agent asks for revisions.
3. **Complete rough or missing message**: The message is rough or absent. Inspect the staged diff and draft a complete commit message before returning it or committing.

In every execution mode, run the normal commit command. Fix only a simple, directly actionable pre-commit failure, re-stage the affected files, and retry once. For any failure requiring non-trivial investigation, a broader change, or an unclear fix, stop and return the error, attempted fix, affected paths, and the parent-agent decision required.

## Interaction And Summary

- The commit message itself is always in English.
- The summary provided to the user must be in Traditional Chinese (zh-TW).
- The main agent should not inspect staged file contents in this workflow. It confirms intent, checks staged filenames/status for obvious forbidden paths, and delegates one concrete objective with explicit paths, requested output, acceptance criteria, the delegation mode, any supplied commit message, and staged submodule gitlink state to `commit-specialist`.
- For an uncommitted submodule, unexpected gitlink delta, or unresolved hook failure, `commit-specialist` stops and returns the failed step, evidence, and the precise parent-agent decision required.

## Post-Commit Memory Check

This check is the **main agent's** responsibility, run after `commit-specialist` reports a successful commit. The subagent only sees the delegated staged scope, not the full session, so it cannot judge these criteria itself:

1. If a related OpenSpec change exists, update its tasks, verification notes, or specs when the commit changes implementation status. Do not create a change retroactively for a simple commit.
2. Review whether the session produced durable project facts, user preferences, decisions, lessons, environment constraints, recurring problems, or verified resolutions.
3. Route durable knowledge through `/save-memory` or `/memory-maintenance` only when it will help future sessions; do not save commit narration or duplicate the plan.
4. Apply `skill-authoring` (`.claude/rules/common/skill-authoring.md`) to this session's work: if it derived something reusable the repository does not already state for a task class that will recur, propose a new or extended skill to the user before writing it.
