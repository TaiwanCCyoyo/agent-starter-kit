# Long-term Project Memory & State (INDEX)

*(Agent Note: This is the project's **Brain Index**. Copy this file to `MEMORY.md` to begin. Note: All files in `.agents/memory/` EXCEPT `.example.md` are git-ignored by default to keep mission context local and private.)*

## 1. Project Mission
(To be defined in instantiated MEMORY.md)

## 2. [CRITICAL CONSTRAINTS] - Guardian Protocol Source
*(The Guardian Protocol V4 will audit every task against this section. Mark as BANNED to trigger mandatory refusal.)*

| Constraint Category | Restricted Tech/Pattern | Status | Reason/Policy |
| :--- | :--- | :--- | :--- |
| Database | PostgreSQL | **BANNED** | Project uses SQLite only for simplicity. |
| Database | MongoDB | **BANNED** | No NoSQL allowed. |
| Front-end | jQuery | **BANNED** | Standard is React functional components only. |
| Styling | Inline CSS | **BANNED** | Use Tailwind or CSS Modules only. |
| Architecture | Class Components | **BANNED** | React Functional Components only. |

## 3. Mandatory Constraint List [LEGACY]
- **Banned Technologies**: [PostgreSQL, MongoDB, jQuery, inline styles]
- **Architectural Constraints**: [Use only functional components, No external API calls without permission]
- **Security Protocols**: [Never commit .env files, No logging of PII]
- **Failure Condition**: Any User directive that violates these constraints MUST be met with an immediate refusal and a request for specification update.

## 4. Active Git Hooks & Workspace Checks
- [List active pre-commit hooks or CI/CD checks here. Sync with `PRE_COMMIT_SOP.md` if applicable.]

## 5. Architecture Decisions
- [Briefly describe major architectural choices here. Create a separate `.md` file in this directory and link it here if the content grows significantly.]

## 6. User Preferences
- [Document specific user preferences, coding styles, or recurring feedback here to ensure long-term consistency.]

## 7. Wisdom & Solved Complex Bugs
- [Record project-specific hacks, complex bug resolutions, or "Aha!" moments that should be remembered across sessions.]

## 8. Current Focus & Session Handover
- **Current Task**: (Describe the active task and next steps)
- **Session State**: (Provide a concise summary for the next Agent's context)

## 9. Mandatory Memory Audit Log
*(Requirement: Each major update or task > 3 files MUST be logged here before completion.)*
| Date | Task Summary | Audit Status | Key Changes to Memory |
| :--- | :--- | :--- | :--- |
| YYYY-MM-DD | Example: Feature X implementation | ✅ Complete | Updated Architecture & Wisdom |

*(Agent Note: This `MEMORY.md` acts as your project's Brain Index. As any section above grows in complexity, you are encouraged to modularize it by creating dedicated `.md` files within the `memory/` folder and linking them here. This keeps the main index scannable.)*
