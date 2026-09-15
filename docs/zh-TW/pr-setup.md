# 下游專案啟用 PR 交付

[共用 Git 工作契約](../en/git-workflow.md) 預設為 local-only。本文件供專案擁有者設定環境，不授予 agent 設定、發布或管理權限；英文版見 [PR setup](../en/pr-setup.md)。

## 身分與權限隔離

- 選定 repository 與預設分支。開發 GitHub App 只取得推送任務分支與建立 PR 所需的權限，不取得規則管理或繞過權限。私鑰保存在擁有者控制的秘密管理工具，由 repository 外部提供短效 installation token。
- 逐一確認 Git HTTPS／SSH、`gh` 與 GitHub plugin 的實際身分；它們可能使用不同憑證。開發 session 不應能改用擁有者憑證。Worktree 不隔離憑證；若要強制角色分離，需隔離執行環境或提供憑證的服務。
- 若指定 session 要正式 Approve，提供獨立審核身分，且只讓那些 session 使用。同帳號的兩張 token 不是兩個審核者；應實測核准是否計入 repository 規則，AI 留言或表情反應不算正式核准。
- 管理憑證不交給開發或審核 session。若只有擁有者能合併，啟用交付前必須建立獨立強制執行的合併界線；一般寫入權限不等於「只能推分支、永遠不能 merge」。平台角色無法拆分時，可使用受限工具服務；開發／審核 session 不應取得底層可合併的憑證。

## Repository 保護

- 確認 GitHub 方案支援該 repository 可見性所需的保護。啟用預設分支的 ruleset，要求 PR、有效的獨立核准、CI 通過、審查討論已處理，以及新增修改後重新核准；禁止 force push 與刪除分支，不設定 bypass 身分。
- 先建立適合專案的 CI，再選擇必要 check 名稱。可從 README 範例開始，採用前將第三方 actions 固定至核實的完整 commit SHA，維持穩定 job 名稱，確認 PR 真的會執行檢查。本地 pre-commit 通過不代表遠端合併條件已成立。
- CI 與 ownership 政策的修改需特別審查。執行 PR 程式時不提供高權限發布或管理憑證；高權限審核／合併自動化應置於待審程式之外。
- 優先使用現有 GitHub／Codex PR 介面與審核整合，再考慮自製收件匣。通知與 reviewer 指派需依實際帳號設定；自動審查意見與 GitHub 必要核准是不同結果。

## 啟用與驗收

1. 在 `git-workflow.md` 的 current-state 項目記錄核准的 repository／remote、base branch、發布身分與啟用狀態；如有常設 reviewer 授權，也在該處記錄。不要記錄憑證。
2. 配合該範圍調整實際 agent 的工具權限。本模板仍保留 Claude push 確認與 Codex 平台核准；改文字不會取消提示。等身分與伺服器保護完成，再調整執行環境設定。
3. 用可丟棄的任務分支與小 PR 驗證建立、CI、審核與擁有者授權的合併。確認直接更新預設分支、未取得必要檢查／核准的合併會被拒絕，且新增 commit 後需重新核准。拒絕測試應使用測試 repository 或擁有者核准的探測；正式 repository 設定錯誤時，測試寫入可能真的成功。
4. 若僅擁有者能合併，驗證開發與審核 session 即使面對所有檢查與核准皆通過的 PR，嘗試合併仍會被拒絕。使用測試 repository 或擁有者核准的探測，記錄實際強制執行機制；界線生效前不啟用常設交付。確認 PR job 不取得 write token 或高權限 secrets。驗證開發／審核憑證不能管理或繞過規則，並確認每個啟用客戶端的實際身分。保留驗收證據與未完成事項，再宣告保護已生效。

本 starter kit 不會安裝 GitHub App、修改 `gh` 登入、啟用 ruleset、新增實際 CI workflow 或取消 push 提示。這些步驟由各下游專案完成；官方參考連結見[英文版](../en/pr-setup.md#references)。
