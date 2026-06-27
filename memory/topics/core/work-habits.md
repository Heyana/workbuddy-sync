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
- **Flutter/Dart 改完代码必须先 `flutter analyze`**：零错误后再让用户跑。不要改完直接让用户试，编译错误浪费用户时间
- **知识文件只用 Edit 追加，禁止 Write 覆写**：`Write` 会替换整个文件导致内容丢失。改记忆/知识文件永远用 `Edit` 做局部替换
- **有参考项目时优先对比参考项目**：遇到框架行为不确定的问题，不要猜，直接看参考项目（如 test_wind_1_1）怎么写的，对齐做法
- **Skills 智能调用**：AI 应根据上下文自动判断触发 skill，不需要用户手动指定 `/skill-name`。匹配到场景就自动加载使用
- **发现即记录**：使用新工具、新网站、新 skill 市场、新安装渠道等 → 立刻记入对应的 knowledge 文件，不等用户提醒。URL 必须可点击
