# Codex 元件參考

Codex 使用 Native Plan Mode、原生 local memories、repo-scoped skills、專用 subagents、project hooks 與已安裝 plugins。其 `.codex/AGENTS.md` 與 `CLAUDE.md` 的共享政策保持語意對齊，同時保留 Codex 專屬 approval 與 tool constraints。

## 原生與 Plugin 對應

| 能力                                         | Codex 實作                                                |
| :------------------------------------------- | :-------------------------------------------------------- |
| 規劃                                         | Native Plan Mode 與 `<proposed_plan>`                     |
| 計畫品質審查                                 | 唯讀 `plan_reviewer` agent                                |
| TDD、除錯、worktree、完成前驗證              | Codex 原生能力、project skills 與明確檢查                 |
| GitHub issues、PR、CI、review comments、發布 | 已安裝的 GitHub plugin                                    |
| Slash commands                               | 自然語言 skill triggers                                   |
| 跨 session planning                          | Native planning 加上選用的 project-owned OpenSpec files   |
| 跨 session recall                            | 由 project configuration 啟用的 Codex 原生 local memories |

Codex 將 planning 與 implementation 權責保留在 main agent。Read-only agents 負責 critique、security review、verification feedback，以及從大範圍搜尋、logs、test output、diffs，或任何 stdout 會淹沒 main context 的指令中整理 context-isolated evidence summaries；它們不取代 Codex Native Plan Mode，也不會在沒有使用者明確授權時接管 commit、push、merge 或 pull request。

## Agents

| Agent                     | 權限     | 用途                                                                                                                                          |
| :------------------------ | :------- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| `signal_miner`            | 唯讀     | 最低成本的機械式探索；在執行前承接預期會產生大量 log 或 stdout 的指令，僅回傳精簡訊號而非原始輸出                                             |
| `task_worker`             | 有界寫入 | 執行已有明確範圍、驗收條件與驗證方式的低至中風險修改；當範圍或風險擴大時停止並回報                                                            |
| `plan_reviewer`           | 唯讀     | 計畫完整性、範圍、排序、repo 對齊、可測試性與風險                                                                                             |
| `implementation_reviewer` | 唯讀     | 正確性、回歸、測試與非預期 diff                                                                                                               |
| `security_reviewer`       | 唯讀     | Secrets、注入、依賴、權限、auth 與敏感資料                                                                                                    |
| `doc_translator`          | 有界寫入 | 低階文件翻譯與同步者：將任何需寫入檔案的翻譯處理到單一明確的非 canonical 目標；main agent 決定來源與目標，衝突時以其維護的 canonical 文件為準 |
| `commit-specialist`       | 有界寫入 | 審查 staged changes，僅在明確要求時 commit                                                                                                    |

### 模型路由

| 層級            | 模型                     | 角色                                        |
| --------------- | ------------------------ | ------------------------------------------- |
| 高可信審查      | `gpt-5.6-sol` / high     | Plan 與 implementation review               |
| Security review | `gpt-5.6-luna` / xhigh   | Security review                             |
| 有界實作        | `gpt-5.6-terra` / medium | 由 `task_worker` 執行明確限定範圍的一般實作 |
| 高流量機械工作  | `gpt-5.6-luna` / medium  | Signal mining、commit 與文件同步            |

`plan_reviewer` 只審查計畫，不取代 Native Plan Mode。Antigravity CLI 可用時，`antigravity-subagent` 是範圍明確、唯讀的 research、inspection、concise review 或 mechanical analysis 的優先低成本外部路徑：以明確 scope 與 acceptance criteria 執行 `agy -p --mode plan --sandbox`，並檢閱回應。模糊、architecture、security-sensitive 或最終 integration judgment 不使用它；若回報 `RESOURCE_EXHAUSTED` 或 `Individual quota reached`，停止而非重試。`signal_miner` 是最低成本的唯讀苦力，負責機械式探索與有界的高輸出指令；若 tests、benchmarks、廣泛搜尋、verbose diagnostics、dependency traces 或大型 diff/log inspections 預期會產生大量輸出，應在 main context 執行前就委派。`task_worker` 則是只供高階 main agent 降級執行有界修改的中價選項，任務必須有明確目標、範圍、驗收條件與驗證方式。最低階 main agent 應自行處理簡單工作或使用適當的原生低成本路由，不升級到 `task_worker`。模糊、跨領域、security-sensitive、architecture 與 planning 工作應留給 main agent 或適合的內建 agent。Authentication、authorization、不可信輸入、database、filesystem、external API、cryptography、payment 與敏感資料變更應觸發 security review。

## Skills

| Skill                  | 用途                                                                                                  |
| :--------------------- | :---------------------------------------------------------------------------------------------------- |
| `python-development`   | Python coding、typing、logging、secrets、security routing、Codex hook ownership 與條件式 FastAPI 指引 |
| `python-testing`       | 精確 pytest、選配 coverage、Ruff、mypy、hook fixtures 與 Windows path 要求                            |
| `gen-commit`           | Commit 審查、Conventional Commits、commit 後 plan 更新與 durable-guidance checks                      |
| `antigravity-subagent` | 透過 headless `agy -p` 將低成本、有界、唯讀工作委派給 Antigravity CLI                                 |

## Claude 能力取捨

| Claude 能力                                                  | Codex 決策               | 原因                                                                                                                                                           |
| :----------------------------------------------------------- | :----------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/plan`                                                      | 原生／選用 artifact 取代 | 對話式規劃由原生 Plan Mode 提供。持久化 PRD-based 或跨 session planning handoff 可在 OpenSpec files 存在時使用。                                               |
| `plan-reviewer`                                              | 已移植                   | 獨立 plan critique 有價值，且不重複 plan creation。                                                                                                            |
| `/feature-dev`                                               | 原生取代                 | Brainstorming、Plan Mode、test-first development、verification 與 review 已構成完整流程。                                                                      |
| `/build-fix`                                                 | 原生取代                 | Evidence-driven debugging 加 repository verification 已涵蓋逐步診斷與修復。                                                                                    |
| `/code-review`                                               | 原生／plugin 取代        | Local review 使用 Codex review stance 與 agents；PR review 使用 GitHub plugin。                                                                                |
| `/python-review`                                             | Skill 取代               | `python-testing` 提供 repo 支援的 Ruff、mypy、pytest 與選配 coverage。                                                                                         |
| `/security-scan`                                             | Agent 與 gates 取代      | 已有 `security_reviewer`、detect-secrets、hooks、pre-commit；未安裝 AgentShield。                                                                              |
| `/test-coverage`                                             | Skill 取代               | 選配 coverage 已在 `python-testing`；Codex 不需要 command wrapper。                                                                                            |
| `github-ops`                                                 | Plugin 取代              | GitHub plugin 提供 repo、issue、PR、CI、comment 與發布流程，且 connector semantics 可維持更新。                                                                |
| `cost-aware-llm-pipeline`                                    | 不移植                   | 它是 application-domain 指引，含 provider-specific model names 與易變價格，不是 Codex 工作流。待 repo 真正建立 LLM API pipeline 時，再依官方資料做共享 skill。 |
| `eval-harness`                                               | 已移除／延後             | 它引用不存在的 `/eval` commands，且沒有 runner、grader、baseline format、Python commands 或 CI integration。具備這些能力後才恢復。                             |
| `llm-trading-agent-security`                                 | 不移植                   | 僅適用會簽交易或有 wallet authority 的 agents；repo 出現該執行面時再共享。                                                                                     |
| `architect`、`code-simplifier`、`loop-operator`、`tdd-guide` | 不鏡像                   | Codex 由 main agent 負責 planning/implementation，並使用 project-scoped skills；複製 write-capable specialists 會造成權責重疊。                                |
| `code-reviewer`、`silent-failure-hunter`、`python-reviewer`  | 已整併                   | `implementation_reviewer`、`security_reviewer`、Python skills 與 systematic debugging 已涵蓋有效面向。                                                         |
| `performance-optimizer`                                      | 主代理審查               | 僅在有量測到的瓶頸時，才要求針對性的效能分析。                                                                                                                 |

## 共享政策對齊

| 共享行為                                                          | Codex owner                                             |
| :---------------------------------------------------------------- | :------------------------------------------------------ |
| Operating contract、prompt defense、scoped changes                | `.codex/AGENTS.md`                                      |
| 實作前 research 與 reuse                                          | `.codex/AGENTS.md` engineering discipline               |
| Review severity 與 CRITICAL/HIGH completion policy                | `.codex/AGENTS.md` review and security section          |
| Security triggers 與 secret handling                              | `.codex/AGENTS.md` 加上 `security_reviewer`             |
| Risk-based test scope                                             | `.codex/AGENTS.md` verification section                 |
| Python development rules                                          | `python-development`                                    |
| Repository Python verification                                    | `python-testing`                                        |
| Planning、TDD、debugging、review、verification、branch completion | Native Codex、project agents 與 repository verification |

共享開發行為現在與 Claude common-rule routing layer 對齊：plan 透過 Native Plan Mode 或選用的 project-owned OpenSpec files；test/debug 透過原生 workflow、task-specific tests 與 project skills；review 透過 `implementation_reviewer` 與專職 reviewers；PR 準備在可用時交給 GitHub plugin；branch completion 則透過明確的原生 Git 操作，並遵守 Codex approval 規則。

## Plans、原生 Memory 與 Commits

- OpenSpec specs、changes 與 tasks 存在時就是一般 project-owned files；當它們屬於專案紀錄時就提交。
- OpenSpec planning artifacts 可以作為一般專案歷史，記錄 goals、decisions、tasks、verification、status 與 related commits；它們不屬於 durable memory，也不需要放進 `.references/`。
- Codex 原生 local memories 位於 repository 外的使用者 Codex home，並提供選用 recall；必要 repository 規則仍放在 checked-in guidance。
- Commit 後若有相關 OpenSpec change 就更新它，並套用 `.codex/AGENTS.md` 的常駐 Skill Authoring 規則。

## Hooks 與 Gates

| 元件                                    | 用途                                                                            |
| :-------------------------------------- | :------------------------------------------------------------------------------ |
| `.codex/hooks/session_start.py`         | 回報 branch/worktree context 並注入 `.codex/AGENTS.md`                          |
| `.codex/hooks/post_tool_use_hygiene.py` | 修改 Python 檔案後執行唯讀的精簡 Ruff `F` diagnostics                           |
| `.pre-commit-config.yaml`               | Formatting、file hygiene、detect-secrets、Ruff T201 與目標檔案 mypy             |
| `.vscode/settings.json`                 | Final newline、trailing whitespace hygiene，以及 Python Ruff formatter defaults |

Python verification 在開發期間使用目標式 `uv run python -m pytest`，並在完成前針對變更檔案執行 pre-commit。若 formatter 修改檔案，agent 會檢查 diff 並重跑相關 checks。Coverage 透過 `uv run python -m pytest --cov --cov-report=term-missing` 選配執行，不設全域百分比 gate。

## 延後能力

- 超出原生 memory extraction 與明確 skill authoring 的背景 skill curation。
- Eval-driven development infrastructure，直到有真實 runner、deterministic graders、baselines、重複執行 metrics 與 CI integration。
- LLM API cost routing 或 transaction-authorized agent 的領域 skills，直到 repo 採用這些 application surfaces。
