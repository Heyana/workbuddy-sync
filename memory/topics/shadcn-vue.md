# shadcn-vue 使用规范

> 血泪教训：绝对不要手动复制 shadcn 组件文件，必须用 CLI。否则 CSS（动画/定位/过渡）全部丢失。
> 
> 📡 MCP Server 分析见：[shadcn-vue-mcp.md](shadcn-vue-mcp.md) — 源码审查、安全评估、集成方案

## 核心命令

### 初始化
```bash
# 新建项目（带预设）
npx shadcn-vue@latest init --preset a2QcktPc --yes

# 已有项目更新预设（覆盖 CSS + 组件）
npx shadcn-vue@latest apply --preset a2QcktPc --yes
```

### 组件
```bash
# 添加组件（自动复制 .vue + 注入 CSS）
npx shadcn-vue@latest add button
npx shadcn-vue@latest add button badge switch checkbox ...  # 批量
```

## 预设码
- 格式：base62 编码的配置串（如 `a2QcktPc`）
- 来源：shadcn-vue.com 主题配置器
- **禁止手动解码、修改、或尝试 fetch**
- 直接传给 CLI 的 `--preset` 参数
- 编码内容：style (reka-nova)、baseColor (neutral)、font (Inter)、iconLibrary (lucide)、radius 等

## CSS 结构

### 必须的三行 import（main.css 顶部）
```css
@import "tailwindcss";
@import "tw-animate-css";
@import "shadcn-vue/tailwind.css";   /* 👈 核心：所有组件的样式都在这 */
```

### shadcn-vue/tailwind.css 提供
- 所有 shadcn 组件的定位（如 sonner 的 fixed bottom-right）
- 动画与过渡（enter/exit animations）
- data-attribute 选择器（`data-state="open"` 等）
- dark 模式样式

### CSS 变量
- Tailwind v4 使用 oklch 色彩空间
- shadcn 使用 `--background`、`--foreground`、`--primary` 等语义 token
- 组件通过 `var(--border)`、`var(--popover)` 等引用全局 token

## vue-sonner (Toast)

### 坑点
- vue-sonner 用 Teleport 渲染到 `<body>`，没有自带 CSS 的话 toast 就是裸的
- shadcn CLI `add sonner` 只生成 Sonner.vue 组件 + CSS 变量，**不会自动注入定位 CSS**
- 需要手动 `import "vue-sonner/style.css"` 获取自带动画

### 正确用法
```ts
// main.ts
import "vue-sonner/style.css"   // 动画 + 定位
```
```vue
<!-- App.vue -->
<Toaster />   <!-- 必须挂载，Sonner 内部 Teleport 到 body -->
```

## Z 组件封装

### 原则：薄封装
- 直接使用 shadcn 组件的类型（如 `ButtonVariants`）
- 只包装必要的 props，其余透传
- 不要重新定义 variant/size 枚举（shadcn 已有）

### 示例：ZButton
```vue
<script setup lang="ts">
import type { ButtonVariants } from "@/components/ui/button"
import { Button } from "@/components/ui/button"

defineProps<{
  variant?: ButtonVariants["variant"]
  size?: ButtonVariants["size"]
  disabled?: boolean
}>()
</script>
```

## 构建验证
```bash
npx vue-tsc --build    # 每次改源码后必跑
```
