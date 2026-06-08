# 記憶系統介紹

Hermes 提供的靈感是有限容量的 `MEMORY.md`／`USER.md`、凍結 prompt snapshot、完整 session 搜尋與 learning loop。本 starter kit 直接依各儲存位置的載入與保留行為描述用途，不另外增加分層術語。

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
| `.agents/memory/MEMORY.md` | Session-start 專案上下文：任務、約束、目前狀態。≤ 2,200 chars。 |
| `.agents/memory/USER.md` | 跨 Agent 使用者偏好：溝通語言、工作風格。≤ 500 chars。 |
| `.agents/memory/decisions.md` | 需要時讀取的活躍持久架構決策。 |
| `.agents/memory/lessons.md` | 需要時讀取的簡潔重複性教訓（尾部由 Claude 與 Codex 自動載入）。 |
| `.agents/memory/changes/` | 活躍多步驟變更計畫（proposal、design、tasks）。 |
| `.agents/memory/memory.db` | 共用可搜尋歷史：SQLite FTS5，儲存已畢業的教訓、決策、workflow、candidate 與 session 元資料（Claude Code 與 Codex MCP）。 |
| `.agents/memory/archive/` | 檔案式歷史：已完成的變更計畫與參考資料。 |
| SessionStart hooks | 在 session 開始時注入一次 `MEMORY.md` + `USER.md`（凍結快照），同時為 Claude 注入 `lessons.md` 尾部。 |
| Stop/AfterAgent reminders | 在有程式碼變更後提醒更新記憶；超過 5 次回覆後提示技能審查。 |
| `memory-manager` | 完整記憶結構的路由規則、生命週期與健康標準。 |
| `memory-sql` | Claude Code 與 Codex skills，透過各平台原生 MCP 設定查詢和寫入共用 `memory.db`。 |
| `learn-eval` / `skill-curator` | session 模式萃取的品質門，確認後才寫入 skill 檔案。 |
| Worktree sync | 在第一次 session 時從主 repo 複製記憶到新 worktree。 |

## Agent 整合

### Codex

Codex 使用：

- `.codex/hooks/session_start.py` 注入 `.codex/AGENTS.md`、分支上下文與 `.agents/memory/MEMORY.md`。
- `.codex/hooks/stop_memory_check.py` 發出低噪音的記憶更新與壓縮提醒。
- `.codex/skills/save-memory/SKILL.md`、`.codex/skills/compress-memory/SKILL.md` 與 `.codex/skills/memory-manager/SKILL.md`。

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
| `scripts/` | 需要 repository 層級 hygiene scripts。 | 保留 Git-facing baseline scripts，Agent 專屬邏輯放在各自 adapter。 |
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

## 技能演進迴圈（Claude Code）

除了把事實存入記憶檔之外，Claude Code 還能把 session 模式萃取為可重用的 skill 檔案：

1. Stop hook（`stop_memory_check.py`）計算有程式碼變更的回覆次數。超過 5 次後提示執行 `/learn-eval`。
2. `/learn-eval` 遵循 `.claude/skills/skill-curator/SKILL.md` 的完整流程：
   - 識別值得保存的信號（使用者糾錯、非顯而易見的技巧、可重用 workflow）。
   - 以清單確認與既有 skills 的重疊程度（品質門）。
   - 發出整體判定：Save / Improve then Save / Absorb into existing / Drop。
   - 僅在使用者核准後儲存。
3. Skills 存放於 `.claude/skills/learned/`（專案特定）或 `~/.claude/skills/learned/`（跨專案）。
4. `skill-curator` skill 也管理生命週期：skills 隨時間推移經歷 active → stale → archived 狀態。

此迴圈為手動觸發並需使用者確認——不會在未經核准的情況下寫入 skill 檔案。

## 記憶寫入模型

**凍結快照**：`MEMORY.md` 與 `USER.md` 在 session 開始時注入一次。工具寫入立即生效於磁碟，但不會更新正在執行的 session 系統提示；下一個 session 才會讀取更新後的檔案。這可保留 LLM 前綴快取。

**§ 分隔符**：當記憶區塊包含多個原子條目時，以單獨一行的 `§` 分隔，便於可靠解析。

**Transcript capture 與記憶整理是兩件事**：Hermes 會保存並索引每一則 user、assistant 與 tool message，讓 `session_search` 能回傳實際歷史訊息。這不代表自動挑選重要內容；重要事實仍需另外整理到有限容量 memory 或 skills。本 starter kit 目前保存精選條目，沒有保存完整訊息串。

## 提醒行為

記憶更新提醒和記憶壓縮提醒是分開的。

更新提醒只應在 repository changes 持續 pending 多個 Agent responses，且記憶尚未更新時出現。

壓縮提醒只應在 memory 大到需要行動時出現，或在明確的記憶稽核與壓縮 workflow 中出現。

技能審查提醒每個 session 只出現一次（超過最低程式碼變更回覆次數後），不會重複出現。

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
