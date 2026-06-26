---
title: Ego Lite Browser
type: concept
created: 2026-06-26
updated: 2026-06-26
tags: [tool-eval, browser, ai-agent, not-adopted]
---

# Ego Lite Browser

专为 AI Agent 设计的 Chromium 浏览器。

## 核心能力

- 共享用户登录态（cookie/session），Agent 直接用你的身份操作
- 独立 Space 容器，Agent 操作不干扰你的标签页
- 3x 更快、94% 更省内存（vs 传统方案）
- 零成本、零配置

## 评估结论：不采用

已有 playwright MCP 覆盖浏览器自动化（截图、表单、测试）。
ego lite 优势在"代理操作需登录的网站"（订票、审批），不是开发主场景。

## See Also

- [[cli-anything]]
- [[skills-orchestration]]
