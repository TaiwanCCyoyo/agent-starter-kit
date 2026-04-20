[English Version (英文版本)](../../README.md)
# AI Agent Starter Kit

這是一個標準化的、無摩擦的 AI Agent 工程基礎設施，專為多 Agent 生態系統（如 Gemini CLI、Antigravity 等）設計。

## 🚀 核心理念

1. **長期記憶持久化 (Long-Term Memory)**：Agent 會透過 `.agents/memory/MEMORY.md` 追蹤專案目標與經驗教訓，消除上下文遺忘。
2. **自動化維護 (Automated Maintenance)**：Python 格式化 (`ruff`) 與檔案衛生檢查（UTF-8、英文限制）透過 Gemini CLI `AfterTool` hook與 Git `pre-commit` hook**完全自動化**執行。
3. **原生安全掃描 (Native Security)**：`detect-secrets` 已整合至 pre-commit 工作流，確保金鑰與敏感資訊不會被提交。
4. **自動授權政策 (Auto-Approval Policies)**：標準化任務（如 `.agents/memory/` 內的更新）在 Gemini CLI 中為自動授權，以減少中斷。
5. **編碼與語言完整性 (Encoding & Language Integrity)**：核心邏輯強制使用 UTF-8 編碼與英文內容，由 `AfterTool` 與 `pre-commit` 執行驗證。
6. **驗證優先執行 (Verification-First)**：Agent 在報告任務完成前，必須提供實質的驗證證據（腳本執行、測試結果）。

## 🧠 記憶管理工作流

本專案使用主動式記憶系統來維持跨 Session 與跨 Worktree 的長期脈絡。

### 1. 日常使用
- **保存記憶**：當您完成子任務時，請使用 `/save-memory`。Agent 會自動更新 `Done` 區塊。
- **自動提醒 (Auto-Nudge)**：如果 Agent 修改了檔案但忘記更新 `MEMORY.md`，系統hook會自動發出提醒。

### 2. 多工作區匯合 (Multi-Worktree Consolidation)
當同時使用多個 Worktree 時，各地的記憶會自然產生分歧。若要將洞察帶回主倉庫：
1. 執行匯合工具：
   ```bash
   uv run python .gemini/skills/worktree-manager/scripts/memory_consolidator.py /path/to/worktree
   ```
2. 根據工具建議，將高價值的 `Lessons Learned` 與 `Done` 項目合併至主倉庫的 `MEMORY.md`。

### 3. 記憶壓縮
若 `MEMORY.md` 變得過於臃腫（超過 2000 tokens），系統會建議壓縮。請執行：
- `/compress-memory`：將舊的 `Done` 項目總結為單一歷史紀錄，保持上下文精簡。

## 🪝 自動化hook與生命週期 (Automated Hooks & Lifecycle)

本儲存庫利用多個hook來維護系統完整性：

| hook類型 | 名稱 | 用途 | 腳本 |
| :--- | :--- | :--- | :--- |
| **Git** | `pre-commit` | 語法檢查、格式化與金鑰掃描。 | `.pre-commit-config.yaml` |
| **Git** | `post-checkout` | 在新 Worktree 中初始化記憶與hook。 | `scripts/git_post_checkout.py` |
| **Gemini CLI** | `SessionStart` | 載入專案記憶與分支上下文。 | `scripts/session_start.py` |
| **Gemini CLI** | `AfterTool` | 格式化程式碼並驗證檔案衛生。 | `scripts/file_hygiene.py` |
| **Gemini CLI** | `AfterAgent` | 在檔案變動後提醒 Agent 更新記憶。 | `scripts/memory_nudger.py` |

### hook故障排除
如果hook沒有觸發：
1. 確保已執行 `uv run pre-commit install --hook-type pre-commit --hook-type pre-push`。
2. 檢查 `.git/hooks/post-checkout` 是否存在且具備執行權限。
3. 驗證 `.gemini/settings.json` 中的 `matcher` 與 `command` 路徑是否正確。

## 🏗️ 系統架構
...

不同 Agent 的協議與工作流已進行隔離：

* **`.agent/`**：**Antigravity 特定**的規則與工作流。
* **`.gemini/`**：**Gemini CLI 特定**的政策、技能與hook。
* **`.agents/memory/`**：**共享**的狀態大腦（Git-ignored）。

## 🛠️ 如何初始化

**開發人員**：
請直接向您的 AI 助手下達指令：*"請按照 README 初始化此儲存庫。"*

**AI Agent 指令**：
當被要求初始化專案時，您必須獨立執行以下步驟：
1. **啟動記憶體**：將 `.agents/memory/MEMORY.example.md` 複製為 `.agents/memory/MEMORY.md`。
   - **關鍵步驟**：您必須立即根據目前的 `README.md` 與專案脈絡填充 `MEMORY.md` 中的 **Mission**（任務目標）區塊，以建立此 Session 的「靈魂」。
2. **安裝 Hook**：執行以下指令安裝標準與自定義 Hook：
   ```bash
   uv run pre-commit install
   # 註冊同步協議 (Linux/macOS)
   printf "#!/bin/bash\nuv run python scripts/git_post_checkout.py \"\$@\"" > .git/hooks/post-checkout
   chmod +x .git/hooks/post-checkout
   ```
3. **驗證設定**：執行 `uv run ruff check .` 確保環境就緒。

---
*注意：本專案強制要求使用 **UTF-8 (without BOM)** 編碼，且技術文件與程式碼必須使用 **英文**。*
