---
title: Impeccable Design Critique
type: concept
created: 2026-06-26
updated: 2026-06-26
tags: [design, ui, critique, impeccable, frontend, audit]
---

# Impeccable Design Critique

使用 Impeccable skill 进行设计审查的标准流程和关键判据。

## AI Slop 指纹清单

| 特征 | 严重度 |
|------|--------|
| Inter/Roboto/Arial/Open Sans 正文字体 | 🔴 |
| 毛玻璃 `backdrop-blur` + 半透明 | 🟡 |
| 卡片套卡片（图标圆 + 数字 + 标签） | 🟡 |
| `animate-pulse` 状态点 | 🟢 |
| Emoji 在 UI 文案中 | 🟢 |
| 英雄指标布局（居中大数字 + 环形） | 🟡 |

## 字体替换规则

- 替换 Inter → DM Sans, Satoshi, Cabinet Grotesk, Geist
- 标题字体可保留个性字体 (Sora 等)

## 启发式评分 (Nielsen 10 项)

每项 0-4，总分 0-40。常见丢分项：错误恢复、帮助引导、键盘快捷方式、可访问性。

## 修复优先级

P0: 设计系统违背 → P1: 通用字体/模板感 → P2: 假数据/无障碍 → P3: Emoji/微交互

## 审计工作流

```
impeccable audit → 分类报告（视觉/布局/交互/文案/性能）
    ↓
视觉/排版类 → impeccable 内置 reference（arrange/typeset/colorize）
结构/逻辑类 → superpowers write-plan → execute-plan
    ↓
polish → harden → 发布
```

## 关联工具

| 场景 | impeccable reference |
|------|---------------------|
| 全面技术审查 | `audit` — a11y/性能/响应式/反模式 |
| 修复布局间距 | `arrange` — 视觉层次、间距一致性 |
| 改进字体排版 | `typeset` — 字体选择、层次、大小 |
| 策略性添加色彩 | `colorize` — 单调界面上色 |
| 响应式适配 | `adapt` — 跨设备 |
| 最终上线打磨 | `polish` — 对齐、间距、一致性 |
| 生产环境加固 | `harden` — 错误处理、i18n、边缘情况 |

技能位置：`~/.workbuddy/skills/skill_2053082862415904768/`

## See Also
- [[flowtime-stitch]]
- Impeccable skill: `~/.workbuddy/skills/skill_2053082862415904768/references/`
