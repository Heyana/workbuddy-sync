# 操作日志

> 追加，不覆盖。

## [2026-06-27] ingest | Qt 6 + 跨平台 GUI + ScreenClip 项目知识归档

本日从 Qt 跨平台开发实战中提取知识归档：

**概念 & 环境**：
- [[qt6-windows-dev-setup]] — Qt 6 Windows 完整环境搭建：MSVC toolchain、aqtinstall、CMake、高 DPI 修复、vcpkg 代理踩坑

**对比分析**：
- [[cross-platform-gui-comparison]] — 20+ 跨平台 GUI 框架全景对比：主流（Qt/Flutter/Electron/Tauri）与 小众（Fyne/Gio/egui/Dioxus/Dear ImGui/Nuklear），即时模式 vs 保留模式，按场景选型

**项目**：
- [[screen-clip-tool]] — Qt 6 截图+剪贴板工具，v0.1 基础 + v0.2 标注编辑器（6 种标注工具），架构 / 技术要点 / 规划

覆盖领域：Qt / C++ / 跨平台 / GUI / 桌面开发。

## [2026-06-26] ingest | 工具评估：ego lite + CLI-Anything

评估 2 个工具并记录不采用决策：
- [[ego-lite-browser]] — AI Agent 浏览器，已有 playwright 替代
- [[cli-anything]] — GUI→CLI 自动生成，已有原生 CLI 工具

## [2026-06-26] ingest | Media Manager 全栈架构分析归档

从 repo-analyzer 两轮深度分析（后端 Go 13K 行 + 前端 Electron/Vue 23K 行）中提取知识归档：

**项目页**：
- [[media-manager-backend]] — Go 后端：双数据库、无状态 Service、AppCore 编排器
- [[media-manager-frontend]] — Electron 前端：Core 单例体系、Preload 安全边界、FFmpeg GPU 检测
- [[media-manager-fullstack]] — 前后端联合综合：架构一致性、Wails 迁移影响矩阵

**概念页**（可复用模式）：
- [[dual-database-pattern]] — 系统库 + 业务库分离，SQLite PRAGMA 调优
- [[core-singleton-pattern]] — Vue3 星型调度 + Manager 单例，替代大 Store
- [[wails-v3-migration]] — 渐进迁移策略、Binding 三组分工、关键陷阱
- [[platform-abstraction-layer]] — 多壳适配模式，领域接口设计原则

Source: raw/media_manager_backed_ANALYSIS_REPORT.md, raw/electron-media-manager_ANALYSIS_REPORT.md

## [2026-06-26] lint | impeccable-design-critique 交叉链接补全

补充审计工作流、关联工具表、impeccable skill reference 位置。联通设计审查概念与实际操作工具。
- [[flowtime-stitch]] — 项目概览
- [[capacitor-android-build]] — Android 构建环境和排坑
- [[capacitor-native-bridge]] — 原生桥接模式
- [[impeccable-design-critique]] — 设计审查方法论
- [[minimal-i18n-pattern]] — 零依赖 i18n
- [[react-stale-closure-timer]] — React 闭包 bug 模式

覆盖领域：React / Capacitor / Android / 设计 / i18n / 排坑。

## [2026-06-26] ingest | 开发工具链与知识图谱

提取 2 个模式页面：
- [[code-knowledge-graph-pattern]] — 代码知识图谱替代逐文件探索
- [[skills-orchestration]] — 多 Skill 按开发阶段编排

覆盖领域：AI 编程工具链、代码探索模式、技能组合策略。

## [2026-06-26] ingest | editorV2 深度架构分析

从 `raw/editorV2-architecture-analysis.md` 摄入 183k 行 3D 编辑器项目的深度分析报告。
- 新增 [[editorv2-architecture-analysis]] — 项目摘要 + 重构优先级矩阵
- 新增 [[3d-editor-engine-patterns]] — 提炼 4 个 3D 引擎设计模式
- 新增 [[vendoring-anti-pattern]] — LiteGraph 魔改防止升级的教训
- 更新 index.md — 新增"架构 & 工程实践"分类

覆盖领域：3D引擎 / Vue3 / TypeScript / 重构 / vendoring。

## [2026-06-26] update | Android Foreground Service + Timer bugs

- 新增 [[android-foreground-service]] — 前台服务方案替代 LocalNotifications
- 更新 [[react-stale-closure-timer]] — 补充 setTimeLeft updater 覆盖 bug 和 deferred completion 修复
- 更新 [[capacitor-native-bridge]] — 引用前台服务作为通知优先方案
