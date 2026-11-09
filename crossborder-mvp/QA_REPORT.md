# QA_REPORT.md — Cross-border Lab v2.2

Date: 2026-11-09
Scope: `github_deploy/cross-border-lab-v2.2.html`
Public URL: https://amoleskyhigh.github.io/retire-anywhere-map/cross-border-lab-v2.2.html

## QA 結果

### 1. 線上版本與部署（PASS）
- Public URL HTTP 200。
- 線上 `<title>`、頁尾與語系內容均標示 `v2.2`。
- 線上 HTML 與本機待部署檔案 SHA-256 一致。
- GitHub Pages 來源 repository：`Amoleskyhigh/retire-anywhere-map`，branch：`main`。

### 2. 核心流程與按鈕（PASS）
- 中文／英文切換可用，標題與介面文字同步切換。
- 第 1 題選項可選取，未選取時「下一題」維持 disabled。
- 第 1 → 第 2 → 第 3 題流程可完成。
- 預算 slider 可操作並更新預算顯示。
- 「看我的推薦」可產生結果。
- Top 3 卡片正常渲染。
- 「查看其他國家」可展開其他 7 國，再次操作可收合。
- 比較表其餘國家可展開。
- 城市／國家詳細視窗可開啟、關閉。
- 「重新設定條件」可回到第 1 題並清除流程狀態。

### 3. 手機版（PASS）
- 測試 viewport：390×844。
- 頁面無水平溢出：`body.scrollWidth = 390`。
- 問卷、按鈕、推薦卡片、比較表與 modal 均可操作。

### 4. Console／錯誤（PASS）
- Playwright 無頭瀏覽器實測無 `console.error`。
- 無 `pageerror`。
- 頁面為自包含靜態 HTML，核心流程不依賴外部 API。

### 5. 測試證據
- HTTP：PASS
- 雙語切換：PASS
- 三題問卷：PASS
- 推薦結果：3 張 Top cards + 7 張展開 cards：PASS
- 比較表展開：7 列：PASS
- 詳細 modal：PASS
- 重設流程：PASS
- Mobile viewport：PASS
- Console/page errors：PASS

## 結論

FINAL: 100% PASS

v2.2 已完成 QA，線上版本確認為 v2.2，無 blocker。
