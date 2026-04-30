# 記憶系統介紹

記憶系統讓長期 Agent 工作能在不同 session、支援的 Agent 與 Git worktree 之間維持一致。

它用來保存應該超越單一對話的專案狀態：專案目標、持久決策、經驗教訓、目前交接狀態與未完成的後續工作。

## 心智模型

這套系統分成三層：

1. `.agents/memory/MEMORY.md` 是持久專案記憶。
2. Agent hooks 會在生命週期邊界載入、提醒並驗證記憶相關狀態。
3. Agent skills 或 commands 提供受控的記憶儲存、壓縮與整合流程。

記憶檔預設刻意被 git 忽略。它是本機專案狀態，不是範本原始碼。

## 元件

| 元件 | 用途 |
| :--- | :--- |
| `.agents/memory/MEMORY.md` | 共用長期專案狀態。 |
| SessionStart hooks | 在工作開始前注入專案記憶、分支上下文與 worktree 上下文。 |
| Stop/AfterAgent reminders | 在 pending changes 持續一段時間後提醒 Agent 更新記憶。 |
| `save-memory` | 保存已完成工作、決策與交接筆記。 |
| `compress-memory` | 當記憶變得冗長時彙整歷史細節。 |
| `memory-maintenance` | 定義記憶初始化、稽核、更新與整合方式。 |
| Worktree sync | 在第一次 session 開始前，將有用的記憶上下文複製到新 worktree。 |

## Agent 整合

### Codex

Codex 使用：

- `.codex/hooks/session_start.py` 注入 `.codex/AGENTS.md`、分支上下文與 `.agents/memory/MEMORY.md`。
- `.codex/hooks/stop_memory_check.py` 發出低噪音的記憶更新與壓縮提醒。
- `.codex/skills/save-memory/SKILL.md`、`.codex/skills/compress-memory/SKILL.md` 與 `.codex/skills/memory-maintenance/SKILL.md`。

當 Gemini 或 Antigravity 尚未同步對應行為時，Codex-specific 進度應明確記錄為 Codex-specific。

### Gemini CLI

Gemini 使用：

- `.gemini/scripts/session_start.py` 提供啟動時的記憶上下文。
- `.gemini/scripts/memory_nudger.py` 提供記憶更新提醒。
- `.gemini/scripts/memory_compressor.py` 檢查記憶大小。
- `.gemini/commands/save-memory.toml`、`.gemini/commands/compress-memory.toml` 與 `.gemini/skills/memory-maintenance/SKILL.md`。

在 Codex-only 實驗期間，Gemini 行為可能刻意落後 Codex。請在 memory 中明確標示這種狀態。

### Antigravity

Antigravity 主要使用 `.agent/workflows/` 與 `.agent/rules/` 作為指令和 workflow 層。

當 Codex 或 Gemini 變更引入新的記憶行為時，只有在設計穩定後才將概念同步到 Antigravity。

## 新專案複製清單

重用此 starter kit 時，只複製你需要的 Agent 層。

| 路徑 | 何時複製 | 需要客製化 |
| :--- | :--- | :--- |
| `.agents/memory/` | 需要共用記憶狀態。 | 將 `MEMORY.md` 替換成目標專案 mission。 |
| `.codex/` | 需要 Codex 支援。 | 檢查 hooks、skills 與 `.codex/AGENTS.md`。 |
| `.gemini/` | 需要 Gemini CLI 支援。 | 檢查 settings、commands 與 scripts。 |
| `.agent/` | 需要 Antigravity 支援。 | 檢查 rules、skills 與 workflows。 |
| `scripts/` | 需要共用 hygiene scripts。 | 只保留啟用的 Agent 會引用的 scripts。 |
| `.pre-commit-config.yaml` | 需要 repository 層級檢查。 | 使用 `uv run pre-commit install` 安裝。 |

複製後：

1. 在 `.agents/memory/MEMORY.md` 定義新專案 mission。
2. 移除不支援的 Agent 層。
3. 安裝需要的 hooks。
4. 執行 repository 驗證命令，通常是 `uv run ruff check .`。

## 操作規則

- 有意義的檔案變更後要儲存記憶。
- 記錄持久決策、經驗教訓與交接筆記。
- 不要保存 secrets、tokens、API keys 或使用者私人資料。
- 不要保存低價值流水帳，例如每個嘗試過的命令。
- 當歷史細節開始掩蓋目前狀態時壓縮記憶。
- 明確標記平台特定進度，例如 `Codex-only`、`Gemini pending` 或 `Antigravity pending`。

## 提醒行為

記憶更新提醒和記憶壓縮提醒是分開的。

更新提醒只應在 repository changes 持續 pending 多個 Agent responses，且記憶尚未更新時出現。

壓縮提醒只應在 memory 大到需要行動時出現，或在明確的記憶稽核與壓縮 workflow 中出現。

GUI 不應在每次回覆後重複顯示「不需要壓縮」訊息。

## 疑難排解

如果記憶沒有被注入：

- 確認 agent-specific SessionStart hook 已啟用。
- 確認 `.agents/memory/MEMORY.md` 存在。
- 確認 project-local agent configuration layer 已被信任。

如果提醒太吵：

- 檢查 Stop 或 AfterAgent hook 是否印出 lean/healthy memory 報告。
- 除非需要行動，否則偏好靜默更新狀態。

如果 worktree memory 分歧：

- 只整合持久 lesson、decision 與目前交接狀態。
- 避免把過時的任務流水帳複製回 main workspace。

如果編碼看起來錯誤：

- 確認檔案是 UTF-8 without BOM。
- 不要用舊版 Windows console 的輸出判斷檔案損壞；請用 repository file hygiene script 驗證。
