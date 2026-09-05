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
| `signal_miner`            | 唯讀     | 低成本的大量輸出隔離工具；委派有具體收益時使用，只回傳精簡證據                                                                                |
| `task_worker`             | 有界寫入 | 執行已有明確範圍、驗收條件與驗證方式的低至中風險修改；當範圍或風險擴大時停止並回報                                                            |
| `plan_reviewer`           | 唯讀     | 計畫完整性、範圍、排序、repo 對齊、可測試性與風險                                                                                             |
| `implementation_reviewer` | 唯讀     | 正確性、回歸、測試與非預期 diff                                                                                                               |
| `security_reviewer`       | 唯讀     | Secrets、注入、依賴、權限、auth 與敏感資料                                                                                                    |
| `doc_translator`          | 有界寫入 | 低階文件翻譯與同步者：將任何需寫入檔案的翻譯處理到單一明確的非 canonical 目標；main agent 決定來源與目標，衝突時以其維護的 canonical 文件為準 |
| `commit-specialist`       | 有界寫入 | 選用的 commit 代理；依 mode 審查 staged diff、執行 pre-commit 與 commit，sandbox 失敗時交還 main agent                                        |

### 模型路由

| 層級            | 模型                     | 角色                                        |
| --------------- | ------------------------ | ------------------------------------------- |
| 高可信審查      | `gpt-5.6-sol` / high     | Plan 與 implementation review               |
| Security review | `gpt-5.6-sol` / high     | Security review                             |
| 有界實作        | `gpt-5.6-terra` / medium | 由 `task_worker` 執行明確限定範圍的一般實作 |
| 高流量機械工作  | `gpt-5.6-luna` / medium  | Signal mining、commit 與文件同步            |

`plan_reviewer` 只審查計畫，不取代 Native Plan Mode。一般程式碼定位使用 `explorer`；需要隔離大量輸出、能節省 context 時使用 `signal_miner`。短檢查直接在本地執行；沒有具體收益時避免同層級 handoff。`task_worker` 讓高階 main agent 將有界實作降級給 Terra，而 Luna 處理機械式工作。模糊、架構與 security-sensitive 的判斷應留給 main agent 或指定 reviewer。Security review 適用於變更的 trust boundary、permissions、secrets、不可信輸入處理與敏感資料流；單純例行檔案存取不需要 delegation。

目前七個角色加上內建 `explorer` 已涵蓋持續出現的工作。只有在證明存在缺口時才新增角色。主要模型仍由使用者選擇；角色的模型預設不代表已量測的成本節省或品質。除非實際 workload 證明需要，否則維持既有的並行數與深度預設。

## Skills

| Skill                | 用途                                                                                                  |
| :------------------- | :---------------------------------------------------------------------------------------------------- |
| `python-development` | Python coding、typing、logging、secrets、security routing、Codex hook ownership 與條件式 FastAPI 指引 |
| `python-testing`     | 精確 pytest、選配 coverage、Ruff、mypy、hook fixtures 與 Windows path 要求                            |
| `gen-commit`         | 有界 local commit、選用 specialist review 與執行、sandbox handoff 及回報                              |

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
- 盡可能將適用的 OpenSpec status 與 workflow 修正納入已驗證的 commit。常駐授權允許在不重複請求核准的情況下，改善專案內的 skills、hooks、rules 與 agent configuration：先驗證、在本地 commit，並回報變更內容與原因。外部操作、全域設定與平台權限不在此授權內。
- Native memory 寫入須依目前的儲存規則取得使用者明確請求。

## Hooks 與 Gates

| 元件                                    | 用途                                                                            |
| :-------------------------------------- | :------------------------------------------------------------------------------ |
| `.codex/hooks/session_start.py`         | 回報 branch/worktree context 並注入 `.codex/AGENTS.md`                          |
| `.codex/hooks/post_tool_use_hygiene.py` | 修改 Python 檔案後執行唯讀的精簡 Ruff `F` diagnostics                           |
| `.pre-commit-config.yaml`               | Formatting、file hygiene、detect-secrets、Ruff T201 與目標檔案 mypy             |
| `.vscode/settings.json`                 | Final newline、trailing whitespace hygiene，以及 Python Ruff formatter defaults |

Python verification 在開發期間使用目標式 `uv run python -m pytest`，並在完成前針對變更檔案執行 pre-commit。若 formatter 修改檔案，agent 會檢查 diff 並重跑相關 checks。Coverage 透過 `uv run python -m pytest --cov --cov-report=term-missing` 選配執行，不設全域百分比 gate。

`gen-commit` 在需要實質審查、訊息粗略或缺漏，或明確要求獨立檢查時使用 `commit-specialist`。main agent 可在訊息完整、沒有無關 staged files 且變更已驗證時，直接 commit 小型 agent-owned 變更，並使用相同驗證與一般 hooks。若 delegated step 在 sandbox 或 cache 權限邊界失敗，specialist 會不重試、不改環境地回傳確切錯誤；main agent 只在既有授權 context 接手受阻步驟。

是否檢查 diff 由明確 mode 決定，不會自動發生。沒有訊息或只有粗略目標時，specialist 會讀 staged diff 並完成訊息；若 main agent 對乾淨且明確的 scope 已提供完整訊息，specialist 不讀 diff，重點是 pre-commit 與 commit。只有 main agent 因具體疑慮明確要求 double-check 時，完整訊息才會搭配額外 diff 檢查；specialist 不得自行升級到該 review mode。

## 延後能力

- 目前專案以外的無人值守背景 curation 或變更；在授權工作期間，專案內改善可使用上述常駐授權。
- Eval-driven development infrastructure，直到有真實 runner、deterministic graders、baselines、重複執行 metrics 與 CI integration。
- LLM API cost routing 或 transaction-authorized agent 的領域 skills，直到 repo 採用這些 application surfaces。

## Runtime Verification

編輯後 hook 保留 Ruff `F`，排除 `F401,F841,F842`，只檢查該次事件指明的 Python 檔案。完整 lint 與排版留給 pre-commit；此 hook 不會自動 fix，也沒有擴大 lint 規則範圍。

SessionStart 保留 instruction injection，因為 `.codex/AGENTS.md` 不是預設 discovery chain 中的 root instruction filename。它回報 checkout metadata，不從 branch names 或 commit messages 推斷 task。Hooks 使用已準備好的環境與 `uv run --no-sync`；使用前需先建立 dependencies。PostToolUse 每次 edit event 執行一次帶有 `--no-fix` 與 timeout 的 Ruff，回報 warnings 而不取代原始 tool result。

Entrypoint tests 驗證 protocol output 與真實 Ruff 執行，不驗證每個 desktop tool path 的 dispatch。將 hooks 視為 enforcement 前，必須在目標 runtime 檢查 live matcher coverage。Pre-commit 仍是完成 gate。

[官方 model guidance](https://developers.openai.com/api/docs/guides/latest-model) 建議審查互相衝突的 skill instructions。[Hook reference](https://learn.chatgpt.com/docs/hooks) 說明 `continue: false` 會取代正常的 PostToolUse result；此處的 diagnostic-only feedback 使用 `systemMessage`。
