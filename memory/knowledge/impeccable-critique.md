# Impeccable 设计审计

> 使用 Impeccable skill 进行设计审查的标准流程和关键判据。

## 审计流程

1. **AI Slop 检测**（第一优先级）— 是否看起来像 AI 生成的 2024-2025 风格界面
2. **启发式评分** — Nielsen 10 项，每项 0-4，总分 0-40
3. **优先级问题分类** — P0-P3，每个含 What/Why/Fix
4. **Persona 红旗** — 选 2-3 persona 走一遍主流程，标具体失败点

## AI Slop 指纹检测（DON'T 清单）

| 特征 | 严重度 | 常见位置 |
|------|--------|----------|
| **Inter / Roboto / Arial / Open Sans** 做正文字体 | 🔴 | 全局 font-sans |
| **毛玻璃** `backdrop-blur` + 半透明背景 | 🟡 | 模态/Header |
| **卡片套卡片** — 图标圆形 + 数字 + 标签三层 | 🟡 | Stats grid |
| **animate-pulse 状态点** | 🟢 | 状态徽章 |
| **Emoji 在文案中** | 🟢 | Toast/Alert |
| **英雄指标布局** — 居中大数字 + 环形进度 | 🟡 | 仪表盘 |
| **全圆角滥用**（即使有设计意图）| 🟢 | 全局 |

## 字体规则

- **DON'T**: Inter, Roboto, Arial, Open Sans, system-ui
- **推荐替代**: DM Sans（几何简洁）、Satoshi（人文现代）、Cabinet Grotesk（个性粗体）、Geist（Vercel 出品）
- 标题字体不受限，可保留 Sora/Display 等个性字体

## 启发式评分参考

| 区间 | 评级 |
|------|------|
| 35-40 | 极优 |
| 28-34 | 良好 |
| 20-27 | 中等，有打磨空间 |
| < 20 | 需重大改进 |

常见丢分项：错误恢复（undo/confirm）、帮助引导、键盘快捷方式、可访问性。

## 修复优先级

- **P0**: 设计系统违背（如玻璃态 vs 固态）→ 立即修
- **P1**: 通用字体、模板感布局 → 本轮修
- **P2**: 硬编码假数据、无障碍缺失 → 可延期
- **P3**: Emoji、微交互缺失 → 低优先

## 修复命令映射

Impeccable 内置命令体系：`/typeset` 字体、`/colorize` 颜色、`/arrange` 布局、`/polish` 打磨、`/critique` 重审。

实际操作中用直接编辑 + Vite HMR 回看更高效。
