# 全项目偏好

## Flutter 项目通用规则
- **禁止 import `package:flutter/widgets.dart`**：shadcn_flutter 已包含所有需要的 widget（Div/WText/WIcon/WButton/WSvg 等），无需额外导入
- **禁止 import `package:flutter/material.dart`**（仅 main.dart 例外，MaterialApp.router 需要）
- **禁止 `Row`、`Column`**：`Div` + className（`row`/`col`/`row-aic`/`col-c` 等）全覆盖所有 flex 布局需求
- 页面文件只 import：`shadcn_flutter/shadcn_flutter.dart` + `fluttersdk_wind/fluttersdk_wind.dart` + `my-wind/div.dart`
- 布局必须使用 fluttersdk_wind（Tailwind CSS 风格）+ my-wind/div.dart 的 Div 封装
- shadcn_flutter import hide：`Scaffold`, `NavigationBar`, `ThemeMode`
- shadcn_flutter 0.0.52 的 **LucideIcons 使用 camelCase**（如 `shoppingCart`、`chevronDown`、`flaskConical`），不是 snake_case。不确定时读 `Pub/Cache/hosted/pub.flutter-io.cn/shadcn_flutter-{ver}/lib/src/icons/lucide_icons.dart` 确认，禁止猜
- **WText 动态颜色用 `foregroundColor:`**，不可用 `style: TextStyle(...)`（style 类型是 WindStyle?）
- **Wind `bg-[#...]` 只支持 6 位 hex（RRGGBB）**，不支持 8 位 ARGB。动态色必须取后 6 位：`'bg-[#${color.toARGB32().toRadixString(16).padLeft(8, '0').substring(2)}]'`
- **material.dart 只在 main.dart 允许**（MaterialApp.router 需要），其他所有文件禁止 import。main.dart 的 shadcn import 必须 hide ThemeMode
- 字符串插值单变量不加花括号：`$index` 而非 `${index}`
- StatelessWidget 子类构造函数加 `const`

## 工作习惯
- 代码修改完成后，**自动**更新当日记忆（`.workbuddy/memory/YYYY-MM-DD.md`），按需更新空间记忆（`.workbuddy/memory/MEMORY.md`）——不用等用户提醒
- **提交代码 = git add -A + git commit + git push**：当说"提交代码"时，自动暂存所有变更、提交并推送，不用追问

## 小红书 MCP 使用规则
- **搜索必须逐个进行**，不要并行多个 search_feeds 调用
- 并行搜索容易触发小红书风控，导致请求超时
- 每次搜索间隔至少 2-3 秒
