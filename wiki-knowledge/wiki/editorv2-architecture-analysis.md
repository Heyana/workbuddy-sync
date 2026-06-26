---
title: editorV2 架构深度分析
type: source-summary
created: 2026-06-26
updated: 2026-06-26
sources: [editorV2-architecture-analysis.md]
tags: [3D引擎, 编辑器, 架构分析, 重构, Three.js, Vue3]
---

# editorV2 架构深度分析

> 原始报告：`raw/editorV2-architecture-analysis.md`

## 项目定位

Web 3D 场景编辑器。双层架构：run-scene-v2（Three.js 封装引擎，~126k 行）+ 3d-editor-2.0（Vue 3 编辑器 UI，~57k 行）。

## 核心架构模式

**RunScene 门面（Facade）**：中央调度器组合 30+ 子系统，每个子系统通过 `this.rs` 互相访问。不是要拆的 God Object——是故意设计。优点：新增子系统极易（new + init + 注册回调）；代价：无显式依赖声明、不可单独测试。

**回调驱动通信**：`CallBack` 命名空间化 Observer 模式，编辑器 ↔ 引擎双向通信通过 `UpdateManager → RunScene.cb`。

**双模式**：`editor`（带 TransformControls/选择框）/ `run`（纯预览）。

## 六大调用热点

| 热点 | 入度 | 问题 |
|------|------|------|
| `MapEx.map` | 501 | 上帝工具函数 |
| `callback.cb` | 227 | 事件总线枢纽（合理） |
| `addOutput/addInput/addWidget` | 167/143/140 | 图节点引擎高内聚 |
| `getUniqueId` | 159 | ID 生成器（合理） |

## 关键发现（P0）

1. **LiteGraph 22 处魔改阻止升级**：3 处核心逻辑完全重写（configure/drawNode/drawNodeWidgets），编辑器侧还有另一份干净版本——双版本不一致
2. **rightMenu.tsx ~71k 行**：函数定义与菜单数据混在一起
3. **Outline/Outline1 95% 重复**：后处理双体系中各有一套

## 重构优先级矩阵

| 优先级 | 任务 | 风险 |
|--------|------|------|
| P0 | LiteGraph 魔改剥离为扩展点 | 中 |
| P0 | rightMenu.tsx 按对象类型拆分 | 低 |
| P0 | Outline/Outline1 合并 | 低 |
| P1 | 后处理双体系 → LtPP 统一 | 中 |
| P1 | 多选系统三合一 | 中 |
| P2 | 模块间引入领域接口替代 this.rs | 高 |

## 执行顺序

```
第1轮 (安全) → rightMenu拆分 / Outline合并 / defMaterial清理 / 删僵尸代码
第2轮 (中等) → 多选统一 / 后处理统一
第3轮 (高风险) → LiteGraph剥离 / 双版本合并
第4轮 (长期) → 领域接口替代this.rs / 场景变更通知层
```

## 限界上下文

5 个域：渲染域（RenderEx + 后处理）/ 场景域（SceneEx/ModelEx/LightEx/TextureEx/MaterialEx）/ 编排域（TimeLine/GraphManager/Script）/ 编辑器域（Core/UpdateManager/Views）/ 基础设施域（CallBack/Undo/Snapshot/Events/Unique）

## 参见

- [[3d-editor-engine-patterns]] — 3D 编辑器引擎的设计模式
- [[vendoring-anti-pattern]] — LiteGraph 魔改的教训
- [[flowtime-stitch]] — 另一个 Web 应用架构案例
