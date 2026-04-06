[English Version (英文版) 🇬🇧](../README.md)

# 🚀 AI Agent Starter Kit

專案的終極長期目標，是為**市面上所有主流的 AI Agent 工具**（例如 Cursor, Claude Code, Gemini CLI, Antigravity 等）量身打造一個共用的專案初始設定包 (Starter Kit)。它提供了標準化的底層工程設施（如 Pre-commit）與工作流程，確保所有 AI 在執行高度自治任務時，能在一個安全、乾淨的環境中運作。

目前的實作首航與架構**特別針對 Antigravity 進行了深度優化**。由於各個 Agent 的自訂掛鉤機制不同，我們將專屬 Antigravity 的客製化設定與自動化指令隔離在 `.agent/` 目錄中，並期望未來持續擴充對其他 Agent 的專屬支援。

## 🧠 核心哲學

1. **長期記憶 (Long-Term Memory)**：Agent 會透過 `.agents/memory/MEMORY.md` 紀錄專案的長期目標、最佳實踐與防呆經驗。這能克服跨 Session 時 AI 發生的「失憶症」。
2. **基底防護網 (Native Pre-Commit)**：拋棄老舊且不可靠的 AI 文字指令檢查，我們直接將安全性掃描（Gitleaks/detect-secrets）與程式碼排版（Ruff）整合在原生的 Git `pre-commit` 框架中。不管是人類還是 AI，只要下了 git commit 就必須通過這道防護網。
3. **驗證優先 (Verification-First)**：Agent 完成程式碼修改後，禁止僅憑猜測宣稱完成，必須主動提供測試 Log、腳本驗證或終端機結果。

## 📂 系統架構

為了不污染使用者的正式原始碼，所有左右 Agent 行為的規則與檔案，皆隱藏於 `.agent/` 目錄下，這也是各種 Agent 預設支援讀取的內部掛載點。

* **`.agent/rules/`**：Agent 的最高決策原則（包含驗證規範、協作除錯 SOP）。
* **`.agent/workflows/`**：由 Agent 執行的自動化任務腳本，包含記憶體自動壓縮 (`/compress-memory`) 與快速筆記 (`/save-memory`)。
* **`.agent/skills/`**：延伸能力工具箱與外部功能掛載。
* **`.agents/memory/MEMORY.md`**：專屬本專案的歷史變遷記錄簿，是 Agent 執行任何任務前必讀的「大腦」。

## ⚙️ 初始化指南 (How to Initialize - 給 AI Agent 的指示)

**人類開發者**：當你使用此模板開啟全新專案時，只需對你的 AI Agent（如 Antigravity）下達指令：
> *「請參照 README 幫我初始化專案。」*

**AI Agent 指令**：當你收到上方的人類請求時，你必須**自動且依序**執行以下三個任務：

### 第一步：建立並同步專案大腦 (Memory)
請檢查 `.agents/memory/MEMORY.md` 是否存在，若不存在：
1. 執行 `cp .agents/memory/MEMORY.example.md .agents/memory/MEMORY.md`
2. **全面初始化大腦**：絕對不要讓檔案留有空白預設值！你必須主動掃描當前專案的 README、設定檔與目錄結構。根據你的分析，全面填寫 `MEMORY.md` 的所有相關區塊（包括但不限於：專案目標定位、技術堆疊、與初步的開發者偏好），以此奠定堅實的上下文基礎。

### 第二步：確保環境依賴與套件同步
本專案嚴重依賴 **[uv](https://astral.sh/)** 作為極速套件管理器。
1. 檢查全域環境是否已安裝 `uv`。
   - 若未安裝，執行：`powershell -c "irm https://astral-sh.uv.run/install.ps1 | iex"`
2. 同步環境：
   - 執行 `uv sync` 以安裝所有設定檔內的開發依賴。

### 第三步：掛載底層安全防護網 (Pre-Commit Hooks)
**這是最重要的一步！** 你必須確保原生的 Git hook 被安裝，以阻擋任何明文密碼被 Commit 到版控中。
- 執行 `uv run pre-commit install`
- 驗證指令是否順利完成。

---

*專為邁向 Agent 世代的高效、無縫防禦開發體驗而生。*
