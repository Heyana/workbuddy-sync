---
title: Qt 6 Windows 开发环境搭建
type: concept
created: 2026-06-27
updated: 2026-06-27
tags: [Qt, C++, Windows, MSVC, 环境配置]
---

# Qt 6 Windows 开发环境搭建

> 从零到编译运行的完整流程，踩坑记录。

## 环境选型

| 组件 | 选择 | 原因 |
|------|------|------|
| 编译器 | MSVC 2022 (VS Community 18) | vcpkg 首选，生成器兼容好 |
| Qt 获取 | aqtinstall (官方预编译包) | 避免 vcpkg 从源码编译的代理问题 |
| Qt 版本 | 6.8.2, win64_msvc2022_64 | 最新稳定版 |
| 构建系统 | CMake + Visual Studio Generator | Ninja + MSVC 找不到 kernel32.lib |
| 部署 | windeployqt | 自动复制 Qt DLL 到 exe 目录 |

## MSVC 工具链配置

VS Community 已安装但 cl.exe 不在 PATH，需手动写入 `~/.profile`：

```bash
# MSVC 2022
VS_HOME="/c/Program Files/Microsoft Visual Studio/18/Community"
MSVC_HOME="$VS_HOME/VC/Tools/MSVC/14.50.35717"
SDK_HOME="/c/Program Files (x86)/Windows Kits/10"
SDK_VER="10.0.26100.0"

export PATH="$MSVC_HOME/bin/Hostx64/x64:$SDK_HOME/bin/$SDK_VER/x64:$PATH"
export INCLUDE="$MSVC_HOME/include;$SDK_HOME/Include/$SDK_VER/ucrt;$SDK_HOME/Include/$SDK_VER/um;$SDK_HOME/Include/$SDK_VER/shared"
export LIB="$MSVC_HOME/lib/x64;$SDK_HOME/Lib/$SDK_VER/ucrt/x64;$SDK_HOME/Lib/$SDK_VER/um/x64"
```

## vcpkg 代理问题

vcpkg 内部使用 WinHTTP 下载，不认 Git Bash 的 `HTTP_PROXY` 环境变量，会报 `WinHttpSetOption failed (exit code 87)`。

**解决方案**：放弃 vcpkg 安装 Qt，改用 `aqtinstall` 直接下载官方预编译二进制：
```bash
pip install aqtinstall
aqt install-qt windows desktop 6.8.2 win64_msvc2022_64 --outputdir C:\Qt
```

⚠️ aqtinstall 在 Git Bash 下 `--outputdir /c/Qt` 会装到 `C:\c\Qt`，需用绝对路径 `C:\Qt`。

## CMake 配置

```cmake
cmake_minimum_required(VERSION 3.16)
project(MyApp LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_AUTOMOC ON)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets Sql)
qt_add_executable(MyApp main.cpp)
target_link_libraries(MyApp PRIVATE Qt6::Core Qt6::Gui Qt6::Widgets Qt6::Sql)

if(WIN32)
    set_target_properties(MyApp PROPERTIES WIN32_EXECUTABLE TRUE)
endif()
```

构建命令：
```bash
cmake .. -DCMAKE_PREFIX_PATH=C:/Qt/6.8.2/msvc2022_64 -G "Visual Studio 17 2022" -A x64
cmake --build . --config Debug
```

> VS Generator 而非 Ninja：Ninja 在 MSVC 环境下找不到 kernel32.lib 链接错误。

## windeployqt 部署

编译后 exe 缺少 Qt DLL，用 windeployqt 自动补全：
```powershell
& "C:\Qt\6.8.2\msvc2022_64\bin\windeployqt.exe" --debug "path\to\app.exe"
```

## 高 DPI 截图问题

`QScreen::grabWindow(0)` 返回物理分辨率（如 3840x2160），但 Qt 高 DPI 缩放后 widget 和鼠标坐标是逻辑分辨率（1920x1080），导致截图区域放大、选区偏移。

**修复**：手动处理 `devicePixelRatio()` — 鼠标坐标 `* dpr` 转为物理像素，pixmap 绘制时 `drawPixmap(rect(), pixmap)` 缩放到 widget 大小。

## 参见

- [[cross-platform-gui-comparison]] — 跨平台 GUI 框架全景对比
- [[screen-clip-tool]] — 基于 Qt 的截图+剪贴板实战项目
