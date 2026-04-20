[English Version (英文版本)](../../README.md)
# AI Agent Starter Kit

這是一個標準化的、無摩擦的 AI Agent 工程基礎設施，專為多 Agent 生態系統（如 Gemini CLI、Antigravity 等）設計。

## 🚀 核心理念

1. **長期記憶持久化 (Long-Term Memory)**：Agent 會透過 `.agents/memory/MEMORY.md` 追蹤專案目標與經驗教訓，消除上下文遺忘。
2. **自動化維護 (Automated Maintenance)**：Python 格式化 (`ruff`) 與檔案衛生檢查（UTF-8、英文限制）透過 Gemini CLI `AfterTool` 鉤子與 Git `pre-commit` 鉤子**完全自動化**執行。
3. **原生安全掃描 (Native Security)**：`detect-secrets` 已整合至 pre-commit 工作流，確保金鑰與敏感資訊不會被提交。
4. **自動授權政策 (Auto-Approval Policies)**：標準化任務（如 `.agents/memory/` 內的更新）在 Gemini CLI 中為自動授權，以減少中斷。
5. **編碼與語言完整性 (Encoding & Language Integrity)**：核心邏輯強制使用 UTF-8 編碼與英文內容，由 `AfterTool` 與 `pre-commit` 執行驗證。
6. **驗證優先執行 (Verification-First)**：Agent 在報告任務完成前，必須提供實質的驗證證據（腳本執行、測試結果）。

## 🏗️ 系統架構

不同 Agent 的協議與工作流已進行隔離：

* **`.agent/`**：**Antigravity 特定**的規則與工作流。
* **`.gemini/`**：**Gemini CLI 特定**的政策、技能與鉤子。
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
