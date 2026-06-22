# 同步规则

## 修改后
- 修改 `~/.workbuddy/` 下文件后 commit + push 到 GitHub（master 分支）
- topic 文件中引用项目时只用项目名，不写绝对路径

## 拉取后
1. `git pull --rebase`
2. 检查 `topics/skills.md`，对缺失的 skill 通过 marketplace 安装
3. 检查 `topics/mcp-rules.md` 配置模板，更新本地 `mcp.json`

## 机器相关
- 各机器本地维护 `project-map.md`（项目名→路径映射表），该文件不入 git
- `mcp.json`、`settings.json` 等不入 git，由各机器各自维护
