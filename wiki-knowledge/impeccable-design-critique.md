---
title: Impeccable Design Critique
type: concept
created: 2026-06-26
updated: 2026-06-26
tags: [design, ui, critique, impeccable, frontend]
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

## See Also
- [[flowtime-stitch]]
