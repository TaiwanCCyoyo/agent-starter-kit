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

## Mode Selection

The main agent must select one mode from what it actually knows and requests. Do not automatically escalate to diff review merely because review could provide extra confidence. Do not duplicate diff review in the main agent; when a mode requires it, delegate it to `commit-specialist`.

1. **Unknown change intent:** Use **complete rough or missing message**. The specialist inspects the staged diff and derives the message.
2. **Approximate change intent:** Use **complete rough or missing message** with the rough intent. The specialist inspects the staged diff, checks the rough intent, and writes the complete message.
3. **Exact intent in a clean, well-understood scope:** Use **execute supplied message**. The specialist must not inspect the staged diff or revise the complete supplied message; it verifies filenames and focuses on pre-commit, bounded ordinary hook recovery, and commit execution.
4. **Exact intent but explicit double-check requested:** Use **review supplied message**. The specialist inspects only the approved staged diff, checks it against the supplied message, and still focuses on pre-commit, bounded ordinary hook recovery, and commit execution. Use this mode only when the main agent explicitly requests the extra review because of a dirty or shared worktree, unexplained state, or another concrete concern. The specialist must not promote itself into this mode merely because additional review might be useful.

In every execution mode, run pre-commit against the approved paths and then run the normal commit command. Fix only a simple, directly actionable pre-commit or commit-hook failure, re-stage only approved files, and retry once. For any failure requiring non-trivial investigation, a broader change, or an unclear fix, stop and return the error, attempted fix, affected paths, and the parent-agent decision required. Never bypass hooks without explicit authorization.

## Interaction And Summary

- The commit message itself is always in English.
- The summary provided to the user must be in Traditional Chinese (zh-TW).
- The main agent should not inspect staged file contents in this workflow. It confirms intent, checks staged filenames/status for obvious forbidden paths, and delegates one concrete objective with explicit paths, requested output, acceptance criteria, the delegation mode, any supplied commit message, and staged submodule gitlink state to `commit-specialist`.
- `commit-specialist` never stages a file on its own initiative. When any target file is not yet staged, the delegation must explicitly list every file to stage by name; omitting this instruction leaves those files uncommitted.
- For an uncommitted submodule, unexpected gitlink delta, or unresolved hook failure, `commit-specialist` stops and returns the failed step, evidence, and the precise parent-agent decision required.

## Post-Commit Memory Check

This check is the **main agent's** responsibility, run after `commit-specialist` reports a successful commit. The subagent only sees the delegated staged scope, not the full session, so it cannot judge these criteria itself:

1. If a related OpenSpec change exists, update its tasks, verification notes, or specs when the commit changes implementation status. Do not create a change retroactively for a simple commit.
2. Review whether the session produced durable project facts, user preferences, decisions, lessons, environment constraints, recurring problems, or verified resolutions.
3. Route durable knowledge through Claude Code's built-in memory (`CLAUDE.md` §Memory) only when it will help future sessions; do not save commit narration or duplicate the plan.
4. Apply `CLAUDE.md` §Skill Authoring to this session's work: if it derived something reusable the repository does not already state for a task class that will recur, propose a new or extended skill to the user before writing it.
