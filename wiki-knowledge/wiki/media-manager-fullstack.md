---
title: media-manager-fullstack
type: synthesis
created: 2026-06-26
updated: 2026-06-26
sources: [media_manager_backed_ANALYSIS_REPORT.md, electron-media-manager_ANALYSIS_REPORT.md]
tags: [media-manager, fullstack, architecture, Wails-v3, migration]
---

# Media Manager 全栈架构综合

前后端联合分析得出的系统性结论。

## 架构全景

```
用户 UI ←→ Vue 3 前端 (Core 单例体系)
              ↕ Platform 抽象
           Preload Bridge (contextBridge)
              ↕ IPC / HTTP
        ┌─ Electron Main ─────────────────┐
        │  Express :23348    Go :23347     │
        │  (API 聚合)       (Gin + GORM)   │
        └──────────────────────────────────┘
                          ↕
                    SQLite 双数据库
              (system.db + 每库 app_go.db)
```

## 跨项目一致性发现

### 1. 多条数据通路问题
两端都存在"并行数据路径"：
- **后端**：HTTP API vs Wails Binding 直连 DB——绕过 Service 层
- **前端**：Preload → Go（直接）vs Preload → Express → Go（聚合）

### 2. 编排器模式复用
- **后端 AppCore**：编排数据库/服务器/配置的初始化顺序
- **前端 ElectronApp**：编排窗口/后端/Express/IPC 的启动顺序

两者的职责完全对应——都是"Facade 模式的启动编排器"。

### 3. 设计哲学一致
- **无状态依赖** → 后端动态 DB 指针 + 前端 Platform 动态检测
- **轻量控制反转** → 后端 AppCore 注入路由 + 前端 Core 调度 Manager
- **外部工具封装** → 后端 utils/ffmpeg_helper.go + 前端 utils/utilsFFmpeg.ts

### 4. 共同的改进方向
- 统一数据通路（HTTP API 和 Binding 走同一 Service 层）
- 废弃代码清理
- 日志系统全覆盖
- 事务/错误处理加强

## Wails v3 迁移影响矩阵

| 组件 | 变化 | 难度 |
|------|------|------|
| Preload Bridge | 消失，被 Wails bindings.js 替代 | 🔴 高 |
| db 适配器 | HTTP → Go 方法直接调用 | 🟡 中 |
| IPC 通道 (37 个) | → Wails 事件系统 | 🟡 中 |
| Express Server | 仅保留扩展网关/静态文件 | 🟢 低 |
| Platform 抽象 | 验证值最大化时机 | 🟢 低 |
| Vue Core | 不变 | 🟢 无 |

## 参见
- [[media-manager-backend]]
- [[media-manager-frontend]]
- [[wails-v3-migration]]
- [[dual-database-pattern]]
- [[core-singleton-pattern]]
