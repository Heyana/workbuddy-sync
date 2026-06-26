---
title: platform-abstraction-layer
type: concept
created: 2026-06-26
updated: 2026-06-26
sources: [electron-media-manager_ANALYSIS_REPORT.md]
tags: [pattern, abstraction, Electron, Wails, Vue3]
---

# Platform 抽象层

多壳环境（Electron / Wails / Web）的前端平台适配模式。

## 模式

```
Platform Detection (index.ts)
  ├─ window.wails !== undefined → Wails 模式
  ├─ window.electronAPI !== undefined → Electron 模式
  └─ 其他 → Web 模式

Abstract Interface (base.ts)
  ├─ Platform.db.assets / folders / categories / ...
  ├─ Platform.shell.openExternal / showItemInFolder
  └─ Platform.window.minimize / maximize / close

Concrete Implementations
  ├─ electron.ts — 完整实现
  ├─ wails.ts — 大部分空操作（待实现）
  └─ web.ts — 退化行为
```

## 核心原则

- **接口定义为领域语义**：`platform.file.openDialog()` 而非 `ipcRenderer.invoke('dialog:openFile')`
- **壳专属细节不外泄**：上层代码不 import Electron/Wails 的任何类型
- **退化优雅**：Web 模式提供空操作或默认值，不抛错

## 当前问题

Electron 实现过度耦合了 IPC/BrowserWindow 概念。`base.ts` 接口中存在 `invoke(channel, ...args)` 这样的 Electron API 直译——Wails 和 Web 实现时需要"丢弃"这些方法。正确的做法是接口全部用领域语义（如 `file.selectAndRead()` 而非 `invokeOpenFile()`）。

## 适用场景

- Electron → Wails/Web 迁移
- 桌面应用 + Web 版同步维护
- Electron API 的单元测试（通过 Mock Platform 替代真实的 contextBridge）

## 参见
- [[media-manager-frontend]]
- [[core-singleton-pattern]]
- [[wails-v3-migration]]
