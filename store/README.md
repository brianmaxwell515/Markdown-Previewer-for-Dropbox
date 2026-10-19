# 商店素材

這個資料夾放上架 Chrome 線上應用程式商店時要另外上傳的圖片。這些圖片**不會**打包進擴充功能的 zip。

```
store/
├── listing.md     上架時要填寫的文字（說明、權限理由、隱私權欄位）
├── screenshots/   商店截圖
└── promo/         宣傳圖塊
```

## screenshots/

| 項目 | 規格 |
| --- | --- |
| 尺寸 | 1280×800 或 640×400，所有截圖用同一種尺寸 |
| 格式 | PNG 或 JPEG |
| 數量 | 至少 1 張，最多 5 張 |

檔名開頭的數字代表在商店顯示的順序。

| 檔案 | 標題 |
| --- | --- |
| `01-before-after.png` | Dropbox's Markdown view, upgraded |
| `02-nothing-to-click.png` | Nothing extra to click |
| `03-quick-view-and-full-page.png` | Works in quick view and full-page preview |
| `04-formatting-dark-mode.png` | Tables, task lists and highlighted code |

這四張由 `make_screenshots.py` 產生，在 repo 根目錄執行 `python store/screenshots/make_screenshots.py` 即可重新產生。素材放在 `raw/`：

- `quickview-*.png`、`full-page-*.png`：以 1440×900、2 倍解析度在 Dropbox 截的快速預覽與完整預覽畫面。`-dropbox` 是 Dropbox 原本的 Markdown 檢視，`-extension` 是裝了擴充功能後的畫面。
- `render-light.png`、`render-dark.png`：用擴充功能的渲染器把 `demo.md` 以 2 倍解析度渲染出的淺色／深色畫面。

截圖請使用示範用的 Markdown 檔，不要露出真實資料、帳號名稱或共享成員的名字。

## promo/

| 檔名 | 尺寸 | 是否必要 |
| --- | --- | --- |
| `small-tile.png` | 440×280 | **必要**，商店首頁、類別頁與搜尋結果會用到 |
| `marquee.png` | 1400×560 | 選用，只有被商店精選時才會用到 |

兩張圖都由腳本產生，在 repo 根目錄執行即可重新產生：

- `python store/promo/make_small_tile.py`：用 `icons/icon.png` 產生 `small-tile.png`
- `python store/promo/make_marquee.py`：用 `icons/icon.png` 和 `screenshots/raw/full-page-*.png` 產生 `marquee.png`（24 位元 PNG，無透明層）

商店圖示（128×128）直接使用 `icons/icon128.png`，不需另外準備。
