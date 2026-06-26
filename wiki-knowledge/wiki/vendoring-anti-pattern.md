---
title: Vendoring 防升级反模式
type: concept
created: 2026-06-26
updated: 2026-06-26
sources: [editorV2-architecture-analysis.md]
tags: [vendoring, 技术债, LiteGraph, 三方库管理]
---

# Vendoring 防升级反模式

从 editorV2 的 LiteGraph 魔改中学到的教训。

## 问题

editorV2 把 LiteGraph（可视化图编辑器）的源码直接拷进项目（`libs/Graph/Graph.core.js`），然后做了 22 处修改——其中 3 处是核心逻辑完全重写。

结果是：**永远无法升级 LiteGraph**。每次上游发新版本，必须手工合并这 22 处修改。更要命的是编辑器侧还有另一份干净的 Graph.js——两套不一致。

## 为什么走到这一步

1. **初期快速迭代**：直接改源码比找扩展点快
2. **缺少扩展点意识**：没有先查 LiteGraph 的 `registerNodeType`/hook 机制
3. **无文档记录**：22 处修改靠 `//hxy` 注释标记，没有独立的 patch 文件
4. **双版本分裂**：编辑器侧和引擎侧各搞各的，没人统一

## 正确的做法

### 短期（已有项目）
1. 用 `diff` 生成所有修改的 patch 文件 → 可追溯
2. 评估每处修改是否可以通过上游的扩展机制替代
3. 能剥离的优先剥离为扩展点

### 长期（新项目引入三方库）
1. **先查扩展机制**：是否有 hook/plugin/register 机制
2. **扩展优先于修改**：能在外部扩展就不动源码
3. **实在要改**：fork + patch 文件 + 定期 rebase
4. **单点管理**：一个三方库只在一处维护，不允许多版本并存

## Vendoring 评估框架

| 维度 | 可接受 | 危险 |
|------|--------|------|
| 修改数量 | <10 处 | >20 处 |
| 修改深度 | API 层面（新增参数/方法） | 核心逻辑重写 |
| 文档 | 独立 patch 文件 + 原因说明 | `//hxy` 注释 |
| 版本 | 单一来源 | 多套不一致的副本 |
| 升级 | 定期 rebase | 从不 rebase |

editorV2 的 LiteGraph 在所有维度上都处于"危险"区。

## 参见

- [[editorv2-architecture-analysis]] — 完整的分析报告
- [[3d-editor-engine-patterns]] — 相关的架构模式
