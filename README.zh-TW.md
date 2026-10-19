# Markdown Previewer for Dropbox

[English](README.md) | 繁體中文

![Markdown Previewer for Dropbox](store/promo/marquee.png)

[![Chrome Web Store](https://img.shields.io/chrome-web-store/v/mcmfjcocjahlihlalehjkfniibgbcbae?label=Chrome%20Web%20Store&logo=googlechrome&logoColor=white&color=0068EF)](https://chromewebstore.google.com/detail/markdown-previewer-for-dr/mcmfjcocjahlihlalehjkfniibgbcbae)

這是一個 Chrome/Brave 擴充功能，用來改善 Dropbox 網頁版顯示 Markdown 檔案的方式。Dropbox 以 Markdown 格式檢視 `.md` 檔時，擴充功能會把 Dropbox 的排版換成 GitHub 風格的排版，有程式碼語法高亮，並會跟著 Dropbox 的主題切換淺色／深色模式。Dropbox 的純文字檢視則維持不變，用 Dropbox 本身的檢視切換按鈕就能看到原始文字。

Dropbox 顯示檔案的兩個地方都可以用：

- 檔案列表右側的快速預覽面板（`/home/...?quickview=...`）
- 完整預覽頁面（`/home/...?preview=...md`）

## 截圖

| | |
| --- | --- |
| ![升級 Dropbox 的 Markdown 檢視](store/screenshots/01-before-after.png) | ![不需要額外點擊](store/screenshots/02-nothing-to-click.png) |
| ![快速預覽面板與完整預覽頁面都能用](store/screenshots/03-quick-view-and-full-page.png) | ![表格、待辦清單與程式碼高亮，支援淺色／深色模式](store/screenshots/04-formatting-dark-mode.png) |

## 安裝

### 從 Chrome 線上應用程式商店安裝（建議）

到 Chrome 線上應用程式商店安裝 **[Markdown Previewer for Dropbox](https://chromewebstore.google.com/detail/markdown-previewer-for-dr/mcmfjcocjahlihlalehjkfniibgbcbae)**。Chrome、Brave 及其他 Chromium 瀏覽器都可以使用，而且會自動更新。

安裝後在 dropbox.com 開啟一個 `.md` 檔案。在 Dropbox 的 Markdown 檢視中，會直接以擴充功能的排版顯示；切換到 Dropbox 的純文字檢視即可看到原始文字。

### 從原始碼安裝

1. 從 [Releases](https://github.com/brianmaxwell515/Markdown-Previewer-for-Dropbox/releases) 下載 zip 並解壓縮，或 clone 這個 repo。
2. 打開 `chrome://extensions`（或 `brave://extensions`）。
3. 開啟右上角的「開發人員模式」。
4. 按「載入未封裝項目」，選擇該資料夾。

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
