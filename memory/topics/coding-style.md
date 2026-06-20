# 编码风格

## Vue 3 — TSX 优先，非必要不 .vue
- **Vue 3 组件优先用 `.tsx` 编写。** .vue SFC 模板限制多：v-model 绑定怪异、动态组件受限、`$event` 类型为 any、slot scoping 不可靠
- TSX 优势：类型全程贯通、组件组合即函数调用、无模板语法陷阱
- ⚠️ 例外：shadcn-vue 原生组件已用 .vue 提供；薄封装透传层可保留 .vue（如 ZButton/ZTag）
- 一旦遇到 v-model 绑定问题、类型丢失、reka-ui/vaul-vue 行为异常 → 立刻切 TSX

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

### ⚠️ 实现方式：TSX + createApp，禁止 `h()` 拼接
- **禁止使用 `h()` render function 拼接组件。** 类型安全完全丢失，传参断路，调试困难
- ✅ 正确：`.tsx` 组件 + `createApp(Component, props).mount(div)`
- ❌ 错误：`h(Component, { prop: val }, () => [h(Child), ...])`
- 典型案例：toast 用 vue-sonner 原生 API；drawer/dialog/rightMenu 用 TSX + createApp
