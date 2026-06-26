# Skills 生态 & 市场

> 2026-06-24 调研 [skillstore.io](https://skillstore.io/zh-hans)、[skills.sh](https://www.skills.sh/)、[skillsmp.com](https://skillsmp.com/)

## 当前已安装 Skills

| Skill | 来源 | 目录 | 用途 |
|-------|------|------|------|
| impeccable | 内置市场 | skill_2053082862415904768 | 前端 UI 生成（偏"生成好看界面"） |
| nano-banana-pro | 内置市场 | skill_2053082421296758784 | AI 图片生成/编辑 |
| grill-me | 内置市场 | skill_2057443369928683520 | 方案压力测试/追问 |
| frontend-design | 手动安装 | frontend-design/ | 前端设计系统与规范（Anthropic 官方） |
| improve-codebase-architecture | 手动安装 | improve-codebase-architecture/ | 代码架构评估与重构建议（Matt Pocock） |
| llm-wiki | 内置市场 | skill_2053082332061896704 | 个人知识库构建（Karpathy Wiki 模式：ingest/query/lint） |
| archive | 手动安装 | archive/ | 持久化记忆+偏好+项目上下文（CONSULT/SAVE/INGEST/QUERY/LINT） |
| github | connector | connector-github | GitHub API 操作 |
| prd-development | skills.sh | .agents/skills/prd-development/ | 结构化 PRD 生成：问题→用户→方案→成功指标（Dean Peters） |
| prd-test-writer | skills.sh | .agents/skills/prd-test-writer/ | PRD + 测试用例双文档，先读代码再写（yunshu0909） |
| refactoring-guide | skillsmp.com (GitHub) | refactoring-guide/ | 20+ 检测信号 + 5 类原则文档（结构耦合/类型设计/架构/模块边界/战术动作），9 级连接散度，LLM 盲区修正（terrylica） |
| ui-ux-pro-max | uipro-cli | ui-ux-pro-max/ | 67 风格/161 配色/57 字体，设计素材生成，MIT 免费。配合 impeccable 使用（Pro Max 生成方案，impeccable 审查） |
| repo-analyzer | skills.sh (GitHub) | repo-analyzer/ | 8 阶段流水线深度架构分析（30%/60%/90% 三档），并行子代理 + Mermaid 架构图 + 竞品对比（yzddmr6） |

## 当前已安装 Plugins

> 插件 ≠ Skill。插件位于 `~/.workbuddy/plugins/marketplaces/`，提供 `/plugin:command` 形式的斜杠命令。

| Plugin | 版本 | 来源 | 位置 | 用途 |
|--------|------|------|------|------|
| superpowers | 4.0.3 | 官方插件市场 (Jesse Vincent) | `plugins/marketplaces/codebuddy-plugins-official/external_plugins/superpowers/` | AI 协作开发工作流：brainstorm → plan → TDD → subagent 执行 → code review → 收尾 |

### superpowers 提供的命令

```
/superpowers:brainstorm    — 苏格拉底式提问，把模糊想法变设计文档
/superpowers:write-plan    — 拆成 2-5 分钟小任务，精确到文件路径+代码+验证
/superpowers:execute-plan  — 子代理批量执行，每批后人工检查点
```

### superpowers 包含的 14 个 skill

| Skill | 阶段 |
|-------|------|
| brainstorming | 设计 |
| using-git-worktrees | 隔离 |
| writing-plans | 计划 |
| subagent-driven-development | 执行（子代理） |
| executing-plans | 执行（批量） |
| test-driven-development | 测试 |
| requesting-code-review | 审查 |
| receiving-code-review | 审查响应 |
| finishing-a-development-branch | 收尾 |
| systematic-debugging | 调试 |
| verification-before-completion | 验证 |
| writing-skills | 元：编写 skill |
| dispatching-parallel-agents | 元：并行代理 |
| using-superpowers | 元：使用说明 |

## 安装渠道

### WorkBuddy 内置市场（BuiltinMarket）
- 工具：`workbuddy_marketplace_skill`（deferred tool）
- 流程：search → install
- 仅限已在市场上架的 skill

### skills.sh 生态
- 命令：`npx skills add <repo_url> --skill <name>`
- 源：GitHub 仓库（anthropics/skills、mattpocock/skills、vercel-labs/skills 等）
- ⚠️ **注意**：`npx skills add` 安装到 `.agents/skills/`（skills.sh 生态位置），WorkBuddy **不读这个目录**。必须手动复制到 `~/.workbuddy/skills/<name>/` 才能生效
- `npx skills add` 会弹出交互式 agent 选择器，用 `-y` 跳过
- 如果交互式安装卡住：直接从 GitHub raw 拉 SKILL.md → 手动写入 `~/.workbuddy/skills/<name>/SKILL.md`

### skillstore.io
- 偏 AI 内容生成（slides、banner、图标等）
- 有一个 `domain-modeling` 概念不错但太重
- 整体与我们的开发场景匹配度低

### skillsmp.com
- 最大 Skills 搜索引擎，收录 180 万+ SKILL.md 文件
- 按职业分类（23 大类 867 个 SOC 岗位）、按创建者、按类别过滤
- 适合按领域搜索：knowledge/wiki/memory 等垂直方向
- 支持 API 接入，GitHub 源可追溯
- 发现 archive 等小众 skill 的主要渠道

## 手动安装 Skill 模板

```bash
mkdir -p ~/.workbuddy/skills/<skill-name>/
# 写入 SKILL.md（必须有 frontmatter: name, description）
# 可选：scripts/ 子目录放辅助脚本
```

## Matt Pocock Skills 生态依赖关系

```
setup-matt-pocock-skills (配置脚手架)
├── 生成 CONTEXT.md（领域术语表）
├── 生成 docs/adr/（架构决策记录）
└── 被以下 skills 读取：
    ├── improve-codebase-architecture（直接依赖）
    ├── to-issues
    ├── to-prd
    ├── tdd
    ├── diagnose
    └── triage

grill-me（独立，不依赖 setup）
```

## 按场景触发建议

| 场景 | 可触发 Skill |
|------|-------------|
| 做架构决策前 | grill-me |
| 审查代码架构 | improve-codebase-architecture |
| 激进重构/深度耦合分析/模块拆分 | refactoring-guide |
| 深度理解项目架构/生成架构报告 | repo-analyzer |
| 新建/重设计 UI 页面 | frontend-design |
| 生成好看的 UI 组件 | impeccable |
| AI 图片生成 | nano-banana-pro |
| 整理/构建个人知识库 | llm-wiki |
| 摄入新资料到知识库 | llm-wiki |
| 查询/检索已积累知识 | llm-wiki |
| 记录偏好/项目上下文 | archive |
| 任务开始时查记忆 | archive |
| 任务结束时存新知 | archive |

## llm-wiki 知识库

- 位置：`~/.workbuddy/wiki-knowledge/`
- 三层：raw（原始资料，只读）→ wiki（LLM 维护的 md）→ WIKI-SCHEMA（约定）
- 操作：ingest（摄入）→ query（查询+归档）→ lint（健康检查）
- 与现有 memory/knowledge/ 互补：memory 记规则，wiki 记深层知识

## archive 记忆仓库

- 位置：`~/.workbuddy/archive-vault/`
- 六层：sources/ → wiki/（entities/concepts/topics）→ preferences/ → projects/ → domains/
- 操作：CONSULT（任务前自动查）→ SAVE（任务后自动存）→ INGEST → QUERY → LINT
- 与 llm-wiki 互补：llm-wiki 管 wiki 知识，archive 管偏好/项目/领域上下文
- 自动触发：任务 >2 步、涉及 auth/config、用户说"和上次一样"时自动 CONSULT

## Hooks 配置

- 位置：`~/.codebuddy/settings.json`（用户级）
- 脚本：`~/.codebuddy/hooks/auto-analyze.py`

### PostToolUse: auto-analyze

每次 Write/Edit 文件后自动触发，根据项目框架运行对应分析工具：

| 文件类型 | 检测条件 | 运行命令 |
|----------|----------|----------|
| `.dart` (Flutter) | `pubspec.yaml` 含 flutter | `flutter analyze` |
| `.dart` (纯 Dart) | `pubspec.yaml` 不含 flutter | `dart analyze` |
| `.ts`/`.tsx` (Vue) | `tsconfig.json` + vue 依赖 | `npx vue-tsc --noEmit` |
| `.ts`/`.tsx` (纯 TS) | `tsconfig.json` 无 vue | `npx tsc --noEmit` |
| `.vue` | `tsconfig.json` 存在 | `npx vue-tsc --noEmit` |
| `.js`/`.mjs`/`.cjs` | `package.json` 存在 | `npx eslint <file>` |
| `.css`/`.scss` | `package.json` 存在 | `npx stylelint <file>` |
| `.go` | `go.mod` 存在 | `go vet ./...` |

- 防抖：同一项目同一框架 30 秒内不重复运行
- 超时：60 秒后自动终止
- 退出码 0 = 静默通过；1 = 发现问题（展示为 warning，不阻塞）；2 = 运行错误

## MCP 服务器

| MCP | 用途 | 配置 |
|-----|------|------|
| playwright | 浏览器自动化 | npx @playwright/mcp |
| RedNote-MCP | 小红书内容读取 | npm 包 |
| ctrip | 携程问道旅行数据 | Python venv |
| codebase-memory-mcp | 代码知识图谱（158 语言，14 工具） | v0.8.1, 二进制 `C:\Users\hzy\AppData\Local\Programs\codebase-memory-mcp\` |

> ⚠️ **UI 可视化**：标准版无前端，需安装时加 `--ui`（`install.ps1 --ui`）下载 UI 版本。运行时加 `--ui` 无效——必须在安装阶段选 UI variant。UI 运行在 `http://localhost:9749`。

### codebase-memory-mcp 工具清单

| 工具 | 用途 |
|------|------|
| `index_repository` | 索引代码库（full/moderate/fast/cross-repo） |
| `search_graph` | 结构化搜索函数/类/路由 |
| `trace_path` | 调用链追踪（calls/data_flow/cross_service） |
| `query_graph` | Cypher 图查询（性能热点/复杂度检测） |
| `get_architecture` | 架构概览 |
| `detect_changes` | Git 变更影响分析 |
| `semantic_query` | 语义向量搜索 |
| `search_code` | 图增强代码搜索 |
| `get_code_snippet` | 读取函数/类源码 |
| `list_projects` | 列出已索引项目 |
| `index_status` | 索引状态查询 |
| `delete_project` | 删除索引 |
| `manage_adr` | 架构决策记录 |
| `ingest_traces` | 运行时调用追踪 |
