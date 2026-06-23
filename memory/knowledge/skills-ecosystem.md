# Skills 生态 & 市场

> 2026-06-24 调研 [skillstore.io](https://skillstore.io/zh-hans) 和 [skills.sh](https://www.skills.sh/)

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

## 安装渠道

### WorkBuddy 内置市场（BuiltinMarket）
- 工具：`workbuddy_marketplace_skill`（deferred tool）
- 流程：search → install
- 仅限已在市场上架的 skill

### skills.sh 生态
- 命令：`npx skills add <repo_url> --skill <name>`
- 源：GitHub 仓库（anthropics/skills、mattpocock/skills、vercel-labs/skills 等）
- 注意：`npx skills add` 会弹出交互式 agent 选择器，用 `-y` 跳过
- 如果交互式安装卡住：直接从 GitHub raw 拉 SKILL.md → 手动写入 `~/.workbuddy/skills/<name>/SKILL.md`

### skillstore.io
- 偏 AI 内容生成（slides、banner、图标等）
- 有一个 `domain-modeling` 概念不错但太重
- 整体与我们的开发场景匹配度低

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
