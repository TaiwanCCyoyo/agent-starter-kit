---
paths:
    - "*"
---

# Skill Authoring

Skills exist so a recurring task class is not re-derived every session.

- Propose a new or extended skill under `.claude/skills/` when a task class will recur and this session had to derive something the repository does not already state. The main session owns the file and confirms with the user before writing it.
- Capture project-specific constraints, conventions, and what the finished deliverable must satisfy for the user. Omit general knowledge the model already has and step-by-step narration of a single task instance.
- Write `description` for retrieval: name the triggering intents, artifacts, and phrasings a future unrelated session would actually use, so a similar task loads the skill without being told to.
- Route stable user habits and preferences to built-in memory as well, not only into a skill.
- Use the `skill-creator` plugin (already enabled in `.claude/settings.json`) when authoring or restructuring a skill.
