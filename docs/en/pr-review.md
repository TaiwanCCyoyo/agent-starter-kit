# PR Review

Owner-approved scope: `TaiwanCCyoyo/agent-starter-kit`, base `main`. Pull request review runs on the hosted Codex GitHub integration, enabled by the owner in Codex settings for this repository. Reviews are triggered per pull request, not on a schedule.

The implementing agent owns [PR follow-through](git-workflow.md#pr-follow-through): assess findings, fix and verify valid issues within scope, push the fixes, and promptly resolve addressed threads before waiting for current-head CI and renewed review. Resolution does not guarantee that a new review will start; verify its actual status before reporting completion. The owner retains merge authority.

## How review runs

- Automatic reviews post findings when a pull request is opened or updated. Commenting `@codex review` on a pull request requests a review on demand.
- The review executes on the provider's infrastructure. It consumes the owner's Codex code review allowance rather than this repository's GitHub Actions minutes.
- Review output is advisory commentary. It is not a GitHub approval and does not merge anything.
- The reviewer's capabilities come from the owner's Codex settings, outside this repository. Nothing in a pull request grants it credentials or widens what it may do, so a change to this file cannot move that boundary.

## Credentials

- No GitHub App private key is stored on a contributor machine, and no App credential is required for review. The former `taiwanccyoyo-dev-agent` and `taiwanccyoyo-review-agent` Apps and their local PowerShell token helper are retired.
- Agent sessions push task branches and open pull requests with the owner's own GitHub credentials, so agent-authored commits are attributed to the owner. Distinguish agent work by branch prefix and commit message, not by identity.
- Because agent and owner share one identity, this arrangement provides no enforced separation between roles. The owner accepts that limitation for this repository.

## Merge conditions

`protect-main` governs `main` and has no bypass actors. It requires a pull request, resolution of every review conversation, and a successful `repository-checks` job for the current revision. That job runs full pre-commit and all repository tests. It requires no approving review, because a single identity cannot approve its own pull request.

Merging is the owner's decision. Before merging, confirm the required check passed on the current head, read the review findings, and resolve or consciously dismiss each one. Do not use admin merge, force push, or weaken the ruleset to land a change.

Downstream projects start in local-only mode and must establish their own review integration, gates, and authorization; copying this file grants none of them.
