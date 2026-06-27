---
title: ScreenClip 截图+剪贴板工具
type: entity
created: 2026-06-27
updated: 2026-06-27
tags: [Qt, C++, 截图, 剪贴板, 项目]
---

# ScreenClip — 截图+剪贴板工具

> 基于 Qt 6.8.2 + MSVC 2022 的 Windows 截图标注 + 剪贴板管理工具。

## 架构

```
main.cpp                    ← QApplication 启动，初始化数据库
screenshottool.h/cpp        ← 核心调度：系统托盘 + 全局热键 + 剪贴板监控
globalhotkey.h/cpp          ← Win32 RegisterHotKey 封装，零依赖
screenshotoverlay.h/cpp     ← 全屏半透明遮罩 + 鼠标拖拽选区
annotationeditor.h/cpp      ← 标注编辑器：6 种工具 + 工具栏 + 渲染
clipboardmodel.h/cpp        ← SQLite 存储剪贴板历史（图片+文字）
clipboardview.h/cpp         ← 历史查看窗口（左列表右预览）
```

## 功能

### v0.1 基础功能
- 系统托盘常驻 + 右键菜单
- 全局热键：`Ctrl+Shift+A` 截全屏 / `Ctrl+Shift+S` 区域截图 / `Ctrl+Shift+V` 历史
- SQLite 自动记录剪贴板图片和文字，上限 500 条
- 缩略图预览 + 搜索过滤 + 重新复制

### v0.2 标注编辑器
- **6 种工具**：箭头(A)、矩形(R)、椭圆(O)、文字(T)、马赛克(M)、序号(N)
- **工具栏**：工具切换 + 6 色盘 + 4 级线宽 + 撤销 + 完成
- 标注完成后渲染到图片 → 复制到剪贴板
- 快捷键驱动：A/R/O/T/M/N 切换工具，1-6 换色，`[]` 调线宽，Ctrl+Z 撤销

## 关键技术点

| 问题 | 解决 |
|------|------|
| 高 DPI 截图放大/偏移 | `devicePixelRatio()` 手动转换坐标 |
| vcpkg 代理下载失败 | 改用 aqtinstall 下载预编译 Qt |
| Ninja 找不到 kernel32.lib | 用 VS Generator |
| exe 缺少 Qt DLL | windeployqt 自动部署 |
| 全局热键 | Win32 `RegisterHotKey` 封装 |

## 后续规划

- 贴图功能（截图钉在桌面）
- 颜色拾取器
- OCR 文字识别
- 滚动截图（长图拼接）

## 参见

- [[qt6-windows-dev-setup]] — Qt 6 Windows 环境搭建
- [[cross-platform-gui-comparison]] — 跨平台 GUI 框架对比（当初选型参考）
