# 同步规则

## 修改后
- 修改 `~/.workbuddy/` 下文件后 commit + push 到 GitHub（master 分支）
- topic 文件中引用项目时只用项目名，不写绝对路径

## 拉取后（新电脑完整流程）

1. `git clone https://github.com/Heyana/workbuddy-sync.git ~/.workbuddy`（或 `git pull --rebase`）
2. 读 `topics/frontend/skills.md`，对缺失的 skill 通过 marketplace 安装
3. 读 `topics/mcp/rules.md` 配置模板，复制对应段落到本地 `mcp.json`
4. 首次对话触发各 MCP → 自动下载依赖（chrome-devtools 下载 Chrome，RedNote-MCP 装 npm 包）
5. 手动：ctrip 需要单独建 Python venv（见 `topics/mcp/rules.md` → ctrip 配置）
6. 去 WorkBuddy MCP 管理页 → 对每个 MCP 点 Trust 激活

## 机器相关
- 各机器本地维护 `project-map.md`（项目名→路径映射表），该文件不入 git
- `mcp.json`、`settings.json` 等不入 git，由各机器各自维护
