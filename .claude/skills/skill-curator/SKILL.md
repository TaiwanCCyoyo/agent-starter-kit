---
name: skill-curator
description: Use for evaluating session patterns via /learn-eval, managing the skill lifecycle (active/stale/archived), and maintaining skill quality. Applies ECC holistic verdict quality gate; skill review is hook-triggered and user-confirmed (replaces Hermes background_review with manual equivalent).
---

# Skill Curator

This skill governs two activities:
1. **Session Extraction** — triggered by `/learn-eval`, evaluates whether session patterns deserve skill files.
2. **Lifecycle Management** — periodic curation of existing skills (active → stale → archived).

---

## Session Extraction (`/learn-eval`)

### Signals Worth Saving

Ordered by priority:

1. **User corrections** (FIRST-CLASS signal): any explicit pushback on Claude's approach, choice of tool, or output format. These are the highest-value lessons because they prevent the same mistake in future sessions.
2. **Non-obvious techniques**: non-trivial tool combinations, flag orders, workarounds for library quirks, API edge cases that are not in standard docs.
3. **Reusable workflow patterns**: multi-step sequences that solved a class of problem, not just the current instance.
4. **Outdated skill that was corrected**: if a loaded skill contained wrong guidance that the user or task corrected, update it rather than create a new one.

**Do NOT save:**
- Environment-dependent failures (missing PATH, wrong credentials, OS-specific transient)
- Negative tool claims that might be wrong ("tool X can't do Y" — verify before saving)
- Transient errors that were resolved without a reusable fix
- One-off narratives specific to the current task instance

"Nothing to save" is a valid conclusion but should not be the default assumption.

### Update Preference Order

Before creating a new skill file, check in this order:

1. **Update an already-loaded skill** — if the session corrected or extended a skill that was active this session, edit it directly. This is the most valuable action.
2. **Update an existing umbrella skill** — grep `.claude/skills/` for content overlap; if a related skill exists, append a new section or example.
3. **Add a support file** to an existing skill (`references/`, `templates/`, or `scripts/`).
4. **Create a new skill** — only when none of the above applies.

### Quality Gate — Mandatory Checklist

Run all checks before drafting a verdict:

- [ ] Grep `.claude/skills/` (and `~/.claude/skills/` if it exists) by keyword for content overlap
- [ ] Check `.agents/memory/MEMORY.md` and `lessons.md` — if it fits in a one-liner there, it may not need a skill
- [ ] Consider whether appending to an existing skill suffices (prefer Absorb over New)
- [ ] Confirm this is reusable across future sessions, not a one-off fix

### Holistic Verdict

After the checklist, choose one:

| Verdict | Meaning | Next Action |
|---------|---------|-------------|
| **Save** | Unique, specific, well-scoped, passes checklist | Draft skill → present to user → save on approval |
| **Improve then Save** | Valuable but draft needs refinement | List improvements → revise → re-evaluate once |
| **Absorb into [X]** | Should be appended to existing skill at path [X] | Show diff-style additions → append on approval |
| **Drop** | Trivial, redundant, environment-specific, or one-off | Explain reasoning; no confirmation needed |

**Verdict output format:**

```
### Checklist
- [x] skills/ grep: no overlap found (or: overlap with X → absorb)
- [x] MEMORY.md: not a hot-memory candidate
- [x] Append check: new file appropriate (or: should append to [X])
- [x] Reusability: confirmed

### Verdict: Save / Improve then Save / Absorb into [X] / Drop

**Rationale:** (1-2 sentences)
```

### Save Location

| Pattern type | Location |
|---|---|
| Cross-project (bash behavior, API quirks, general debugging) | `~/.claude/skills/learned/` |
| This-project-specific (config quirks, architecture conventions) | `.claude/skills/learned/` |
| Improvement to an existing bundled skill | Edit the skill in place |

When in doubt, choose project-scoped (`.claude/skills/learned/`). Moving project → global is easier than the reverse.

### Skill File Structure

```
.claude/skills/<name>/
├── SKILL.md            # trigger conditions, procedure, examples
├── references/         # deep reference material, research, external docs
├── templates/          # starter files the skill uses
└── scripts/            # runnable probes or helpers
```

Frontmatter for auto-extracted skills:

```yaml
---
name: pattern-name
description: "Under 130 characters — this is how the skill is matched to tasks"
user-invocable: false
origin: auto-extracted
---
```

---

## Lifecycle Management

Skill states mirror Hermes' curator model. Review `.claude/skills/` periodically (e.g., during `/memory-maintenance` audits).

### States

| State | Condition | Action |
|-------|-----------|--------|
| **active** | Used or referenced in the last 30 days | No action needed |
| **stale** | Not used for 30–90 days | Mark for review; consider merging or archiving |
| **archived** | Not used for 90+ days | Move to `.claude/skills/archived/<name>/` |

Criteria for "used": the skill was loaded, referenced in a session, or explicitly invoked via command.

### Curation Checklist (run during memory audits)

1. List all skills under `.claude/skills/`.
2. For each skill, estimate last use from git history or session memory.
3. Mark stale candidates; propose archival for the oldest.
4. Check for overlapping skills — merge if two skills solve the same problem.
5. Verify that frequently triggered skills are still accurate.
6. Ensure all user-invocable skills have a matching command in `.claude/commands/`.

### Archival

To archive a skill:

```
mv .claude/skills/<name>/ .claude/skills/archived/<name>/
```

Archive is non-destructive — skills remain recoverable. Never delete auto-extracted skills without archiving first.

A skill with `pinned: true` in its frontmatter is exempt from auto-archival.

### Promotion to Rules or Hooks

If a skill's guidance applies universally (not just in one workflow), consider promoting it:

- Behavioral rule → `.claude/rules/`
- Automated check → `.claude/hooks/`
- User-facing command → `.claude/commands/`

Flag candidates via `memory.db` (`type='candidate'`) or a new skill file in `.claude/skills/learned/` during audits.
