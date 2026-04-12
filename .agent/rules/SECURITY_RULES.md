---
trigger: always_on
description: Core Rule - Security, Secrets Scanning, and Dynamic Evolution
---
# Security & Evolution Rules

1. **NO SECRETS POLICY**: Never commit API keys, passwords, tokens, or any sensitive credentials to the repository.
2. **IMMUTABLE SECURITY STEP**: The Credential Scanning step in the native `.pre-commit-config.yaml` is **MANDATORY and IMMUTABLE**. You are forbidden from deleting, bypassing, or disabling this specific check during any "evolution" or update of the project.
3. **MANDATORY PRE-COMMIT HOOKS**: The native pre-commit hooks will execute automatically before every `git commit`. Do not bypass them (e.g., via `--no-verify`) unless strictly authorized.
   - **Installation Requirement**: You MUST ensure hooks are locally installed. If `.git/hooks/pre-commit` is missing, you MUST execute `uv run pre-commit install` immediately.
4. **ACTIVE EVOLUTION**: You have the responsibility to update and evolve `.pre-commit-config.yaml` as the project grows.
   - If you add Python code, ensure Ruff or a proper linting step is configured.
   - Always reference `.agents/memory/MEMORY.md` to track which checks are currently active.
5. **ENVIRONMENTAL ISOLATION**: Sensitive data belongs in `.env` or `.env.local` (which must be in `.gitignore`). Use `.env.example` for templates.
*(Agent Note: Reference `.agents/memory/MEMORY.md` to track which checks are currently active.)*
