[English](../../README.md)

# AI Agent Starter Kit

一套專案模板，讓 Codex 與 Claude Code 共享一份操作契約、配對式工具設置與相同的本地及 CI 驗證流程。

當你希望新專案中的兩個 agent 都能無需特別指引而發現專案的規則、skills 與驗收標準時，可以把本套組當作範本複製使用。

## The idea: one contract, enforced elsewhere

兩個 agent 都讀取單一根目錄的 `AGENTS.md`。Claude Code 與 Codex 原生會自動探索該檔名，所以不需要注入任何設定。

`AGENTS.md` 刻意保持精簡。一項規則只有在無法由其他層級陳述或執行時，才值得列在其中。所有其他指引都存放在實際執行的地方：

| 層級                                | 負責範圍                                               |
| :---------------------------------- | :----------------------------------------------------- |
| `AGENTS.md`                         | 授權、專案慣例、審查嚴重性與記憶邊界                   |
| `.pre-commit-config.yaml`           | 編碼、語言邊界、secret 掃描、格式化、linting、型別檢查 |
| `.github/workflows/ci.yml`          | repository 層級的合併前檢查閘道                        |
| `.claude/rules/`                    | 路徑限定的程式碼規範，觸發時才載入                     |
| `.claude/skills/`, `.codex/skills/` | 任務類別工作流程，由各自的 `description` 觸發載入      |
| `.claude/agents/`, `.codex/agents/` | Subagent 角色與路由，由各自的 `description` 選定       |

有兩點值得直言：

- **`AGENTS.md` 不列舉個別 skill 或 subagent。** 路由應由各元件的 `description` 指定，檢索已在該處進行。在契約中列舉名稱會重複且容易過時。
- **`AGENTS.md` 不陳述模型已知的事項。** 通用工程素養、讀程式碼後再改動、不 commit secrets 等原則被省略了，因為模型自帶前兩項，`detect-secrets` 強制執行第三項。

結果就是一份簡潔的契約，只在專案實際約束改變時才需要更新。

## What to copy

| 路徑                      | 用途                                                              |
| :------------------------ | :---------------------------------------------------------------- |
| `AGENTS.md`               | 所有 agent 的共用根目錄操作契約                                   |
| `.pre-commit-config.yaml` | Repository 驗證 hooks                                             |
| `scripts/`                | 所有 agent 共用的 shell 中立衛生與格式檢查                        |
| `.claude/`                | Claude Code 設定、hooks、slash commands、subagents、skills 與規則 |
| `.codex/`                 | Codex 組態、hooks、command-like skills 與專職 agents              |
| `.github/workflows/`      | 執行與 agent 本地相同檢查的 CI                                    |
| `docs/en/git-workflow.md` | Git 與交付授權契約；保留路徑，重置狀態                            |
| `docs/en/pr-setup.md`     | 擁有者設定指南，用於啟用 PR 交付                                  |
| `.vscode/`                | 檔案衛生與 Ruff 工作流程對齊的編輯器預設值                        |

只複製你使用的 agent 目錄。兩個 agent 都不需要另一個的層級。

## Setting up

```bash
uv sync --group dev
uv run pre-commit install
```

然後驗證檢查執行：

```bash
uv run pre-commit run --all-files
uv run python -m pytest scripts/tests .codex/hooks/tests .claude/hooks/tests
```

## Adapting it to your project

### 1. Reset delivery authorization

`docs/en/git-workflow.md` 記錄了此 repository 自己的交付狀態。**在用範本於他處前，先將其目前狀態項目重設為 local-only。** 複製檔案並不授予發佈權限；啟用它請見 [PR setup](pr-setup.md)。

永遠不變的規則：agent 永不 commit 或 push 到預設分支。一切都必須經過 pull request 到達。

### 2. Adjust the CI workflow

`.github/workflows/ci.yml` 在 Windows 上執行完整的 pre-commit 加 agent hook 測試，因為 Windows 是此範本的主要開發平台。更改 runner、Python 版本與測試路徑以符合你的專案，然後把該 job 設為預設分支上的必需檢查。將任何第三方 action 鎖定到完整 commit SHA。

本地 pre-commit 結果不是合併閘道。CI 才是。

### 3. Rewrite the rules that are actually yours

開啟 `AGENTS.md` 並刪除不適用於你專案的內容。繁體中文溝通、`scripts/` shell 中立需求與 Windows 路徑預期都是此範本的約束，不是通用的。保持形狀——授權、慣例、審查、skills、記憶、驗證、委派——並替換內容。

對你加入的任何東西套用同一套測試：如果 pre-commit、CI、路徑限定的規則或 skill description 能承載它，就把它放在那裡，而不是這裡。

### 4. Consider OpenSpec for durable planning

此範本不 commit `openspec/` 目錄，`AGENTS.md` 也不提及它，因為規劃狀態屬於各專案而非範本。從此 kit 建構的專案已發現它值得添加來應付長期工作：執行 `openspec init`，然後把生成的 specs、changes 與 tasks 當作一般專案檔案對待並 commit 為專案紀錄的一部分。它為跨 session 工作提供持久追蹤，超越任何單一 agent session。

### 5. Set up permissions

Claude Code 權限位於 `.claude/settings.json` 且無需觸及全域設定即可生效。此範本允許普通 `git push` 並禁用 force-push、mirror、prune 與 delete 變體，加上 `.git` 刪除。這些是便利性設施，不是安全邊界——server 端分支保護才是。

Codex 此處不提供 repository 本地權限規則；它使用自己的核准控制。

## Per-agent references

從你使用的 agent 對應參考文件開始。不必設定兩個都。

- **[Claude Code Components](claude-components.md)** — `.claude/` 中的 subagents、slash commands、skills、hooks 與路徑限定規則。
- **[Codex Components](codex-components.md)** — `.codex/` 中的專職 agents、command-like skills、hooks 與模型路由。
- **[Git Workflow Contract](../en/git-workflow.md)** — 任務隔離、交付授權與審查和合併邊界。
- **[PR Review](pr-review.md)** — 此 repository 自己託管的審查與合併條件如何設定。

## Hooks

兩個 agent 都執行一個唯讀的 `PostToolUse` hook，在編輯後的 Python 檔案上回報 Ruff 診斷而不修改它們。兩者都不執行 `SessionStart` hook：根目錄 `AGENTS.md` 原生被探索，Git 脈絡是一個指令遠而已。

| Agent           | Script                                          | 回報內容                                     |
| :-------------- | :---------------------------------------------- | :------------------------------------------- |
| **Claude Code** | `.claude/hooks/claude_post_tool_use_hygiene.py` | Ruff `E722,F601,F602,F634`，補充 Pyright LSP |
| **Codex**       | `.codex/hooks/codex_post_tool_use_hygiene.py`   | Ruff `F` checks，因為 Codex 沒有 Python LSP  |

若 hooks 未觸發，確認 `uv run pre-commit install` 已執行、`.codex/config.toml` 啟用 `hooks`、`.claude/settings.json` 宣告 `hooks` 區塊，以及 agent 信任了 project 本地設定。

## Design influences

- **[Everything Claude Code (ECC)](https://github.com/affaan-m/ECC)** — 專職 agents 與程式碼規則改編自 ECC v2.0.0-rc.1。大多數開發 slash commands 已陸續退役，改採原生 Plan Mode 與 autoloaded project skills。

---

本專案強制 UTF-8 without BOM 與英文用於源碼、技術文件、workflows 與設定。繁體中文內容屬於 `docs/zh-TW/`、`.references/` 與 `.tmp/`。
