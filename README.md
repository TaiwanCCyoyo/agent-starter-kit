[繁體中文版 (Traditional Chinese) 🇹🇼](./README.zh-TW.md)

# 🚀 Agent Starter Kit

A robust, highly autonomous, and evolving multi-agent template designed specifically for AI-driven IDEs and CLI tools (such as Antigravity, Claude Code, and Cursor).

This starter kit is built upon the philosophy of **Verification-First execution**, **Long-Term Memory persistence**, and **Self-Evolving security SOPs**.

## 🧠 Core Principles

1. **Verification-First**: AI agents must verify tasks by providing tangible evidence (logs, outputs, terminal text). Human dependencies (e.g., waiting for authentication) MUST be requested upfront during the planning phase.
2. **Evolving Pre-Commit Security**: Before any commit is made, an unskippable and evolving SOP (`PRE_COMMIT_SOP.md`) is executed. The first rule is ALWAYS a credential/secret scan (e.g., `gitleaks`). As the project grows in complexity, the agent is responsible for dynamically adding related linter checks to this SOP.
3. **Long-Term Memory**: Agents track project preferences, architectures, and Git hooks via `.agents/memory/MEMORY.md`. This prevents context amnesia across sessions. (Note: Use `memory/MEMORY.example.md` as a starting template).
4. **Team Bootstrapping**: If the underlying AI CLI lacks native subagent capabilities, the main orchestrated agent is instructed to actively seek human guidance to build a script that spawns background CLI worker instances.
5. **Reusability**: Equipped with **Claude's official `skill-creator`** (from [anthropics/skills](https://github.com/anthropics/skills)), allowing the agent to systematically draft, test, benchmark, and deploy new skills without reinventing the wheel.

## 📂 Architecture

All agent-specific intellect and protocols are stealthily placed in the `.agents/` directory, natively readable by tools like Antigravity.

* **`.agents/rules/`**: The Core Beliefs (e.g., Security, Delegation, Memory triggers).
* **`.agents/workflows/`**: The Execution SOPs (e.g., Evolving Pre-Commit loops).
* **`.agents/skills/`**: Extended tools and external CLI linkages (including `skill-creator` and fallback subagent delegate tools).
* **`.agents/memory/MEMORY.example.md`**: The blueprint for the project's long-term memory tracking.
* **`.agents/TEAM.md`**: The repository of recognized subagent roles and responsibilities.

---
*Built aiming for maximum autonomy, dynamic safety, and seamless multi-agent orchestration.*
