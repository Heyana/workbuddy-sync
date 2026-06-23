# Skills 生态 & 市场

> 2026-06-24 调研 skillstore.io 和 skills.sh

## 当前已安装 Skills

| Skill | 来源 | 目录 | 用途 |
|-------|------|------|------|
| impeccable | 内置市场 | skill_2053082862415904768 | 前端 UI 生成（偏"生成好看界面"） |
| nano-banana-pro | 内置市场 | skill_2053082421296758784 | AI 图片生成/编辑 |
| grill-me | 内置市场 | skill_2057443369928683520 | 方案压力测试/追问 |
| frontend-design | 手动安装 | frontend-design/ | 前端设计系统与规范（Anthropic 官方） |
| improve-codebase-architecture | 手动安装 | improve-codebase-architecture/ | 代码架构评估与重构建议（Matt Pocock） |
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
