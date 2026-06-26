# 操作日志

> 追加，不覆盖。

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
