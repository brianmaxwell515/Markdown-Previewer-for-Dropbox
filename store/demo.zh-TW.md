---
title: 專案啟動會議紀錄
author: 示範團隊
---

<!-- 這段註解在預覽畫面中不會顯示。 -->

# 專案啟動會議紀錄

> **目標**：在 **3 月 31 日**前推出 *Orbit Planner* 第一個正式版本。

## 里程碑

| 階段 | 負責人 | 期限 | 狀態 |
| --- | --- | --- | :---: |
| 設計審查 | 小安 | 1/15 | ✅ |
| 測試版 | 阿傑 | 2/20 | 🚧 |
| 正式發布 | 小晴 | 3/31 | ⏳ |

## 本週待辦

- [x] 完成新手導覽流程
- [x] 撰寫 API 文件
- [ ] 準備發布檢查清單
- [ ] 預約發表會直播

## 快速開始

```bash
npm install orbit-planner
orbit init my-project
```

```js
import { Planner } from 'orbit-planner';

const planner = new Planner({ timezone: 'Asia/Taipei' });
planner.addTask('撰寫版本說明', { due: '2026-03-28' });
console.log(planner.summary());
```

## 注意事項

1. Pull request 盡量**小而聚焦**。
2. 每次 commit 前先執行 `orbit lint`。
3. 有問題請參考 [Markdown 指南](https://www.markdownguide.org/)。

---

*最後更新：示範團隊*
