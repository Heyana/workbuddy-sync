# 用户级偏好记忆

## Flutter 项目通用规则
- 技术栈：shadcn_flutter + fluttersdk_wind + LucideIcons
- 禁止使用 material/forui 组件（main.dart 例外）
- 布局使用 Div + Wind className（row/col/row-aic/col-c 等），禁止 Flutter 原生 Expanded/Spacer/Flexible
  - 原因：Wind Column/Row 被 WindFlexOverflowScope 包裹，原生 FlexParentData 不兼容
- flex-1 用 WDiv(className: 'flex-1', children: [...])，但禁止嵌套 flex-1（内部 Expanded > Expanded 冲突）
- 页面只 import shadcn_flutter + wind + my-wind/div
- shadcn_flutter import 需 hide Scaffold, NavigationBar, ThemeMode
- LucideIcons 使用 camelCase
- WText 动态颜色用 foregroundColor:，非 style:
- Wind bg-[#...] 只支持 6 位 hex
- 查询必须用 proper where 子句，禁止 '1=1' 原始 SQL

## 同步规则
- 修改 `~/.workbuddy/` 下文件时，必须同步更新 `D:\hxy\github\workbuddy-sync/` 中对应文件
- 需要同步的文件：`mcp.json`、`MEMORY.md`、`models.json`、`settings.json`、`skills/`、`connectors/`
- 同步后一并 commit + push 到 GitHub

## 工作习惯
- 代码修改完成后自动更新记忆，不用等提醒
- "提交代码" = git add -A + commit + push 全流程
- 完成修改后自动 commit 并 push

## 当前项目
- Flutter 资产记账 App（WorkBuddy-Space/asset_manager）：WebDAV 多账号文件级增量同步
- Electron 媒体管理器（electron-media-manager）：Go 后端 + SQLite
- osvtoolbox：ffmpeg 编码优化（RTX 4070 GPU）
- Flutter 'dots' 个人追踪 App：Timeline 功能开发中

## MCP 使用规则
- RedNote-MCP 搜索必须逐个进行，间隔 2-3 秒
- 并行搜索易触发风控
- 工具名使用 snake_case
