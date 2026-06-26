---
title: Skills Orchestration
type: concept
created: 2026-06-26
updated: 2026-06-26
tags: [skills, superpowers, impeccable, workflow, dev-process]
---

# Skills Orchestration

多个 AI 编程 Skill 的编排模式：按开发阶段分派不同 Skill 组合。

## 开发阶段 → Skill 映射

| 阶段 | 技能 | 说明 |
|------|------|------|
| 需求梳理 | `prd-development` | 从想法生成结构化 PRD |
| 需求 + 测试基准 | `prd-test-writer` | PRD + 测试用例双文档 |
| 架构审查 | `improve-codebase-architecture` | 深度扫描，出可视化报告 |
| 设计审查 | `impeccable` (audit) | AI Slop 检测、启发式评分 |
| 头脑风暴 | `superpowers:brainstorm` | 苏格拉底式问答，精确定义 |
| 任务规划 | `superpowers:write-plan` | 拆成 2-5 分钟小任务 |
| 批量实现 | `superpowers:execute-plan` | 子代理并行执行 |
| 设计修复（视觉） | `impeccable` (arrange/typeset) | 布局、字体、色彩 |
| 设计修复（结构） | `superpowers:write-plan` | 拆为非可视类修改任务 |
| 调试 | `superpowers:systematic-debugging` | 四阶段根因分析 |
| 代码审查 | `superpowers:requesting-code-review` | 对照计划审查 |
| 上线前 | `superpowers:verification-before-completion` | 确保真修好 |

## 审计 → 修复闭环

```
impeccable audit
    ↓
视觉/排版问题 → impeccable 内置 reference
逻辑/结构问题 → superpowers write-plan → execute-plan
    ↓
polish → harden → 发布
```

## 技能来源

| Skill | 来源 | 位置 |
|-------|------|------|
| superpowers | 插件 | `~/.workbuddy/plugins/marketplaces/codebuddy-plugins-official/external_plugins/superpowers/` |
| impeccable | 内置市场 | `~/.workbuddy/skills/skill_2053082862415904768/` |
| prd-development | skills.sh | `~/.workbuddy/skills/prd-development/` |
| prd-test-writer | skills.sh | `~/.workbuddy/skills/prd-test-writer/` |
| grill-me | 内置市场 | `~/.workbuddy/skills/skill_2057443369928683520/` |

## 注意

- skills.sh 安装的 skill 在 `.agents/skills/`，需手动 cp 到 `~/.workbuddy/skills/` 后 WorkBuddy 才能用
- 插件和 Skill 是不同机制：插件提供 `/command` 形式，Skill 由 AI 自动匹配触发

## See Also

- [[code-knowledge-graph-pattern]]
- [[impeccable-design-critique]]
