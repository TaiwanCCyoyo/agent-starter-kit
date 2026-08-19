# 記憶系統介紹

本專案將可提交的 Agent 基礎設施與本機實例化記憶分開。

## 目錄

```text
.memories/                       # 完整 gitignore 的本機記憶
├── memories/
│   ├── MEMORY.md
│   └── USER.md
└── memory_store.db
```

`MEMORY.md` 與 `USER.md` 採用 Hermes 的有界原子條目格式，每筆以獨立一行的 `§` 分隔，並在 session 啟動時以凍結快照注入。

`memory_store.db` 是 SQLite，採用 Hermes Holographic fact-store schema，並加入本專案的重複問題生命週期資料表。

## 職責

| 儲存                                                     | 用途                                                               |
| :------------------------------------------------------- | :----------------------------------------------------------------- |
| `MEMORY.md`                                              | 多數未來 session 都需要的穩定專案、環境與工具事實；最多 2,200 字元 |
| `USER.md`                                                | 穩定的使用者偏好與協作期待；最多 500 字元                          |
| `facts`                                                  | 可搜尋的決策、lesson、workflow、工具與環境事實                     |
| `entities`、`fact_entities`、`memory_banks`、`facts_fts` | 與 Holographic 相容的 entity、retrieval 與 FTS5 支援               |
| `problem_patterns`                                       | 重複 blocker、workaround、錯誤假設或混淆的穩定識別                 |
| `problem_occurrences`                                    | 每次問題再次出現的具體證據                                         |
| `resolutions`                                            | Root cause、解法、驗證證據，以及相關 skill 或 instruction 修改     |

Plan、已完成 plan、原始 transcript 與任意歷史文件不屬於長期記憶。請使用 Agent 原生 planning state、`.tmp/`、維護中的 `docs/` 與 Git history。

## 重複問題閉環

同一問題第二次出現時：

1. 查詢既有 facts、patterns、occurrences 與 resolutions。
2. 記錄新的 occurrence 與證據。
3. 停止重複未驗證的 workaround。
4. 調查 root cause。
5. 記錄已驗證 resolution，或明確的外部 blocker。
6. 必要時更新既有 skill、instruction 或 regression test。

## Hermes 相容性

有界檔案格式與 Hermes 的 `memories/MEMORY.md`、`memories/USER.md` 相容。SQLite schema 以 Holographic provider tables 為基礎，未來可讓 Hermes Holographic 指向同一個 `memory_store.db`。

Hermes 的 `SOUL.md` 與 `state.db` 不在本契約內。Agent identity 繼續由各平台原生 instruction files 管理；目前 hooks 也沒有可靠的完整訊息生命週期可建立 transcript database。

## 目前平台狀態

- **Codex**：已遷移至 `.memories/` 與 `memory_store.db`。
- **Claude Code**：已退出（2026-08-20）——Claude 改用 Claude Code 的內建記憶。僅作為 `.memories/` 的保管者（建立骨架、同步 worktree），以供 Codex 與 Antigravity sessions 尋找其狀態；詳見 `.claude/rules/common/memory.md`。
- **Antigravity**：adapter 已實作，尚待 runtime 驗證。

## Antigravity 生命週期

- `.agent/hooks/session_start.py` 會初始化 bounded files 與 SQLite schema、複製 worktree 缺少的記憶，並注入 `MEMORY.md` 與 `USER.md`。
- `.agent/hooks/stop_memory_check.py` 會檢查 bounded-file 限制與嚴格 taxonomy。
- `.agent/skills/memory-manager/SKILL.md` 定義記憶路由。
- `.agent/skills/memory-sql/SKILL.md` 定義 SQLite 查詢與寫入流程。
- Antigravity 的 `memory-db` MCP server 必須設定在平台支援的全域設定中。
