---
description: Guided feature development with codebase understanding and architecture focus
---

A structured feature-development workflow that emphasizes understanding existing code before writing new code.

## Phases

### 1. Discovery

- read the feature request carefully
- identify requirements, constraints, and acceptance criteria
- ask clarifying questions if the request is ambiguous

### 2. Codebase Exploration

- use `repo-explorer` when delegated exploration adds value
- trace execution paths and architecture layers
- understand integration points and conventions

### 3. Clarifying Questions

- present findings from exploration
- ask targeted design and edge-case questions
- wait for user response before proceeding

### 4. Architecture Design

- use Native Plan Mode for design and trade-offs
- use `architect` only for a read-only second opinion on high-risk architecture
- wait for approval before implementing

### 5. Implementation

- implement the feature following the approved design
- follow `superpowers:test-driven-development` for behavior changes
- keep commits small and focused

### 6. Quality Review

- use `implementation-reviewer` for pre-commit correctness review
- use `code-reviewer` only for a broader quality review when requested
- address CRITICAL findings and resolve or disclose HIGH findings

### 7. Summary

- summarize what was built
- list follow-up items or limitations
- provide testing instructions
