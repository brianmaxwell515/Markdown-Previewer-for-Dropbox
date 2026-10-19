# Chrome Web Store 上架文字

依 Developer Dashboard 的分頁與欄位排列，直接複製貼上即可。

---

## 1. 商店資訊（Store listing）

### 名稱與摘要

名稱和摘要來自 `manifest.json` 的 `name`、`description`，不在後台填寫。

| 欄位 | 內容 |
| --- | --- |
| 名稱 | Markdown Previewer for Dropbox |
| 摘要（上限 132 字元） | Replaces Dropbox's Markdown view with clean GitHub-style formatting, tables, task lists and code highlighting. |

### 說明（Description）— English

```text
View your Markdown files the way they are meant to be read — right inside Dropbox.

Markdown Previewer for Dropbox replaces the formatting of Dropbox's Markdown view with clean, GitHub-style rendering: proper headings, tables, task lists and highlighted code. There is nothing extra to click. Dropbox's plain-text view is left unchanged, so you can still switch to the source with Dropbox's own view toggle.

FEATURES
• Works in both the quick-view side panel and the full-page file preview
• GitHub-style formatting: headings, tables, task lists, block quotes, links and more
• Syntax highlighting for code blocks
• Follows Dropbox's light or dark theme
• Hides YAML front matter and HTML comments
• Works with any Markdown file in your Dropbox

PRIVATE BY DESIGN
• Everything runs locally in your browser
• No data is collected, stored or sent anywhere
• No analytics, no tracking, no ads
• Open source: https://github.com/brianmaxwell515/Markdown-Previewer-for-Dropbox

HOW TO USE
1. Open dropbox.com and click a Markdown file.
2. In Dropbox's Markdown view, the file is shown with the extension's formatting.
3. Switch Dropbox to its plain-text view to see the source.

Note: images referenced with relative paths inside the Markdown file are not displayed.

This extension is not affiliated with, endorsed by, or sponsored by Dropbox, Inc. Dropbox is a trademark of Dropbox, Inc.
```

### 說明（Description）— 繁體中文

在後台「商店資訊」右上角新增語言「中文（台灣）」後，貼在該語言的說明欄。

```text
直接在 Dropbox 裡，以排版後的樣子閱讀 Markdown 檔案。

Markdown Previewer for Dropbox 會把 Dropbox「以 Markdown 格式檢視」的排版，換成整齊的 GitHub 風格：清楚的標題、表格、待辦清單與程式碼高亮，不需要額外按任何按鈕。Dropbox 的純文字檢視維持不變，用 Dropbox 本身的檢視切換按鈕就能看到原始文字。

功能特色
• 支援檔案列表的快速預覽面板，以及完整預覽頁面
• GitHub 風格排版：標題、表格、待辦清單、引言區塊、連結等
• 程式碼區塊語法高亮
• 自動配合 Dropbox 的淺色／深色主題
• 自動隱藏 YAML front matter 與 HTML 註解
• 適用於 Dropbox 中的任何 Markdown 檔案

重視隱私
• 所有處理都在你的瀏覽器中完成
• 不收集、不儲存、不傳送任何資料
• 沒有分析、追蹤或廣告
• 開放原始碼：https://github.com/brianmaxwell515/Markdown-Previewer-for-Dropbox

使用方式
1. 開啟 dropbox.com，點選一個 Markdown 檔案。
2. 在 Dropbox 的 Markdown 檢視中，會直接以擴充功能的排版顯示。
3. 切換到 Dropbox 的純文字檢視即可看到原始文字。

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
The content script runs on www.dropbox.com only to display Markdown files with the extension's formatting in Dropbox's file viewer. Access to previews.dropbox.com is used to download the original Markdown file that the user is currently viewing (the same URL Dropbox's own viewer loads), so the rendered preview is complete. No other sites are accessed and no data leaves the browser.
```

### 遠端程式碼（Remote code）

選 **No, I am not using remote code**。

```text
All JavaScript (marked, DOMPurify, highlight.js) is bundled in the package. The extension does not load or execute any code from external servers.
```

### 資料使用（Data usage）

- 「你打算收集哪些使用者資料」：只勾選**網站內容**（Website content），其他都不勾。擴充功能會讀取 Dropbox 頁面上的 Markdown 檔案文字；雖然只在瀏覽器裡處理、不會傳出裝置，但 Google 的 User Data FAQ 規定在本機處理的資料也必須揭露。
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
