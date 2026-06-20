# shadcn-vue 使用规范

> 参考：https://www.shadcn-vue.com/

## 初始化

```bash
# 安装依赖
pnpm add tailwindcss @tailwindcss/vite
# 初始化 shadcn-vue
pnpm dlx shadcn-vue@latest init
```

- CSS 入口：`@import "tailwindcss";`（Tailwind v4）
- vite.config.ts：`plugins: [vue(), tailwindcss()]` + `resolve.alias: { '@': path.resolve(__dirname, './src') }`
- tsconfig：`compilerOptions.baseUrl: "."`, `paths: { "@/*": ["./src/*"] }`

## 添加组件

```bash
pnpm dlx shadcn-vue@latest add button
pnpm dlx shadcn-vue@latest add card dialog dropdown-menu
```

- **必须用 CLI 添加**，禁止手动复制组件文件
- 组件文件生成在 `src/components/ui/<name>.vue`

## 导入与使用

```vue
<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardContent } from '@/components/ui/card'
</script>

<template>
  <Button variant="outline" size="sm">Click</Button>
</template>
```

- **命名导出**：`import { Button } from '@/components/ui/button'`（非 default import）
- 子组件从同一文件导出：`import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'`
- 路径别名固定为 `@/components/ui/`

## 图标

```vue
import { ArrowUpIcon, GitBranchIcon } from '@lucide/vue'
```

- 使用 `@lucide/vue`（Vue 版 Lucide），非 `lucide-vue-next`
- 图标名 PascalCase，作为 Vue 组件直接放模板

## 常用 Props

| Prop | 值 |
|------|-----|
| `variant` | `"default"` / `"outline"` / `"secondary"` / `"ghost"` / `"destructive"` / `"link"` |
| `size` | `"default"` / `"sm"` / `"lg"` / `"icon"` / `"icon-sm"` / `"icon-lg"` |
| `as-child` | `boolean`：让子元素继承按钮样式（如 `<a>` 变按钮外观） |
| `disabled` | `boolean` |

## 禁止事项

- ❌ 不要手动从 GitHub 复制 `.vue` 组件文件到项目
- ❌ 不要用 default import：`import Button from ...`（shadcn-vue 是命名导出）
- ❌ 不要用错误的图标库（如 `lucide-vue-next`、`lucide-vue` 的 default import 等）
- ❌ 组件 class 不要额外加自定义类名定位（`<Button class="my-btn">">），组件标签本身已可定位；布局容器才需要语义化 class

## 常见坑

### CSS 无样式
- `shadcn-vue init` 生成的 CSS 文件必须在 `main.ts` 中显式 import，否则 Tailwind 不会注入页面
- CSS @import 路径是标准写法无需修改：`@import "tw-animate-css"` 和 `@import "shadcn-vue/tailwind.css"` 通过 exports 的 style 字段映射到实际文件
- 不要给这些路径加 `/dist/` 前缀，会破坏 exports 解析
