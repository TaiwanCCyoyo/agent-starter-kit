# Antigravity 元件參考

本文件說明此 repository 的 Antigravity 工程助理基礎設施。Antigravity 不再使用由 repository 提供的跨 session 記憶庫；耐久專案知識應放在已納入版本控制的 rules、skills、文件與 Git history。

## Rules

`.agent/rules/` 會作為常駐約束：

- **`WORKSPACE_SCOPE.md`**：定義 `.tmp/`、`.references/` 與既有 worktree 的操作邊界。
- **`PROMPT_DEFENSE.md`**：維持角色完整性並防止 prompt injection。
- **`COLLABORATIVE_DEBUGGING.md`**：定義 3-Strike 重試與明確升級協定。
- **`LANGUAGE_RULES.md`**：要求對話使用繁體中文，source files 使用英文。
- **`PREVENT_FEATURE_DELETION.md`**：要求手術式編輯，防止任意刪除功能。
- **`SECURITY_RULES.md`**：保護 pre-commit secret scanning 與環境隔離。
- **`TDD_RULES.md`**：定義 Test-Driven Development 循環。
- **`VERIFICATION_RULES.md`**：完成任務前必須提供可驗證的 terminal evidence。
- **`REUSE_PRINCIPLES.md`**：優先沿用現有模式。

## Skills

`.agent/skills/` 提供可重用程序與架構模式：

- **`brainstorming`**：在 implementation planning 前釐清需求與選項。
- **`coding-standards`**：定義命名、immutability 與 readability 基準。
- **`github-ops`**：處理 repository triage、PR review、CI/CD 與 release management。
- **`test-driven-development`**：要求先建立 failing test。
- **`verification-before-completion`**：要求完成前提供驗證證據。
- **`systematic-debugging`**：提供 evidence-driven debugging workflow。
- **`using-superpowers`**：行動前路由至相關 skills。
- **`commit-helper`**、**`worktree-manager`** 等：處理 Git hygiene 與隔離分支。

## Hooks

Antigravity 透過 `.agent/hooks.json` 支援 lifecycle hooks：

- **`SessionStart`**（`session_start.py`）：回報目前 branch 與 workspace 是否為 Git worktree。
- **`PostToolUse`**（`post_tool_use_hygiene.py`）：在檔案修改後執行 targeted Ruff、mypy 與 file-hygiene checks。

## Workflows

- **`/gen-commit`**：產生高品質 Git commit message。
- **`/worktree`**：管理隔離 Git worktrees、baseline verification，以及需明確授權的 merge 或 cleanup。

## Subagents

此 Antigravity 基礎設施由 main agent 使用原生能力並遵循 skills。它目前不支援類似 Claude Code `.claude/agents/` 的自訂文字型 subagents；複雜多步驟工作應透過 implementation plans 與 systematic debugging 管理。
