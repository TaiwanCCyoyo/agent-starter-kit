# Git Workflow Contract

Shared by Codex, Claude Code, and Antigravity. Use native Git and GitHub capabilities; commit skills own local verification and commits.

## Task isolation

- Place task worktrees under `<primary-checkout>/.worktrees/<task-name>/`, not `.tmp/`. Resolve this path from the primary checkout even when operating inside a linked worktree. Reserve `.tmp/` for temporary reports, probes, and disposable artifacts.
- Use one task branch and isolated worktree per independent modification task. Reuse an existing worktree for the same unfinished task only after checking its ownership and changes; one primary writer at a time.
- Keep the default branch free of task edits and commits. Start independent tasks from the latest available default-branch state; report when it cannot be refreshed. Read-only work needs no new branch. Explicit user checkout instructions take precedence.
- Preserve unrelated work. Subagents operate within the parent-assigned scope; they do not independently publish or integrate changes.

## Delivery authorization

- **Current state: local-only.** GitHub identity, server-side protection, and unattended publishing are not configured by this contract. Finish with a verified local commit and report its branch/worktree; do not push or create a PR unless explicitly requested.
- Only explicit owner instructions may enable or change delivery status, destination, base branch, publishing identity, reviewer roles, or merge authority; workflow-improvement permission cannot grant these powers. Repository edits alone are not owner approval. The owner may enable standing PR delivery by replacing the current-state bullet with the approved repository/remote, base branch, permitted publishing identity, and enabled status after completing [PR setup](pr-setup.md). Copying this starter kit or detecting credentials does not enable delivery.
- Once enabled, an implementation request authorizes the main agent to push its task branch and create/update that task's PR, including review fixes, without repeated confirmation. Local-only requests override this authorization. Report the PR and actual check status; a local commit is not a delivered PR.
- Use only the approved destination and identity across Git, CLI, and plugins. If unavailable or rejected, preserve the local result and report the blocker; do not switch credentials or broaden permissions. Platform permission controls still apply.

## Review and integration

- A review request authorizes analysis and a report. Publishing review comments or a formal approval requires explicit authorization or an owner-enabled reviewer role scoped to the repository. Review authority does not include merge authority.
- Review the PR's current head commit and identify it in the result. New commits require renewed review; an internal reviewer report is not a GitHub approval.
- Development and review roles must not directly push the default branch, bypass protection, or change repository rules. Merging requires separate owner authorization and must go through a PR; it does not grant administration or bypass authority.
- Force pushes, history rewrites, discarding work, and deleting branches/worktrees require explicit authorization. Before authorized cleanup, verify the task result is preserved and no other session owns the worktree.
