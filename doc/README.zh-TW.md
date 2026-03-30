[English Version (英文版) 🇬🇧](./README.md)

# 🚀 Agent Starter Kit

這是一個專為 AI IDE 與 CLI 工具（例如 Antigravity, Claude Code, Cursor）量身打造的高自治度、擁有多 Agent 協作潛力、且具備自我演化能力的開發模板。

本套件立基於四大核心哲學：**驗證優先執行**、**長期記憶持久化**、**動態進化的安全 SOP**，以及**預設的不重複造輪子原則**。

## 🧠 核心運作原則

1. **驗證優先 (Verification-First)**：Agent 完成任務時必須提供實質證據（例如測試 Log 或執行結果）。若任務需要人類授權（如網頁登入），Agent **必須**在最初的計畫階段就主動提出要求，避免中途卡死。
2. **會進化的提交防護 (Evolving Pre-Commit)**：每次 `git commit` 前，Agent 必須嚴格執行 `pre-commit-sop.md`。第一條永遠是強制性的金鑰掃描（如 `gitleaks`）；隨著專案加入新語言或工具，Agent 有責任主動將新的 Lint 與測試檢查更新入該 SOP 中。
3. **長期記憶 (Long-Term Memory)**：Agent 會透過 `.agents/memory/MEMORY.md` 紀錄專案的架構決策與使用習慣。這樣能確保不同 Session 的 Agent 也能無縫接軌。（註：請複製 `memory/MEMORY.example.md` 當作全新專案的記憶起點）。
4. **團隊協作自舉 (Team Bootstrapping)**：當底層工具尚不支援原生子 Agent 喚醒時，主 Agent 被賦予了「向人類尋求腳本協助」的權利，以透過 CLI 背景執行的方式創造出子 Agent 來執行特定職務（定義於 `TEAM.md` 中）。
5. **高度重用 (Reuse)**：內建了強大的 **Claude 官方 `skill-creator`**（源自官方技能庫 [anthropics/skills](https://github.com/anthropics/skills)），確保 Agent 在撰寫新功能時，擁有標準化的生成、測試、基準驗證與部署迴圈。

## 📂 系統架構

所有左右 Agent 思維與行為的檔案，皆靜靜地配置於系統預設讀取的 `.agents/` 目錄下：

* **`.agents/rules/`**：大腦最高指導原則（涵蓋資安底線、委派邏輯與記憶觸發要件）。
* **`.agents/workflows/`**：標準作業程序（包含嚴謹的預提交防線與驗證迴圈）。
* **`.agents/skills/`**：延伸能力工具箱（包含內建技能製造機與備援的委派子程式）。
* **`.agents/memory/MEMORY.example.md`**：專屬本專案的歷史變遷記錄簿模板。
* **`.agents/TEAM.yaml`**：專案子角色清單，供主 Agent 分配資源使用。

## ⚙️ 環境設定 (Local Setup)

本專案使用 **[uv](https://github.com/astral-sh/uv)** 作為高效能的 Python 套件管理與虛擬環境工具。

### 1. 安裝環境
確保您的系統已安裝 `uv`：
```powershell
powershell -c "irm https://astral-sh.uv.run/install.ps1 | iex"
```

### 2. 初始化本地環境
在專案根目錄執行以下指令，以建立本地 `.venv` 並安裝所有必要的依賴（如 `pyyaml`）：
```powershell
uv sync
```

### 3. 執行 Subagent 調度
若要使用 `delegate-task` 技能啟動本地環境：
```powershell
uv run .agents/skills/delegate-task/delegate.py --role Feature_Developer --task "您的任務內容"
```

使用 `uv run` 會確保腳本在正確的本地虛擬環境中執行，且不會干擾您的全局 Python 安裝。

---

---
*專為邁向 AGI 世代的高效、安全、無縫接軌開發體驗而生。*

## 💡 推薦工具
為了獲得最佳的安全與開發體驗，強烈建議安裝以下工具：
- **[Gitleaks](https://github.com/gitleaks/gitleaks)**：內建的 `security-scanner` 技能將優先使用它進行強大的金鑰掃描。
- **[Pre-commit](https://pre-commit.com/)**：用於更專業地管理 Git Hook 生命週期。
