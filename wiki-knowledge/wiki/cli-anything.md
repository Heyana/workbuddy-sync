---
title: CLI-Anything
type: concept
created: 2026-06-26
updated: 2026-06-26
tags: [tool-eval, cli, ai-agent, not-adopted, hkuds]
---

# CLI-Anything

港大数据科学实验室（HKUDS）开源，10k+ stars。为任意 GUI 软件自动生成标准化 CLI 接口。

## 核心思路

大多数专业 GUI 软件有脚本接口（API/SDK），但没人包装成 CLI。
CLI-Anything 用 7 阶段自动化流水线扫描代码库 → 生成 CLI 封装。

## 覆盖软件

GIMP（图片）、Blender（3D）、LibreOffice（文档）、以及数百款其他软件。

## 评估结论：不采用

已有原生 CLI 工具覆盖需求：

| 需求 | 已用工具 |
|------|---------|
| 图片处理 | ImageMagick |
| 视频编码 | ffmpeg |
| 元数据 | exiftool |

CLI-Anything 价值在 3D 渲染、高级图片编辑、办公套件自动化——非当前主战场。

## See Also

- [[ego-lite-browser]]
- [[skills-orchestration]]
