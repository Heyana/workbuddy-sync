# MCP 使用规则

## 已安装 MCP Servers
- **chrome-devtools** — 前端调试主力（截图/console/network/性能/a11y树），Google 官方，50+工具
- **RedNote-MCP** — 小红书笔记搜索/内容获取
- **ctrip** — 携程数据抓取

## 配置模板（mcp.json）

以下为各服务器完整配置。`{HOME}` 替换为本机用户目录（如 `C:\Users\hy`）。
各机照此写入本地 `~/.workbuddy/mcp.json`（不入 git）。

### RedNote-MCP
```json
{
  "RedNote-MCP": {
    "command": "{HOME}\\.workbuddy\\binaries\\node\\versions\\22.22.2\\npx.cmd",
    "args": ["rednote-mcp", "--stdio"],
    "disabled": false
  }
}
```

### ctrip
```json
{
  "ctrip": {
    "command": "{HOME}\\.ctrip-mcp\\.venv\\Scripts\\ctrip-mcp.exe",
    "env": {
      "CTRIP_DATA_DIR": "{HOME}\\ctrip-data",
      "CTRIP_CHROMIUM": "{HOME}\\AppData\\Local\\ms-playwright\\chromium-1223\\chrome-win64\\chrome.exe"
    },
    "disabled": false
  }
}
```

### chrome-devtools（前端调试主力）
```json
{
  "chrome-devtools": {
    "command": "{HOME}\\.workbuddy\\binaries\\node\\versions\\22.22.2\\npx.cmd",
    "args": ["-y", "chrome-devtools-mcp@latest"]
  }
}
```
> Google 官方出品，50+ 工具。核心：`take_snapshot`（a11y树）、`take_screenshot`、`list_console_messages`、`list_network_requests`、`evaluate_script`、`performance_start_trace`。
> 首次执行会自动下载 Chrome。推荐加 `--headless` 无头模式。

## 使用规则
- RedNote-MCP 搜索必须逐个进行，间隔 2-3 秒
- 并行搜索易触发风控
- 工具名使用 snake_case

## Chrome DevTools MCP 截图工作流（标准操作）

1. `navigate_page` → 打开目标页面
2. `take_screenshot` → `filename: "xxx.png"`（只用文件名）
3. 截图默认在沙箱根目录，拷贝到项目：`cp ~/.workbuddy/logs/mcp-runtime/custom-mcp_chrome-devtools-*/xxx.png <项目路径>`
4. `Read` 截图验证 → `present_files` 展示给用户
5. 用完后清理项目中的临时截图

## Chrome DevTools MCP 组件审查工作流
1. 截图亮色模式 → `navigate_page` + `take_screenshot`
2. 切换到暗色 → `click` 日夜切换按钮 → `take_screenshot`
3. 对比两图写出分析
4. 发现具体 UI 问题时 `take_snapshot` 拿到 a11y 树结构，定位元素和 CSS class
5. `evaluate_script` 执行 JS 验证 DOM 状态
