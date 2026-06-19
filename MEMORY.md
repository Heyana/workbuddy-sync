# 用户级偏好记忆

## 前端项目通用规则
- **Tailwind 语义类名**：布局容器（页面、section、wrapper）必须有语义化 class 名方便定位；shadcn 组件本身不需要额外类名
  - 需要：`<div class="feature-list p-4">`、`<div class="page-wrapper">`、`<section class="sidebar">`
  - 不需要：`<Button class="my-btn">`、`<Card class="my-card">`（组件标签已可定位）
- 技术栈：shadcn_flutter + fluttersdk_wind (^1.1.0) + LucideIcons
- 禁止使用 material/forui 组件（main.dart 例外）
- 布局使用 WDiv + Wind className（row/col/row-aic/col-c 等），禁止 Flutter 原生 Spacer/Flexible
  - 原因：Wind Column/Row 被 WindFlexOverflowScope 包裹，原生 FlexParentData 不兼容
  - **例外**：Stack 内部必须用 `Expanded`/`Positioned.fill`（不能用 WDiv 替代 flex-1）
- flex-1 用 WDiv(className: 'flex-1', children: [...])，但禁止嵌套 flex-1（内部 Expanded > Expanded 冲突）
- Spacer 禁止，用 `WDiv(className: 'flex-1')` 替代
- 浮动元素陷阱：WDiv(className: 'relative') 不能让 Positioned 工作，必须用 `Stack` 包裹
  - 正确结构：`Stack(children: [Positioned.fill(child: 主内容), Positioned(bottom: x, child: 浮动元素)])`
- 页面只 import shadcn_flutter + fluttersdk_wind + my-wind/div
- shadcn_flutter import 需 hide Scaffold, NavigationBar, ThemeMode
- LucideIcons 使用 camelCase
- WText 动态颜色用 foregroundColor:，非 style:
- Wind bg-[#...] 只支持 6 位 hex
- 查询必须用 proper where 子句，禁止 '1=1' 原始 SQL

## Wind 配置规范
- 包名：fluttersdk_wind（非 wind）
- 版本：^1.1.0
- 主题配置：WindTheme + WindThemeData
  - light theme 用 WindThemeData(brightness: Brightness.light, syncWithSystem: true, ...)
  - dark theme 用 light.copyWith(brightness: Brightness.dark, colors: {...})
  - MaterialApp 放在 WindTheme.builder 内，用 controller.toThemeData() 转 Material ThemeData
- baseSpacingUnit：默认 4，设计系统用 8 时设为 8（p-1=8px）
- aliases 字段配置缩写类名（见下方别名表）
- 颜色：colors 字段用 MaterialColor（_swatch() 辅助函数从单色生成 50-950 shades）
- 字体：fontFamilies: {'sans': '字体名'}，applyDefaultFontFamily: true

## Wind 常用别名（aliases）
在 WindThemeData(aliases: {...}) 中配置：
- w=w-full, h=h-full, f=w-full h-full
- row=flex flex-row, col=flex flex-col
- aic=items-center, ais=items-start, aie=items-end
- jcc=justify-center, jcb=justify-between, jce=justify-end, jcs=justify-start
- center=flex items-center justify-center
- row-c=flex flex-row items-center justify-center
- col-c=flex flex-col items-center justify-center
- row-aic=flex flex-row items-center
- col-aic=flex flex-col items-center
- bgc-f=bg-white（背景色别名，按设计系统自定义）

## 同步规则
- 修改 `~/.workbuddy/` 下文件时，必须同步更新 `D:\hxy\github\workbuddy-sync/` 中对应文件
- 需要同步的文件：`mcp.json`、`MEMORY.md`、`models.json`、`settings.json`、`skills/`、`connectors/`
- 同步后一并 commit + push 到 GitHub

## 工作习惯
- 代码修改完成后自动更新记忆，不用等提醒
- "提交代码" = git add -A + commit + push 全流程
- 完成修改后自动 commit 并 push
- 包管理优先使用 yarn；如遇 yarn 问题可回退 npm

## 当前项目
- Flutter 资产记账 App（WorkBuddy-Space/asset_manager）：WebDAV 多账号文件级增量同步
- Electron 媒体管理器（electron-media-manager）：Go 后端 + SQLite
- osvtoolbox：ffmpeg 编码优化（RTX 4070 GPU）
- Flutter 'dots' 个人追踪 App：Timeline 功能开发中
- Wails3 demo（wails3_test_vue_ts）：Vue3+TSX+Go / v3.0.0-alpha2.104，文件拖放+窗口控制+Frameless，前端已迁 shadcn-vue
- shadcn-vue-demo：shadcn-vue 组件库试验场，reka-nova+stone+noto-sans，全局无 border（Card 除外）
- PureRaw（构想中）：照片筛选工具，Wails3 + RAW解码 + AI评分 + 快捷键操作

## Flutter 桌面截图
- **不适合。** 经 8 轮验证无可用方案
- 截图应改用 Electron（BrowserWindow + desktopCapturer），剪贴板留在 Flutter

## MCP 使用规则
- RedNote-MCP 搜索必须逐个进行，间隔 2-3 秒
- 并行搜索易触发风控
- 工具名使用 snake_case
