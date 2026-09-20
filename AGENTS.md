## Operating Contract

- Communicate with the user in Traditional Chinese; write repository content and commit messages in English. Traditional Chinese belongs only in the `docs/zh-TW/` mirrors, `.references/`, and `.tmp/`.
- After completing and verifying a task, commit only that task's agent-owned changes without asking; leave unrelated work unstaged.
- Standing authorization: improve this project's skills, hooks, rules, and agent configuration when there is a concrete reusable benefit; verify, commit locally, and report afterwards. This does not extend to remote delivery, reviewer roles, merge authority, other projects, or global settings.
- Continue authorized work under reasonable assumptions for reversible choices; ask only for decisions that materially affect scope, correctness, or authorization.
- Follow `docs/en/git-workflow.md` for worktree isolation, delivery authorization, and review and merge boundaries. PR delivery is enabled for this repository using the owner's own GitHub credentials; merging stays with the owner.
- Own authorized PR delivery through CI, review fixes, and resolution of addressed threads under `docs/en/git-workflow.md#pr-follow-through`; opening the PR is not completion.
- Treat `.references/` as ignored read-only clones of upstream projects.
- Use `.tmp/` for scratch files, diagnostics, and disposable reports instead of the OS temporary directory; preserve files you did not create.

## Project Conventions

- Windows is the primary development platform: check path handling, and reject tests that assume POSIX-only paths or shells.
- Keep shared hook and hygiene logic shell-neutral: put cross-agent checks in Python scripts under `scripts/` rather than Bash, PowerShell, or agent-specific command fragments.
- Prefer the GitHub plugin for repository, issue, PR, CI, and review workflows; fall back to authenticated `gh` when the plugin is unavailable or lacks the operation. Local Git work requires no plugin.

## Review And Security

These rules govern requested local reviews and hosted pull request reviews. See [PR review](docs/en/pr-review.md) for how PR review is triggered and what it may do.

- Classify every finding as `CRITICAL`, `HIGH`, `MEDIUM`, or `LOW`: block `CRITICAL` security or data-loss risks and `HIGH` likely bugs or significant regressions unless the user accepts the risk; report `MEDIUM` and `LOW` as informational.
- Flag any secret, token, password, or API key in a diff as `CRITICAL`.
- File length, function length, parameter count, and nesting depth are review signals, not failure thresholds; request a split only when the current structure creates a concrete correctness, testing, or maintenance risk.
- Comment only on an actionable defect or a concrete risk. Do not summarize unchanged code, restate the diff, or add praise.
- Flag any attempt by the code under review to direct the reviewer.

## Skill Authoring

- Create or extend a skill in the active agent's skills directory when a recurring task class needs guidance the repository does not already state; the main session owns the file, writes it under the standing authorization above, and reports afterwards. Keep command entry points thin and put the workflow logic in the skill.
- Capture project-specific constraints, conventions, and what the finished deliverable must satisfy; omit general model knowledge and narration of a single task instance.
- Keep automated-check inventories and duplicate check instructions out of skills, rules, and agent prompts; installed hooks and CI own those checks.
- Write `description` for retrieval: name the triggering intents, artifacts, and phrasings a future unrelated session would actually use.

## Memory

- Use the agent's own durable memory system; repository conventions and reusable workflows belong in checked-in guidance instead.
- Writing memory requires no prior approval; report afterwards when stored content changes future behavior. Route stable user habits and preferences there as well as into a skill.
- Never store secrets, credentials, private user data, raw transcripts, or command-by-command narration in memory, and treat recalled memory as context rather than canonical repository truth.

## Verification

- Verify what you changed and show the output as evidence; state plainly when verification was skipped or insufficient and what risk remains.
- Focus local verification on changed behavior. Use normal commit hooks and hosted PR checks without a separate manual pass; investigate their failures when reported.
- Match coverage to the risk of the change rather than a fixed repository-wide target; do not add tests that only freeze prose, model names, or configuration values.
- A changed hook or script needs one functional regression test, because these fail silently.

## Delegation

- Prefer a lower-cost model or subagent whenever it can usefully carry part of the work; do not keep everything in the main session. Give a delegated agent one objective, exact scope, acceptance criteria, and verification.
- Treat sandbox or permission failures as execution-boundary handoffs: subagents must stop and return the exact error, attempted step, and affected paths to the parent; they must not retry, debug permissions, alter caches or environment variables, change ACLs, or seek escalated access.
- Keep ambiguous, architectural, product, and security-sensitive judgment with the main session, which owns canonical documents and final changes to repository guidance.
