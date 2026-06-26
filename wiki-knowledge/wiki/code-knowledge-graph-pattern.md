---
title: Code Knowledge Graph Pattern
type: concept
created: 2026-06-26
updated: 2026-06-26
tags: [codebase-memory-mcp, knowledge-graph, ai-coding, token-optimization, architecture]
---

# Code Knowledge Graph Pattern

将代码库预先索引为知识图谱，替代逐文件 grep/read 的 AI 代码探索模式。

## 核心对比

| 维度 | 传统逐文件 | 知识图谱 |
|------|-----------|---------|
| 风格 | grep → read → grep → read 级联 | 一次索引，毫秒查询 |
| Token 消耗 | ~412k（5 次结构查询） | ~3.4k（同样 5 次） |
| 调用链 | 手动读多个文件拼凑 | `trace_path` 单次 BFS |
| 架构理解 | 靠 LLM 从文件内容推断 | `get_architecture` 直接输出 |
| 变更影响 | 肉眼判断 | `detect_changes` 自动计算波及范围 |

## 工具选择

| 任务 | 用 |
|------|-----|
| 查函数定义 | `search_graph` |
| 追踪调用链 | `trace_path` |
| 理解项目结构 | `get_architecture` |
| 代码搜索 | `search_code`（图增强） |
| 语义搜索 | `search_graph(semantic_query=...)` |
| 性能热点 | `query_graph` (Cypher) |
| 回退条件 | MCP 无结果 或 需要完整源码上下文 |

## 索引约定

- 项目首次加载时自动问"要索引吗"
- 索引产物放 `docs/codebase/graph.db.zst`，git add 进仓库
- 每个会话优先走知识图谱，不索引的项目不回退到 Grep/Glob

## 工具链

- [codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp)：纯 C 二进制，158 语言，14 MCP 工具
- UI 可视化：安装时加 `--ui` 参数，访问 `http://localhost:9749`
- 论文：[arXiv:2603.27277](https://arxiv.org/abs/2603.27277)

## See Also

- [[skills-orchestration]]
