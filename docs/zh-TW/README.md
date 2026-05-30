[English Version](../../README.md)
# AI Agent Starter Kit

這是一套標準化、低摩擦的多 Agent 工程基礎設施，支援 Gemini CLI、Codex、Antigravity 等工具。當你希望新專案中的各種 Agent 能快速理解任務、記憶、規則、工作流程與驗證要求時，可以把本 repository 當作模板使用。

## 核心理念

1. **長期記憶持久化**：Agent 透過 `.agents/memory/MEMORY.md` 保存專案目標與經驗，降低跨 session 的上下文流失。
2. **Agent 專屬啟動層**：每個 Agent 擁有自己的原生 instruction 與 hook 層，但共用同一份專案記憶。
3. **自動化維護**：格式化、lint、檔案衛生檢查與記憶提醒由 Agent hooks 與 repository 驗證腳本執行。
4. **原生安全檢查**：透過 `detect-secrets` 整合 pre-commit secret scanning。
5. **編碼與語言一致性**：驗證 repository 檔案使用 UTF-8 without BOM，並遵守語言邊界。
6. **驗證優先**：Agent 必須提供具體驗證結果，才能宣告任務完成。

## 記憶管理流程

本專案使用主動式記憶系統，維持跨 session 與 worktree 的長期上下文。

詳細架構、設定模型與複製清單請參考 [記憶系統介紹](MEMORY_SYSTEM_INTRODUCTION.md)。

### 1. 日常使用

- **儲存記憶**：完成有意義的子任務後，透過對應 Agent workflow 更新 `.agents/memory/MEMORY.md`。
- **自動提醒**：當 Agent 已經進行多輪工作且仍有 pending changes 時，hook 會提醒更新記憶。
- **記憶壓縮**：當 `MEMORY.md` 過大時，系統會提醒進行壓縮。

### 2. 多 Worktree 整合

使用多個 worktree 時，各 worktree 的記憶可能逐漸分歧。要把洞見合併回主 repository：

1. 使用 Gemini CLI 指令：
   ```bash
   /worktree finish <path/to/worktree>
   ```
2. Agent 會執行 AI semantic consolidation，將高價值的 `Lessons Learned` 與 `Done` 項目合併回主要 `MEMORY.md`。

### 3. Agent 工作流程

- **Gemini CLI**：使用 `.gemini/commands/` 與 `.gemini/skills/`。
- **Codex**：使用 `.codex/skills/` 裡的 command-like skills；可以用 `/gen-commit` 這類純文字呼叫，但不會註冊成真正的 slash command。
- **Antigravity**：使用 `.agent/workflows/` 與 `.agent/rules/`。

## 自動化 Hooks 與生命週期

本 repository 使用各 Agent 原生 hooks 維護系統一致性：

| Agent | Hook 類型 | 用途 | Script |
| :--- | :--- | :--- | :--- |
| **Gemini CLI** | `SessionStart` | 載入專案記憶與分支上下文。 | `.gemini/scripts/session_start.py` |
| **Gemini CLI** | `AfterTool` | 格式化程式碼並驗證檔案衛生。 | `.gemini/scripts/after_tool_auto_format.py`, `.gemini/scripts/after_tool_file_hygiene.py` |
| **Gemini CLI** | `AfterAgent` | 檔案變更後提醒 Agent 更新記憶。 | `.gemini/scripts/memory_nudger.py` |
| **Gemini CLI** | `AfterAgent` | 檢查記憶檔案大小，必要時提醒壓縮。 | `.gemini/scripts/memory_compressor.py` |
| **Codex** | `SessionStart` | 注入 `.codex/AGENTS.md`、專案記憶、分支與 worktree 上下文。 | `.codex/hooks/session_start.py` |
| **Codex** | `PostToolUse` | 檔案編輯後執行 lint 與檔案衛生檢查。 | `.codex/hooks/post_tool_use_hygiene.py` |
| **Codex** | `Stop` | 有 pending changes 且經過多輪回覆後提醒 Codex 更新記憶，並檢查記憶大小。 | `.codex/hooks/stop_memory_check.py` |

### Hook 疑難排解

如果 hooks 沒有觸發：

1. 確認 Git hooks 已安裝：
   ```bash
   uv run pre-commit install
   ```
2. Gemini CLI：檢查 `.gemini/settings.json` 的 matcher 與 command path。
3. Codex：檢查 `.codex/config.toml` 是否啟用 `codex_hooks`，以及 `.codex/hooks.json` 是否指向 `.codex/hooks/`。
4. 確認 Agent 已信任 project-local configuration layer。

## 模板使用方式

套用到新專案時，依照支援的工具複製對應的 Agent 基礎設施：

| Path | 用途 |
| :--- | :--- |
| `.agents/memory/` | 共用長期專案記憶位置。 |
| `.agent/` | Antigravity rules、skills、workflows。 |
| `.gemini/` | Gemini CLI commands、policies、hooks、skills。 |
| `.codex/` | Codex instructions、hooks、private command-like skills。 |
| `scripts/` | Repository 層級的檔案衛生與格式化腳本，供 Git 與 Agent adapters 呼叫。 |
| `.pre-commit-config.yaml` | Repository 層級驗證 hooks。 |

複製後，請將 `.agents/memory/MEMORY.md` 替換成目標專案的真實 mission，檢查各 Agent 專屬規則，使用 `uv run pre-commit install` 安裝 hooks，並以 `uv run ruff check .` 驗證。

### 整合 Superpowers 技能（供 Antigravity 使用）

為了提供 Antigravity 代理人強大的推理與任務執行能力（例如結構化需求釐清與測試驅動開發），本儲存庫整合了源自開源專案 [obra/superpowers](https://github.com/obra/superpowers) 的一系列精選技能。這些技能已複製至 `.agent/skills/` 底下，並遵守 MIT 授權條款（版權所有 (c) 2026 Jesse Vincent）。

## 初始化

要初始化此儲存庫並設定驗證工具：

1. **安裝 Git Hooks**
   ```bash
   uv run pre-commit install
   ```
2. **驗證環境設定**
   ```bash
   uv run ruff check .
   ```

### 為新專案初始化記憶
儲存庫初始化完成後：
1. 請確認 `.agents/memory/MEMORY.md` 中的專案 **Mission（任務）** 區塊已填寫完畢。

---

本專案要求 source code、技術文件、workflows 與 configuration 使用 UTF-8 without BOM 並以英文撰寫。繁體中文內容應放在 `docs/zh-TW/` 與 `.agents/memory/`。
