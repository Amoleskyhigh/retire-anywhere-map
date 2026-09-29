# 城市圖片資產工作流程

新增城市圖片時，必須遵循以下流程：

1. **選擇合法來源**：優先使用 Wikimedia Commons 等可確認授權的來源；記錄原始檔案頁、作者與授權條款。
2. **AI 編修**：以原始合法圖片作為參考，做一致化的色彩、清晰度與裁切處理。不得移除或弱化原始授權要求，也不得把 AI 編修圖標示成原始攝影作品。
3. **下載到 repository**：將最終 PNG/JPEG 存放在 `assets/cities/`，城市資料的 `img` 必須使用 repository-relative path，例如 `assets/cities/da_nang_ai_edited.png`；執行時不得依賴外部圖片 URL。
4. **保留 metadata**：城市資料必須包含 `image_source`、`image_license`、`image_edit_note`，並在 `data/image_attributions.md` 登錄來源、作者、授權與成品路徑。
5. **執行 QA**：依序執行 `python tests/qa_city_image_assets.py` 與 `python tests/qa_vietnam_city_images.py`。前者檢查所有 repository-local 圖片的存在性、檔案大小、格式、兩份資料檔一致性、授權 metadata 與共同圖片解析器；後者檢查指定城市的圖片映射，以及 popup/detail modal 的圖片載入流程。
6. **部署前驗證**：QA PASS 後才可 commit/push；部署後再確認線上頁面能讀取本地 asset path，避免只驗證 GitHub push 成功。

## 不接受的做法

- 只貼外部 hotlink 而不下載資產。
- 沒有作者、來源或授權資訊的圖片。
- 只在 popup 修圖片、卻沒有同步修 city detail modal。
- 以「圖片 URL 有字串」取代實際檔案與圖片格式檢查。
