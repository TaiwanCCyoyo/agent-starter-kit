[English Version](../../README.md)
# AI Agent Starter Kit

這是一套標準化、低摩擦的多 Agent 工程基礎設施，支援 Codex、Claude Code 與 Antigravity。當你希望新專案中的各種 Agent 能快速理解任務、記憶、規則、工作流程與驗證要求時，可以把本 repository 當作模板使用。

## 核心理念

1. **長期記憶持久化**：Codex 透過 `.memories/memories/MEMORY.md` 與 `.memories/memory_store.db` 保存跨 session 的專案記憶。
2. **Agent 專屬啟動層**：每個 Agent 擁有自己的原生 instruction 與 hook 層，但共用同一份專案記憶。
3. **自動化維護**：格式化、lint、檔案衛生檢查與記憶提醒由 Agent hooks 與 repository 驗證腳本執行。
4. **原生安全檢查**：透過 `detect-secrets` 整合 pre-commit secret scanning。
5. **編碼與語言一致性**：驗證 repository 檔案使用 UTF-8 without BOM，並遵守語言邊界。
6. **驗證優先**：Agent 在進行非瑣碎變更前須先說明驗證計畫，修改後執行驗證，並提供結果作為完成的證據。

## 記憶管理流程

本專案使用主動式記憶系統，維持跨 session 與 worktree 的長期上下文。

詳細架構、設定模型與複製清單請參考 [記憶系統介紹](memory-system-introduction.md)。

### 1. 日常使用

- **儲存記憶**：完成有意義的子任務後，透過對應 Agent workflow 更新 `.memories/memories/MEMORY.md` 或 `.memories/memory_store.db`。
- **自動提醒**：當 Agent 已經進行多輪工作且仍有 pending changes 時，hook 會提醒更新記憶。
- **記憶壓縮**：當 `MEMORY.md` 過大時，系統會提醒進行壓縮。

### 2. 多 Worktree 整合

使用多個 worktree 時，各 worktree 的記憶可能逐漸分歧。要把洞見合併回主 repository：

1. 使用目前 Agent 的 worktree workflow：
   ```bash
   /worktree finish <path/to/worktree>
   ```
2. Agent 會執行 AI semantic consolidation，將高價值的 `Lessons Learned` 與 `Done` 項目合併回主要 `MEMORY.md`。

### 3. Agent 工作流程

- **Codex**：使用原生 Plan Mode、`.codex/skills/` 裡的 repo-scoped skills，以及 `.codex/agents/` 裡的專職 reviewer agents。Command-like skills 可以用 `/gen-commit` 這類純文字呼叫，但不會註冊成真正的 slash command。詳細內容請見 [Codex 元件參考](codex-components.md)。
- **Claude Code**：使用 `.claude/commands/` 裡已註冊的 slash commands（例如 `/gen-commit`、`/worktree`、`/learn-eval`）。子代理人定義在 `.claude/agents/`。Path-scoped 程式碼規範放在 `.claude/rules/`。完整元件清單請參考 [Claude Code 元件參考](claude-components.md)。
- **Antigravity**：使用 `.agent/workflows/`、`.agent/rules/` 與 `.agent/skills/`。完整元件與 hooks 請參考 [Antigravity 元件參考指南](antigravity-components.md)。

## 自動化 Hooks 與生命週期

本 repository 使用各 Agent 原生 hooks 維護系統一致性：

| Agent | Hook 類型 | 用途 | Script |
| :--- | :--- | :--- | :--- |
| **Codex** | `SessionStart` | 注入 `.codex/AGENTS.md`、專案記憶、分支與 worktree 上下文。 | `.codex/hooks/session_start.py` |
| **Codex** | `PostToolUse` | 執行 targeted post-edit hygiene。Python 檔會 format、lint、檢查 file hygiene，並提醒 `print()` calls；文件與設定檔只跑 file hygiene。 | `.codex/hooks/post_tool_use_hygiene.py`, `scripts/python_hygiene.py`, `scripts/file_hygiene.py` |
| **Codex** | `Stop` | 有 pending changes 且經過多輪回覆後提醒 Codex 更新記憶，並檢查記憶大小。 | `.codex/hooks/stop_memory_check.py` |
| **Claude Code** | `SessionStart` | 注入 `CLAUDE.md`、專案記憶、分支與 worktree 上下文。 | `.claude/hooks/session_start.py` |
| **Claude Code** | `PostToolUse` | 針對 `.py` 檔：自動執行 `ruff format` 排版、`ruff check --fix` lint、`mypy` 型別檢查，並警告 `print()` 用法。針對設定檔與文件：驗證檔案衛生。 | `.claude/hooks/post_tool_use_hygiene.py` |
| **Claude Code** | `Stop` | 有 pending changes 且經過多輪回覆後提醒 Claude 更新記憶，檢查記憶大小，並在 session 達到一定規模後提示技能審查。 | `.claude/hooks/stop_memory_check.py` |
| **Antigravity** | `SessionStart` | 初始化 SQLite、複製 worktree 缺少的記憶，並注入 bounded files。 | `.agent/hooks/session_start.py` |
| **Antigravity** | `PostToolUse` | 針對修改檔案執行 Ruff、mypy 與 file hygiene。 | `.agent/hooks/post_tool_use_hygiene.py` |
| **Antigravity** | `Stop` | 檢查 bounded-file 限制與嚴格 memory taxonomy。 | `.agent/hooks/stop_memory_check.py` |

### Hook 疑難排解

如果 hooks 沒有觸發：

1. 確認 Git hooks 已安裝：
   ```bash
   uv run pre-commit install
   ```
2. Codex：檢查 `.codex/config.toml` 是否啟用 `codex_hooks`，以及 `.codex/hooks.json` 是否指向 `.codex/hooks/`。
3. Claude Code：檢查 `.claude/settings.json` 是否有 `hooks` 區塊；若 hooks 是在 session 中途新增的，請在 Claude Code UI 中開啟 `/hooks` 重新載入設定。
4. Antigravity：檢查 `.agent/hooks.json` 是否正確定義事件。
5. 確認 Agent 已信任 project-local configuration layer。

## 權限與安全政策設定

各 Agent 層皆附有自己的權限設定。共通原則：自動允許安全的讀取與非破壞性操作；需確認才可執行發布動作（`git push`）；封鎖破壞性或會直接修改 `.git` 的指令。

### Claude Code（`.claude/settings.json`）

權限宣告在 `.claude/settings.json`，不需修改全域設定即可生效：

- **自動允許 (allow)**：workspace 內所有讀寫、常用 CLI 工具（`ls`、`cat`、`grep`、`find`、`diff`、`uv`、`ruff`、`pytest`、`npm`、`jq` 等），以及安全的 git 操作（`status`、`diff`、`log`、`add`、`commit`、`fetch`、`branch`、`merge` 等）。
- **需要確認 (ask)**：`git push`，防止意外推送到遠端。
- **封鎖 (deny)**：`git push --force`、`git push --force-with-lease`、任何刪除或修改 `.git` 目錄的指令（`rm -rf .git`、`rd /s`、`Remove-Item -Recurse … .git`），以及直接呼叫 `powershell`/`pwsh`（指令應直接執行，不透過殼層包裝）。

### Codex

Codex 在本 starter kit 不提供 repository-local permission rules。Permission review 交由已設定的 approvals reviewer 處理，例如「代我審核」/ auto-review workflow，而不是 `.codex/rules/`。

Codex 的規劃由主 agent 透過 Plan Mode 承擔；本 starter kit 不新增獨立的 Codex planner agent。

## CI/CD Setup

Agent 透過 hooks 在本地端執行品質把關，但 CI pipeline 能在每次推送時捕捉問題，並讓整個團隊看到品質閘道的狀態。本節提供一個最精簡的起點。

### 建議的 GitHub Actions Workflow

在你的專案中建立 `.github/workflows/ci.yml`：

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install uv && uv sync --group dev

      - name: Lint
        run: uv run ruff check --fix .

      - name: Type check
        run: uv run mypy .

      - name: Test
        run: uv run pytest

      - name: Secret scan
        run: uv run pre-commit run detect-secrets --all-files
```

請調整 `pytest` 步驟以符合你的專案測試目錄，並將 Python 版本調整為與 `.python-version` 一致。

### 何時使用 `github-ops` 技能

CI 設定完成後，可透過 Claude Code 使用 `github-ops` 技能執行日常操作：

| 任務 | 指令 |
| :--- | :--- |
| 查看失敗執行的日誌 | `gh run view <run-id> --log-failed` |
| 重新執行失敗步驟 | `gh run rerun <run-id> --failed` |
| 列出最近的失敗記錄 | `gh run list --status failure --limit 10` |
| 檢查 Dependabot 警示 | `gh api repos/{owner}/{repo}/dependabot/alerts` |

需先安裝 `gh` CLI 並完成驗證（`gh auth login`）。

### CI 失敗疑難排解

1. **先在本地重現** — 在遠端調查之前，先執行 workflow 所使用的相同指令（`ruff check --fix .`、`mypy .`、`pytest`）。
2. **閱讀完整日誌** — `gh run view <run-id> --log-failed` 只會顯示失敗步驟的輸出。
3. **檢查環境差異** — Python 版本不符、缺少環境變數或未執行 `uv sync` 是最常見的原因。
4. **區分偶發性失敗與真實錯誤** — 若同一個測試在本地通過但在遠端持續失敗，通常是環境問題，而非偶發性不穩定測試。

## 模板使用方式

套用到新專案時，依照支援的工具複製對應的 Agent 基礎設施：

| Path | 用途 |
| :--- | :--- |
| `.memories/` | Git-ignored 的本機長期記憶：`MEMORY.md`、`USER.md` 與 SQLite `memory_store.db`。 |
| `.agents/` | 可提交至 Git 的共用 Agent 基礎設施。 |
| `.agent/` | Antigravity rules、skills、workflows。 |
| `.codex/` | Codex instructions、hooks、private command-like skills、specialist agents。 |
| `.claude/` | Claude Code settings、hooks、slash commands、subagents、skills 與 path-scoped 程式碼規範。 |
| `scripts/` | Repository 層級的檔案衛生與格式化腳本，供 Git 與 Agent adapters 呼叫。 |
| `.pre-commit-config.yaml` | Repository 層級驗證 hooks。 |

複製後，請初始化 `.memories/memories/MEMORY.md`，檢查各 Agent 專屬規則，使用 `uv run pre-commit install` 安裝 hooks，並以 `uv run ruff check --fix .` 驗證。

### 整合 Superpowers 技能

本儲存庫在三個 Agent 中均整合了 superpowers 能力：

- **Claude Code**：官方外掛 `superpowers@claude-plugins-official` 已於 `.claude/settings.json` 啟用，無需手動安裝，自動生效。
- **Antigravity**：源自開源專案 [obra/superpowers](https://github.com/obra/superpowers) 的一系列精選技能已複製至 `.agent/skills/`，並遵守 MIT 授權條款（版權所有 (c) 2026 Jesse Vincent）。
- **Codex**：Superpowers plugin 已安裝並啟用；repository instructions 會將其 workflows 限制在 Codex 的 approval、delegation、commit 與 branch safety 規則內。

## 設計來源

本 starter kit 的架構設計受到兩個開源專案的啟發：

- **[Everything Claude Code (ECC)](https://github.com/affaan-m/ECC)** — 提供生產就緒的 agents、skills、hooks、commands 與 rules。專職 agents（`code-reviewer`、`tdd-guide`、`security-reviewer` 等）、程式碼規範，以及 `CLAUDE.md` 中的 Prompt Defense Baseline，均移植或改編自 ECC v2.0.0-rc.1。大多數開發用 slash commands 已陸續退役，改以 Native Plan Mode、Superpowers 與 autoloaded skills 取代。

- **[Hermes Agent (NousResearch)](https://github.com/NousResearch/hermes-agent)** — 本專案參考其有限容量的 `MEMORY.md`／`USER.md`、frozen prompt snapshot、SQLite FTS5 session recall 與 learning loop，再依 starter kit 需求改編，而不是直接移植 Hermes。

## 初始化

要初始化此儲存庫並設定驗證工具：

1. **安裝 Git Hooks**
   ```bash
   uv run pre-commit install
   ```
2. **安裝開發相依套件**（包含 mypy 型別檢查器）
   ```bash
   uv sync --group dev
   ```
3. **驗證環境設定**
   ```bash
   uv run ruff check --fix .
   ```
4. **設定 Antigravity MCP**

   Antigravity 的 SQLite `memory-db` MCP server 必須設定在平台支援的全域設定中，例如使用者家目錄下的 `~/.mcp.json`。

### 為新專案初始化記憶
儲存庫初始化完成後：
1. 請確認 `.memories/memories/MEMORY.md` 已記錄必要的專案長期資訊。

---

本專案要求 source code、技術文件、workflows 與 configuration 使用 UTF-8 without BOM 並以英文撰寫。繁體中文內容應放在 `docs/zh-TW/` 與 `.memories/`。
