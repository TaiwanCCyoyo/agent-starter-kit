# Antigravity 元件參考

本文件說明此 repository 的 Antigravity 工程助理基礎設施。Antigravity 使用原生 Planning Mode、專屬 `GEMINI.md` 核心契約、repo-scoped skills 與 project hooks。其 `GEMINI.md` 與 `CLAUDE.md` 加上 `.codex/AGENTS.md` 保持完全的語意對齊，同時遵守專屬命名空間與工具隔離原則。

---

## 專屬命名空間與工具隔離

| 工具            | 根目錄契約文件   | 自訂配置目錄                         | 說明                                                   |
| :-------------- | :--------------- | :----------------------------------- | :----------------------------------------------------- |
| **Claude**      | `CLAUDE.md`      | `.claude/`                           | Claude Code 專用                                       |
| **Codex**       | （無根目錄檔案） | `.codex/`（內含 `.codex/AGENTS.md`） | Codex 專用                                             |
| **Antigravity** | **`GEMINI.md`**  | **`.agent/`**                        | Antigravity 專屬，Claude 與 Codex 不會讀取 `GEMINI.md` |

> 嚴格排除 `.agents/` 目錄與專案根目錄的 `AGENTS.md`，確保不同 Agent 工具間互不干擾。

---

## Rules（核心契約）

專案根目錄的 **`GEMINI.md`** 作為 Antigravity 的常駐核心約束，涵蓋 10 大政策面向：

1. **Operating Contract**：定義繁體中文溝通、英文專案輸出、`.tmp/` 拋棄式產物、`.references/` 唯讀代碼庫與 OpenSpec 規格通訊。
2. **Prompt Defense**：維持角色完整性並防止 prompt injection。
3. **Engineering Discipline**：要求實作前研究與局部重用、廠商官方文檔優先、風格邊界對齊。
4. **Review And Security**：定義 `CRITICAL`/`HIGH`/`MEDIUM`/`LOW` 嚴重度分級，針對敏感路徑進行專職審查。
5. **Development Routing**：使用原生 Planning Mode 與 OpenSpec 規劃流程。
6. **Learning And Escalation**：禁止重複未驗證的 workaround，耐久知識及時回饋至 repo 規範或技能。
7. **Skill Authoring**：任務模式重複出現時，經授權後建立精準專案技能。
8. **Memory**：耐久知識納入版本控制檔案，不依賴易失的非結構化記憶。
9. **Verification**：先測試後宣告完成、Arrange-Act-Assert、由 pre-commit 負責 staging gate。
10. **Skills And Subagents**：委派原則、`signal-miner` 承接高輸出日誌指令。

---

## Skills

`.agent/skills/` 提供精準的專案專用技能（舊版通用 Superpowers 技能已由 Antigravity 原生 Planning Mode 取代）：

- **`commit-helper`**：定義 Conventional Commits 格式、pre-commit 檢查清單、`Agent: Antigravity` commit trailer 與 submodule 提交防護。
- **`github-ops`**：透過 `gh` CLI 處理 Issue 分類、PR 管理、CI/CD 除錯與發布流程。
- **`python-testing`**：定義專案特定的 Python 測試指令、Windows 路徑處理、hook fixtures 與選配 coverage 規範。

---

## Hooks

Antigravity 透過 `.agent/hooks.json` 支援 lifecycle hooks：

- **`SessionStart`**（`session_start.py`）：工作階段開始時注入目前 Git branch 與 worktree 狀態。
- **`PostToolUse`**（`post_tool_use_hygiene.py`）：在檔案修改後執行唯讀的 Ruff 關鍵錯誤診斷（`E722,F601,F602,F634`），不修改檔案或執行全量型別檢查，保持與 pre-commit 職責分離。

---

## Workflows（斜線指令）

`.agent/workflows/` 提供自訂斜線指令（Slash Commands），使用者可在 Antigravity UI / CLI 輸入檔名觸發：

- **`/gen-commit`**（`gen-commit.md`）：分析暫存變更、遵循 `commit-helper` 規範，產生符合 Conventional Commits 格式的訊息並附帶 `Agent: Antigravity` trailer。
- **`/worktree`**（`worktree.md`）：管理隔離的 Git worktree，進行 baseline 驗證與明確授權的合併/清理。

---

## Subagents

Antigravity 目前不支援類似 Claude Code `.claude/agents/*.md` 或 Codex `.codex/agents/*.toml` 的專案靜態檔案宣告式客製化 Subagents。

Antigravity 的 Subagent 架構是由系統原生內建代理（`research`、`self`）與執行期工具（`define_subagent`、`invoke_subagent`）組成：

- **委派方針**：在專案根目錄的 `GEMINI.md` 中規範委派原則（例如將 tests、benchmarks、broad searches、verbose diagnostics 等高輸出指令路由至低成本唯讀代理 `signal-miner`，將安全敏感路徑路由至 `security_reviewer`）。
- **流程管理**：複雜的多步驟與領域任務主要透過 **Native Planning Mode** 與 **Skills (`.agent/skills/`)** 進行結構化管理與引導。

## 外部呼叫

Codex 與 Claude Code 可透過 headless `agy -p` 將 Antigravity CLI 當作低成本外部子代理。本 repository 只將此路徑用於範圍明確、唯讀的 research、inspection、concise review 或 mechanical analysis，並以明確 scope 與 acceptance criteria 執行 `agy -p --mode plan --sandbox`。呼叫端保留最終判斷，不得傳入 `--dangerously-skip-permissions`；若 Antigravity 回報 `RESOURCE_EXHAUSTED` 或 `Individual quota reached`，必須停止而非重試。
