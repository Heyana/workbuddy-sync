# MCP 使用规则

## 已安装 MCP Servers
- **playwright** — 浏览器自动化（截图/DOM检查/交互），用于 Vue/前端组件调试
- **RedNote-MCP** — 小红书笔记搜索/内容获取
- **ctrip** — 携程数据抓取

## 使用规则
- RedNote-MCP 搜索必须逐个进行，间隔 2-3 秒
- 并行搜索易触发风控
- 工具名使用 snake_case

## Playwright MCP 截图工作流（标准操作）

1. `browser_navigate` → 打开目标页面
2. `browser_take_screenshot` → `filename: "xxx.png"`（只用文件名，不用路径）
3. 截图默认存在沙箱根目录：`~/.workbuddy/logs/mcp-runtime/custom-mcp_playwright-*/xxx.png`
4. 用一行命令拷贝到项目：`cp ~/.workbuddy/logs/mcp-runtime/custom-mcp_playwright-*/xxx.png /d/hxy/github/vue3_zui/xxx.png`
5. `Read` 截图验证 → `present_files` 展示给用户
6. 用完后清理项目中的临时截图

## Playwright MCP 组件审查工作流
1. 截图亮色模式 → `browser_navigate` + `browser_take_screenshot`
2. 切换到暗色 → `browser_click` 日夜切换按钮 → `browser_take_screenshot`
3. 对比两图写出分析
4. 发现具体 UI 问题时 `browser_snapshot` 拿到 DOM 结构，定位 CSS class
