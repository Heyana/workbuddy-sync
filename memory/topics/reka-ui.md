# reka-ui 尽职调查 — 核心组件机制与薄封装陷阱

> 仓库：`D:\hxy\github\reka-ui` (`unovue/reka-ui`, v2.10.0, MIT)
> 
> 分析时间：2026-06-21
> 
> 66 个组件，其中 60 个公开导出，6 个内部（Menu/Popper/Collection/FocusGuards/Teleport/ColorPicker）

---

## 1. ContextMenu 完整工作流

### 1.1 组件树

```
ContextMenuRoot (provide ContextMenuRootContext)
  └─ MenuRoot (provide MenuContext + MenuRootContext)
       └─ PopperRoot
            ├─ ContextMenuTrigger (inject rootContext)
            │    ├─ MenuAnchor (as="template", :reference=virtualEl)
            │    └─ Primitive (@contextmenu → onOpenChange(true))
            │         └─ <slot />
            └─ ContextMenuContent (inject menuContext)
                 └─ MenuContent (hardcodes side="right" offset="2" align="start")
                      └─ MenuContentImpl
                           ├─ Presence (:present="menuContext.open.value")
                           │    └─ FocusScope → DismissableLayer → RovingFocusGroup → PopperContent
                           │         └─ <slot />
                           └─ [20+ provide 注入]
```

### 1.2 不依赖 slot props，全用 provide/inject

这是 reka-ui 的**核心设计原则**。兄弟组件之间不通过 slot props 通信，而是靠 Vue 的 provide/inject：

```
ContextMenuRoot
  ├─ provideContextMenuRootContext({ open, onOpenChange, triggerElement, modal, dir })
  └─ <MenuRoot>
       ├─ provideMenuContext({ open, onOpenChange, content, onContentChange })
       └─ provideMenuRootContext({ onClose, isUsingKeyboardRef, dir, modal })

ContextMenuTrigger
  ├─ injectContextMenuRootContext()  → 读到 open/onOpenChange
  └─ @contextmenu → rootContext.onOpenChange(true)

ContextMenuContent (via MenuContentImpl)
  ├─ injectMenuContext()  → 读到 open.value
  └─ <Presence :present="menuContext.open.value">
       → Content 显示/隐藏
```

**关键推论**：只要 render 树链路完整（祖先有 ContextMenuRoot，后代有 Content/Trigger），状态就能自动传递。**不需要手动传 open state 给 slot。**

### 1.3 定位原理（为什么位置总是对的）

ContextMenuTrigger 通过虚拟元素定位：

```ts
const point = ref({ x: 0, y: 0 })
const virtualEl = computed(() => ({
  getBoundingClientRect: () => ({
    width: 0, height: 0,
    left: point.value.x, right: point.value.x,
    top: point.value.y, bottom: point.value.y,
    ...point.value,
  })
}))

function handleContextMenu(event: PointerEvent) {
  point.value = { x: event.clientX, y: event.clientY }
  rootContext.onOpenChange(true)
  event.preventDefault()
}
```

`MenuAnchor` 使用这个虚拟元素的 bounding rect 作为 Popper 定位的参考点。所以**定位基于右键点击坐标**，不受 DOM 布局影响。

---

## 2. ContextMenuSub 机制

### 2.1 双层 MenuContext

```
ContextMenuRoot
  └─ MenuRoot (provide MenuContext#1 — 根菜单)
       └─ ContextMenuContent
            └─ ContextMenuSubTrigger
                 └─ ContextMenuSub (provide MenuContext#2 — 子菜单)
                      └─ MenuSub
                           ├─ provideMenuContext({ open, ... })
                           ├─ injectMenuContext() → 父 MenuContext#1
                           └─ watchEffect: 父 open=false → 子 open=false
                      └─ ContextMenuSubContent
                           └─ MenuSubContent (使用 MenuContext#2)
```

子菜单重新 `provideMenuContext()`，覆盖父级的 context 但通过 `injectMenuContext()` 拿到父级 context 做联动（父关闭时子也跟着关）。

### 2.2 SubTrigger 的 Grace 区域（防止抖关）

MenuSubTrigger 在 hover 到子菜单时使用"grace area"（三角形容忍区域）防止菜单抖动关闭：

```ts
// 从 SubTrigger 到 SubContent 画一个三角形
// 只要鼠标在这个区域移动，就不关闭子菜单
contentContext.onPointerGraceIntentChange({
  area: [
    { x: clientX, y: clientY },
    { x: contentNearEdge, y: contentRect.top },
    { x: contentFarEdge, y: contentRect.top },
    // ... 三角形区域
  ],
  side,
})
```

---

## 3. 其他菜单类组件（对比）

### DropdownMenu

与 ContextMenu 结构相同，但：
- 使用 `useVModel` 控制 open（外部可 v-model:open）
- Content 使用 `side="bottom"` align="start"（下弹）
- Trigger 是点击触发，非右键

### Menubar

最复杂：多个 MenuRoot 共享一个 MenubarRoot，通过 MenubarRoot 的 provide 统一管理：
- 只有一个菜单能同时打开
- hover 行为互斥
- 支持键盘导航在菜单间跳转

---

## 4. Popper 定位引擎

所有弹出组件（Menu/Popover/Select/Combobox/DropdownMenu/HoverCard/Tooltip）共享 `Popper`：

```
PopperRoot    — 提供 Popper 上下文、计算定位
  ├─ PopperAnchor   — 定位锚点（作为 template）
  └─ PopperContent  — 浮动内容（基于 floating-ui 计算 position）
```

定位由 `@floating-ui/vue` 库驱动，`data-side`/`data-align` 属性反映最终位置。

---

## 5. 常见薄封装"内容不显示"陷阱

### ❌ 陷阱 1：v-if 打断组件树

```vue
<!-- 错误 -->
<template>
  <ContextMenuRoot>
    <ContextMenuTrigger><slot name="trigger"/></ContextMenuTrigger>
    <ContextMenuContent v-if="isOpen">  <!-- isOpen 来自外部 -->
      <slot />
    </ContextMenuContent>
  </ContextMenuRoot>
</template>
```

**问题**：ContextMenuContent 的渲染依赖于内部的 `menuContext.open.value`（来自 provide/inject），不是外部的 `isOpen`。如果在第一次右键前 Content 没挂载，`onContentChange` 回调不会触发，菜单可能无法正确显示。

### ❌ 陷阱 2：ContextMenuSub 丢弃 slot props

```vue
<!-- shadcn-vue 的 ContextMenuSub 薄封装 -->
<template>
  <ContextMenuSub data-slot="context-menu-sub" v-bind="forwarded">
    <slot />   <!-- 丢弃了 reka-ui 的 :open="open" -->
  </ContextMenuSub>
</template>
```

**影响**：用户代码无法访问子菜单的 open 状态（但子菜单内部组件不受影响，因为内部用 inject）。

### ❌ 陷阱 3：as-child 不兼容

```vue
<ContextMenuTrigger as-child>
  <YourComponent />  <!-- YourComponent 必须能接收并转发所有 props -->
</ContextMenuTrigger>
```

ContextMenuTrigger 内部使用 `<Primitive :as-child="..." v-bind="$attrs">`。如果 `YourComponent` 没有 `inheritAttrs: false` + 手动 `v-bind="$attrs"`，data-*、aria-* 等属性会丢失。

### ❌ 陷阱 4：用 div 包裹打断 provide/inject

```vue
<!-- 错误 -->
<template>
  <ContextMenuRoot>
    <div>  <!-- 多余包裹层 -->
      <ContextMenuTrigger><slot name="trigger"/></ContextMenuTrigger>
      <ContextMenuContent><slot /></ContextMenuContent>
    </div>
  </ContextMenuRoot>
</template>
```

Vue 的 inject 会向上查找，不会受 `<div>` 影响。这个**实际是安全的**。但如果在中间插入了其他会 `provide` 同名 key 的组件，就会覆盖。

### ❌ 陷阱 5：ContextMenu 与 ContextMenuTrigger 不在同一条渲染链

```vue
<!-- 典型用户代码 -->
<ZContextMenu>
  <template #trigger>
    <ZButton>右键</ZButton>
  </template>
  <ZContextMenuItem>复制</ZContextMenuItem>
  <ZContextMenuItem>删除</ZContextMenuItem>
</ZContextMenu>
```

如果 `ZButton` 内部使用 `<Primitive>` 或 `<button>` 并且正确 forwards attrs，这没问题。但如果 `ZButton` 的根元素不是交互元素（例如是 `<span>` 但没有 tabindex），浏览器不会触发 contextmenu 事件。

### ✅ 正确的薄封装模板

```vue
<!-- ZContextMenu.vue -->
<script setup lang="ts">
import {
  ContextMenu,
  ContextMenuContent,
  ContextMenuItem,
  ContextMenuSeparator,
  ContextMenuShortcut,
  ContextMenuTrigger,
} from "@/components/ui/context-menu"

defineSlots<{
  trigger?: (props: {}) => any
  default?: (props: {}) => any
}>()
</script>

<template>
  <ContextMenu>
    <ContextMenuTrigger>
      <slot name="trigger" />
    </ContextMenuTrigger>
    <ContextMenuContent>
      <slot />
    </ContextMenuContent>
  </ContextMenu>
</template>
```

**关键点**：
- Root/Trigger/Content 紧邻，没有中间组件
- `<slot name="trigger" />` 直接是 Trigger 的子节点
- `<slot />` 直接是 Content 的子节点
- 不传 `as-child`（让 Trigger 的默认 `as="span"` 包裹）
- 不用 `v-if` 控制 Content

---

## 6. 调试方法

### 检查 provide/inject 链

```ts
// 在组件的 setup 中打印
const ctx = injectContextMenuRootContext()  // 如果是 undefined → 链断了
```

### 检查 open 状态

```ts
const menuContext = injectMenuContext()
watch(menuContext.open, (val) => console.log('menu open:', val))
```

### 检查 DOM 属性

打开 DevTools → 检查浮动元素（document.body 下）：
- `[data-reka-menu-content]` → Content 是否在 DOM 中
- `[data-state="open"]` → 是否 open
- `data-side` → 定位在哪个方向

### 检查 Trigger 事件

```ts
// 在 Trigger 包裹元素上加原生事件
<div @contextmenu="(e) => console.log('contextmenu!', e.defaultPrevented)">
```

---

## 7. 依赖与版本

```
reka-ui: 2.10.0
@floating-ui/vue: 定位引擎
@vueuse/core: useVModel
vue: >= 3.4.0
```

**子路径导出**：
- `reka-ui` → 所有公开组件
- `reka-ui/internal` → `useForwardProps`, `useForwardExpose`, `useEmitAsProps`, `useForwardPropsEmits`
- `reka-ui/constant` → 常量
- `reka-ui/date` → 日期工具
