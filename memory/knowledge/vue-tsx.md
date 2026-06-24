# Vue 3 TSX 知识库

> TSX 模式下的组件编写、函数式调用、类型安全踩坑与最佳实践。
> 保持精炼——只记结论和关键约束，不记推导过程。

---

## 铁律：TSX 优先，非必要不 .vue

- Vue 3 组件**优先用 `.tsx`**，.vue SFC 只在以下情况用：
  - shadcn-vue 原生组件（已用 .vue 提供，不动它）
  - 薄封装透传层（如 ZButton/ZTag）可保留 .vue
- **触发切换 TSX 的信号**：v-model 绑定问题、类型丢失、reka-ui/vaul-vue 行为异常

### .vue SFC 的已知限制
- `v-model` 绑定怪异——类型映射不可靠
- 动态组件受限（`:is` 的 props 透传有问题）
- `$event` 类型是 `any`，丢失类型安全
- slot scoping 在某些 edge case 不可靠

### TSX 的优势
- 类型全程贯通（泛型、props、events 全类型化）
- 组件组合即函数调用，无模板语法陷阱
- IDE 智能提示完整

---

## 函数式交互组件（核心模式）

### 原则
- 弹窗、右键菜单、抽屉、Toast 等交互组件，**优先用函数式调用**
- 不插声明式 JSX + 一堆 `visible` 状态

### ✅ 正确方式
```tsx
// 对话框
onClick={() => dialog.confirm({ title: '确认删除？' })}

// 右键菜单
onContextMenu={(e) => rightMenu.open({ items: [...], x: e.clientX, y: e.clientY })}

// Toast
toast.success('保存成功')
```

### ❌ 错误方式
```vue
<Dialog :open="showDialog" @update:open="showDialog = $event">
  <!-- 一堆模板 -->
</Dialog>
```

### 原因
- 减少中间状态变量
- 调用即释放，不用管理生命周期
- 代码更紧凑

---

## 实现方式：TSX + createApp（禁止 h() 拼接）

### ❌ 禁止 `h()` render function
```ts
// 错误——类型安全完全丢失，传参断路，调试困难
h(Component, { prop: val }, () => [h(Child), ...])
```

### ✅ 正确：.tsx + createApp
```tsx
// my-dialog.tsx
export function openMyDialog(props: Props) {
  const div = document.createElement('div')
  document.body.appendChild(div)
  const app = createApp(MyDialogComponent, { ...props, onClose: () => {
    app.unmount()
    div.remove()
  }})
  app.mount(div)
}
```

### 典型案例
| 组件 | 方案 |
|------|------|
| Toast | vue-sonner 原生 API：`toast('message')` |
| Dialog | TSX + createApp |
| Drawer | TSX + createApp |
| RightMenu | TSX + createApp |

---

## 项目结构（Vue/TSX 前端）

```
src/
├── pages/          # 路由页面（一个路由一个文件）
├── views/          # 视图片段
├── components/
│   ├── ui/         # shadcn 基础组件
│   └── controls/   # 自定义控件
├── composables/    # Hooks / 组合式函数
├── stores/         # Pinia 状态管理
├── api/modules/    # API 请求层
├── router/         # 路由
├── utils/          # 纯工具函数
├── lib/            # cn, constants 等
├── types/          # TS 类型
└── App.tsx         # 仅布局 + RouterView
```

### 分层边界
- **view 层**：只调 store/composable，不直接 import platform 或 HTTP client
- **store 层**：内部调 `platform.db.xxx` 或 api 模块
- **简单系统能力**（窗口/剪贴板/主题）：放 composable 封装
- 好处：换后端只需改 store 内部实现，view 代码不动

---

## ZUI v2 特定

- 技术栈：Vite 6 + Vue 3.5 + TS 5.6 + Tailwind v4 + shadcn-vue
- 35 个组件，构建产物：dist/zui.js (ES, gzip 37.8KB) + dist/zui.umd.cjs (UMD, gzip 29.4KB)
- 组件如 ZButton, ZTable, ZVirtualList 等
- 预设代码 `a2QcktPc`（禁止解码）
- 函数式 API：toast/dialog/drawer 均通过 TSX + createApp 实现
- reka-ui 底层组件行为查源码，不靠文档脑补

---

## 已知踩坑

| 问题 | 根因 | 方案 |
|------|------|------|
| v-model 类型丢失 | .vue 模板限制 | 切 TSX |
| `__vccOpts` 路由报错 | 组件未 export default | 加 `export default` |
| reka-ui 行为异常 | .vue 下 slot scoping 问题 | 切 TSX |
| 反复翻车的组件 | 猜行为而非看源码 | 直接读 reka-ui / vaul-vue 源码 |
| `onChange` 回调收到 `[object Event]` | emits 名以 `on` 开头，外部监听时被当成 DOM 原生事件 | 见下方详解 |

---

## ⚠️ emits 命名不得以 `on` 开头

### 问题现象

```tsx
// ZInputV1 内部
emits: ['onChange', ...]
emit('onChange', val)  // 发出字符串 val

// 外部消费
<ZInputV1 onChange={(e) => console.log(e)} />
// 打印 [object Event]  ← 收到的是原生 DOM change 事件！
```

### 根因

Vue 的事件绑定规则：JSX/模板中的 `onXxx` → 监听名为 `xxx` 的事件。
当 `emits: ['onChange']` 时，外部要监听它必须写 `onOnChange`。
而 `onChange` 这个写法已被 Vue 解释为监听原生 DOM 的 `change` 事件 → 收到 Event 对象。

```
emits 声明名      → 外部监听属性名
'change'         → onChange      ✅ 自然
'update:value'   → onUpdate:value
'onChange'       → onOnChange    ⚠️ 丑陋（命名 bug）
```

### 修复方案

**根本修复**：emits 名永远不要加 `on` 前缀：

```ts
// ✅ 正确
emits: ['change', 'pressEnter', 'update:value']
emit('change', val)

// 外部
<MyInput onChange={(v: string) => { ... }} />
```

**临时绕过**（不改组件时）：

```tsx
<ZInputV1 onOnChange={(v: string) => { ... }} />
```

### 兼容适配层注意

ZUI v1 兼容层 `ZInputV1` 存在此问题（`emits: ['onChange']`），外部调用必须用 `onOnChange`。

---

_最后更新：2026-06-24 | 新增 emits 命名不得以 `on` 开头的规则与 [object Event] 坑_
