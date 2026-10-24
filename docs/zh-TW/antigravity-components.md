# Antigravity 元件參考

Antigravity 使用內建規劃指令與對話 artifacts、位於 `.agents/skills/` 的 repo-scoped skills、內建 subagents（`self` 與 `research`）、位於 `.agents/hooks.json` 的生命週期 hooks，以及終端機 sandbox。它會原生讀取共用的根目錄 `AGENTS.md`，以及任何巢狀的 `AGENTS.md` 或 `GEMINI.md`。

## 原生與內建能力對應

| 能力                                         | Antigravity 實作                                                          |
| :------------------------------------------- | :------------------------------------------------------------------------ |
| 規劃                                         | 內建 `/plan`、`/grill-me` 斜線指令與對話 artifacts                        |
| TDD、除錯、worktree、完成前驗證              | Antigravity 原生能力、project skills 與明確檢查                           |
| GitHub issues、PR、CI、review comments、發布 | 已驗證的 `gh` CLI（受限環境下搭配內建 `permissioned-github` 權限機制）    |
| Slash commands                               | `.agents/skills/<name>/SKILL.md`（原生支援 `/<name>` 觸發與語意自動探索） |
| 跨 session planning                          | 受維護的 repository 計畫文件（單一 session 內審視可使用對話 artifacts）   |
| 跨 session recall                            | Antigravity 持久記憶與全域使用者規則（`~/.gemini/config/`）               |

Antigravity 將 planning 與 implementation 權責保留在 main agent。唯讀的 `research` subagents 與有界的 `self` subagents 負責從大範圍搜尋、logs、test output、diffs 或重複性編輯中整理隔離脈絡的證據摘要；它們不取代主 session 的架構判斷，也不擁有發布與整合權限。主 agent 遵守[共用 Git 工作契約](../en/git-workflow.md)。

## 委派

有界實作或驗證工作使用內建 `self` subagent；唯讀程式碼探索或網頁調查使用內建 `research` subagent。本專案不定義自訂 subagent 類型（一般工作無須使用 `define_subagent`）。共用委派原則由 `AGENTS.md` 管理；skills 保留各任務專屬的工作流程細節。

`invoke_subagent` 提供 `Model`（`"inherit"`、`"flash_lite"`、`"flash"`、`"pro"`）與 `Workspace`（`"inherit"`、`"branch"`、`"share"`）控制：

- 當大量輸入、輸出、雜訊或重複作業使隔離脈絡有具體效益時，優先選擇 `"flash_lite"` 或 `"flash"` 處理簡單工作，包括長篇翻譯、文件同步、大型 diff/log 檢視與機械式 hook 修復。
- 需要較高判斷力的有界實作保留 `"inherit"`（或依需求選用 `"pro"`），並尊重使用者對主模型的明確設定。若當前環境僅允許繼承主模型，明確回報限制並直接執行；或只在隔離 context、平行處理有具體效益時委派，不宣稱已切換模型或降低成本。
- Repository 任務一律傳遞 `Workspace: "inherit"`，讓 subagent 在父 session 指定的 checkout 內作業；任務 worktrees 依據 `docs/en/git-workflow.md` 與 `scripts/worktree_inventory.py` 在 `.worktrees/<name>/` 下明確管理，不使用未受控的 `branch` 或 `share` 複製。
- Subagents 與背景任務完成時會自動喚醒父對話（Reactive Wakeup），禁止輪詢狀態或使用 shell sleep 計時。
- 將終端機 sandbox 或權限失敗（例如 `.git` 寫入或網路存取需要 `BypassSandbox: true`、`EPERM`、或 `permissioned-github` 阻擋）視為執行邊界交接：subagents 必須立即停止並將確切錯誤、嘗試步驟與受影響路徑回傳給主 agent，不得自行重試或尋求提權。

文件翻譯或同步由 main agent 選定權威來源與明確目標。保留結構、連結、程式碼與識別字；遇到來源衝突或術語不明時回報。

## Skills

Antigravity 採用漸進式揭露（progressive disclosure）探索 `.agents/skills/<name>/SKILL.md`（預設僅載入 `name` 與 `description`，觸發時才讀取完整內容）。舊版 `.agents/workflows/*.md` 在 Antigravity 中已棄用，本專案不使用。

| Skill                    | 用途                                                                  |
| :----------------------- | :-------------------------------------------------------------------- |
| `python-development`     | Python logging 與以 log 輔助除錯                                      |
| `gen-commit`             | 有界 local commit、內建委派協助大量 diff 檢視與簡單 hook 修復，並回報 |
| `dependabot-remediation` | 唯讀警示擷取、最小安全升級與完成證據                                  |

## Claude 能力取捨

| Claude 能力                                                      | Antigravity 決策       | 原因                                                                                                               |
| :--------------------------------------------------------------- | :--------------------- | :----------------------------------------------------------------------------------------------------------------- |
| `/plan`                                                          | 內建斜線指令／artifact | Antigravity 提供 `/plan`、`/grill-me` 與對話 artifacts 進行互動式規劃；跨 session 持久計畫存放於 repository 文件。 |
| `plan-reviewer`、`implementation-reviewer`、`security-reviewer`  | 不鏡像                 | 目前模型能力、hosted Codex PR review 與 pre-commit gates 已涵蓋；委派改用內建 `self` 與 `research` subagents。     |
| `/feature-dev`、`/build-fix`、`/python-review`、`/test-coverage` | 原生能力取代           | Evidence-driven debugging、test-first workflow 與 repository verification 已涵蓋這些工作流程。                     |
| `/code-review`、`/security-scan`                                 | 原生與 gates 取代      | 本地審查遵循 `AGENTS.md` 嚴重性規則；`detect-secrets`、pre-commit 與 hosted PR review 強制執行檢查閘道。           |
| `/worktree`                                                      | 契約取代               | Worktree 生命週期直接由 `docs/en/git-workflow.md` 與 `scripts/worktree_inventory.py` 管理。                        |
| `github-ops`                                                     | 內建／CLI 取代         | 已驗證的 `gh` CLI（受限時搭配內建 `permissioned-github` skill）加上 `dependabot-remediation` 已涵蓋相關流程。      |
| `cost-aware-llm-pipeline`、`llm-trading-agent-security`          | 不移植                 | 屬於應用領域指引，待下游專案實際採用該執行面時再加入。                                                             |
| `eval-harness`                                                   | 延後                   | 待具備真實 runner、deterministic graders、baselines 與 CI integration 後再恢復。                                   |

## 共享政策對齊

| 共享行為                                                          | Antigravity owner                                                 |
| :---------------------------------------------------------------- | :---------------------------------------------------------------- |
| Operating contract、scoped changes                                | `AGENTS.md`                                                       |
| 專案慣例與工具偏好                                                | `AGENTS.md` project conventions                                   |
| Review severity 與 CRITICAL/HIGH completion policy                | `AGENTS.md` review and security section                           |
| Verification scope                                                | `AGENTS.md` verification section                                  |
| Python development rules                                          | `python-development`                                              |
| 暫存檔與拋棄式診斷報告                                            | Workspace 內的 `.tmp/`（優先於 brain 目錄下的 `scratch/`）        |
| Planning、TDD、debugging、review、verification、branch completion | 原生 Antigravity、內建 subagents 與 repository verification gates |

## Hooks 與 Gates

| 元件                                                 | 用途                                                                            |
| :--------------------------------------------------- | :------------------------------------------------------------------------------ |
| `.agents/hooks/antigravity_post_tool_use_hygiene.py` | 修改 Python 檔案後執行唯讀的精簡 Ruff `F` diagnostics                           |
| `.pre-commit-config.yaml`                            | Formatting、file hygiene、detect-secrets、Ruff（含 T201）、mypy 與 pyright      |
| `.vscode/settings.json`                              | Final newline、trailing whitespace hygiene，以及 Python Ruff formatter defaults |

Local Python verification 只針對行為變更。Installed commit hooks 與 PR CI 負責自動化檢查；skills 與 reviewers 不要求另外執行一次手動檢查。

## Runtime Verification

Antigravity 在 `.agents/hooks.json` 中設定 workspace hooks，頂層 key 為具名 hook 群組（`python-hygiene`），對應至生命週期事件（`PostToolUse`，matcher 為 `edit_file|write_file`）。與 Claude Code 不同，Antigravity 的 agent 工具執行流程不會在 `edit_file` 或 `write_file` 步驟自動附加 Pyright LSP diagnostics，因此此 hook 與 Codex 相同，執行唯讀的 Ruff `F` 檢查並排除 `F401,F841,F842`（`--no-fix --select F --ignore F401,F841,F842 --output-format concise`）。

Antigravity 此處不執行 `SessionStart`、`PreInvocation` 或 `PostInvocation` hook：根目錄 `AGENTS.md` 會被原生探索，且避免在每次唯讀回合都啟動 Python 子程序。Antigravity 執行 hook 指令時，工作目錄固定為包含 `hooks.json` 的 `.agents/` 目錄（Windows 使用 `cmd /c`，Unix 使用 `sh -c`），因此 `.agents/hooks.json` 使用跨平台相容的 `uv run --no-sync --project .. python hooks/antigravity_post_tool_use_hygiene.py`，不依賴僅限 POSIX 的 `$(...)` 語法。

依據 Antigravity 的 `PostToolUse` protojson 契約，hook 從 `stdin` 讀取 `workspacePaths` 與 `toolCall.args.Path`，在 `stdout` 固定輸出 `{}`，並透過 Python `logging` 將任何 Ruff diagnostics 寫入 `stderr`，不會修改任何檔案。
