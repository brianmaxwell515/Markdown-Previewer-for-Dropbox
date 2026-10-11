# Markdown Previewer for Dropbox

[English](README.md) | 繁體中文

這是一個 Chrome/Brave 擴充功能，會在 Dropbox 網頁版的檔案檢視器加上 **Preview** 按鈕。按下後會把 `.md`／`.markdown` 檔案顯示成排版後的 Markdown，採用 GitHub 風格，有程式碼語法高亮，並會自動切換淺色／深色模式。

Dropbox 顯示檔案的兩個地方都可以用：

- 檔案列表右側的快速預覽面板（`/home/...?quickview=...`）
- 完整預覽頁面（`/preview/...md`）

## 安裝

1. 打開 `chrome://extensions`（或 `brave://extensions`）。
2. 開啟右上角的「開發人員模式」。
3. 按「載入未封裝項目」，選擇這個資料夾。
4. 在 dropbox.com 開啟一個 `.md` 檔案，按檢視器右上角的 **Preview**。按 **Source** 可回到原始文字。

## 打包上架用的 zip

```powershell
powershell -ExecutionPolicy Bypass -File .\build.ps1
```

會產生 `dist/markdown-previewer-for-dropbox-<版本>.zip`，只包含擴充功能需要的檔案。發布更新前，請先把 `manifest.json` 的 `version` 加一。上架文字與圖片放在 [store/](store/)。

## 隱私權

本擴充功能不收集、不儲存、不傳送任何資料。詳見[隱私權政策](PRIVACY.zh-TW.md)。

## 運作方式

- Dropbox 的檢視器會從 `previews.dropbox.com/p/orig/.../p.md` 下載原始檔案。擴充功能用 `PerformanceObserver` 偵測這個請求，再用你目前的登入狀態抓取同一個網址。
- 抓到的內容會跟畫面上顯示的文字比對。內容不符或下載失敗時，就改用頁面上的文字來渲染。
- Markdown 由 [marked](https://github.com/markedjs/marked) 轉換、[DOMPurify](https://github.com/cure53/DOMPurify) 過濾不安全的內容、[highlight.js](https://highlightjs.org/) 做語法高亮，樣式採用 [github-markdown-css](https://github.com/sindresorhus/github-markdown-css)。這些函式庫都放在 `lib/` 資料夾，因為 Manifest V3 不允許從網路載入程式碼。
- 按鈕和預覽畫面放在 Shadow DOM 裡，樣式不會跟 Dropbox 互相干擾。

## 限制

- Markdown 裡使用相對路徑的圖片（`![](img.png)`）不會顯示。
- 擴充功能依靠 Dropbox 頁面上的 `data-testid="fvsdk_text_preview"` 和 `fvsdk_preview_content` 找到預覽區。若 Dropbox 改版，請更新 `content.js` 開頭的選擇器。
