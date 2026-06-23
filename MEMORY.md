# 用户级偏好记忆（索引）

> 详细内容按领域拆分到 `memory/topics/` 子目录，按主题独立文件。
>
> **维护原则**：个人开发习惯与排坑知识库。每次踩坑、学到新规则、项目有新约定，立刻更新对应 topic。保持精炼——只记结论和关键约束，不记推导过程。
>
> **记忆管理**：无论用户级还是工作区级记忆，过大时拆分为独立小文件，不删除。

> ⚠️ **同步规则**：修改 `~/.workbuddy/` 下文件后 commit + push。本地备份克隆路径见 `project-map.md` → `workbuddy-sync`。各机器项目路径见各自的 `project-map.md`。

## 目录结构

```
topics/
├── core/              🔴 通用，每次必读
├── frontend/          前端通用规则
├── vue/               Vue + shadcn-vue 生态
├── flutter/           Flutter 项目
├── mcp/               MCP 工具配置
├── projects/          当前项目列表
└── meta/              记忆系统自身
```

## 🔴 通用（每次必读）

| 主题 | 文件 |
|------|------|
| 编码风格 | `topics/core/coding-style.md` |
| 工作习惯 | `topics/core/work-habits.md` |
| 项目结构规范 | `topics/core/project-structure.md` |
| 个人背景 | `topics/core/personal-context.md` |

## 🟢 按领域按需

### 前端通用
| 主题 | 文件 |
|------|------|
| 前端通用规则 | `topics/frontend/rules.md` |
| Impeccable 设计工具集 | `topics/frontend/impeccable.md` |
| Skills 清单 | `topics/frontend/skills.md` |

### Vue 生态
| 主题 | 文件 |
|------|------|
| shadcn-vue 使用规范 | `topics/vue/shadcn-vue.md` |
| shadcn-vue MCP Server | `topics/vue/shadcn-vue-mcp.md` |
| shadcn-vue 组件层分析 | `topics/vue/shadcn-vue-components.md` |
| shadcn-vue CLI 内部机制 | `topics/vue/shadcn-vue-cli-internals.md` |
| reka-ui 核心机制 | `topics/vue/reka-ui.md` |

### Flutter
| 主题 | 文件 |
|------|------|
| Flutter 通用规则 | `topics/flutter/flutter.md` |
| Wind 配置规范 | `topics/flutter/wind-config.md` |
| Flutter 桌面截图 | `topics/flutter/screenshot.md` |

### MCP
| 主题 | 文件 |
|------|------|
| MCP 配置规则 | `topics/mcp/rules.md` |

### 项目
| 主题 | 文件 |
|------|------|
| 当前项目列表 | `topics/projects/current.md` |

### 记忆系统
| 主题 | 文件 |
|------|------|
| 同步规则 | `topics/meta/sync.md` |

## 🔧 工具/技术笔记

### 知识库 & 检索

| 工具 | 说明 |
|------|------|
| PixelRAG | Berkeley 开源，用页面截图替代 HTML 解析做视觉 RAG。文档→截图→Qwen3-VL-Embedding→FAISS 检索。预构建 828 万 Wikipedia 索引。不适合调试/开发工具场景。 |

## 📍 项目备份位置

| 项目 | 路径 | 说明 |
|------|------|------|
| vue3_zui (v2 当前) | 见 project-map.md → `vue3_zui` | 干净重建的 ZUI v2，无 v1 legacy |
| vue3_zui_backup | 见 project-map.md → `vue3_zui_backup` | 2026-06-21 覆写为 commit 9da1d6a (来自 vue3_zui repo)，保留 project-map.md 和 .workbuddy 记忆 |
