# Memory Architecture and Rules

## Unified Location

Shared instantiated memory lives under `.memories/`. Never write memory to the legacy `.agents/memory/` directory.

## Taxonomy

- `.memories/memories/MEMORY.md`: stable project, environment, and tool facts needed in most sessions; no more than 2,200 characters.
- `.memories/memories/USER.md`: stable user preferences; no more than 500 characters.
- `.memories/memory_store.db`: searchable facts, decisions, lessons, workflows, recurring-problem evidence, root causes, and verified resolutions.

No other non-hidden durable memory files or directories are part of the approved taxonomy.

## Routing

- Store high-frequency project facts in `MEMORY.md`.
- Store stable user preferences in `USER.md`.
- Store searchable knowledge in SQLite through `memory-sql`.
- Query for duplicates before database writes.
- Keep plans in native planning state, `.tmp/`, maintained `docs/`, or Git history.

## Safety

- Preserve unrelated existing facts when editing bounded files.
- Store only curated and verified information.
- Never store secrets, credentials, private user data, raw transcripts, or temporary task narration.
