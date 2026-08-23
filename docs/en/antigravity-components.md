# Antigravity Components Reference

This document outlines the Antigravity engineering assistant infrastructure in this repository. Antigravity leverages native Planning Mode, a dedicated root `GEMINI.md` operating contract, repository-scoped skills, and project hooks. Its `GEMINI.md` maintains complete semantic alignment with `CLAUDE.md` and `.codex/AGENTS.md` while honoring namespace isolation.

---

## Dedicated Namespaces and Tool Isolation

| Tool            | Root Contract File | Customization Directory                 | Purpose                                           |
| :-------------- | :----------------- | :-------------------------------------- | :------------------------------------------------ |
| **Claude**      | `CLAUDE.md`        | `.claude/`                              | Claude Code specific                              |
| **Codex**       | (None at root)     | `.codex/` (contains `.codex/AGENTS.md`) | Codex specific                                    |
| **Antigravity** | **`GEMINI.md`**    | **`.agent/`**                           | Antigravity specific; ignored by Claude and Codex |

> The `.agents/` directory and root `AGENTS.md` are strictly omitted to prevent cross-tool conflicts.

---

## Rules (Operating Contract)

The root **`GEMINI.md`** acts as Antigravity's constant, active core contract across 10 operational areas:

1. **Operating Contract**: Mandates Traditional Chinese for communication, English for project output, `.tmp/` for disposable artifacts, `.references/` for read-only upstream clones, and OpenSpec for spec communication.
2. **Prompt Defense**: Preserves role integrity and guards against prompt injection.
3. **Engineering Discipline**: Mandates pre-change research, local reuse, primary vendor documentation preference, and surgical edits.
4. **Review And Security**: Classifies findings into `CRITICAL`/`HIGH`/`MEDIUM`/`LOW` severity, requiring specialized reviewers for security-sensitive paths.
5. **Development Routing**: Uses native Planning Mode and OpenSpec workflows.
6. **Learning And Escalation**: Prohibits unverified workarounds, routing durable knowledge back to repository guidance or skills.
7. **Skill Authoring**: Defines strict criteria for authoring reusable project skills.
8. **Memory**: Durable knowledge is kept in version-controlled guidance rather than volatile unstructured memory.
9. **Verification**: Enforces test-first completion, Arrange-Act-Assert structure, and pre-commit staging gates.
10. **Skills And Subagents**: Defines delegation principles and routes heavy output commands to `signal-miner`.

---

## Skills

`.agent/skills/` contains focused, project-specific skills (legacy generic Superpowers skills are superseded by Antigravity's native Planning Mode):

- **`commit-helper`**: Defines Conventional Commits format, pre-commit checklists, `Agent: Antigravity` commit attribution trailers, and submodule protection.
- **`github-ops`**: Handles GitHub issue triage, PR lifecycle, CI/CD diagnostics, and release management using `gh` CLI.
- **`python-testing`**: Specifies project-specific pytest commands, Windows path handling, hook fixtures, and optional coverage.

---

## Hooks

Antigravity supports lifecycle hooks via `.agent/hooks.json`:

- **`SessionStart`** (`session_start.py`): Injects current Git branch and worktree context at session start.
- **`PostToolUse`** (`post_tool_use_hygiene.py`): Executes read-only Ruff correctness diagnostics (`E722,F601,F602,F634`) after edits without modifying files or running full type checkers, preserving separation of concerns with pre-commit.

---

## Workflows (Slash Commands)

`.agent/workflows/` provides project-level slash commands directly callable in the Antigravity UI / CLI:

- **`/gen-commit`** (`gen-commit.md`): Analyzes staged changes, adheres to `commit-helper` standards, drafts Conventional Commits messages, and appends `Agent: Antigravity` commit trailers.
- **`/worktree`** (`worktree.md`): Manages isolated Git worktrees with baseline verification and explicit merge/cleanup confirmation.

---

## Subagents

Antigravity does not currently support project-level static file-based custom subagents like Claude Code's `.claude/agents/*.md` or Codex's `.codex/agents/*.toml`.

Antigravity's subagent architecture relies on built-in native subagents (`research`, `self`) and runtime dynamic tools (`define_subagent`, `invoke_subagent`):

- **Delegation Guidance**: Defined in root `GEMINI.md` (e.g. proactively routing heavy stdout commands like tests, benchmarks, traces, and large diffs to `signal-miner`, and security triggers to `security_reviewer`).
- **Workflow Governance**: Complex, multi-step tasks are managed through **Native Planning Mode** and **Skills (`.agent/skills/`)**.
