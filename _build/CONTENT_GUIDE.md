# Olimedi 專欄寫作與上架規範（給每週自動發文用）

## 上架流程
1. 從 `_build/topics.md` 取第一個 `[ ]` 題目。
2. 新增 `_build/posts/YYYY-MM-DD-NN-<英文-slug>.html`（日期用台北時間當天）。檔案開頭是 META JSON，格式照現有文章：
   `slug, title, desc(搜尋摘要 80–120 字), cat(排班考勤／庫存管理／診所經營), intro, date, sources[[名稱,網址]], related[其他文章 slug]`，接著是文章 HTML 內文（h2/h3/p/ul/ol/table，表格外包 `<div class="table-wrap">`，提醒用 `<p class="note">`）。
3. 執行 `python3 _build/build.py`（會產生 blog/ 頁面、專欄首頁、sitemap.xml）。
4. 在 topics.md 把該題改成 `[x]` 並附 slug；commit 並 push 到 main。

## 內容原則
- 對象：所有醫療院所（西醫、牙醫、中醫、復健、醫美…），不要只寫牙醫或醫美；例子要通用。
- 寫實用做法，不寫成廣告；1,500–2,500 字；段落短、多用小標、清單、表格。
- 產品名稱固定用「Oli 考勤管理系統」「Oli 庫存管理系統」；品牌「Olimedi 奧里醫療資訊」。文末 CTA 由版型自動加上，內文最多自然提到一次產品。
- 法規內容（勞基法、勞健保、醫材法規等）：必須先查勞動部、衛福部、食藥署、全國法規資料庫等官方來源，sources 附上官方連結；文末加 `<p class="note">本文為一般性說明，不構成法律意見…以主管機關最新公告為準</p>`。不確定的數字不要寫。
- 不用絕對用語（保證、一定、完全、防止、最…）；不寫「符合法規」「通過認證」；不捏造數據、案例、客戶或推薦語。
- 不提及真實診所、病患或廠商名稱。

## 每次完成後要回報給 Jim 的內容
- 文章標題與網址 https://olimedi.com/blog/<slug>.html
- FB 貼文（網站連結放第一個網址，LINE 連結放後面，3–5 個 hashtag）
- IG 圖文短文（連結請放個人檔案）
- Threads 短版（口語、200 字內）
