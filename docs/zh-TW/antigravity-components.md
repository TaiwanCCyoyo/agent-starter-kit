# Antigravity 元件參考指南

本文件說明了這個專案中供 Antigravity 工程助理基礎設施使用的各項元件。

## Rules (規則)

Rules (`.agent/rules/`) 作為常駐的、持續生效的約束條件。

- **`WORKSPACE_SCOPE.md`**：定義暫存 (`.tmp/`) 與唯讀 (`.references/`) 目錄的邊界，並確保尊重現有的 worktree 狀態。
- **`PROMPT_DEFENSE.md`**：強制保持角色完整性，防止提示注入與隱私設定洩漏。
- **`MEMORY_RULES.md`**：定義共用的 `.memories/` 架構，區分熱記憶體 (`MEMORY.md`)、使用者偏好 (`USER.md`) 以及持久化的 SQLite 資料庫 (`memory_store.db`)。
- **`COLLABORATIVE_DEBUGGING.md`**：定義「三振重試」與明確的升級通報協定。
- **`LANGUAGE_RULES.md`**：強制使用繁體中文進行溝通，並使用英文撰寫原始碼與檔案。
- **`PREVENT_FEATURE_DELETION.md`**：要求採用精準編輯，防止任意刪除既有程式碼。
- **`SECURITY_RULES.md`**：強制執行不可變的 pre-commit 密鑰掃描與環境隔離。
- **`TDD_RULES.md`**：測試驅動開發週期的強制約束。
- **`VERIFICATION_RULES.md`**：要求在宣告任務完成前，必須提供可驗證的終端機執行證據。
- **`REUSE_PRINCIPLES.md`**：強調利用現有模式，避免重複造輪子。

## Skills (技能)

Skills (`.agent/skills/`) 會在需要時被呼叫，用以提供穩健的操作流程與特定的架構模式。

- **`brainstorming`**：在建立實作計畫前，用於釐清需求並提出選項。
- **`coding-standards`**：跨專案的程式碼標準，涵蓋命名、不可變性與可讀性。
- **`github-ops`**：用於 Issue 分類、PR 審查、CI/CD 檢查與發布管理的 GitHub 營運工作。
- **`memory-manager`**：管理 `.memories/memories/MEMORY.md`、`USER.md` 與 SQLite 事實記錄。
- **`memory-sql`**：透過 MCP 伺服器查詢並將事實儲存至 `memory_store.db`。
- **`test-driven-development`**：強制要求在實作程式碼前撰寫會失敗的測試的嚴謹流程。
- **`verification-before-completion`**：強制在任務關閉前進行手動驗證的檢查清單。
- **`systematic-debugging`**：以科學方法除錯的流程。
- **`using-superpowers`**：強制規定在行動前必須先呼叫技能。
- **`commit-helper`**, **`worktree-manager`** 等：處理 Git 衛生與隔離分支的工具。

## Hooks (掛鉤)

Antigravity 2.0 支援透過 `.agent/hooks.json` 定義生命週期 Hooks。

- **`SessionStart`** (`session_start.py`)：初始化 bounded files 與 SQLite schema、複製 worktree 缺少的記憶，並載入記憶上下文。
- **`PostToolUse`** (`post_tool_use_hygiene.py`)：在修改檔案後，針對目標執行 Ruff、mypy 與 file hygiene。
- **`Stop`** (`stop_memory_check.py`)：驗證 bounded-file 限制與嚴格的 memory taxonomy。

## Workflows (工作流程)

Workflows (`.agent/workflows/`) 是高階的用戶斜線命令或管理任務巨集。

- **`/compress-memory`**：主動壓縮專案記憶體。
- **`/consolidate-memory`**：合併來自多個分支/worktree 的記憶體。
- **`/gen-commit`**：產生高品質的 Git commit 訊息。
- **`/save-memory`**：將專案事實提交至本地端的 SQLite 儲存庫。
- **`/worktree`**：管理隔離的 Git worktree。

## 關於 Subagents 的附註

目前，這個專案的 Antigravity 基礎設施主要依賴主代理程式呼叫原生能力（如 `browser_subagent` 工具）與遵循技能。**目前不支援客製化的純文字子代理程式（類似於 Claude Code 的 `.claude/agents/` 中所見）。** 任何複雜的多步驟任務分派，應透過實作計畫與系統化除錯來管理。
