# 前端项目通用规则

- **Tailwind 语义类名**：布局容器（页面、section、wrapper）必须有语义化 class 名方便定位；shadcn 组件本身不需要额外类名
  - 需要：`<div class="feature-list p-4">`、`<div class="page-wrapper">`、`<section class="sidebar">`
  - 不需要：`<Button class="my-btn">`、`<Card class="my-card">`（组件标签已可定位）
- **桌面 App 布局**：App 层 100vw/100vh flex-col，titlebar 普通 flex 子元素（非 fixed），content flex-1，路由在 content 内
