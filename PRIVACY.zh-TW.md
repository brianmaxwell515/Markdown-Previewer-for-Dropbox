# 隱私權政策

[English](PRIVACY.md) | 繁體中文

**Markdown Previewer for Dropbox**
生效日期：2026 年 10 月 19 日

Markdown Previewer for Dropbox（以下簡稱「本擴充功能」）是一個開放原始碼的瀏覽器擴充功能，用來在 Dropbox 網頁版的檔案檢視器中顯示排版後的 Markdown 檔案。本政策說明本擴充功能會存取哪些資料，以及如何處理這些資料。

## 摘要

本擴充功能**不會**收集、儲存、販售或傳送任何個人資料，所有處理都在你的瀏覽器中進行。

## 本擴充功能會存取的資料

當你在 Dropbox 網站以 Markdown 格式檢視 Markdown 檔案時，本擴充功能會：

1. 讀取 Dropbox 頁面上正在顯示的文字，用來確認開啟的是哪個檔案。
2. 從 `previews.dropbox.com` 下載同一個檔案，這也是 Dropbox 自己的檢視器使用的網址。下載時使用你瀏覽器中現有的 Dropbox 登入狀態，因此只能讀取你本來就正在檢視的檔案。
3. 將 Markdown 轉換成排版後的內容，取代 Dropbox 原本的排版顯示在頁面上。

檔案內容只會在 Dropbox 頁面開啟期間暫存在記憶體中，關閉或重新整理頁面後即被捨棄。

## 本擴充功能不會做的事

- 不會將你的檔案、檔名或任何其他資料傳送給開發者或任何第三方。
- 不會在你的電腦上儲存資料，不使用擴充功能儲存空間、Cookie 或 Local Storage。
- 不使用任何分析、追蹤或廣告服務。
- 不會讀取你的 Dropbox 密碼或存取權杖，也不會修改、上傳或刪除任何檔案。
- 不會從網路載入程式碼，所有函式庫都已隨擴充功能一起打包。

## 權限說明

| 權限 | 用途 |
| --- | --- |
| 在 `https://www.dropbox.com/*` 上執行 | 在 Dropbox 檔案檢視器中，以本擴充功能的排版顯示 Markdown 檔案。 |
| 存取 `https://previews.dropbox.com/*` | 下載你正在檢視的 Markdown 原始檔，讓預覽內容完整且正確。 |

## 開放原始碼

完整原始碼公開在 <https://github.com/brianmaxwell515/Markdown-Previewer-for-Dropbox>，你可以自行查核本擴充功能的運作方式。

## 政策變更

本政策如有變更，會在同一網址公布新版本並更新生效日期。

## 聯絡方式

對本政策有任何疑問，請到 <https://github.com/brianmaxwell515/Markdown-Previewer-for-Dropbox/issues> 提出 issue。

---

本擴充功能與 Dropbox, Inc. 無任何關聯，亦未經其認可或贊助。Dropbox 是 Dropbox, Inc. 的商標。
