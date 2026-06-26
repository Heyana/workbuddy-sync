---
title: media-manager-frontend
type: entity
created: 2026-06-26
updated: 2026-06-26
sources: [electron-media-manager_ANALYSIS_REPORT.md]
tags: [Electron, Vue3, TSX, Preload, Express, ffmpeg, media-manager, architecture]
---

# Media Manager Frontend (Electron/Vue)

Electron + Vue 3 + TSX + Express 的三层桌面前端，全栈媒体资源管理系统的用户界面。

## 技术栈

| 维度 | 选型 |
|------|------|
| 桌面框架 | Electron 38 + electron-vite 3 |
| 前端 | Vue 3.3 + Composition API + TSX(80%)/SFC(20%) + Pinia |
| 服务层 | Express :23348（聚合）+ Go 后端 :23347（内嵌） |
| 样式 | Tailwind CSS + Less + Element Plus |
| 通信 | IPC + contextBridge + HTTP + WebSocket |

## 关键设计

### Core 单例体系
前端核心模式：12 个业务 Manager 类（Asset/Folder/Tags/Preview/RightMenu/Drag/Event/Multi/Config + 3 个 Media），各司其职、互不依赖，通过 Core.ts 星型调度。比传统 Vuex/Pinia 大 Store 更内聚。

### Preload 安全边界
`contextIsolation: true` + `contextBridge.exposeInMainWorld` 白名单模式。5 个全局命名空间（electronAPI/ipc/task/callback/file），37 个 IPC 通道。所有 EventBus 方法必须用箭头函数（实例属性），因为 contextBridge 不序列化原型方法。

### FFmpeg GPU 自动检测
启动时通过 nvidia-smi/system_profiler/lspci 检测 GPU，自动选最优编码器（nvenc/videotoolbox/amf/libx264）。统一进度解析层屏蔽不同编码器的输出差异。

### Platform 抽象层
Electron > Wails > Web 三壳降级策略。当前过度耦合 Electron 概念。

### 问题
- Go 后端无崩溃恢复
- 三套回调系统并存（BindEvent/EventBus/LegacyBus）
- Logger 迁移率仅 5%
- 废弃代码未清理（downloadTaskManagement.ts）
- `as any` 类型断言泛滥

## 规模
128 个源文件，~23,000 行有效代码，12 个 Core Manager，39 个 Utils 文件。

## 参见
- [[media-manager-backend]]
- [[media-manager-fullstack]]
- [[wails-v3-migration]]
- [[core-singleton-pattern]]
- [[platform-abstraction-layer]]
