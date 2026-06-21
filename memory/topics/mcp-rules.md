# MCP 使用规则

## 已安装 MCP Servers
- **playwright** — 浏览器自动化（截图/DOM检查/交互），用于 Vue/前端组件调试
- **RedNote-MCP** — 小红书笔记搜索/内容获取
- **ctrip** — 携程数据抓取

## 使用规则
- RedNote-MCP 搜索必须逐个进行，间隔 2-3 秒
- 并行搜索易触发风控
- 工具名使用 snake_case
- Playwright MCP：调试网站时先 `browser_navigate` 打开页面，再用 `browser_snapshot` 获取 DOM 结构
