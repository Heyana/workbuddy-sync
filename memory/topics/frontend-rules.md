# 前端项目通用规则

- **Tailwind 语义类名**：布局容器（页面、section、wrapper）必须有语义化 class 名方便定位；shadcn 组件本身不需要额外类名
  - 需要：`<div class="feature-list p-4">`、`<div class="page-wrapper">`、`<section class="sidebar">`
  - 不需要：`<Button class="my-btn">`、`<Card class="my-card">`（组件标签已可定位）
- **桌面 App 布局**：App 层 100vw/100vh flex-col，titlebar 普通 flex 子元素（非 fixed），content flex-1，路由在 content 内

## 🔴 重构策略（血泪教训）

### 核心原则：逐模块渐进迁移，禁止全量替换

- **全量重构 = 自杀**：一次性替换所有页面/组件/功能，每个差距项都可能引入数据流断裂，排查效率指数级下降
- **正确做法**：每次只迁移一个模块，迁移完立即验证运行通过，再继续下一个
- **迁移顺序**：基础层（platform/router/store）→ 独立页面（设置→标签→下载）→ 核心页面（资产列表→预览系统）

### 迁移前必须准备

- **差距分析文档**：逐文件对比新旧代码的功能/API/事件/样式，列出每个差距项的原始行号
- **可运行的 baseline**：确保新老代码都独立可运行，有回退路径
- **环境可用性检查清单**：`prompt()` 不可用、`-webkit-app-region` 拖拽、`ContextMenu` 需挂载到 App 等平台陷阱

### 架构决策：基础设施先行

- **Platform 抽象层**：接口 → Electron 实现 → Web 降级，三文件分离，先建好再写页面
- **Composables 模块单例**：右键菜单/键盘/确认弹窗等全局交互，用 module-level reactive state 而非 prop drilling
- **向后兼容的持久化**：`load()` 必须 `{ ...defaults(), ...parsed }`，新增字段由 defaults 兜底，否则旧数据 undefined 崩溃

### 验证节奏

- 每迁移一个页面 → `yarn dev` 启动 → 验证该页面 CRUD 和交互 → 截图留底 → 再继续下一个
- 不要攒多个模块一起测，问题定位成本指数的
