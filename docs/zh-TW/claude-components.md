# Claude Code 元件參考

本文件列出 `.claude/` 目錄中所有啟用的 agents、commands、skills、hooks 與 rules。
適用對象：Python 及 SystemVerilog/UVM 開發者。

**ECC 來源版本**：v2.0.0-rc.1
**整合日期**：2026-06-02

---

## Agents

Agents 是由主要 Claude 工作階段呼叫的專用子代理，用於執行特定任務。

### 記憶體與工作流程（原創——非來自 ECC）

| Agent | 模型 | 工具 | 用途 |
|---|---|---|---|
| `commit-specialist` | sonnet | Bash, Read | 審查已暫存的變更並草擬 commit 訊息 |
| `doc-translator` | sonnet | Read, Write, Edit | 將 `docs/en/` 檔案翻譯為 `docs/zh-TW/` |
| `implementation-reviewer` | opus | Read, Grep, Glob, Bash | 唯讀程式碼審查：正確性、風格、安全性 |
| `memory-auditor` | sonnet | Read, Grep, Glob | 在重大工作完成後建議記憶體更新 |
| `memory-compressor` | sonnet | Read, Grep, Glob | 草擬熱記憶體／暖記憶體的壓縮提案 |
| `repo-explorer` | sonnet | Read, Grep, Glob, Bash | 定位檔案、追蹤執行路徑、繪製相依關係圖 |

### 開發（從 ECC v2.0.0-rc.1 移植）

| Agent | 模型 | 工具 | 用途 |
|---|---|---|---|
| `architect` | opus | Read, Grep, Glob | 系統設計、取捨分析、ADR |
| `code-reviewer` | sonnet | Read, Grep, Glob, Bash | 跨語言通用程式碼審查 |
| `code-simplifier` | sonnet | Read, Write, Edit, Bash, Grep, Glob | 在保留行為的前提下簡化程式碼結構 |
| `loop-operator` | sonnet | Read, Grep, Glob, Bash, Edit | 監控自主循環並安全介入 |
| `performance-optimizer` | sonnet | Read, Write, Edit, Bash, Grep, Glob | 識別瓶頸、最佳化演算法與查詢 |
| `planner` | opus | Read, Grep, Glob | 建立詳細實作計畫；確認後才開始撰寫程式碼 |
| `python-reviewer` | sonnet | Read, Grep, Glob, Bash | Python 專屬審查：型別提示、安全性、Pythonic 慣例 |
| `security-reviewer` | sonnet | Read, Write, Edit, Bash, Grep, Glob | OWASP Top 10、機密偵測、交易安全性 |
| `silent-failure-hunter` | sonnet | Read, Grep, Glob, Bash | 尋找被吞掉的例外、錯誤的 fallback、遺漏的錯誤傳播 |
| `tdd-guide` | sonnet | Read, Write, Edit, Bash, Grep | 強制執行 Red-Green-Refactor；目標涵蓋率 80%+ |

### 未從 ECC 移植（含原因）

| Agent | 原因 |
|---|---|
| `refactor-cleaner` | 依賴 Node.js 工具（knip、depcheck、ts-prune）；本專案使用 Python |
| `harness-optimizer` | 需要 ECC 內部的 `/harness-audit`；無法移植 |
| 所有 `*-build-resolver`（共 11 個 agents） | 未使用非 Python 語言 |
| 非 Python 語言的程式碼審查器 | 未使用的語言 |
| `gan-*`、`seo-specialist` | 超出範疇 |
| `homelab-*`、`network-*`、`healthcare-reviewer` | 領域不符 |
| `marketing-agent` | 延後——待短片製作規劃啟動時新增 |

---

## Commands（斜線指令）

### 記憶體與工作流程（原創——非來自 ECC）

| Command | 用途 |
|---|---|
| `/compress-memory` | 當 `.agents/memory/` 過大時進行壓縮 |
| `/gen-commit` | 透過 `commit-specialist` 產生符合 Conventional Commits 格式的訊息 |
| `/learn-eval` | 以整體品質門評估 session 模式；核准後萃取為 skills |
| `/memory-maintenance` | 初始化、更新、審查或整合專案記憶體 |
| `/memory-sql` | 透過 memory-db MCP server 查詢或寫入 `.agents/memory/memory.db`（SQLite FTS5） |
| `/save-memory` | 將教訓、決策或交接筆記儲存至 `.agents/memory/` |
| `/worktree` | 建立、管理並合併 Git worktree，同時保留記憶體 |

### 開發（從 ECC v2.0.0-rc.1 移植）

| Command | 用途 |
|---|---|
| `/build-fix` | 偵測建構系統並逐步修正建構／型別錯誤 |
| `/code-review` | 審查本地端 diff |
| `/feature-dev` | 結構化功能開發：先理解需求，再撰寫程式碼 |
| `/plan` | 建立實作計畫；等待使用者確認後才開始撰寫程式碼 |
| `/python-review` | 對 Python 變更呼叫 `python-reviewer` agent |
| `/security-scan` | 對 agent、hook、MCP、權限表面執行安全性審查 |
| `/test-coverage` | 分析涵蓋率缺口並產生遺漏的測試 |

### 未從 ECC 移植（含原因）

| Command | 原因 |
|---|---|
| `/pr`、`/review-pr` | 不需要 PR 工作流程 |
| `/multi-*`（共 5 個指令） | 多代理協作尚未成熟 |
| `/learn`、`/skill-create` | 依賴 ECC observation hooks 與完整 instinct pipeline；由 `/learn-eval` 取代 |
| `/evolve` | 由 `/learn-eval` 中的 skill-curator 生命週期取代 |
| `/hookify-*`（共 4 個指令） | ECC 內部 hook 管理 |
| `/sessions`、`/save-session`、`/resume-session` | 已由 `.agents/memory/` 系統取代 |
| 語言專屬的建構／測試／審查指令 | Go/Rust/Kotlin/Java 等語言未使用 |
| `/cost-report`、`/model-route` | 有需要時再新增 |
| `/jira`、`/prp-*`、`/plan-prd` | 未規劃 PM 整合 |

---

## Skills

Skills 是內部工作流程文件，在對應的 command 或 agent 需要時載入。

### 記憶體與工作流程（原創——非來自 ECC）

| Skill | 用途 |
|---|---|
| `commit-helper` | Conventional Commits 格式、pre-commit 檢查清單 |
| `memory-manager` | 讀取、更新、壓縮專案記憶體的完整流程；包含凍結快照模型、Hermes 對齊路由規則與大小健康標準 |
| `memory-sql` | SQLite FTS5 冷記憶：schema、session 記錄、搜尋查詢與層級路由規則 |
| `skill-curator` | session 萃取品質門（整體判定）、skill 生命週期（active/stale/archived）、儲存位置指引 |
| `worktree-manager` | Worktree 建立／完成／合併，並整合記憶體；雙模式：Mode A 使用內建 `EnterWorktree`/`ExitWorktree`，Mode B 使用 git worktree 搭配完整生命週期 |

### 開發（從 ECC v2.0.0-rc.1 移植）

| Skill | 用途 |
|---|---|
| `coding-standards` | 跨語言基準：KISS/DRY/YAGNI、命名規範、錯誤處理 |
| `cost-aware-llm-pipeline` | LLM 成本控制：模型路由、預算追蹤、提示快取 |
| `eval-harness` | Claude Code 工作階段的正式評估框架 |
| `git-workflow` | 分支策略、commit 慣例、衝突解決 |
| `github-ops` | CI/CD 除錯、版本管理、Dependabot 監控 |
| `llm-trading-agent-security` | 交易代理安全性：消費上限、斷路器、金鑰處理 |
| `python-testing` | pytest、fixtures、mocking、parametrization、涵蓋率 |
| `tdd-workflow` | Red-Green-Refactor 循環，目標涵蓋率 80%+ |
| `verification-loop` | 執行 → 分析 → 修正的迭代流程 |

### 未從 ECC 移植（含原因）

| Skill | 原因 |
|---|---|
| `python-patterns` | PEP 8 格式化由 ruff 處理；慣例由 `python-reviewer` agent 涵蓋 |
| `deep-research` | 需要 firecrawl + exa MCP——延後至 MCP 設定完成 |
| `api-design`、`backend-patterns` | 本股票專案非 web backend |
| `security-review` | 已由 `security-reviewer` agent 和 `llm-trading-agent-security` 涵蓋 |
| 非 Python 語言模式 | 未使用的語言 |
| `homelab-*`、`network-*`、`healthcare-*` | 領域不符 |
| `angular-developer`、`react-*`、`nextjs-*` | 未規劃前端 |

---

## Hooks

Hooks 是由 Claude Code harness 自動執行的 Python 腳本。

| Hook | 觸發時機 | 執行內容 |
|---|---|---|
| `session_start.py` | 工作階段開始 | 以凍結快照模式將 `CLAUDE.md` 與 `.agents/memory/MEMORY.md` 注入上下文（session 執行中不重新讀取，保留 LLM 前綴快取）；並將記憶體分類結構複製到新 worktree |
| `post_tool_use_hygiene.py` | Edit 或 Write 之後 | 對 `.py` 檔案：執行 `ruff format`、`ruff check`、`mypy`，並對 `print()` 發出警告；對 `.md/.py/.toml/.json/.yaml/.yml` 檔案：執行 `file_hygiene.py` |
| `stop_memory_check.py` | 每次回覆後 | 若有重大工作則提示記憶更新；在 5 次以上有程式碼變更的回覆後，每 session 提示一次技能審查（`/learn-eval`） |

### 已注意但未從 ECC 移植的 hook 概念

| 概念 | 狀態 | 原因 |
|---|---|---|
| PostToolUse 持續學習 | **部分實作** | 已在 `stop_memory_check.py` 加入技能審查觸發器；完整 hook 觀察管線（instinct YAML、背景 Haiku agent）未移植——在沒有持久程序的情況下過於重量級 |
| Stop 治理捕捉 | 延後 | ECC 在 session 結束時記錄安全事件——若專案發展到包含自主交易代理時將有其相關性 |

---

## Rules

Rules 是依路徑範圍載入的 Markdown 檔案，當 Claude 處理符合的檔案類型時生效。

| 規則集 | 路徑 | 來源 | 備註 |
|---|---|---|---|
| `rules/common/` | 所有檔案 | ECC v2.0.0-rc.1 | 通用原則：KISS/DRY/YAGNI、命名規範、錯誤處理、不可變性、檔案大小限制 |
| `rules/python/` | `**/*.py`、`**/*.pyi` | ECC v2.0.0-rc.1（已修改） | 所有函式簽名須加型別注解；格式化工具由 black 改為 **ruff**；必須使用 logging（禁用 `print()`） |

### 未從 ECC 移植（含原因）

| 規則集 | 原因 |
|---|---|
| `rules/typescript/`、`rules/react/` 等 | 未使用的語言 |
| `rules/cpp/` | SV/UVM 與 C++ 差異過大；延後——待 UVM 專案啟動時建立 `rules/systemverilog/` |

---

## 延後項目

| 項目 | 類型 | 前提條件 |
|---|---|---|
| **冷記憶搜尋（SQLite FTS5）** | Hermes 移植 | 見下方說明 |
| `deep-research` skill | ECC 移植 | 先設定 firecrawl + exa MCP |
| `marketing-agent` agent | ECC 移植 | 確認短片製作規劃啟動 |
| `uvm-patterns` skill | 自訂建置 | UVM 專案啟動 |
| `rules/systemverilog/` | 自訂建置 | UVM 專案啟動 |
| README 中的 CI/CD 指引 | 文件更新 | 整合穩定後進行 |

### 冷記憶搜尋——SQLite FTS5（延後）

**Hermes** 將所有 session 訊息儲存在本機 SQLite 資料庫（`~/.hermes/state.db`），搭配 FTS5 全文搜尋，讓過去任何對話都能在約 20ms 內被召回，無需 LLM 彙整。

**為什麼尚未實作**：Claude Code Stop hook 的 event 中只有 `session_id` 和 `cwd`，沒有對話內容。然而，Claude Code 的 transcript 本身以 JSONL 格式儲存於磁碟（`~/.claude/projects/<hash>/<session_id>.jsonl`），Stop hook 理論上可在 session 結束後讀取它。實作需要：
1. Stop hook 讀取目前 session 的 JSONL transcript。
2. 解析工具呼叫與助手訊息，萃取有意義內容。
3. 寫入 `.agents/memory/sessions.db`（FTS5 虛擬表，git-ignored）。
4. 新增 `/session-search <query>` 斜線指令支援 FTS5 查詢。

**狀態：已實作。** `memory-db` MCP server（`uvx mcp-server-sqlite`）已配置在 `.claude/mcp.json`（透過 `uv run python .claude/scripts/start_memory_mcp.py` 啟動）。Claude 透過 MCP `write_query` 明確寫入資料庫——Stop hook 會提示 Claude upsert session 記錄並歸檔已畢業的條目。Schema 與查詢範例請參考 `.claude/skills/memory-sql/SKILL.md`。
