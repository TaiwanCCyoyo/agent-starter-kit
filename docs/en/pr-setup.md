# Enable PR Delivery in a Downstream Project

Reset the [Git workflow contract](git-workflow.md) to local-only when adopting this template. This guide is for repository owners; it does not grant agents setup, publishing, or administration authority. This source repository's separately approved configuration is documented in [daily review](daily-review.md).

## Identity and enforcement

- Choose the repository and default branch. Configure a development GitHub App with only the repository permissions needed for task-branch pushes and PR creation, without rules administration or bypass privileges. Keep its private key in an owner-controlled secret manager; issue short-lived installation tokens outside the repository.
- Audit every authentication route: Git HTTPS/SSH, `gh`, and the GitHub plugin can use different identities. Ensure development sessions cannot fall back to an owner's credentials. Separate worktrees do not isolate credentials; isolate the execution environment or credential-providing service when roles need enforced separation.
- If designated sessions must submit binding approvals, use an independent reviewer identity and expose it only to those sessions. Two tokens for the same user do not create independent reviewers. Confirm that the review counts toward the actual repository rules; an AI comment or reaction is not approval.
- Keep administration credentials outside development and review sessions. For owner-only merge, require a separately enforced merge boundary before enabling delivery: ordinary write permissions are not a universal "push branches but never merge" role. Use a restricted tool service if platform roles cannot separate these capabilities; development/review sessions must not receive the underlying merge-capable credentials.

## Repository gates

For owner-authorized automatic review and merge, an independent reviewer App can receive Contents/Pull requests write and Actions/Checks/Commit statuses read. Grant it a PR-only exception only in a separate Restrict updates ruleset; keep the quality-gate ruleset without bypass actors. Trusted sessions on one computer may use explicit role selection instead of hard credential isolation only when the owner accepts that limitation. This does not permit fallback to personal credentials.

- Confirm the GitHub plan supports the required protection for the repository's visibility. Enable an active default-branch ruleset requiring PRs, valid independent approval, passing CI checks, resolved review conversations, and renewed approval after new changes. Block force pushes and branch deletion; leave the bypass list empty.
- Add project-appropriate CI before selecting required check names. Use the README example as a starting point, pin third-party actions to verified full commit SHAs before adoption, keep job names stable, and verify checks actually run for PRs. Local pre-commit results do not establish a remote merge gate.
- Review changes to CI and ownership policy with particular care. Run PR code without privileged publishing/admin credentials; keep any privileged review/merge automation outside the code being reviewed.
- Use GitHub/Codex PR views and review integration before building a custom inbox. Configure notifications and review assignment for the actual account. Automatic review feedback and a required GitHub approval are separate outcomes.

## Activate and verify

1. Record the approved repository/remote, base branch, and publishing identity in the current-state bullet of `git-workflow.md`, and enable standing PR delivery. Record any separately authorized reviewer role there as well. Do not record credentials.
2. Align the installed agent's tool permissions with that scope. This template retains Claude's push confirmation rules and Codex's platform approval controls; changing prose does not remove those prompts. Adjust runtime settings only after identity and server-side protection are ready.
3. Use a disposable task branch and a small PR to verify creation, CI, review, and owner-authorized merge. Verify protection rejects direct default-branch updates and merging without required checks/approval, and that an additional commit requires renewed review. Use a test repository or an owner-approved probe for rejection tests; a misconfigured production rule could accept the attempted write.
4. For owner-only merge, verify that development and reviewer sessions are rejected when attempting to merge even a PR that satisfies every check and approval. Use a test repository or owner-approved probe and record the enforcement mechanism; do not enable standing delivery until this boundary works. Verify PR jobs receive neither write tokens nor privileged secrets. Verify development/review credentials cannot administer or bypass rules. Confirm the effective identity through each enabled client. Record evidence and remaining gaps before claiming enforcement works.

Copying this starter kit does not configure Apps, credentials, rulesets, or scheduling for a downstream repository, or remove runtime push prompts. Perform those owner setup steps in each adopting project.

## References

- [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [Required PR reviews](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/approving-a-pull-request-with-required-reviews)
- [GitHub App installation authentication](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-as-a-github-app-installation)
- [Codex GitHub review integration](https://learn.chatgpt.com/docs/third-party/github)
