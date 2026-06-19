# 编码风格

## 适配器优先
- **不要写死代码。** 任何第三方依赖、平台 API、外部服务，通过适配器层封装
- 换实现只需改适配器内部，调用方不动
- 典型案例：storage adapter / platform adapter / api client adapter

## 封装复用
- 多次使用的常量 → 抽到 `constants/`
- 多次使用的工具函数 → 抽到 `utils/` 或 `composables/`
- 不撒胡椒面——同一段逻辑出现在 2 处以上就必须封装

## 函数式交互组件
- 弹窗、右键菜单、抽屉、Toast 等交互组件，**优先用函数式调用**，不插声明式 JSX
- ✅ 好：`onClick={() => dialog.confirm({ title: '确认删除？' })}`
- ❌ 差：`<Dialog :open="showDialog">...</Dialog>` + 一堆 visible 状态管理
- ✅ 好：`rightMenu.open({ items: [...], x, y })`
- ❌ 差：`<RightMenu :visible="..." :items="..." />`
- 原因：减少中间状态、调用即释放、代码更紧凑
