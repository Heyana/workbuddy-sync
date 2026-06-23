# 工作习惯

- 代码修改完成后自动更新记忆，不用等提醒
- "提交代码" = git add -A + commit + push 全流程
- 完成修改后自动 commit 并 push
- 包管理优先使用 yarn；如遇 yarn 问题可回退 npm
- **yarn 国内慢**：项目根目录放 `.yarnrc` 设 `registry "https://registry.npmmirror.com"`
- **yarn 报 `--use-system-ca is not allowed`**：前面加 `NODE_OPTIONS=""`，如 `NODE_OPTIONS="" yarn install`
- **大型任务先 spec 再闭环**：大任务先出一个 spec（计划/步骤文档），然后逐项执行闭环，防止上下文过长导致信息丢失
- **接收需求时先分析**：判断是否需要新建 spec、是否需要记录记忆留痕，再动手
- **反复翻车的组件直接看源码**：不要猜。一个问题反复出现解决不了，就去读组件的真实源码，不猜行为、不靠文档脑补。不知道就说不知道，不要假装知道
- **Skills 智能调用**：AI 应根据上下文自动判断触发 skill，不需要用户手动指定 `/skill-name`。匹配到场景就自动加载使用
