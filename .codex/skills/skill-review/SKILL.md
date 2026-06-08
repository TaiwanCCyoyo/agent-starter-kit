---
name: skill-review
description: Use after meaningful work to decide whether a reusable correction, technique, or workflow should become or update a skill.
---

# Skill Review

This is the Codex-native equivalent of the ECC quality gate and the manual portion of Hermes skill curation.

The Stop hook reminds Codex to perform this review after meaningful work. That reminder is not Hermes-style lifecycle telemetry: it does not automatically record skill views, management actions, or `last_used_at`.

## Evaluate

Prioritize user corrections, non-obvious techniques, reusable workflows, and outdated skill guidance corrected during the session.

Do not save transient environment failures, unverified negative claims, one-off task narration, or material that fits in a concise memory entry.

## Decision Order

1. Update a skill used in the session.
2. Absorb the guidance into an existing related skill.
3. Add a focused support file to an existing skill.
4. Create a project skill only when no existing skill fits.
5. Store an unready candidate in `memory.db` with `type='candidate'`, or drop it.

Search `.codex/skills/`, available user skills, and active memory before deciding.

Return one verdict: `Save`, `Improve then Save`, `Absorb into <skill>`, or `Drop`, with a short rationale. Do not create or modify a skill without user approval unless the user explicitly requested the change.
