---
title: 3D 编辑器引擎设计模式
type: concept
created: 2026-06-26
updated: 2026-06-26
sources: [editorV2-architecture-analysis.md]
tags: [3D引擎, 编辑器, 设计模式, Facade, 回调系统]
---

# 3D 编辑器引擎设计模式

从 editorV2（run-scene-v2 + 3d-editor-2.0）的实践中提炼的 3D 编辑器架构模式。

## 1. 门面模式（Facade）作为引擎入口

**场景**：3D 引擎有 30+ 子系统（场景/模型/材质/纹理/相机/光照/后处理/动画/脚本...），需要一个统一的入口。

**editorV2 做法**：RunScene 中央门面，构造函数中 new 所有子系统，每个子系统持有 `this.rs` 全引用。

**优点**：
- 新增子系统只需一行 `new Foo(this)` + 在 `initLibs()` 中 `this.foo.init()`
- 调用路径简洁：`rs.modelEx.add(...)` 而非通过多层依赖注入
- 初始化顺序由门面保证，避免循环依赖陷阱

**代价**：
- 无显式依赖声明——不可静态分析"MaterialEx 依赖 TextureEx"
- 不可单独单元测试——必须构造完整 RunScene
- 边界模糊——子系统可以随意访问任何其他子系统

**适用场景**：小团队维护的中型引擎，子系统数量 <50，生命周期集中在门面控制。

## 2. 命名空间回调总线

**场景**：编辑器 UI 事件需要触发引擎层操作，引擎层状态变更需要通知 UI 刷新。

**editorV2 做法**：`CallBack` 系统——每个业务域独立命名空间（`cb.load`、`cb.renderEx`、`cb.modelEx`），通过字符串 name 注册/移除回调。`custom` Proxy 按需创建事件。

**vs 通用事件总线**：
- 通用总线（EventEmitter）：灵活但丢失类型安全
- 命名空间回调：类型安全但命名空间膨胀

**编辑器的桥梁**：`UpdateManager`——在 Core.tsx 中向 RunScene.cb 各命名空间注册监听器，将引擎事件转为 Vue 响应式更新。

## 3. 双模式引擎

**场景**：同一套引擎代码既要支持编辑器（带编辑工具），又要支持纯预览。

**editorV2 做法**：`mode: "editor" | "run"` 标志，通过 `globalConfig.setRenderMode()` 控制：
- editor：启用 TransformControls、SelectionBox、GRepeat
- run：纯渲染，无编辑交互

**问题**：mode 判断散落在多处（RenderEx、ControlsEx...），缺少统一的策略模式。

## 4. 快照系统（Snapshot）

**场景**：编辑器的 undo/redo 和场景持久化需要序列化所有子系统状态。

**editorV2 做法**：Snapshot 基类采用极致的开闭原则——各子系统通过回调向 Snapshot 注册自己的序列化逻辑。Snapshot 本身完全不知道业务数据类型。

**差异快照**（MaterialEx）：只存与默认值的差异，压缩体积。
**全量快照**（ModelEx）：属性值少且多变，全量更简单。

## 参见

- [[editorv2-architecture-analysis]] — 完整的 editorV2 分析报告
- [[vendoring-anti-pattern]] — LiteGraph 魔改的教训
