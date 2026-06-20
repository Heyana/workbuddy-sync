# shadcn-vue 组件层深度分析 — 薄封装指南

> 仓库：`D:\hxy\github\shadcn-vue` (`unovue/shadcn-vue`, v2.7.4, MIT)
> 
> 🔍 底层依赖 reka-ui 分析见：[reka-ui.md](reka-ui.md) — provide/inject 链路、薄封装陷阱排查
> 
> 分析时间：2026-06-20
> 
> 源码格式：registry JSON（含内联 .vue 源码），路径 `apps/v4/public/r/styles/new-york-v4/`

---

## 1. 组件全量清单（60 个）

### 分类一：按复杂度

| 复杂度 | 特征 | 数量 | 组件 |
|--------|------|:---:|------|
| **纯 HTML** | 无 reka-ui，纯 div 封装 | 6 | card, empty, kbd, skeleton, spinner, table |
| **简单封装** | Primitive + cva + class prop | 8 | badge, button, label, separator, aspect-ratio, avatar, scroll-area, progress |
| **输入型** | HTML element + useVModel | 2 | input, textarea |
| **片段组合** | 多子组件，每个薄包一层 reka-ui 原语 | 20 | accordion, alert, alert-dialog, checkbox, collapsible, context-menu, dropdown-menu, hover-card, menubar, native-select, navigation-menu, number-field, pin-input, popover, radio-group, scroll-area, slider, switch, tabs, toggle, toggle-group, tooltip, breadcrumb |
| **复杂组合** | 多子组件 + 自定义逻辑 | 12 | dialog, select, combobox, command, drawer, sidebar, stepper, chart, carousel, input-group, input-otp, item, resizable, sheet, tags-input |
| **特殊集成** | 引入第三方库 | 7 | form (vee-validate), calendar (date-fns), range-calendar, sonner (vue-sonner), pagination, button-group, field |

### 分类二：按是否有 variants（cva）

| 有 variants | 无 variants |
|-------------|------------|
| button (6 variant × 6 size), badge (6 variant), toggle (2 variant × 3 size), toggle-group (2 variant × 2 size), input-group (3 size), alert (4 variant), carousel (2 orientation), sidebar (2 variant, 2 side, 2 collapsible), tabs (2 orientation), switch (3 size), spinner (2 size) | 其余 50 个 |

> **薄封装关键**：有 variants 的组件需要导出 `XVariants` 类型供上层复用。

---

## 2. 组件内部模式（6 种模板）

### 模板 A：超薄纯 HTML

**代表**：card, skeleton, kbd, spinner

```vue
<script setup lang="ts">
import type { HTMLAttributes } from "vue"
import { cn } from "@/lib/utils"

const props = defineProps<{
  class?: HTMLAttributes["class"]
}>()
</script>

<template>
  <div data-slot="card" :class="cn('rounded-lg border bg-card text-card-foreground shadow-sm', props.class)">
    <slot />
  </div>
</template>
```

**关键点**：
- 无 reka-ui 依赖
- 只接收 `class` prop
- `data-slot` 用于外部 CSS 定位（组合组件用）
- `cn()` 合并默认样式 + 用户 class

### 模板 B：Primitive + cva（带 variants）

**代表**：button, badge, toggle

```vue
<script setup lang="ts">
import type { PrimitiveProps } from "reka-ui"
import type { HTMLAttributes } from "vue"
import type { ButtonVariants } from "."
import { Primitive } from "reka-ui"
import { cn } from "@/lib/utils"
import { buttonVariants } from "."

interface Props extends PrimitiveProps {
  variant?: ButtonVariants["variant"]
  size?: ButtonVariants["size"]
  class?: HTMLAttributes["class"]
}

const props = withDefaults(defineProps<Props>(), {
  as: "button",
})
</script>

<template>
  <Primitive
    data-slot="button"
    :data-variant="variant"
    :data-size="size"
    :as="as"
    :as-child="asChild"
    :class="cn(buttonVariants({ variant, size }), props.class)"
  >
    <slot />
  </Primitive>
</template>
```

**对应的 index.ts**：
```ts
import type { VariantProps } from "class-variance-authority"
import { cva } from "class-variance-authority"

export { default as Button } from "./Button.vue"

export const buttonVariants = cva("base classes...", {
  variants: {
    variant: { default: "...", destructive: "...", outline: "..." },
    size: { default: "...", sm: "...", lg: "...", icon: "..." },
  },
  defaultVariants: { variant: "default", size: "default" },
})

export type ButtonVariants = VariantProps<typeof buttonVariants>
```

**薄封装要点**：
- 必须 `import type { ButtonVariants } from "@/components/ui/button"` 复用类型
- 透传 `variant`/`size` 时用 `ButtonVariants["variant"]` 保持类型安全

### 模板 C：输入型（v-model）

**代表**：input, textarea

```vue
<script setup lang="ts">
import { useVModel } from "@vueuse/core"
import { cn } from "@/lib/utils"

const props = defineProps<{
  defaultValue?: string | number
  modelValue?: string | number
  class?: HTMLAttributes["class"]
}>()

const emits = defineEmits<{
  (e: "update:modelValue", payload: string | number): void
}>()

const modelValue = useVModel(props, "modelValue", emits, {
  passive: true,
  defaultValue: props.defaultValue,
})
</script>
```

**薄封装要点**：
- 用 `@vueuse/core` 的 `useVModel` 做双向绑定
- 如果有 reka-ui 版本的（如 NumberField），额外依赖 `reka-ui`

### 模板 D：多部件组合（Root + Sub-components）

**代表**：dialog (9 文件), select (11 文件), accordion (4 文件)

**Root 组件模式**（Dialog.vue）：
```vue
<script setup lang="ts">
import type { DialogRootEmits, DialogRootProps } from "reka-ui"
import { DialogRoot, useForwardPropsEmits } from "reka-ui"

const props = defineProps<DialogRootProps>()
const emits = defineEmits<DialogRootEmits>()
const forwarded = useForwardPropsEmits(props, emits)
</script>

<template>
  <DialogRoot v-slot="slotProps" data-slot="dialog" v-bind="forwarded">
    <slot v-bind="slotProps" />
  </DialogRoot>
</template>
```

**子组件模式**（DialogContent.vue）：
```vue
<script setup lang="ts">
import { reactiveOmit } from "@vueuse/core"
import { DialogContent, DialogPortal, useForwardPropsEmits } from "reka-ui"
import { cn } from "@/lib/utils"

defineOptions({ inheritAttrs: false })

const props = withDefaults(
  defineProps<DialogContentProps & { class?: HTMLAttributes["class"], showCloseButton?: boolean }>(),
  { showCloseButton: true }
)
const emits = defineEmits<DialogContentEmits>()
const delegatedProps = reactiveOmit(props, "class")
const forwarded = useForwardPropsEmits(delegatedProps, emits)
</script>

<template>
  <DialogPortal>
    <DialogOverlay />
    <DialogContent
      data-slot="dialog-content"
      v-bind="{ ...$attrs, ...forwarded }"
      :class="cn('bg-background ...', props.class)"
    >
      <slot />
    </DialogContent>
  </DialogPortal>
</template>
```

**关键模式**：
- `reactiveOmit(props, "class")` — 分离 class 避免传给原生 DOM
- `useForwardPropsEmits(props, emits)` — Reka-UI 的 props/emits 透传工具
- `v-bind="{ ...$attrs, ...forwarded }"` — 非 prop attrs 透传
- `defineOptions({ inheritAttrs: false })` — 阻止 attrs 自动继承到根元素
- `data-slot` 标注每个子组件角色，供 CSS/父组件定位
- `:data-state`, `:data-variant`, `:data-size` — CSS 状态钩子

### 模板 E：provide/inject 上下文（非 Reka-UI 提供）

**代表**：form（vee-validate）, sidebar

Form 组件通过 `provide(FORM_ITEM_INJECTION_KEY, id)` 建立父子链路：
```
FormField (vee-validate)
  └─ FormItem (provide id)
       ├─ FormLabel  (inject id → useFormField())
       ├─ FormControl (inject id)
       ├─ FormDescription (inject id)
       └─ FormMessage (inject id → vee-validate ErrorMessage)
```

**useFormField.ts**：
```ts
const fieldContext = inject(FieldContextKey)     // from vee-validate
const fieldItemContext = inject(FORM_ITEM_INJECTION_KEY) // from FormItem

return {
  id, name,
  formItemId: `${id}-form-item`,
  formDescriptionId: `${id}-form-item-description`,
  formMessageId: `${id}-form-item-message`,
  error,
  valid: computed(...),
  isDirty: computed(...),
  isTouched: computed(...),
}
```

**薄封装要点**：
- Form 组件的 provide/inject 链路不能断
- 薄封装时如果包裹 FormItem，必须透过 provide
- 不能自己定义新的 injection key（会打断链路）

### 模板 F：直接透传（zero logic）

**代表**：SelectGroup, SelectValue, SelectItemText, DialogTrigger

```vue
<script setup lang="ts">
import type { SelectGroupProps } from "reka-ui"
import { SelectGroup } from "reka-ui"

const props = defineProps<SelectGroupProps>()
</script>

<template>
  <SelectGroup data-slot="select-group" v-bind="props">
    <slot />
  </SelectGroup>
</template>
```

**用途**：只是给 Reka-UI 原语加 `data-slot`。

---

## 3. 类型导出清单

| 类型 | 来源 | 示例 |
|------|------|------|
| `XVariants` | `VariantProps<typeof xVariants>` | ButtonVariants, BadgeVariants, ToggleVariants |
| `XRootProps` | `reka-ui` | DialogRootProps, SelectRootProps |
| `XRootEmits` | `reka-ui` | DialogRootEmits, SelectRootEmits |
| `XContentProps` | `reka-ui` | DialogContentProps, SelectContentProps |
| `XContentEmits` | `reka-ui` | DialogContentEmits |
| `XTriggerProps` | `reka-ui` | DialogTriggerProps, SelectTriggerProps |
| `XItemProps` | `reka-ui` | SelectItemProps |
| `<slot> bindings` | Root 组件的 `v-slot` | `v-slot="{ open, close }"` |

### 薄封装类型复用策略

```ts
// ✅ 正确：直接 import shadcn 的类型
import type { ButtonVariants } from "@/components/ui/button"
import { Button } from "@/components/ui/button"

// ✅ 正确：透传 reka-ui 类型
import type { DialogRootProps, DialogRootEmits } from "reka-ui"

// ❌ 错误：自己重新定义 variant 枚举
// 会导致类型分歧，shadcn 更新 variant 时漏改
```

---

## 4. CSS 变量契约（Tokens）

shadcn-vue 组件依赖以下 CSS 自定义属性（在 `@theme` 块中定义）：

### 核心语义 Token（组件直接引用）

| Token | 用途 | 常见使用 |
|-------|------|---------|
| `--background` | 主背景色 | Card、Dialog Content、Popover、Sheet |
| `--foreground` | 主前景色 | 文本默认色 |
| `--primary` | 主色（按钮/链接） | Button variant=default、Badge |
| `--primary-foreground` | 主色上的文字 | Button 内部文字 |
| `--secondary` | 次要背景 | Button variant=secondary、Badge |
| `--secondary-foreground` | 次要前景 | 次要按钮文字 |
| `--muted` | 弱化背景 | Skeleton、进度条背景 |
| `--muted-foreground` | 弱化文字 | Label、Description、Placeholder |
| `--accent` | 强调背景 | Hover 状态、Dropdown Item hover |
| `--accent-foreground` | 强调前景 | Hover 文字 |
| `--destructive` | 错误/危险色 | Button variant=destructive、Form error |
| `--destructive-foreground` | 错误色前景 | Destructive 按钮文字 |
| `--border` | 边框色 | Card、Input、Select trigger |
| `--input` | 输入框背景 | Input、Select、Combobox |
| `--ring` | 聚焦环 | Focus-visible 状态 |
| `--popover` | 弹出层背景 | Popover、Select Content、Dropdown |
| `--popover-foreground` | 弹出层前景 | 弹出层文字 |
| `--card` | 卡片背景 | Card |
| `--card-foreground` | 卡片前景 | Card 内文字 |
| `--radius` | 默认圆角 | — |
| `--chart-1` ~ `--chart-5` | 图表色板 | Chart 组件 |

### data-* 属性钩子

| 属性 | 触发条件 |
|------|---------|
| `data-state="open"` | 弹出组件展开 |
| `data-state="closed"` | 弹出组件关闭 |
| `data-state="checked"` | Toggle/Checkbox 选中 |
| `data-state="active"` | Tabs/Navigation 激活 |
| `data-orientation="horizontal"` | Tabs 水平 |
| `data-orientation="vertical"` | Tabs 垂直 |
| `data-side="left/right/top/bottom"` | Popover/Sheet 弹出方向 |
| `data-disabled="true"` | 禁用状态 |
| `data-selected="true"` | 选中状态 |
| `data-slot="*"` | 组件部件标识 |

### Tailwind v4 自定义变体（来自 `shadcn-vue/tailwind.css`）

```css
data-open:bg-red-500      /* 等价于 [data-state="open"] */
data-closed:opacity-0      /* 等价于 [data-state="closed"] */
data-checked:border-primary
data-selected:bg-accent
data-disabled:opacity-50
data-active:font-semibold
data-horizontal:*          /* orientation */
data-vertical:*
```

**薄封装绝对不能**:
- 覆盖 `data-slot` 值（父组件/全局 CSS 依赖它选择元素）
- 删除组件根元素的 data-* 属性绑定
- 改变 CSS 变量名（组件内部硬编码了 `--primary` 等 token 名）

---

## 5. 组件粒度矩阵

### 单体（导出 2-3 个 export）

| 组件 | 导出 | 特殊依赖 |
|------|------|---------|
| card | Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter | 无 |
| alert | Alert, AlertTitle, AlertDescription | 无 |
| badge | Badge, badgeVariants, BadgeVariants | cva |
| button | Button, buttonVariants, ButtonVariants | cva |
| input | Input | @vueuse/core |
| textarea | Textarea | @vueuse/core |
| skeleton | Skeleton | 无 |
| spinner | Spinner | 无 |
| kbd | Kbd | 无 |
| separator | Separator | 无 |
| progress | Progress | reka-ui |
| label | Label | reka-ui |
| checkbox | Checkbox | reka-ui |
| switch | Switch | reka-ui |
| slider | Slider | reka-ui |
| toggle | Toggle, toggleVariants, ToggleVariants | cva |
| avatar | Avatar, AvatarImage, AvatarFallback | reka-ui |
| aspect-ratio | AspectRatio | reka-ui |
| empty | Empty | 无 |
| native-select | NativeSelect | reka-ui |

### 中度组合（4-10 个 export）

| 组件 | 子部件数 | 关键部件 |
|------|:---:|------|
| accordion | 4 | Accordion, AccordionItem, AccordionTrigger, AccordionContent |
| alert-dialog | 7 | AlertDialog, Trigger, Content, Header, Footer, Title, Description, Action |
| carousel | 4 | Carousel, CarouselContent, CarouselItem, CarouselPrevious, CarouselNext |
| collapsible | 2 | Collapsible, CollapsibleTrigger, CollapsibleContent |
| drawer | 7 | Drawer, Trigger, Portal, Close, Content, Header, Footer, Title, Description |
| navigation-menu | 7 | NavigationMenu, List, Item, Trigger, Content, Link, Viewport, Indicator |
| pagination | 5 | Pagination, PaginationList, PaginationListItem, PaginationEllipsis, PaginationFirst, PaginationPrev, PaginationNext, PaginationLast |
| pin-input | 2 | PinInput, PinInputGroup, PinInputInput |
| radio-group | 2 | RadioGroup, RadioGroupItem |
| resizable | 2 | ResizablePanelGroup, ResizablePanel, ResizableHandle |
| scroll-area | 4 | ScrollArea, ScrollBar, Thumb, Corner |
| sheet | 8 | Sheet, Trigger, Close, Content, Header, Footer, Title, Description |
| sonner | 1 | Sonner (Toaster) |
| stepper | 4 | Stepper, StepperItem, StepperTrigger, StepperIndicator, StepperTitle, StepperDescription, StepperSeparator |
| tabs | 4 | Tabs, TabsList, TabsTrigger, TabsContent |
| toggle-group | 2 | ToggleGroup, ToggleGroupItem |
| tooltip | 5 | Tooltip, TooltipProvider, TooltipTrigger, TooltipContent |

### 重度组合（10+ 个 export，有自定义逻辑）

| 组件 | 子部件数 | 关键特征 |
|------|:---:|------|
| **select** | 11 | Select, Trigger, Value, Content, Group, Label, Item, ItemText, Separator, ScrollUp/DownButton |
| **dialog** | 9 | Dialog, Trigger, Close, Content, ScrollContent, Overlay, Header, Footer, Title, Description |
| **combobox** | 整合模式 | 组合 command + popover + input，内部渲染逻辑 |
| **command** | 8 | Command, Input, List, Empty, Group, Item, Shortcut, Separator, Dialog |
| **form** | 5 + 2 injection | FormItem, FormLabel, FormControl, FormDescription, FormMessage + useFormField + injectionKeys |
| **sidebar** | 10+ | Sidebar, Provider, Trigger, Content, Header, Footer, Menu, MenuButton, MenuAction, Group, GroupLabel, GroupContent, GroupAction, Input, Separator |
| **input-group** | 3+ | InputGroup, InputGroupAddon, InputGroupButton, InputGroupText |
| **chart** | 2+ charts | ChartContainer, ChartTooltipContent, + 各种 config |
| **calendar** | 复杂 | Calendar, + formatter, + header/footer |
| **tags-input** | 4 | TagsInput, TagsInputItem, TagsInputItemText, TagsInputItemDelete |
| **breadcrumb** | 6 | Breadcrumb, List, Item, Link, Page, Separator, Ellipsis |
| **context-menu** | 11 | 同 dropdown-menu 结构 |
| **dropdown-menu** | 11 | Menu, Trigger, Content, Group, Item, CheckboxItem, RadioItem, Sub, SubTrigger, SubContent, Separator, Shortcut, Label |
| **menubar** | 10+ | Menubar, Menu, Trigger, Content, Item, Sub, SubTrigger, SubContent, Separator, Shortcut, CheckboxItem, RadioItem, Group |
| **table** | 5 | Table, Header, Body, Footer, Row, Head, Cell, Caption |

---

## 6. 薄封装策略 — 按复杂度分档

### L0：零封装（直接用）

直接 import shadcn 组件，不包装。适用于不需要定制的项目：
```vue
import { Button } from "@/components/ui/button"
```

### L1：类型透传薄封装

```vue
<script setup lang="ts">
import type { ButtonVariants } from "@/components/ui/button"
import { Button } from "@/components/ui/button"

defineProps<{
  variant?: ButtonVariants["variant"]
  size?: ButtonVariants["size"]
  disabled?: boolean
  loading?: boolean
}>()

defineEmits<{
  click: [e: MouseEvent]
}>()
</script>

<template>
  <Button
    :variant="variant"
    :size="size"
    :disabled="disabled || loading"
    @click="$emit('click', $event)"
  >
    <slot v-if="!loading" />
    <Spinner v-else class="mr-2" />
    <slot v-if="loading" />
  </Button>
</template>
```

> **规则**：不重新定义 variant/size 枚举，只用 `XVariants["variant"]` 引用。

### L2：v-bind="$attrs" 全透传

适用于纯样式封装：
```vue
<template>
  <Button v-bind="$attrs" class="my-custom-class">
    <slot />
  </Button>
</template>
```

> ⚠️ 注意：需要 `defineOptions({ inheritAttrs: false })`

### L3：组合体封装（多部件聚合成一个）

```vue
<!-- ZFormField = FormField + FormItem + FormLabel + FormControl + FormMessage 的快捷组合 -->
<template>
  <FormField v-slot="field" :name="name">
    <FormItem>
      <FormLabel>{{ label }}</FormLabel>
      <FormControl>
        <slot :field="field" />
      </FormControl>
      <FormMessage />
    </FormItem>
  </FormField>
</template>
```

> **规则**：不重新定义 injection key，不打断 provide/inject 链路。

### ⚠️ 禁止的做法

| 禁止 | 原因 |
|------|------|
| 手动复制 .vue 文件 | CSS 动画/定位/过渡丢失 |
| 重新定义 variant 枚举 | shadcn 更新时不联动，类型分歧 |
| 覆盖 `data-slot` 值 | 父组件 CSS 选择器失效 |
| 删除 `data-state/data-variant` 绑定 | 动态样式失效 |
| 创建新的 injection key 替代 shadcn 的 | provide/inject 链路断开 |
| 用 `v-if` 包装 Root 组件 | Reka-UI 内部状态机需要 v-slot 的 slotProps |
| 缓存 Primitive 的 `as` prop | as-child/as 机制依赖动态性 |

---

## 7. 构建与类型

- **构建工具**：tsdown（基于 esbuild 的 tsup 替代）
- **类型检查**：`vue-tsc --noEmit`
- **包入口**：`bin: "./dist/index.js"`，CLI 直接运行
- **子路径导出**：`./mcp`, `./registry`, `./schema`, `./utils`, `./icons`, `./preset`, `./tailwind.css`

项目使用 shadcn 组件后：
```bash
npx vue-tsc --build  # 每次修改后必跑
```

---

## 8. 版本锁定建议

```
shadcn-vue: 2.7.4
reka-ui: catalog:（通过 pnpm-workspace catalog 锁定）
class-variance-authority: ^0.7.0
tailwindcss: ^4.1.x
vue: ^3.5
@vueuse/core: ^13.x
```
