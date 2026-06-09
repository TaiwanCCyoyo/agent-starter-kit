# Codex 元件參考

Codex 使用 Native Plan Mode、repo-scoped skills、專用 subagents、project hooks、已安裝 plugins 與專案級 memory MCP。它與 Claude Code 對齊結果及政策，但不逐一複製每個 Claude command 或 agent。

## 原生與 Plugin 對應

| 能力 | Codex 實作 |
| :--- | :--- |
| 規劃 | Native Plan Mode 與 `<proposed_plan>` |
| 計畫品質審查 | 唯讀 `plan_reviewer` agent |
| TDD、除錯、worktree、完成前驗證 | 已安裝的 Superpowers plugin |
| GitHub issues、PR、CI、review comments、發布 | 已安裝的 GitHub plugin |
| Slash commands | 自然語言 skill triggers |
| 跨 session plans | Git-ignored `.references/plans/*.plan.md` |
| 可搜尋記憶 | 專案級 `memory-db` MCP server |

## Agents

| Agent | 權限 | 用途 |
| :--- | :--- | :--- |
| `repo_explorer` | 唯讀 | Repo 導覽與依賴追蹤 |
| `plan_reviewer` | 唯讀 | 計畫完整性、範圍、排序、repo 對齊、可測試性與風險 |
| `implementation_reviewer` | 唯讀 | 正確性、回歸、測試與非預期 diff |
| `python_reviewer` | 唯讀 | Python runtime、typing、Ruff、測試、logging 與維護性 |
| `security_reviewer` | 唯讀 | Secrets、注入、依賴、權限、auth 與敏感資料 |
| `performance_reviewer` | 唯讀 | 已量測的延遲、記憶體、複雜度、I/O 與工具成本 |
| `memory_auditor`／`memory_compressor` | 唯讀 | 記憶建議與 bounded-file 壓縮草案 |
| `doc_translator` | 有界寫入 | 只修改明確指定的翻譯目標 |
| `commit_specialist` | 有界寫入 | 審查 staged changes，僅在明確要求時 commit |

`plan_reviewer` 只審查計畫，不取代 Native Plan Mode。Authentication、authorization、不可信輸入、database、filesystem、external API、cryptography、payment 與敏感資料變更應觸發 security review。

## Skills

| Skill | 用途 |
| :--- | :--- |
| `python-testing` | 精確 pytest、選配 coverage、Ruff、mypy、hook fixtures 與 Windows path 要求 |
| `gen-commit` | Commit 審查、Conventional Commits、commit 後 plan 更新、memory routing 與 skill review |
| `memory-manager`、`save-memory`、`compress-memory` | 共用 bounded 與 structured memory 生命週期 |
| `memory-sql` | 與 Holographic 相容的 SQLite facts 與重複問題 workflow |
| `skill-review` | 人工 reusable-pattern 品質門與 skill candidate routing |
| `worktree-memory-sync` | 跨 worktree 的 ignored memory 初始化與整合 |
| `plan-artifact` | 持久化跨 session/跨 agent 計畫產出——PRD 讀取、pattern grounding、結構化 `.references/plans/` 輸出。原生規劃負責互動式規劃；此 skill 專用於持久化結構化輸出。 |

## Claude 能力取捨

| Claude 能力 | Codex 決策 | 原因 |
| :--- | :--- | :--- |
| `/plan` | Skill + 原生取代 | 對話式規劃由原生 Plan Mode 提供。持久化產出（PRD-based 或跨 session）使用 `plan-artifact` skill；不需要 slash command。 |
| `plan-reviewer` | 已移植 | 獨立 plan critique 有價值，且不重複 plan creation。 |
| `/feature-dev` | Superpowers／原生取代 | Brainstorming、Plan Mode、TDD、verification 與 review 已構成完整流程。 |
| `/build-fix` | Superpowers／原生取代 | Systematic debugging 加 repository verification 已涵蓋逐步診斷與修復。 |
| `/code-review` | 原生／plugin 取代 | Local review 使用 Codex review stance 與 agents；PR review 使用 GitHub plugin。 |
| `/python-review` | Agent 取代 | `python_reviewer` 使用 repo 支援的 Ruff、mypy、pytest 與選配 coverage。 |
| `/security-scan` | Agent 與 gates 取代 | 已有 `security_reviewer`、detect-secrets、hooks、pre-commit；未安裝 AgentShield。 |
| `/test-coverage` | Skill 取代 | 選配 coverage 已在 `python-testing`；Codex 不需要 command wrapper。 |
| `github-ops` | Plugin 取代 | GitHub plugin 提供 repo、issue、PR、CI、comment 與發布流程，且 connector semantics 可維持更新。 |
| `cost-aware-llm-pipeline` | 不移植 | 它是 application-domain 指引，含 provider-specific model names 與易變價格，不是 Codex 工作流。待 repo 真正建立 LLM API pipeline 時，再依官方資料做共享 skill。 |
| `eval-harness` | 已移除／延後 | 它引用不存在的 `/eval` commands，且沒有 runner、grader、baseline format、Python commands 或 CI integration。具備這些能力後才恢復。 |
| `llm-trading-agent-security` | 不移植 | 僅適用會簽交易或有 wallet authority 的 agents；repo 出現該執行面時再共享。 |
| `architect`、`code-simplifier`、`loop-operator`、`tdd-guide` | 不鏡像 | Codex 由 main agent 負責 planning/implementation，並使用 Superpowers；複製 write-capable specialists 會造成權責重疊。 |
| `code-reviewer`、`silent-failure-hunter` | 已整併 | `implementation_reviewer`、`python_reviewer`、`security_reviewer` 與 systematic debugging 已涵蓋有效面向。 |
| `performance-optimizer` | 唯讀對等 | Codex 使用 `performance_reviewer`，要求先量測再最佳化。 |

## Plans、Memory 與 Commits

- `.references/plans/` 是原則上唯讀的 `.references/` 內唯一可寫例外。
- 核准的跨 session plan 記錄 goal、decisions、tasks、verification、更新時間、狀態與 related commit；保持 gitignored，且不屬於 durable memory。
- Commit 後，若存在相關 plan 就更新它，再把真正 durable 的 facts、decisions、lessons、重複問題或 verified resolutions 路由到 memory。
- 可重用修正與 workflows 經 `skill-review`；尚未成熟的想法可存成低信任 `candidate` facts。

## Hooks 與 Gates

| 元件 | 用途 |
| :--- | :--- |
| `.codex/hooks/session_start.py` | 初始化 `.memories/`、SQLite schema 與 bounded session context |
| `.codex/hooks/post_tool_use_hygiene.py` | 聚焦格式化、lint、file hygiene 與 Python no-print feedback |
| `.codex/hooks/stop_memory_check.py` | Memory limits、taxonomy、plan routing 與一次性 skill-review reminder |
| `.pre-commit-config.yaml` | File hygiene、detect-secrets、Ruff、no-print 與完整專案 mypy |

Python verification 使用 `uv run python -m pytest`、`uv run ruff check .` 與 `uv run mypy .`。Coverage 透過 `uv run python -m pytest --cov --cov-report=term-missing` 選配執行，不設全域百分比 gate。

## 延後能力

- 自動 transcript capture 與透明召回。
- 常駐非同步 memory 或背景 skill curation。
- Eval-driven development infrastructure，直到有真實 runner、deterministic graders、baselines、重複執行 metrics 與 CI integration。
- LLM API cost routing 或 transaction-authorized agent 的領域 skills，直到 repo 採用這些 application surfaces。
