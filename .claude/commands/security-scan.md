---
description: Review agent, hook, MCP, permission, dependency, and secret surfaces with repository-supported checks.
agent: security-reviewer
subtask: true
---

# Security Scan Command

Delegate a read-only review to `security-reviewer`, then turn verified findings into a prioritized remediation plan.

## Usage

`/security-scan [path]`

- `path` defaults to the repository root.

## Repository-Supported Checks

- Inspect tracked configuration, hooks, MCP servers, agent prompts, permissions, and the relevant diff.
- Use `detect-secrets` through pre-commit for secret scanning.
- Run only scanners already installed and configured by the repository.
- Do not download or execute AgentShield, Bandit, npm audit, or other scanners unless the user explicitly requests and approves them.

## Review Checklist

1. Identify active runtime findings first:
   - hardcoded secrets
   - broad permissions
   - executable hooks
   - MCP servers with shell, filesystem, remote transport, or unpinned `npx`
   - agent prompts that handle untrusted content without defenses
2. Separate lower-confidence inventory:
   - docs examples
   - template examples
   - plugin manifests
   - project-local optional settings
3. For each critical or high finding, return:
   - file path
   - severity
   - runtime confidence
   - why it matters
   - exact remediation
   - whether it is safe to auto-fix
4. Keep the reviewer read-only; return remediation to the main agent.

## Output Contract

Return:

1. Counts by severity and runtime confidence.
2. CRITICAL/HIGH findings with exact paths and evidence.
3. Lower-confidence findings grouped separately.
4. A remediation order.
5. Commands run and checks skipped because tooling was unavailable.

## Arguments

$ARGUMENTS: optional target path
