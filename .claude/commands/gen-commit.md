---
description: Generate or execute a Git commit through the commit-specialist subagent.
---

# Gen Commit

Delegate this task to the `commit-specialist` subagent, which MUST follow `.claude/skills/commit-helper/SKILL.md`.

## Workflow

1. Run `git branch --show-current` before staging or committing anything. `git status --short` does not report the branch and no session hook supplies it, so this is the only step that establishes it. If the checkout is on the default branch, stop and report: `docs/en/git-workflow.md` forbids committing there, and standing commit authorization does not override it.
2. Confirm whether the user wants only a commit message or wants Claude to execute a commit.
3. Do a filename/status-level-only preflight of the staged (or, if nothing is staged, unstaged) scope. Do not inspect staged file contents in the main agent.
4. Stop and ask before delegating if that preflight shows obvious forbidden or suspicious paths. If nothing is staged, ask before staging unless the user explicitly requested autonomous staging.
5. When the user explicitly authorizes commit execution or autonomous staging, identify intended submodule paths. Confirm each submodule has a committed `HEAD`, run `git add -- <submodule-path>` in the superproject, and record its staged gitlink state. Do not stage a submodule without that authorization.
6. Select and state the delegation mode using `commit-helper`'s four Mode Selection situations: `execute supplied message`, `review supplied message`, or `complete rough or missing message`. Do not automatically request diff review when a complete message and clean, well-understood scope make `execute supplied message` sufficient. `review supplied message` requires an explicit concrete concern from the main agent.
7. Delegate one concrete objective with explicit paths, requested output, acceptance criteria, the user's intent, filename-level staged scope, delegation mode, any supplied commit message, and every staged submodule gitlink state to `commit-specialist`.
8. The specialist verifies staged filenames and each handed-off gitlink, follows only the selected mode's diff policy, and must not commit inside a submodule. It runs pre-commit in every mode. It must return a handoff failure for an uncommitted submodule, unexpected gitlink delta, or non-trivial hook failure; the main agent decides the next step.
9. If the user requested only a message, instruct `commit-specialist` to return the message without committing.
10. If the user requested a commit, instruct `commit-specialist` to execute `git commit` and handle only simple hook failures.
11. After `commit-specialist` reports a successful commit, the main agent, not the subagent, runs `commit-helper` SKILL.md's Post-Commit Memory Check itself.
