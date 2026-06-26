---
title: dual-database-pattern
type: concept
created: 2026-06-26
updated: 2026-06-26
sources: [media_manager_backed_ANALYSIS_REPORT.md]
tags: [Go, SQLite, database, pattern]
---

# 双数据库模式 (Dual Database Pattern)

项目采用的"系统库 + 业务库"分离方案，用于支持多租户/多工作空间场景。

## 适用场景

需要管理多个独立数据空间，且需要一个"元数据库"记录有哪些空间。

## 实现方式

```
~/Documents/MediaManager/
├── static/system/system.db     ← 系统库（固定路径）
│   ├── library        — 素材库列表（name, path, createdAt）
│   ├── library_history — 操作审计
│   └── system_config  — KV 配置
│
└── {素材库路径}/app_go.db       ← 业务库（每个素材库独立）
    ├── assets / folders / categories
    ├── tasks / download_tasks
    ├── asset_folders / asset_categories
    └── media_playback_*
```

## 对比方案

| 方案 | 优点 | 缺点 |
|------|------|------|
| 单库 + library_id | 简单 | 单库膨胀、一损俱损 |
| 每库独立 SQLite | 隔离好 | 无处存"有哪些库"的元信息 |
| **系统库 + 业务库** | 兼具隔离性和元数据 | 需管理两个连接 |

## 关键实现细节

- 系统库路径固定（用户目录下），启动时先打开
- 业务库路径存于系统库的 `libraries` 表
- 切换素材库 = 关闭旧业务库 → 打开新业务库 → 更新全局 `businessDB` 指针
- Service 层通过 `getDB()` 运行时获取连接，对切换透明

## SQLite PRAGMA 调优

每次打开数据库时执行：WAL 模式、NORMAL 同步、64MB 缓存、10s busy_timeout、4 连接池。WAL 模式只需设置一次（持久化到文件），其他 PRAGMA 每次连接都要设置。

## 参见
- [[media-manager-backend]]
- [[wails-v3-migration]]
