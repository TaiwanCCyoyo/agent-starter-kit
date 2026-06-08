# Codex 元件參考

Codex 使用原生 Plan Mode、repo skills、專用 subagents、project hooks、plugins 與專案級 MCP，不逐一複製 Claude Code 的 slash commands。

## 原生對應

| Claude／ECC 概念 | Codex 實作 |
| :--- | :--- |
| `/plan` 與 planner agent | 原生 Plan Mode 與 `<proposed_plan>` |
| Loop operator | `verification-loop` skill |
| GitHub operations skill | 已安裝的 GitHub plugin |
| Slash commands | 自然語言觸發 skills |
| `memory-db` MCP | `.codex/config.toml` 專案級 server |

## Agents

| Agent | 用途 |
| :--- | :--- |
| `repo_explorer` | 唯讀探索 repo 與依賴路徑 |
| `implementation_reviewer` | 正確性、回歸、測試與非預期 diff 審查 |
| `python_reviewer` | Python typing、ruff、logging、測試與可維護性審查 |
| `security_reviewer` | secrets、危險命令、注入、依賴與權限審查 |
| `performance_reviewer` | 延遲、吞吐、記憶體、複雜度與工具成本審查 |
| `commit_specialist` | 從 repo root 審查 staged changes 並執行明確要求的 commit |
| `doc_translator` | 有界限的翻譯修改 |
| `memory_auditor`／`memory_compressor` | 唯讀記憶建議與壓縮草案 |

## Skills

| Skill | 用途 |
| :--- | :--- |
| `coding-standards` | Codex 原生架構與限縮實作判斷 |
| `python-testing` | 聚焦 Python 回歸與靜態檢查 |
| `tdd-workflow` | 從 ECC 改編的風險導向 RED-GREEN-REFACTOR |
| `verification-loop` | 精簡的實作、檢查、修正循環 |
| `gen-commit` | Commit 審查與 Conventional Commit workflow |
| `memory-manager`、`save-memory`、`compress-memory` | 共用專案記憶生命週期 |
| `memory-sql` | 與 Holographic 相容的 SQLite facts 與重複問題 workflow |
| `skill-review` | ECC 萃取品質門與手動 Hermes 式技能整理 |
| `worktree-manager` | 含記憶整合的 worktree 生命週期 |

## Hooks 與 Gates

| 元件 | 用途 |
| :--- | :--- |
| `.codex/hooks/session_start.py` | 初始化 `.memories/` 與 SQLite schema，並注入 `MEMORY.md`、`USER.md` |
| `.codex/hooks/post_tool_use_hygiene.py` | 執行聚焦格式化、lint、檔案 hygiene 與 Python print 檢查 |
| `.codex/hooks/stop_memory_check.py` | 容量、嚴格 taxonomy、session 隔離提醒、SQL 畢業指引與一次性 skill review |
| `.pre-commit-config.yaml` | Hygiene、secrets、ruff、no-print 與 mypy commit gate |

## 可搜尋記憶 MCP

`.codex/config.toml` 將 `memory-db` 定義為專案級 stdio MCP：

- 使用 `uvx mcp-server-sqlite`
- 資料庫為 `.memories/memory_store.db`
- 透過 `cwd = ".."` 從 repo root 啟動
- 讀取工具自動核准
- Schema 與寫入工具需要提示核准
- 啟動失敗不會阻止 Codex 啟動

Codex 與 Claude Code 已完成遷移。Antigravity adapter 已實作但尚待 runtime 驗證；Gemini CLI 仍待遷移。

## ECC 對應

已移植或改編：

- Coding、Python testing、TDD、verification、security、performance 與 review 原則。
- Prompt Defense baseline。
- Hook 或 script 修改必須包含 functional test。
- Session skill-review 品質門。

由 Codex 原生功能取代：

- Planner agent 與 `/plan`。
- Loop operator。
- GitHub operations workflow。
- Claude slash-command wrappers。

未移植：

- ECC observation／instinct pipeline 與背景學習程序。
- Hookify 與 harness 內部工具。
- 本 starter kit 未使用的語言或領域 workflow。

## Hermes 對應

已實作：

- 有容量上限的 `MEMORY.md` 與 `USER.md`。
- SessionStart 凍結快照。
- 與 Hermes 相容的有界檔案與凍結 session-start snapshot。
- 與 Holographic 相容的 SQLite facts、FTS5、entities、trust metadata、重複問題 occurrences 與已驗證 resolutions。
- 手動 skill review 與生命週期判斷。

尚未實作：

- 自動記錄每一則對話。
- 無感 transcript recall。
- Hermes 背景 skill curator。
- 常駐非同步 memory process。
