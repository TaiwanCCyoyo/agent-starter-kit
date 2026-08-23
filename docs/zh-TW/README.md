[English Version](../../README.md)

# AI Agent Starter Kit

這是一套標準化、低摩擦的多 Agent 工程基礎設施，支援 Codex、Claude Code 與 Antigravity。當你希望新專案中的各種 Agent 能快速理解規則、工作流程與驗證要求時，可以把本 repository 當作模板使用。

## 核心理念

1. **Agent 原生 Context**：Codex 與 Claude Code 使用各自的原生 local memory；必要專案知識保留在版本控制 guidance。
2. **Agent 專屬啟動層**：每個 Agent 擁有自己的原生 instruction 與 hook 層。
3. **自動化維護**：格式化、lint 與檔案衛生檢查由 Agent hooks 與 repository 驗證腳本執行。
4. **原生安全檢查**：透過 `detect-secrets` 整合 pre-commit secret scanning。
5. **編碼與語言一致性**：驗證 repository 檔案使用 UTF-8 without BOM，並遵守語言邊界。
6. **驗證優先**：Agent 在進行非瑣碎變更前須先說明驗證計畫，修改後執行驗證，並提供結果作為完成的證據。

## 目前預設值

- **共用開發規則**：Codex 與 Claude Code 採用同一套階段路由：原生規劃負責 plan，repository-owned skills 與直接驗證負責實作工作，品質與安全由專用 reviewers 處理，commit/PR 流程有明確 owner。
- **分層驗證**：Claude Code 透過官方 Pyright LSP plugin 與唯讀的 Ruff `E722,F601,F602,F634` check 取得即時 diagnostics；Codex 因沒有 Python LSP，對 Python 編輯使用較廣的唯讀 Ruff `F` check。兩者都會在完成前執行 pre-commit，由其統一負責 formatting、linting、型別檢查與檔案驗證。
- **安全審查契約**：涉及安全敏感面的變更會路由到 dedicated security reviewers；任何 `CRITICAL` security 或 data-loss 風險都必須先修正，不能直接宣告完成。
- **低成本外部委派**：安裝 Antigravity CLI 時，可用 `agy -p --mode plan --sandbox` 處理範圍明確、唯讀的 research、inspection、review 或 mechanical analysis。呼叫端保留最終判斷；若 Antigravity 回報 quota exhausted，改用其他合適路徑。
- **編輯器衛生**：`.vscode/settings.json` 會移除行尾空白、保留單一 final newline、啟用 Python Ruff formatting，並將產生的 cache 與本機 agent state 排除於搜尋與 watcher 之外。

## Agent 記憶與工作流程

- **Codex memory**：`.codex/config.toml` 會啟用原生 local memories，資料存放於 repository 外的使用者 Codex home；使用 `/memories` 控制單一 chat。必要 project rules 仍放在 checked-in guidance。
- **Claude Code memory**：Claude 使用內建記憶，repository conventions 則寫入 `CLAUDE.md`、rules、文件或 skills。
- **Antigravity**：本 repository 不提供跨 session 記憶庫；耐久知識應放在 checked-in artifacts 與 Git history。

### Agent 工作流程

- **Codex**：使用原生 Plan Mode、`.codex/skills/` 裡的 repo-scoped skills，以及 `.codex/agents/` 裡的專職 reviewer agents。其 `antigravity-subagent` skill 會將符合條件的低成本外部委派路由至 headless `agy -p`。Command-like skills 可以用 `/gen-commit` 這類純文字呼叫，但不會註冊成真正的 slash command。詳細內容請見 [Codex 元件參考](codex-components.md)。
- **Claude Code**：使用 `.claude/commands/` 裡已註冊的 slash commands（例如 `/gen-commit`、`/worktree`）。子代理人定義在 `.claude/agents/`。Path-scoped 程式碼規範放在 `.claude/rules/`。完整元件清單請參考 [Claude Code 元件參考](claude-components.md)。
- **Antigravity**：使用根目錄 `GEMINI.md` 作為核心契約，並以 `.agent/workflows/` 提供自訂斜線指令（例如 `/gen-commit`、`/worktree`）、`.agent/skills/` 存放 repo-scoped skills，以及 `.agent/hooks.json` 定義生命週期勾子。完整元件與 hooks 請參考 [Antigravity 元件參考指南](antigravity-components.md)。

## 自動化 Hooks 與生命週期

本 repository 使用各 Agent 原生 hooks 維護系統一致性：

| Agent           | Hook 類型      | 用途                                                               | Script                                   |
| :-------------- | :------------- | :----------------------------------------------------------------- | :--------------------------------------- |
| **Codex**       | `SessionStart` | 注入 `.codex/AGENTS.md`、branch、worktree 與 last-commit context。 | `.codex/hooks/session_start.py`          |
| **Codex**       | `PostToolUse`  | 對修改後的 Python 檔案回報唯讀的 Ruff `F` diagnostics。            | `.codex/hooks/post_tool_use_hygiene.py`  |
| **Claude Code** | `PostToolUse`  | 回報補充 Pyright 的唯讀 Ruff `E722,F601,F602,F634` diagnostics。   | `.claude/hooks/post_tool_use_hygiene.py` |
| **Antigravity** | `SessionStart` | 回報目前 branch 與 workspace 是否為 worktree。                     | `.agent/hooks/session_start.py`          |
| **Antigravity** | `PostToolUse`  | 對修改後的 Python 檔案回報唯讀的 Ruff `E722,F601,F602,F634` 診斷。 | `.agent/hooks/post_tool_use_hygiene.py`  |

### Hook 疑難排解

如果 hooks 沒有觸發：

1. 確認 Git hooks 已安裝：
    ```bash
    uv run pre-commit install
    ```
2. Codex：檢查 `.codex/config.toml` 是否啟用 `hooks` 與 `memories`，以及 `.codex/hooks.json` 是否指向 `.codex/hooks/`。
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

### GitHub CLI 操作

CI 設定完成後，可直接使用 `gh` 執行日常操作。Dependabot 警示的讀取與修復由共用的 `dependabot-remediation` skill 負責。

| 任務               | 指令                                      |
| :----------------- | :---------------------------------------- |
| 查看失敗執行的日誌 | `gh run view <run-id> --log-failed`       |
| 重新執行失敗步驟   | `gh run rerun <run-id> --failed`          |
| 列出最近的失敗記錄 | `gh run list --status failure --limit 10` |

需先安裝 `gh` CLI 並完成驗證（`gh auth login`）。

### CI 失敗疑難排解

1. **先在本地重現** — 在遠端調查之前，先執行 workflow 所使用的相同指令（`ruff check --fix .`、`mypy .`、`pytest`）。
2. **閱讀完整日誌** — `gh run view <run-id> --log-failed` 只會顯示失敗步驟的輸出。
3. **檢查環境差異** — Python 版本不符、缺少環境變數或未執行 `uv sync` 是最常見的原因。
4. **區分偶發性失敗與真實錯誤** — 若同一個測試在本地通過但在遠端持續失敗，通常是環境問題，而非偶發性不穩定測試。

## 模板使用方式

套用到新專案時，依照支援的工具複製對應的 Agent 基礎設施：

| Path                      | 用途                                                                                       |
| :------------------------ | :----------------------------------------------------------------------------------------- |
| `GEMINI.md`               | Antigravity 根目錄核心契約。                                                               |
| `.agent/`                 | Antigravity hooks、workflows（斜線指令）與 repo-scoped skills。                            |
| `.codex/`                 | Codex instructions、hooks、private command-like skills、specialist agents。                |
| `.claude/`                | Claude Code settings、hooks、slash commands、subagents、skills 與 path-scoped 程式碼規範。 |
| `.vscode/`                | 與 file hygiene 與 Python Ruff workflow 對齊的 workspace editor defaults。                 |
| `scripts/`                | Repository 層級的檔案衛生與格式化腳本，供 Git 與 Agent adapters 呼叫。                     |
| `.pre-commit-config.yaml` | Repository 層級驗證 hooks。                                                                |

複製後，請檢查各 Agent 專屬規則，使用 `uv run pre-commit install` 安裝 hooks，並以 `uv run ruff check --fix .` 驗證。

### Agent workflow plugins 與 skills 整合

本儲存庫依不同 Agent 採用不同方式整合原生能力、project-owned skills 與選用的 plugins：

- **Claude Code**：專案設定刻意停用 Superpowers、Ponytail 與 Karpathy plugins。工作流程由 Claude 原生能力，以及 project-owned 的 `.claude/` agents、commands、skills、rules 與 hooks 提供；GitHub、skill-creator 與 Pyright LSP 仍維持啟用。
- **Codex**：不依賴 Superpowers、Ponytail 或外部 Karpathy skills。工作流程由 Codex 原生能力、project-scoped agents 與 skills 提供；GitHub 整合則由可用的 GitHub plugin 提供。
- **Antigravity**：使用原生 Planning Mode、專屬根目錄 `GEMINI.md` 核心契約，以及 `.agent/skills/` 裡的 repo-scoped skills。其架構與 Claude Code、Codex 保持完全語意對齊，同時嚴格遵守命名空間隔離。

## 設計來源

本 starter kit 的架構設計受到一個開源專案的啟發：

- **[Everything Claude Code (ECC)](https://github.com/affaan-m/ECC)** — 提供生產就緒的 agents、skills、hooks、commands 與 rules。專職 agents（`code-reviewer`、`tdd-guide`、`security-reviewer` 等）、程式碼規範，以及 `CLAUDE.md` 中的 Prompt Defense Baseline，均移植或改編自 ECC v2.0.0-rc.1。大多數開發用 slash commands 已陸續退役，改以 Native Plan Mode 與 autoloaded project skills 取代。

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

---

本專案要求 source code、技術文件、workflows 與 configuration 使用 UTF-8 without BOM 並以英文撰寫。繁體中文內容應放在 `docs/zh-TW/`、`.references/` 與 `.tmp/`。
