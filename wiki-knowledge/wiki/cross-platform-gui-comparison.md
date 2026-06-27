---
title: 跨平台 GUI 框架横向对比
type: comparison
created: 2026-06-27
updated: 2026-06-27
tags: [GUI, 跨平台, 桌面开发, 框架选型]
---

# 跨平台 GUI 框架横向对比

> 2026 年主流及小众跨平台桌面/移动 GUI 框架的生态、性能、工具链对比。

## 主流框架

| 框架 | 语言 | 渲染方式 | 包体 | 适合场景 |
|------|------|----------|------|----------|
| [[qt6-windows-dev-setup\|Qt 6]] | C++/QML | 原生 + 自绘 | 15-30MB | 桌面/嵌入式优先，性能敏感 |
| Flutter | Dart | 自绘 Skia/Impeller | ~20MB | 移动优先 + 桌面/Web，全端一体 |
| React Native | JS/TS | 原生桥接 | ~20MB | 移动端，复用 Web 团队 |
| Electron | JS/HTML | Chromium 壳 | 150MB+ | 桌面，Web 前端团队快速出活 |
| Tauri v2 | Rust + JS | 系统 WebView | 5-15MB | Electron 轻量替代，体积敏感 |
| Kotlin Multiplatform | Kotlin | 原生编译 | 原生 | Android 团队扩展 iOS，共享业务逻辑 |
| .NET MAUI | C# | 原生渲染 | ~50MB | .NET 生态，Windows 优先 |
| Compose Multiplatform | Kotlin | 自绘 Skia | ~30MB | JetBrains 生态，声明式 UI |

## 小众框架

| 框架 | 语言 | 渲染方式 | 特点 |
|------|------|----------|------|
| Fyne | Go | 自绘 OpenGL | 纯 Go，无 cgo，跨桌面+移动 |
| Gio | Go | 即时模式 GPU | Fyne 竞品，每帧重绘，学习曲线陡 |
| Wails v3 | Go + JS | WebView | Go 后端 + 任意前端，打包 ~12MB |
| egui | Rust | 即时模式 GPU | Rust 最流行 GUI，50+ 内置控件 |
| Dioxus | Rust | WebView/WGPU | 类 React 语法，工具链最完整 |
| Dear ImGui | C++ | 即时模式 | 游戏/引擎调试 UI 标配，60k+ star |
| Nuklear | C | 即时模式 | 单头文件 <20KB，嵌入式友好 |
| Slint | C++/Rust/JS | 自绘 | 专用 .slint 标记语言，桌面+嵌入式 |
| Avalonia UI | C# | 自绘/XAML | WPF 精神续作，.NET 圈口碑最好 |
| Neutralinojs | JS | 系统 WebView | 比 Electron 轻 100 倍 (~5MB) |

## 即时模式 vs 保留模式

- **保留模式**（Qt/Flutter/React）：UI 是组件树，框架管理状态和重绘
- **即时模式**（Dear ImGui/Nuklear/egui/Gio）：每帧重绘全部 UI，代码即界面，无状态管理

即时模式优势：开发快（工具/面板场景）、无状态同步问题、极轻量。劣势：无原生外观、性能依赖 GPU 重绘效率。

## 按场景选型

| 场景 | 推荐 |
|------|------|
| 截图/剪贴板工具 | Qt（QScreen + QClipboard 原生支持） |
| 桌面轻量小工具 | Tauri / Wails |
| 移动+桌面+Web 全端 | Flutter |
| 嵌入式/工控/车载 | Qt（几乎没有替代品） |
| 游戏工具/编辑器 | Dear ImGui / egui |
| Web 团队转桌面 | Electron / Wails |
| 国内小程序 | Uni-app / Taro |

## 参见

- [[qt6-windows-dev-setup]] — Qt 6 Windows 开发环境搭建实录
- [[screen-clip-tool]] — 基于 Qt 的截图+剪贴板实战项目
