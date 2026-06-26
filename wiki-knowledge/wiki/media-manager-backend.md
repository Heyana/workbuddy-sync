---
title: media-manager-backend
type: entity
created: 2026-06-26
updated: 2026-06-26
sources: [media_manager_backed_ANALYSIS_REPORT.md]
tags: [Go, GORM, SQLite, Gin, Wails-v3, media-manager, architecture]
---

# Media Manager Backend (Go)

Go + Gin + GORM + SQLite 的媒体资源管理系统后端，是 electron-media-manager 的数据层服务。

## 技术栈

| 维度 | 选型 |
|------|------|
| 语言 | Go 1.25 |
| Web 框架 | Gin v1.10 |
| ORM | GORM v1.30 + glebarez/sqlite（纯 Go 驱动） |
| 桌面壳 | Wails v3 alpha2.104（迁移中） |
| 日志 | Logrus |
| WebSocket | gorilla/websocket |
| API 文档 | swaggo/swag |

## 关键设计

### 双数据库架构
系统库 (`system.db`) + 每个素材库独立的业务库 (`app_go.db`)。系统库存"有哪些素材库"的元信息，业务库存实际数据。每个库独立 SQLite 文件意味着备份/迁移/删除互不影响。

### 无状态 Service + 动态 DB
大多数 service 是空结构体，通过 `getDB()` 运行时获取当前业务数据库连接。素材库切换后下一次 `getDB()` 自动指向新库——无需重建实例。

### AppCore 编排器
将启动流程从入口抽离到独立编排器模块，双入口（dev / Wails）复用相同路径。教科书级的 Facade 模式。

### 问题
- API 响应格式不统一：半 `response.go` 信封、半 `gin.H` 手写
- MediaControlController 业务泄漏（565 行）
- Wails DB Binding 绕过 Service 层
- 批量操作缺少事务保护

## 规模
66 个 Go 源文件，~12,800 行（有效业务 ~10,500 行），17 个 API 控制器，15 个 Service。

## 参见
- [[media-manager-frontend]]
- [[media-manager-fullstack]]
- [[wails-v3-migration]]
- [[dual-database-pattern]]
