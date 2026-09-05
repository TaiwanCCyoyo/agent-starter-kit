# Claude Code 元件參考

本文件列出 `.claude/` 目錄中所有啟用的 agents、commands、skills、hooks 與 rules。
適用對象：Python 及 SystemVerilog/UVM 開發者。

**ECC 來源**：[affaan-m/ECC](https://github.com/affaan-m/ECC) v2.0.0-rc.1
**ECC 整合日期**：2026-06-02
**記憶**：Claude 僅使用 Claude Code 的內建記憶；必要 repository guidance 仍納入版本控制——詳見 `CLAUDE.md` §Memory。

本專案設定刻意停用外部的 Superpowers、Ponytail 與 Karpathy plugins。本參考文件描述 repository-owned 的 Claude 元件與 Claude 原生能力；GitHub、skill-creator 與 Pyright LSP 仍在 `.claude/settings.json` 中啟用。

---

## Agents

Agents 是由主要 Claude 工作階段呼叫的專用子代理，用於執行特定任務。

Claude 的自動分派主要由各 agent 的 description 與目前任務脈絡引導。`signal-miner` 是最低成本的原生唯讀苦力，負責有界的高輸出指令；當 tests、benchmarks、廣泛搜尋、verbose diagnostics、dependency traces 或大型 diff/log inspections 值得為了隔離輸出付出一次往返時，就委派給它；短而聚焦的檢查直接在 main context 執行，一般的程式碼定位則使用內建 Explore agent。`task-worker` 則是只供高階 main session 降級執行有界修改的中價選項，任務必須有明確目標、範圍、驗收條件與驗證方式。最低階 main session 應自行處理簡單工作，或視情況使用內建 Explore 或 general-purpose，不升級到 `task-worker`。模糊、跨領域、security-sensitive、architecture 與 planning 工作應留給 main session 或適合的內建 agent。

`.claude/settings.json` 保留 `model: "opusplan"`：原生 Plan Mode 使用 `opus`，執行模式使用 `sonnet`。不使用 custom agent 將計畫交回 main session。

### 工作流程（原創——非來自 ECC）

| Agent                     | 模型            | 工具                                | 用途                                                                                                                                            |
| ------------------------- | --------------- | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `commit-specialist`       | haiku           | Bash, Read                          | 審查已暫存的變更並草擬 commit 訊息                                                                                                              |
| `doc-translator`          | haiku           | Read, Write, Edit                   | 低階文件翻譯與同步者：將任何需寫入檔案的翻譯處理到單一明確的非 canonical 目標；main session 決定來源與目標，衝突時以其維護的 canonical 文件為準 |
| `implementation-reviewer` | opus            | Read, Grep, Glob, Bash              | 唯讀程式碼審查：正確性、風格、安全性                                                                                                            |
| `plan-reviewer`           | opus（high）    | Read, Grep, Glob, Bash              | 實作前計畫品質審查：完整性、範疇蔓延、步驟排序、Repo 對齊、可測試性                                                                             |
| `signal-miner`            | haiku           | Read, Grep, Glob, Bash              | 以最低成本隔離預期會產生大量 log 或 stdout 的指令，僅回傳精簡訊號而非原始輸出                                                                   |
| `task-worker`             | sonnet (medium) | Read, Grep, Glob, Write, Edit, Bash | 執行已有明確範圍、驗收條件與驗證方式的低至中風險修改；當範圍或風險擴大時停止並回報                                                              |
| `security-reviewer`       | opus（high）    | Read, Grep, Glob, Bash              | 唯讀 secrets、注入、依賴、權限、auth 與敏感資料審查                                                                                             |

### 未從 ECC 移植（含原因）

| Agent                                                                                                                                              | 原因                                                                          |
| -------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `planner`                                                                                                                                          | 2026-06-08 移除——已由 Native Plan Mode（`EnterPlanMode`/`ExitPlanMode`）取代  |
| `architect`、`code-reviewer`、`code-simplifier`、`loop-operator`、`performance-optimizer`、`python-reviewer`、`silent-failure-hunter`、`tdd-guide` | 2026-07-13 移除——原生 Claude 功能與聚焦 reviewer 已涵蓋其責任，無須重複委派。 |
| `refactor-cleaner`                                                                                                                                 | 依賴 Node.js 工具（knip、depcheck、ts-prune）；本專案使用 Python              |
| `harness-optimizer`                                                                                                                                | 需要 ECC 內部的 `/harness-audit`；無法移植                                    |
| 所有 `*-build-resolver`（共 11 個 agents）                                                                                                         | 未使用非 Python 語言                                                          |
| 非 Python 語言的程式碼審查器                                                                                                                       | 未使用的語言                                                                  |
| `gan-*`、`seo-specialist`                                                                                                                          | 超出範疇                                                                      |
| `homelab-*`、`network-*`、`healthcare-reviewer`                                                                                                    | 領域不符                                                                      |
| `marketing-agent`                                                                                                                                  | 延後——待短片製作規劃啟動時新增                                                |

---

## 互動、自動化與公司使用

- 互動工作：進入 Native Plan Mode；複雜或高風險計畫可選用 `plan-reviewer`；核准計畫後再回到執行模式。
- 無人值守工作：使用分離的 planning 與 execution sessions。planning session 寫入 OpenSpec 或受維護的 plan artifact；execution session 讀取已核准 artifact。不要以 planner subagent 作為 main-session handoff。
- Claude-only 公司移植：保留 instructions、rules、agents、skills 與 hygiene hooks。使用公司核准的固定模型 ID 或 alias mapping，不依賴本 repo 個人 Pro 的預設。

`REVIEW.md` 不屬於本機 baseline；只有 repository 加入 Claude 託管的 Team 或 Enterprise Code Review 時才加入。

---

## Commands（斜線指令）

### 工作流程（原創——非來自 ECC）

| Command       | 用途                                                            |
| ------------- | --------------------------------------------------------------- |
| `/gen-commit` | 透過 `commit-specialist` 產生符合 Conventional Commits 格式訊息 |
| `/worktree`   | 建立、驗證、管理、合併與清理 Git worktree                       |

只有在使用者明確要求 PR 時，Claude Code 才使用原生 Git/GitHub 操作準備 PR：檢查完整 branch history、比較 `base...HEAD`、撰寫 PR summary，並附上最新 test plan。Publishing、pushing 與 branch completion 都需要使用者明確授權。

### 已移除（2026-06-10 清理——agents 與內建 `/code-review` 已涵蓋）

| Command          | 替代方案                                                                       |
| ---------------- | ------------------------------------------------------------------------------ |
| `/build-fix`     | 原生 evidence-driven debugging + `python-testing` skill                        |
| `/code-review`   | 內建 `/code-review`（含 `ultra` 雲端 review）+ `implementation-reviewer` agent |
| `/feature-dev`   | Native Plan Mode + 原生 test-first workflow + `signal-miner` agent             |
| `/python-review` | `python-testing` skill 與 `implementation-reviewer`                            |
| `/security-scan` | `security-reviewer` agent + `detect-secrets` gate                              |
| `/test-coverage` | `python-testing` skill（`pytest --cov`）                                       |

### 未從 ECC 移植（含原因）

| Command                                         | 原因                                                                                                      |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `/pr`、`/review-pr`                             | 不需要 PR 工作流程                                                                                        |
| `/multi-*`（共 5 個指令）                       | 多代理協作尚未成熟                                                                                        |
| `/learn`、`/skill-create`                       | 依賴 ECC observation hooks 與完整 instinct pipeline；由 `skill-authoring` 規則與 `skill-creator` 外掛取代 |
| `/evolve`                                       | 由 `skill-authoring` 規則與 `skill-creator` 外掛取代                                                      |
| `/hookify-*`（共 4 個指令）                     | ECC 內部 hook 管理                                                                                        |
| `/sessions`、`/save-session`、`/resume-session` | 已由 Claude Code 內建記憶與 session history 取代                                                          |
| 語言專屬的建構／測試／審查指令                  | Go/Rust/Kotlin/Java 等語言未使用                                                                          |
| `/cost-report`、`/model-route`                  | 有需要時再新增                                                                                            |
| `/jira`、`/prp-*`、`/plan-prd`                  | 未規劃 PM 整合                                                                                            |

---

## Skills

Skills 是內部工作流程文件，在對應的 command 或 agent 需要時載入。

### 工作流程（原創——非來自 ECC）

| Skill                    | 用途                                           |
| ------------------------ | ---------------------------------------------- |
| `commit-helper`          | Conventional Commits 格式、pre-commit 檢查清單 |
| `dependabot-remediation` | 唯讀警示擷取、最小安全升級與完成證據           |

### 開發（從 ECC v2.0.0-rc.1 移植）

| Skill            | 用途                                                                                                                                     |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `python-testing` | 僅含專案特定驗證需求：`uv run python -m pytest`、ruff、mypy、hook JSON fixtures、Windows 路徑行為。Test-first 決策使用 Claude 原生能力。 |

### 已移除（2026-08-23 清理——原生 GitHub 操作與聚焦的安全工作流）

| Skill        | 原因                                                                                                                                                                       |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `github-ops` | 通用 Issue、PR、CI 與 release 指令重複 Claude 原生 `gh` 能力，並強加多人協作的 stale 政策。Dependabot 工作已移至 `dependabot-remediation`；PR 操作維持僅在明確要求時執行。 |

### 已移除（2026-08-19 清理——`/learn-eval` 未曾在實務中觸發）

| Skill / Command                | 原因                                                                                                                                                                                                                                                                      |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `skill-curator`、`/learn-eval` | ECC 整體品質門與 Hermes curator 生命週期的手動移植未曾被觸發——唯一提示是每週的 Stop hook 提醒。已由常駐載入的 `rules/common/skill-authoring.md` 規則取代，該規則陳述耐用的意圖（當任務類別會重複出現時，撰寫 project skill），加上已啟用的 `skill-creator` 外掛用於撰寫。 |

### 已移除（2026-08-07 清理——待機設計 ECC demo skills，無下游使用方）

| Skill                        | 原因                                                                                                                                                                                                                                                         |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `cost-aware-llm-pipeline`    | 本 repo 未呼叫任何 LLM API（僅為 meta-tooling），因此此 skill 只能透過描述在下游專案中符合條件；其硬編碼了陳舊的模型 ID（`claude-sonnet-4-6`）與 2025-2026 年度價格表，可能滲入產生的程式碼。待有實際呼叫 LLM API 的專案建置自此 kit 時，再從 ECC 重新加入。 |
| `llm-trading-agent-security` | 本 repo 無交易代理功能。移除它會縮小下方 `security-review` 的涵蓋聲明——若開始交易代理工作，可視需要恢復。                                                                                                                                                    |

### 已移除（2026-06-08 清理——Claude 原生 verification 現已涵蓋這些功能）

| Skill               | 原因                                                                                                                 |
| ------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `coding-standards`  | Claude 原生 guidance 與縮減後的 `coding-style` rule 已涵蓋                                                           |
| `tdd-workflow`      | 由原生 test-first workflow 取代                                                                                      |
| `verification-loop` | 由原生 testing、review 與 pre-commit verification 取代                                                               |
| `git-workflow`      | 716 行 Git 教科書；repo 提交規範現在僅在 `commit-helper` skill（`git-workflow` rule 也於 2026-06-13 清理中一併移除） |

### 未從 ECC 移植（含原因）

| Skill                                      | 原因                                                                                                                                               |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `python-patterns`                          | PEP 8 格式化由 ruff 處理；慣例由 `python-reviewer` agent 涵蓋                                                                                      |
| `deep-research`                            | 需要 firecrawl + exa MCP——延後至 MCP 設定完成                                                                                                      |
| `api-design`、`backend-patterns`           | 本股票專案非 web backend                                                                                                                           |
| `security-review`                          | 已由 `security-reviewer` agent 涵蓋；交易相關模式（消費上限、斷路器）因 `llm-trading-agent-security` 於 2026-08-07 移除而不再涵蓋                  |
| 非 Python 語言模式                         | 未使用的語言                                                                                                                                       |
| `homelab-*`、`network-*`、`healthcare-*`   | 領域不符                                                                                                                                           |
| `angular-developer`、`react-*`、`nextjs-*` | 未規劃前端                                                                                                                                         |
| `eval-harness`                             | 2026-06-09 移除：引用不存在的 `/eval` commands，且沒有 runner、graders、baseline format、Python commands 或 CI integration。具備這些能力後才恢復。 |

---

## Hooks

Hooks 是由 Claude Code harness 自動執行的 Python 腳本。

| Hook                       | 觸發時機             | 執行內容                                                                                        |
| -------------------------- | -------------------- | ----------------------------------------------------------------------------------------------- |
| `post_tool_use_hygiene.py` | Python Edit/Write 後 | 執行補充 Pyright 的唯讀 Ruff `E722`、`F601`、`F602`、`F634` diagnostics；不會格式化或修改檔案。 |

Workspace editor defaults 放在 `.vscode/settings.json`：移除行尾空白、保留單一 final newline、使用 Ruff 進行 Python formatting 與 explicit code actions，並將產生的 cache 與本機 agent state 排除於 search、watchers 與 local history 之外。

Claude Code 使用官方 Pyright plugin 提供即時型別導覽與 diagnostics；其 PostToolUse hook 額外對修改後的 Python 檔案執行唯讀的 Ruff `E722`、`F601`、`F602`、`F634` check，補足 Pyright 不負責的問題並避免重複回報 undefined-name 與 unused-symbol diagnostics。hook 指令本身與其內部的 Ruff 呼叫都使用 `uv run --no-sync`，避免每次編輯都觸發環境 resync。完整 Ruff linting 與 formatting 延後由 pre-commit 負責，因此正常編輯期間不會觸發 repository-wide formatting。Agent 會在完成前針對變更檔案執行 pre-commit，由 pre-commit 負責 formatting 與 validation。

### 已注意但未從 ECC 移植的 hook 概念

| 概念                 | 狀態       | 原因                                                                                          |
| -------------------- | ---------- | --------------------------------------------------------------------------------------------- |
| PostToolUse 持續學習 | **未實作** | 完整 hook 觀察管線（instinct YAML、背景 Haiku agent）未移植——在沒有持久程序的情況下過於重量級 |
| Stop 治理捕捉        | 延後       | ECC 在 session 結束時記錄安全事件——若專案發展到包含自主交易代理時將有其相關性                 |

---

## Rules

Rules 是依路徑範圍載入的 Markdown 檔案，當 Claude 處理符合的檔案類型時生效。

| 規則集          | 路徑                  | 來源                      | 備註                                                                                 |
| --------------- | --------------------- | ------------------------- | ------------------------------------------------------------------------------------ |
| `rules/python/` | `**/*.py`、`**/*.pyi` | ECC v2.0.0-rc.1（已修改） | Type annotations、Ruff、logging、repository hooks、pytest 與風險導向 security review |

詳細流程放在 skills 或 agent definitions。

### 已移除（2026-08-23 清理——併入 CLAUDE.md）

`rules/common/` 每個檔案的 `paths` 都是 `"*"`，因此會在 session 第一次存取任何檔案時注入，與 CLAUDE.md 相比實際上沒有真正的路徑範圍效益，只是載入時機不同。其路由內容（review severity、security triggers、phase routing、skill authoring、memory routing、風險導向測試基線）已直接併入 `CLAUDE.md`，該目錄已刪除。

| 規則                     | 原因                                                       |
| ------------------------ | ---------------------------------------------------------- |
| `rules/common/*`（全部） | 實務上並非路徑範圍限定（`paths: "*"`）；已併入 `CLAUDE.md` |

### 已移除（2026-06-13 清理——由 skills 與 CLAUDE.md 擁有）

| 規則                        | 原因                                                                                                                                                         |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `rules/common/git-workflow` | commit 格式由 `commit-helper` 擁有；明確要求的 PR 準備使用原生 Git/GitHub 操作（完整 history、`base...HEAD` diff、摘要、test plan）；push 與建立都需明確授權 |
| `rules/common/agents`       | agent 索引由 CLAUDE.md `Subagents` 擁有；parallel-execution 指引已遷移至此                                                                                   |

### 已移除（2026-08-07 清理——模型先驗與 CLAUDE.md 已涵蓋）

由於 `rules/common/` 每個檔案的 `paths` 都是 `"*"`，整組會在 session 第一次存取任何檔案時注入，因此其內容是在與 CLAUDE.md 競爭 context，而非延後成本。此次移除通用工程常識，只保留無法推導的路由決策。

| 規則                                      | 原因                                                                                                                   |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `rules/common/coding-style`               | 通用工程常識，與 CLAUDE.md `Engineering Discipline` 重複；結構性 review heuristic 已移至 `rules/common/code-review.md` |
| `development-workflow` §Research & Reuse  | 與 CLAUDE.md `Engineering Discipline` 逐字重複                                                                         |
| `development-workflow` §Pre-Review Checks | 通用 pre-merge 常識，由 CI 與原生 GitHub 操作負責                                                                      |
| `testing` §AAA 與 §Test Naming            | 通用 pytest 結構與命名範例，由 `skill: python-testing` 擁有                                                            |
| `code-review` §Security Review Triggers   | 純指標區塊；reviewer routing 清單已連結 `security.md`                                                                  |

### 未從 ECC 移植（含原因）

| 規則集                                 | 原因                                                                       |
| -------------------------------------- | -------------------------------------------------------------------------- |
| `rules/typescript/`、`rules/react/` 等 | 未使用的語言                                                               |
| `rules/cpp/`                           | SV/UVM 與 C++ 差異過大；延後——待 UVM 專案啟動時建立 `rules/systemverilog/` |

---

## 延後項目

| 項目                            | 類型                    | 前提條件                                                                                               |
| ------------------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------ |
| `deep-research` skill           | ECC 移植                | 先設定 firecrawl + exa MCP                                                                             |
| `marketing-agent` agent         | ECC 移植                | 確認短片製作規劃啟動                                                                                   |
| `uvm-patterns` skill            | 自訂建置                | UVM 專案啟動                                                                                           |
| `rules/systemverilog/`          | 自訂建置                | UVM 專案啟動                                                                                           |
| Eval-driven development harness | Workflow infrastructure | 加入真實 runner、deterministic graders、baselines、重複執行 metrics、Python commands 與 CI integration |

### OpenSpec Planning Handoff

OpenSpec 是選用的專案狀態，不是 starter kit 需要提交的內容。Specs、changes 與 tasks 存在時就是一般 project-owned files；當它們屬於專案紀錄時就提交。Plans 不屬於 durable memory。
