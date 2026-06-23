---
title: WIKI-SCHEMA
type: schema
created: 2026-06-24
updated: 2026-06-24
---

# WIKI-SCHEMA — 知识库结构约定

> 本文档与 LLM 共同演化。修改前先和 LLM 讨论。

## 目录结构

```
wiki-knowledge/
├── raw/                  ← 原始资料（只读，不可变）
│   └── assets/           ← 下载的图片等附件
├── wiki/                 ← LLM 维护的 markdown 页面
│   ├── index.md          ← 内容目录
│   └── log.md            ← 操作日志
└── WIKI-SCHEMA.md        ← 本文档
```

## 页面类型

| 类型 | 说明 |
|------|------|
| entity | 实体（人、公司、项目、工具） |
| concept | 概念/技术 |
| source-summary | 来源摘要 |
| comparison | 对比分析 |
| synthesis | 综合总结 |

## 页面模板

```markdown
---
title: 页面标题
type: entity | concept | source-summary | comparison | synthesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [来源文件名列表]
tags: [标签]
---

# 页面标题

内容。使用 [[wiki-links]] 做交叉引用。

## 参见
- [[相关页面1]]
- [[相关页面2]]
```

## 交叉引用

- 用 `[[页面名]]` 链接 wiki 内其他页面
- 引用 raw 来源：`[文件名](../raw/文件名)`
- 外部链接：标准 Markdown `[文字](URL)`

## 和 WorkBuddy 记忆体系的关系

| WorkBuddy 记忆 | llm-wiki | 用途 |
|---------------|----------|------|
| `topics/` | 不重叠 | 编码规则、项目约定（随身必读） |
| `knowledge/` | wiki/ | 技术深层知识、排坑记录 |
| 每日日志 | log.md | 操作记录 |
| — | raw/ | 原始资料归集（新能力） |

- wiki 是 knowledge/ 的**扩展和补充**，不做重复录入
- 新学到的技术知识优先放 wiki，编码排坑优先放 knowledge/
- 两者通过 `[[wiki-links]]` 或明确引用互连

## 领域分类

当前关注领域：
- **编程**：Go、Vue 3/TSX、Flutter、TypeScript
- **工具**：ffmpeg GPU 编码、WebDAV 同步、SQLite
- **设计**：UI/UX 组件设计、shadcn 生态
- **架构**：代码审查、模块深度、接口设计

## 工作流

1. **Ingest**：一次一个来源，LLM 读完 → 写摘要 → 更新索引 → 更新相关页面
2. **Query**：问 → LLM 读索引定位 → 合成答案 → 好答案归档回 wiki
3. **Lint**：定期查矛盾、过期、孤页、缺交叉引用
