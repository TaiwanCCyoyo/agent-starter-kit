# Long-term Project Memory & State (TEMPLATE)

*(Agent Note: When adapting this starter kit for a new project, copy this file to `MEMORY.md` and begin tracking state there.)*

## 1. Project Mission
(To be defined in instantiated MEMORY.md)

## 2. Active Git Hooks & Commit Checks
*The following checks are tracked and must be synced with `PRE_COMMIT_SOP.md`:*
- [x] **Credential Scanning** (Tool: Gitleaks/Shell Regex) - *MANDATORY*
- [ ] Python Linting (Planned)
- [ ] Unit Testing (Planned)

## 3. Architecture Decisions
- Antigravity standard path: `.agents/`
- SOP Execution: `PRE_COMMIT_SOP.md` must run before every commit.
- Evolution: Agent is responsible for updating SOPs when project context changes.
