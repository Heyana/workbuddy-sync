---
title: UI UX Pro Max
type: concept
created: 2026-06-26
updated: 2026-06-26
tags: [tool-eval, design, ui, skill, adopted]
---

# UI UX Pro Max

AI 设计素材 Skill，MIT 开源免费。67 种 UI 风格、161 套配色、57 套字体、99 条 UX 规范。

## 核心能力

将结构化设计知识库注入 AI 助手，让 AI 生成 UI 时有专业参考：

| 资源 | 数量 | 示例 |
|------|------|------|
| 设计风格 | 67 | Glassmorphism/Neumorphism/Minimalism/Aurora/Bento |
| 色彩系统 | 161 | 按行业（SaaS/医疗/电商/金融） |
| 字体搭配 | 57 | 含 Google Fonts + Tailwind config |
| UX 规范 | 99 | 动画/可访问性/z-index/加载状态 |
| 技术栈 | 16 | Flutter/Vue/React/shadcn/Three.js |

## 安装

```bash
npm install -g uipro-cli
uipro init --ai codebuddy
cp -r .codebuddy/skills/ui-ux-pro-max ~/.workbuddy/skills/
```

## 与 impeccable 配合

| | UI UX Pro Max | impeccable |
|------|------|------|
| 角色 | 设计素材库 | 设计审查员 |
| 使用时机 | 从零生成新页面 | 审查已有设计 |
| 输出 | 具体色盘/字体/风格方案 | 问题清单+改正方向 |

工作流：Pro Max 生成方案 → impeccable 审查 → 修复 → 发布

## See Also

- [[impeccable-design-critique]]
- [[skills-orchestration]]
