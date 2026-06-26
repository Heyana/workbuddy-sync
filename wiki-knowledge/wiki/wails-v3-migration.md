---
title: wails-v3-migration
type: concept
created: 2026-06-26
updated: 2026-06-26
sources: [media_manager_backed_ANALYSIS_REPORT.md, electron-media-manager_ANALYSIS_REPORT.md]
tags: [Wails-v3, migration, Electron, Go]
---

# Wails v3 迁移

从 Electron + Express + Go 三层架构合并为 Wails v3 + Go 一体化桌面架构。

## 当前状态（2026-06）

后端已完成主体框架：入口（main_wails.go）、12 个 Binding Service（db/services/system 三组）、窗口管理和事件系统。Gin HTTP API 保留给浏览器扩展通信。

前端尚未开始迁移。当前 Electron 架构完整运行。

## 迁移策略

与用户确认的渐进策略：逐步以 Wails 为主，独立 HTTP 模式临时保留。不是一次性切换。

## 三组 Binding 分工

| 绑定文件 | 职责 | 数据通路 |
|---------|------|---------|
| `wails/bindings/db.go` | Asset/Folder/Category/Task CRUD | **直连 GORM**（问题：绕过 Service） |
| `wails/bindings/services.go` | Download/Library/Media/Highlight | 调用 Service 层 |
| `wails/bindings/system.go` | File/Config/Window/FFmpeg | 系统工具 |

## 迁移影响矩阵

| 组件 | 变化 | 难度 |
|------|------|------|
| Preload Bridge | 消失 | 🔴 高（28 文件，20+ 管线） |
| db 适配器 | HTTP → Go 方法直接调用 | 🟡 中（性能提升，无网络开销） |
| IPC 通道 (37 个) | → Wails 事件系统 (5 个自定义事件) | 🟡 中（逐个映射） |
| Express Server | 仅保留浏览器扩展网关 | 🟢 低 |
| Platform 抽象 | 验证其设计正确性 | 🟢 低 |
| Vue Core | 完全不需改动 | 🟢 无 |

## 关键陷阱

1. **DB Binding 绕过 Service**：Wails 前端通过 binding 直连 GORM，可能跳过 AssetService 的业务逻辑（如自动创建 AssetHistory）
2. **事件系统映射**：Electron 的 37 个 IPC 通道映射到 Wails 5 个自定义事件，粒度差距大
3. **contextBridge 依赖**：前端大量模块通过 `window.db.xxx()` 调用，迁移时需要全局替换

## 参见
- [[media-manager-backend]]
- [[media-manager-frontend]]
- [[media-manager-fullstack]]
- [[platform-abstraction-layer]]
