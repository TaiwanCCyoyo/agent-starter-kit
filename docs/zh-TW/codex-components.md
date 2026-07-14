# Codex 元件參考

Codex 使用 Native Plan Mode、repo-scoped skills、專用 subagents、project hooks、已安裝 plugins 與專案級 memory MCP。其 `.codex/AGENTS.md` 與 `CLAUDE.md` 加上 `.claude/rules/common/` 的共享政策保持語意對齊，同時保留 Codex 專屬 approval 與 tool constraints。

## 原生與 Plugin 對應

| 能力 | Codex 實作 |
| :--- | :--- |
| 規劃 | Native Plan Mode 與 `<proposed_plan>` |
| 計畫品質審查 | 唯讀 `plan_reviewer` agent |
| TDD、除錯、worktree、完成前驗證 | 已安裝的 Superpowers plugin |
| GitHub issues、PR、CI、review comments、發布 | 已安裝的 GitHub plugin |
| Slash commands | 自然語言 skill triggers |
| 跨 session planning | Native planning 加上選用的 project-owned OpenSpec files |
| 可搜尋記憶 | 專案級 `memory-db` MCP server |

Codex 將 planning 與 implementation 權責保留在 main agent。Read-only agents 負責 critique、security review、verification feedback，以及從大範圍搜尋、logs、test output、diffs，或任何 stdout 會淹沒 main context 的指令中整理 context-isolated evidence summaries；它們不取代 Codex Native Plan Mode，也不會在沒有使用者明確授權時接管 commit、push、merge 或 pull request。

## Agents

| Agent | 權限 | 用途 |
| :--- | :--- | :--- |
| `signal_miner` | 唯讀 | 最低成本的機械式探索，從 repository searches、execution traces、冗長 logs、diffs、tests 與 command output 挖出關鍵訊號 |
| `task_worker` | 有界寫入 | 執行已有明確範圍、驗收條件與驗證方式的低至中風險修改；當範圍或風險擴大時停止並回報 |
| `plan_reviewer` | 唯讀 | 計畫完整性、範圍、排序、repo 對齊、可測試性與風險 |
| `implementation_reviewer` | 唯讀 | 正確性、回歸、測試與非預期 diff |
| `security_reviewer` | 唯讀 | Secrets、注入、依賴、權限、auth 與敏感資料 |
| `memory_auditor`／`memory_compressor` | 唯讀 | Save 分類與 compression 草案的 advisory layer；final writes 仍由主代理與 memory skills 負責 |
| `doc_translator` | 有界寫入 | 低階文件同步者：依 main agent 提供的 source diff 修改單一明確的非 canonical 目標；衝突時以 main agent 維護的 canonical 文件為準 |
| `commit_specialist` | 有界寫入 | 審查 staged changes，僅在明確要求時 commit |

### 模型路由

| 層級 | 模型 | 角色 |
|---|---|---|
| 高可信審查 | `gpt-5.6` / high | Plan、implementation 與 security review |
| 平衡判斷 | `gpt-5.6-terra` / low-medium | Memory compression |
| 有界實作 | `gpt-5.6-terra` / medium | 由 `task_worker` 執行明確限定範圍的一般實作 |
| 高流量機械工作 | `gpt-5.6-luna` / medium | Signal mining、commit、文件同步與 memory 分類 |

`plan_reviewer` 只審查計畫，不取代 Native Plan Mode。`signal_miner` 是最低成本的唯讀苦力，負責機械式探索與消化冗長輸出；`task_worker` 則是只供高階 main agent 降級執行有界修改的中價選項，任務必須有明確目標、範圍、驗收條件與驗證方式。最低階 main agent 應自行處理簡單工作或使用適當的原生低成本路由，不升級到 `task_worker`。模糊、跨領域、security-sensitive、architecture 與 planning 工作應留給 main agent 或適合的內建 agent。Authentication、authorization、不可信輸入、database、filesystem、external API、cryptography、payment 與敏感資料變更應觸發 security review。

## Skills

| Skill | 用途 |
| :--- | :--- |
| `python-development` | Python coding、typing、logging、secrets、security routing、Codex hook ownership 與條件式 FastAPI 指引 |
| `python-testing` | 精確 pytest、選配 coverage、Ruff、mypy、hook fixtures 與 Windows path 要求 |
| `gen-commit` | Commit 審查、Conventional Commits、commit 後 plan 更新、memory routing 與 skill review |
| `memory-manager` | Memory 初始化、讀取、audit、taxonomy、health checks 與 operation routing |
| `save-memory` | 明確 durable writes、分類、bounded-file limits 與 deduplication handoff |
| `compress-memory` | Bounded-file 清理、去重與低頻知識 graduation |
| `memory-sql` | SQLite 唯一 owner，負責 schema discovery、reads、writes、重複問題與 verified resolutions |
| `skill-review` | 人工 reusable-pattern 品質門與 skill candidate routing |
| `worktree-memory-sync` | 跨 worktree 的 ignored memory 初始化與整合 |

## Claude 能力取捨

| Claude 能力 | Codex 決策 | 原因 |
| :--- | :--- | :--- |
| `/plan` | 原生／選用 artifact 取代 | 對話式規劃由原生 Plan Mode 提供。持久化 PRD-based 或跨 session planning handoff 可在 OpenSpec files 存在時使用。 |
| `plan-reviewer` | 已移植 | 獨立 plan critique 有價值，且不重複 plan creation。 |
| `/feature-dev` | Superpowers／原生取代 | Brainstorming、Plan Mode、TDD、verification 與 review 已構成完整流程。 |
| `/build-fix` | Superpowers／原生取代 | Systematic debugging 加 repository verification 已涵蓋逐步診斷與修復。 |
| `/code-review` | 原生／plugin 取代 | Local review 使用 Codex review stance 與 agents；PR review 使用 GitHub plugin。 |
| `/python-review` | Skill 取代 | `python-testing` 提供 repo 支援的 Ruff、mypy、pytest 與選配 coverage。 |
| `/security-scan` | Agent 與 gates 取代 | 已有 `security_reviewer`、detect-secrets、hooks、pre-commit；未安裝 AgentShield。 |
| `/test-coverage` | Skill 取代 | 選配 coverage 已在 `python-testing`；Codex 不需要 command wrapper。 |
| `github-ops` | Plugin 取代 | GitHub plugin 提供 repo、issue、PR、CI、comment 與發布流程，且 connector semantics 可維持更新。 |
| `cost-aware-llm-pipeline` | 不移植 | 它是 application-domain 指引，含 provider-specific model names 與易變價格，不是 Codex 工作流。待 repo 真正建立 LLM API pipeline 時，再依官方資料做共享 skill。 |
| `eval-harness` | 已移除／延後 | 它引用不存在的 `/eval` commands，且沒有 runner、grader、baseline format、Python commands 或 CI integration。具備這些能力後才恢復。 |
| `llm-trading-agent-security` | 不移植 | 僅適用會簽交易或有 wallet authority 的 agents；repo 出現該執行面時再共享。 |
| `architect`、`code-simplifier`、`loop-operator`、`tdd-guide` | 不鏡像 | Codex 由 main agent 負責 planning/implementation，並使用 Superpowers；複製 write-capable specialists 會造成權責重疊。 |
| `code-reviewer`、`silent-failure-hunter`、`python-reviewer` | 已整併 | `implementation_reviewer`、`security_reviewer`、Python skills 與 systematic debugging 已涵蓋有效面向。 |
| `performance-optimizer` | 主代理審查 | 僅在有量測到的瓶頸時，才要求針對性的效能分析。 |

## 共享政策對齊

| 共享行為 | Codex owner |
| :--- | :--- |
| Operating contract、prompt defense、scoped changes | `.codex/AGENTS.md` |
| 實作前 research 與 reuse | `.codex/AGENTS.md` engineering discipline |
| Review severity 與 CRITICAL/HIGH completion policy | `.codex/AGENTS.md` review and security section |
| Security triggers 與 secret handling | `.codex/AGENTS.md` 加上 `security_reviewer` |
| Risk-based test scope | `.codex/AGENTS.md` verification section |
| Python development rules | `python-development` |
| Repository Python verification | `python-testing` |
| Planning、TDD、debugging、review、verification、branch completion | Native Codex、project agents 與 Superpowers phase routing |

Superpowers 已在 Codex 啟用。它提供 workflow guidance，但不得繞過 user intent、sandbox approvals、dirty-worktree protections、repository ownership，或 delegation、commit、destructive action、push、merge 與 pull request 所需的明確授權。Codex 的 PR 準備與發布行為由 GitHub plugin workflows 擁有。

共享開發行為現在與 Claude common-rule routing layer 對齊：plan 透過 Native Plan Mode、選用的 project-owned OpenSpec files，或 Superpowers planning skills；test/debug 透過 Superpowers；review 透過 `implementation_reviewer` 與專職 reviewers；PR 準備交給 GitHub plugin；branch completion 則由 Superpowers 在 Codex approval 規則內處理。

## Plans、Memory 與 Commits

- OpenSpec specs、changes 與 tasks 存在時就是一般 project-owned files；當它們屬於專案紀錄時就提交。
- OpenSpec planning artifacts 可以作為一般專案歷史，記錄 goals、decisions、tasks、verification、status 與 related commits；它們不屬於 durable memory，也不需要放進 `.references/`。
- Commit 後，若存在相關 OpenSpec change 就更新它，再把真正 durable 的 facts、decisions、lessons、重複問題或 verified resolutions 路由到 memory。
- 可重用修正與 workflows 經 `skill-review`；尚未成熟的想法可存成低信任 `candidate` facts。

## Hooks 與 Gates

| 元件 | 用途 |
| :--- | :--- |
| `.codex/hooks/session_start.py` | 初始化 `.memories/`、SQLite schema 與 bounded session context |
| `.codex/hooks/post_tool_use_hygiene.py` | 聚焦格式化、lint、file hygiene，並透過 Ruff 阻擋 Python print calls |
| `.codex/hooks/memory_health_check.py` | Memory limits、taxonomy 與 plan routing |
| `.pre-commit-config.yaml` | File hygiene、detect-secrets、Ruff T201 print blocking 與完整專案 mypy |
| `.vscode/settings.json` | Final newline、trailing whitespace hygiene，以及 Python Ruff formatter defaults |

Python verification 使用 `uv run python -m pytest`、`uv run ruff check --fix .` 與 `uv run mypy .`。Coverage 透過 `uv run python -m pytest --cov --cov-report=term-missing` 選配執行，不設全域百分比 gate。

## 延後能力

- 自動 transcript capture 與透明召回。
- 常駐非同步 memory 或背景 skill curation。
- Eval-driven development infrastructure，直到有真實 runner、deterministic graders、baselines、重複執行 metrics 與 CI integration。
- LLM API cost routing 或 transaction-authorized agent 的領域 skills，直到 repo 採用這些 application surfaces。
