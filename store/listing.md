# Chrome Web Store 上架文字

依 Developer Dashboard 的分頁與欄位排列，直接複製貼上即可。

---

## 1. 商店資訊（Store listing）

### 名稱與摘要

名稱和摘要來自 `manifest.json` 的 `name`、`description`，不在後台填寫。

| 欄位 | 內容 |
| --- | --- |
| 名稱 | Markdown Previewer for Dropbox |
| 摘要（上限 132 字元） | Adds a Preview button to Dropbox's web file viewer that renders Markdown files. |

### 說明（Description）— English

```text
View your Markdown files the way they are meant to be read — right inside Dropbox.

Dropbox's web viewer shows .md files as plain text. Markdown Previewer for Dropbox adds a Preview button to the viewer. Click it to see the file rendered with headings, tables, lists and highlighted code. Click Source to switch back.

FEATURES
• Works in both the quick-view side panel and the full-page file preview
• GitHub-style formatting: headings, tables, task lists, block quotes, links and more
• Syntax highlighting for code blocks
• Follows your system's light or dark mode
• Hides YAML front matter and HTML comments
• Supports .md, .markdown, .mdown, .mkd, .mkdn and .mdx files

PRIVATE BY DESIGN
• Everything runs locally in your browser
• No data is collected, stored or sent anywhere
• No analytics, no tracking, no ads
• Open source: https://github.com/brianmaxwell515/Markdown-Previewer-for-Dropbox

HOW TO USE
1. Open dropbox.com and click a Markdown file.
2. Click Preview at the top right of the viewer.
3. Click Source to return to the original text.

Note: images referenced with relative paths inside the Markdown file are not displayed.

This extension is not affiliated with, endorsed by, or sponsored by Dropbox, Inc. Dropbox is a trademark of Dropbox, Inc.
```

### 說明（Description）— 繁體中文

在後台「商店資訊」右上角新增語言「中文（台灣）」後，貼在該語言的說明欄。

```text
直接在 Dropbox 裡，以排版後的樣子閱讀 Markdown 檔案。

Dropbox 網頁版只會把 .md 檔顯示成純文字。Markdown Previewer for Dropbox 會在檢視器加上 Preview 按鈕，按下後即可看到包含標題、表格、清單與程式碼高亮的排版結果；按 Source 即可切回原始文字。

功能特色
• 支援檔案列表的快速預覽面板，以及完整預覽頁面
• GitHub 風格排版：標題、表格、待辦清單、引言區塊、連結等
• 程式碼區塊語法高亮
• 自動配合系統的淺色／深色模式
• 自動隱藏 YAML front matter 與 HTML 註解
• 支援 .md、.markdown、.mdown、.mkd、.mkdn、.mdx 檔案

重視隱私
• 所有處理都在你的瀏覽器中完成
• 不收集、不儲存、不傳送任何資料
• 沒有分析、追蹤或廣告
• 開放原始碼：https://github.com/brianmaxwell515/Markdown-Previewer-for-Dropbox

使用方式
1. 開啟 dropbox.com，點選一個 Markdown 檔案。
2. 按檢視器右上角的 Preview。
3. 按 Source 回到原始文字。

注意：Markdown 中使用相對路徑的圖片不會顯示。

本擴充功能與 Dropbox, Inc. 無任何關聯，亦未經其認可或贊助。Dropbox 是 Dropbox, Inc. 的商標。
```

### 其他欄位

| 欄位 | 內容 |
| --- | --- |
| 類別（Category） | Productivity → Tools |
| 語言（Language） | English（預設），另加「中文（台灣）」 |
| 商店圖示 | `icons/icon128.png` |
| 截圖 | `store/screenshots/01` ～ `04`，依檔名順序上傳 |
| 小型宣傳圖塊 | `store/promo/small-tile.png`（440×280） |
| 官方網址（Official URL） | 留空（需要經 Google Search Console 驗證網域才能填） |
| 首頁網址（Homepage URL） | https://github.com/brianmaxwell515/Markdown-Previewer-for-Dropbox |
| 支援網址（Support URL） | https://github.com/brianmaxwell515/Markdown-Previewer-for-Dropbox/issues |
| 成人內容（Mature content） | 否 |

---

## 2. 隱私權（Privacy）

### 單一用途說明（Single purpose）

```text
Render Markdown files as formatted text inside the Dropbox website's file viewer.
```

### 權限理由（Permission justification）

**Host permission**（`https://previews.dropbox.com/*`，以及內容腳本執行的 `https://www.dropbox.com/*`）：

```text
The content script runs on www.dropbox.com only to add a Preview button to Dropbox's file viewer. Access to previews.dropbox.com is used to download the original Markdown file that the user is currently viewing (the same URL Dropbox's own viewer loads), so the rendered preview is complete. No other sites are accessed and no data leaves the browser.
```

### 遠端程式碼（Remote code）

選 **No, I am not using remote code**。

```text
All JavaScript (marked, DOMPurify, highlight.js) is bundled in the package. The extension does not load or execute any code from external servers.
```

### 資料使用（Data usage）

- 「你打算收集哪些使用者資料」：**全部不勾選**。檔案內容只在瀏覽器裡處理，不會傳出裝置，依 Chrome 線上應用程式商店的定義不算「收集」。
- 下方三項聲明全部**勾選**：
  - I do not sell or transfer user data to third parties, outside of the approved use cases
  - I do not use or transfer user data for purposes that are unrelated to my item's single purpose
  - I do not use or transfer user data to determine creditworthiness or for lending purposes

### 隱私權政策網址（Privacy policy URL）

```text
https://github.com/brianmaxwell515/Markdown-Previewer-for-Dropbox/blob/main/PRIVACY.md
```

---

## 3. 發布（Distribution）

| 欄位 | 建議 |
| --- | --- |
| 付款 | 免費 |
| 可見度 | 公開（Public）；想先小範圍測試可選「不公開」（Unlisted） |
| 地區 | 所有地區 |
