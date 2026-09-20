# PR 審核

擁有者授權範圍為 `TaiwanCCyoyo/agent-starter-kit` 的 `main`。PR 審核由擁有者在 Codex 設定中啟用的 GitHub 整合服務執行，以每個 PR 為單位觸發，不是排程；完整契約見[英文版](../en/pr-review.md)。

實作 agent 負責[PR 後續處理](../en/git-workflow.md#pr-follow-through)：等待 CI 與審核結果、處理範圍內成立的意見，並在確認修正後解決對應的審核討論，才算完成。合併權仍由擁有者保留。

- PR 建立或更新時自動審核；在 PR 留言 `@codex review` 可隨時手動觸發。
- 審核在服務商端執行，消耗擁有者的 Codex 程式碼審核額度，不佔用本專案的 GitHub Actions 分鐘數。
- 審核結果是建議性留言，不等於 GitHub Approve，也不會執行合併。審核者的權限來自擁有者在 Codex 設定中的配置，位於本 repository 之外；PR 內容無法授予它憑證或擴大其權限，因此修改本檔案也不會改變該邊界。
- 本機不存放任何 GitHub App 私鑰。原本的 `taiwanccyoyo-dev-agent`、`taiwanccyoyo-review-agent` 兩個 App 與本機 PowerShell 取權杖助手已停用。
- Agent session 以擁有者本人的 GitHub 憑證推送任務分支並建立 PR，因此 agent 產出的 commit 會歸屬於擁有者。以分支前綴與 commit 訊息區分 agent 工作，不以身分區分。
- 由於 agent 與擁有者共用同一身分，這個安排沒有強制的角色隔離；擁有者接受此限制。
- `protect-main` 沒有 bypass 對象，要求走 PR、所有審核討論都已解決、且當前 revision 的 `repository-checks` 通過。該 job 執行完整 pre-commit 與全部測試。它不要求 Approve，因為單一身分無法核准自己的 PR。
- 合併由擁有者決定。合併前確認必要檢查在當前 head 通過、讀過審核發現並逐項處理。不得使用 admin merge、force push 或放寬規則來強行合併。

下游專案須自行設定審核整合、規則與授權；複製文件不代表啟用。
