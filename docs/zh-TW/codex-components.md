# Codex 元件參考

這份文件說明 starter kit 裡 Codex 專屬的組件。Codex 不逐項複製 Claude Code 的 slash commands，而是使用原生 Plan Mode、repo-scoped skills、少量專職 reviewer agents，以及輕量 hooks。

## 原生規劃

Codex 的規劃由主 agent 透過 Plan Mode 與 `<proposed_plan>` 輸出承擔。本 repository 不新增獨立的 `planner` agent，也不為 Codex 建立 Claude-style command layer。

當任務需要釐清產品意圖、架構取捨、migration 形狀，或需要 decision-complete 的實作交接時，使用 Codex 的規劃流程。

## Agents

| Agent | 用途 |
| :--- | :--- |
| `repo_explorer` | Read-only repository orientation 與 codebase discovery。 |
| `implementation_reviewer` | 一般 correctness、regression、test coverage 與 unintended diff review。 |
| `python_reviewer` | Python typing、ruff、logging、tests 與 maintainability review。 |
| `security_reviewer` | Secrets、unsafe commands、injection risks、dependency surfaces 與 permission boundaries。 |
| `performance_reviewer` | Targeted latency、throughput、memory、algorithmic 與 tooling-cost review。 |
| `commit_specialist` | Staged-change review、Conventional Commit drafting，以及明確要求時執行 commit。 |
| `doc_translator` | 只針對明確指定的目標文件做 bounded translation edits。 |
| `memory_auditor` / `memory_compressor` | Read-only memory maintenance analysis 與 compression drafts。 |

專職 reviewer agents 是可選的分析工具，用來補強主 Codex agent，不取代 Codex 的一般實作或規劃流程。

## Skills

| Skill | 用途 |
| :--- | :--- |
| `coding-standards` | Codex-native architecture judgment、scoped implementation 與 review readiness。 |
| `python-testing` | Focused Python test 與 static-check strategy。 |
| `verification-loop` | 不新增 loop operator agent 的 concise implement-check-fix workflow。 |
| `gen-commit` | Commit review 與 Conventional Commit workflow。 |
| `memory-maintenance`, `save-memory`, `compress-memory` | Shared memory lifecycle operations。 |
| `worktree-manager` | Worktree creation、finish 與 memory consolidation workflow。 |

## Hooks 與 Gates

| Layer | 責任 |
| :--- | :--- |
| `.codex/hooks/session_start.py` | 注入 Codex instructions、memory、branch 與 worktree context。 |
| `.codex/hooks/post_tool_use_hygiene.py` | 編輯後的快速 targeted feedback。Python 檔會 format、lint、檢查 file hygiene，並提醒 `print()` calls；文字與設定檔只跑 file hygiene。 |
| `.codex/hooks/stop_memory_check.py` | 長時間工作且有 pending changes 時提醒更新 memory，並檢查 memory size。 |
| `.pre-commit-config.yaml` | Repository-level commit gate，包含 file hygiene、secrets、ruff、no-print Python hygiene 與 full-project mypy。 |

共用 hygiene 邏輯應放在 `scripts/`，讓 PowerShell、Bash、Git Bash 與 CI 都能使用同一套行為。

## 設計備註

- 不新增 Codex `planner` agent：原生 Plan Mode 負責規劃。
- 不新增 Codex `loop-operator` agent：迭代驗證放在 `verification-loop` skill。
- 不建立 Codex slash-command layer：command-like behavior 由 skills 與自然語言觸發承擔。
- Full-project `mypy .` 屬於 pre-commit 與 CI，不放在 post-edit hook。
