# 擴充功能圖示

| 檔案 | 說明 |
| --- | --- |
| `icon.af` | Affinity Designer 原始設計檔 |
| `icon.png` | 從設計檔匯出的原圖（1024×1024），用來產生下面三個尺寸 |
| `icon16.png` | 16×16，瀏覽器工具列、分頁 |
| `icon48.png` | 48×48，`chrome://extensions` 管理頁 |
| `icon128.png` | 128×128，安裝對話框、Chrome 線上應用程式商店 |

只有 `icon16.png`、`icon48.png`、`icon128.png` 會打包進擴充功能，並寫在 `manifest.json` 的 `icons` 裡。

修改圖示時：

1. 在 Affinity Designer 編輯 `icon.af`，匯出覆蓋 `icon.png`。
2. 重新產生三個尺寸，檔名保持不變：
   - 16 和 48：圖案置中後直接縮放，填滿整個圖示。
   - 128：圖案縮到中央 96×96，四周各留 16px 透明邊。
3. 背景保持透明，不可使用 Dropbox 的 logo。
