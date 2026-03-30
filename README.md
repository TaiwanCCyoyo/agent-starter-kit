[繁體中文版 (Traditional Chinese) 🇹🇼](./doc/README.zh-TW.md)

# 🚀 Agent Starter Kit

A robust, highly autonomous, and evolving multi-agent template designed specifically for AI-driven IDEs and CLI tools (such as Antigravity, Claude Code, and Cursor).

This starter kit is built upon the philosophy of **Verification-First execution**, **Long-Term Memory persistence**, and **Self-Evolving security SOPs**.

## 🧠 Core Principles

1. **Verification-First**: AI agents must verify tasks by providing tangible evidence (logs, outputs, terminal text). Human dependencies (e.g., waiting for authentication) MUST be requested upfront during the planning phase.
2. **Evolving Pre-Commit Security**: Before any commit is made, an unskippable and evolving SOP (`pre-commit-sop.md`) is executed. The first rule is ALWAYS a credential/secret scan (e.g., `gitleaks`). As the project grows in complexity, the agent is responsible for dynamically adding related linter checks to this SOP.
3. **Long-Term Memory**: Agents track project preferences, architectures, and Git hooks via `.agents/memory/MEMORY.md`. This prevents context amnesia across sessions. (Note: Use `memory/MEMORY.example.md` as a starting template).
4. **Team Bootstrapping**: If the underlying AI CLI lacks native subagent capabilities, the main orchestrated agent is instructed to actively seek human guidance to build a script that spawns background CLI worker instances.
5. **Reusability**: Equipped with **Claude's official `skill-creator`** (from [anthropics/skills](https://github.com/anthropics/skills)), allowing the agent to systematically draft, test, benchmark, and deploy new skills without reinventing the wheel.

## 📂 Architecture

All agent-specific intellect and protocols are stealthily placed in the `.agents/` directory, natively readable by tools like Antigravity.

* **`.agents/rules/`**: The Core Beliefs (e.g., Security, Delegation, Memory triggers).
* **`.agents/workflows/`**: The Execution SOPs (e.g., Evolving Pre-Commit loops).
* **`.agents/skills/`**: Extended tools and external CLI linkages (including `skill-creator` and fallback subagent delegate tools).
* **`.agents/memory/MEMORY.example.md`**: The blueprint for the project's long-term memory tracking.
* **`.agents/TEAM.yaml`**: The repository of recognized subagent roles and responsibilities.

## ⚙️ Getting Started (Local Setup)

This project uses **[uv](https://github.com/astral-sh/uv)** for high-performance Python package management and virtual environments.

### 1. Prerequisite
Ensure you have `uv` installed on your system:
```powershell
powershell -c "irm https://astral-sh.uv.run/install.ps1 | iex"
```

### 2. Initialize Local Environment
Run the following command in the root directory to create a local `.venv` and install all required dependencies:
```powershell
uv sync
```

### 3. Running Orchestration
To use the `delegate-task` skill with the local environment:
```powershell
uv run .agents/skills/delegate-task/delegate.py --role Feature_Developer --task "Your task here"
```

Using `uv run` ensures that the script correctly loads the local virtual environment and its dependencies (like `pyyaml`) without polluting your global Python installation.

---

---
*Built aiming for maximum autonomy, dynamic safety, and seamless multi-agent orchestration.*

## 💡 Recommended Tools
For the best security and development experience, please consider installing:
- **[Gitleaks](https://github.com/gitleaks/gitleaks)**: Automatically used by our `security-scanner` skill if available.
- **[Pre-commit](https://pre-commit.com/)**: To manage Git hook lifecycles.
