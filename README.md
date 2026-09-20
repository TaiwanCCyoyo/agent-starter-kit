[繁體中文](docs/zh-TW/README.md)

# AI Agent Starter Kit

A project template that gives Codex and Claude Code a shared operating contract, matching per-agent tooling, and verification that runs the same way locally and in CI.

Copy it into a new project when you want both agents to find the project's rules, skills, and quality gates without being told where to look.

## The idea: one contract, enforced elsewhere

Both agents read a single root `AGENTS.md`. Claude Code and Codex discover that filename natively, so nothing has to inject it.

`AGENTS.md` is deliberately short. A rule earns a place in it only when no other layer can state or enforce that rule. Everything else lives where it actually takes effect:

| Layer                               | Owns                                                                             |
| :---------------------------------- | :------------------------------------------------------------------------------- |
| `AGENTS.md`                         | Authorization, project conventions, review severity, and memory boundaries       |
| `.pre-commit-config.yaml`           | Encoding, language boundaries, secret scanning, formatting, linting, type checks |
| `.github/workflows/ci.yml`          | The repository-wide gate that merging depends on                                 |
| `.claude/rules/`                    | Path-scoped coding rules, loaded when a matching file is touched                 |
| `.claude/skills/`, `.codex/skills/` | Task-class workflows, loaded by their own `description`                          |
| `.claude/agents/`, `.codex/agents/` | Subagent roles and routing, selected by their own `description`                  |

Two consequences are worth stating outright:

- **`AGENTS.md` names no individual skill or subagent.** Routing belongs in each component's `description`, where retrieval already happens. Listing names in the contract duplicates that and goes stale.
- **`AGENTS.md` states nothing the model already knows.** General engineering craft, reading code before changing it, and not committing secrets are left out, because the model brings the first two and `detect-secrets` enforces the third.

The result is a contract that fits on one screen and changes only when the project's actual constraints change.

## What to copy

| Path                      | Purpose                                                                   |
| :------------------------ | :------------------------------------------------------------------------ |
| `AGENTS.md`               | Shared root operating contract for every agent                            |
| `.pre-commit-config.yaml` | Repository verification hooks                                             |
| `scripts/`                | Shell-neutral hygiene and formatting checks shared by every agent         |
| `.claude/`                | Claude Code settings, hooks, slash commands, subagents, skills, and rules |
| `.codex/`                 | Codex configuration, hooks, command-like skills, and specialist agents    |
| `.github/workflows/`      | CI that runs the same checks the agents run locally                       |
| `docs/en/git-workflow.md` | Git and delivery authorization contract; keep the path, reset the status  |
| `docs/en/pr-setup.md`     | Owner guide for enabling PR delivery in the adopting project              |
| `.vscode/`                | Editor defaults that match the file hygiene and Ruff workflows            |

Take only the agent directories you use. Neither agent needs the other's layer.

## Setting up

```bash
uv sync --group dev
uv run pre-commit install
```

Then verify the checks run:

```bash
uv run pre-commit run --all-files
uv run python -m pytest scripts/tests .codex/hooks/tests .claude/hooks/tests
```

## Adapting it to your project

### 1. Reset delivery authorization

`docs/en/git-workflow.md` records this repository's own delivery status. **Reset its current-state bullet to local-only before using the template elsewhere.** Copying the file grants no publishing authority; see [PR setup](docs/en/pr-setup.md) for enabling it deliberately.

The one rule that never relaxes: agents never commit or push to the default branch. Everything reaches it through a pull request.

### 2. Adjust the CI workflow

`.github/workflows/ci.yml` runs full pre-commit plus the agent hook tests on Windows, because Windows is this template's primary development platform. Change the runner, the Python version, and the test paths to match your project, then make the job a required check on your default branch. Pin any third-party action to a full commit SHA.

Local pre-commit results are not a merge gate. CI is.

### 3. Rewrite the rules that are actually yours

Open `AGENTS.md` and delete what does not apply to your project. Traditional Chinese communication, the `scripts/` shell-neutral requirement, and the Windows path expectation are this template's constraints, not universal ones. Keep the shape — authorization, conventions, review, skills, memory, verification, delegation — and replace the content.

Apply the same test to anything you add: if pre-commit, CI, a path-scoped rule, or a skill description can carry it, put it there instead.

### 4. Consider OpenSpec for durable planning

This template commits no `openspec/` directory and `AGENTS.md` says nothing about it, because planning state belongs to each project rather than to the template. Projects built from this kit have found it worth adding for long-running work: run `openspec init`, then treat the generated specs, changes, and tasks as ordinary project files and commit them as part of the project record. It gives multi-session work a durable trail that outlives any single agent session.

### 5. Set up permissions

Claude Code permissions live in `.claude/settings.json` and take effect without touching global config. The template allows ordinary `git push` and denies the destructive forms: every force, delete, mirror, and prune flag in its bare, trailing-argument, and mid-command spelling, the refspec equivalents (`origin :branch` and a leading `+`), and `.git` removal.

Treat that list as defence in depth, not as the boundary. It matches command text, so a spelling nobody enumerated slips through, and a default-branch ruleset protects only the default branch — task branches stay writable by anything holding the credential. Server-side rules are what actually stop an unauthorized remote update.

Codex ships no repository-local permission rules here; it uses its own approval controls.

## Per-agent references

Start with the reference for the agent you use. You do not need to configure both.

- **[Claude Code Components](docs/en/claude-components.md)** — subagents, slash commands, skills, hooks, and path-scoped rules in `.claude/`.
- **[Codex Components](docs/en/codex-components.md)** — specialist agents, command-like skills, hooks, and model routing in `.codex/`.
- **[Git Workflow Contract](docs/en/git-workflow.md)** — task isolation, delivery authorization, and review and merge boundaries.
- **[PR Review](docs/en/pr-review.md)** — how this repository's own hosted review and merge conditions are configured.

## Hooks

Both agents run one read-only `PostToolUse` hook that reports Ruff diagnostics on edited Python files without modifying them. Neither runs a `SessionStart` hook: the root `AGENTS.md` is discovered natively, and Git context is a command away.

| Agent           | Script                                          | Reports                                                   |
| :-------------- | :---------------------------------------------- | :-------------------------------------------------------- |
| **Claude Code** | `.claude/hooks/claude_post_tool_use_hygiene.py` | Ruff `E722,F601,F602,F634`, complementing the Pyright LSP |
| **Codex**       | `.codex/hooks/codex_post_tool_use_hygiene.py`   | Ruff `F` checks, since Codex has no Python LSP            |

If hooks do not fire, confirm `uv run pre-commit install` has run, that `.codex/config.toml` enables `hooks`, that `.claude/settings.json` declares the `hooks` section, and that the agent trusts the project-local configuration.

## Design influences

- **[Everything Claude Code (ECC)](https://github.com/affaan-m/ECC)** — the specialist agents and coding rules are adapted from ECC v2.0.0-rc.1. Most development slash commands have since been retired in favour of native Plan Mode and autoloaded project skills.

---

This project enforces UTF-8 without BOM and English for source code, technical documentation, workflows, and configuration. Traditional Chinese content belongs in `docs/zh-TW/`, `.references/`, and `.tmp/`.
