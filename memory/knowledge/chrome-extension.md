# Chrome Extension MV3 排坑

> offscreen document & Service Worker API 限制，实际验证结论。

## Offscreen Document API 可用性

| API | 可用 | 替代方案 |
|-----|------|---------|
| `chrome.runtime.sendMessage` | ✅ | — |
| `chrome.runtime.onMessage` | ✅ | — |
| `chrome.storage` | ✅ | — |
| DOM (document/window/Blob/URL.createObjectURL) | ✅ | — |
| `fetch` | ⚠️ 有 CORS 限制 | 改在 background SW 中 fetch |
| `chrome.downloads` | ❌ | 发消息让 background 下载 |
| `chrome.offscreen.*` | ❌ | 发消息让 background 关闭 |
| `chrome.tabs` | ❌ | 发消息让 background 操作 |
| `HLS.js` / `mux.js` | ✅ | 可正常加载运行 |

## Service Worker API 可用性

| API | 可用 | 替代方案 |
|-----|------|---------|
| `fetch` | ✅ 全跨域权限 | — |
| `chrome.downloads.download()` | ✅ | — |
| `chrome.offscreen.createDocument()` | ✅ | — |
| `URL.createObjectURL()` | ❌ | 用原始 URL 调 chrome.downloads.download |
| `Blob` | ✅ | — |
| DOM | ❌ 无 DOM | 需要 DOM 的操作放 offscreen |

## 跨上下文下载模式

```
直接下载（图片/视频）:
  popup → background SW → chrome.downloads.download(原始URL) ✅

M3U8 流下载:
  popup → background → offscreen(HLS.js解析+下载TS) → 合并Blob
       → createObjectURL → background → chrome.downloads(blobUrl) ✅

FFmpeg 合并下载:
  popup → downloader.html（需 DOM + iframe + postMessage）→ 手动关闭
```

## 经验教训

1. **Offscreen 不等于完整浏览器 tab** —— 只有 runtime/storage/DOM 三件套
2. **SW 里的 fetch 是跨域利器** —— host_permissions 全开，无 CORS
3. **SW 不能 createObjectURL** —— 裸用原始 URL 调 downloads.download 即可
4. **不要强行在 offscreen 做一切** —— 简单下载直接在 SW 里完成
5. **M3U8 才需要 offscreen** —— HLS.js 依赖 DOM（video 元素）
