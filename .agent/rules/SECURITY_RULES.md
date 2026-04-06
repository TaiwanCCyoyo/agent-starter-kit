---
description: Core Rule - Security, Secrets Scanning, and Dynamic Evolution
---
# Security & Evolution Rules

1. **NO SECRETS POLICY**: Never commit API keys, passwords, tokens, or any sensitive credentials to the repository.
2. **IMMUTABLE SECURITY STEP**: The "Credential Scanning" step in `PRE_COMMIT_SOP.md` is **MANDATORY and IMMUTABLE**. You are forbidden from deleting, bypassing, or disabling this specific check during any "evolution" or update of the workflow.
3. **MANDATORY PRE-COMMIT SOP**: You MUST execute the `.agents/workflows/PRE_COMMIT_SOP.md` before every `git commit`. 
4. **ACTIVE EVOLUTION**: You have the responsibility to update and evolve `PRE_COMMIT_SOP.md` as the project grows. 
   - If you add Python code, add a linting step.
   - If you add a new service, add a connectivity check.
   - Always reference `.agents/MEMORY.md` to track which checks are currently active.
5. **ENVIRONMENTAL ISOLATION**: Sensitive data belongs in `.env` or `.env.local` (which must be in `.gitignore`). Use `.env.example` for templates.
*(Agent Note: Reference `.agents/memory/MEMORY.md` to track which checks are currently active.)*
