# 项目结构规范

**核心原则：文件短小精悍，命名分层清晰，单个文件不超 200 行。**

## 前端 (Vue/React/TSX)
```
src/
├── pages/          # 路由页面组件（一个路由一个文件）
├── views/          # 视图片段（页面内嵌的子视图）
├── components/     # 可复用 UI 组件
│   ├── ui/         # shadcn 等基础组件
│   └── controls/   # 自定义控件（TitleBar 等非 shadcn 组件）
├── composables/    # Hooks / 组合式函数
├── stores/         # Pinia/Vuex 状态管理
├── api/            # API 请求层（按模块拆分）
│   └── modules/
├── router/         # 路由配置
├── utils/          # 纯工具函数
├── lib/            # 共享库（cn, constants 等）
├── types/          # TypeScript 类型定义
├── styles/         # 全局样式
└── App.tsx         # 根组件（仅布局 + RouterView，不入业务逻辑）
```

## 后端 (Go)
```
├── handlers/       # 请求处理器（薄层，仅解析+调用 service）
├── services/       # 业务逻辑
├── models/         # 数据模型
├── middleware/     # 中间件
├── utils/          # 工具函数
└── main.go         # 入口（初始化 + 注册路由）
```

## 通用规则
- **单文件长度**：尽量保持在 200-300 行内，职责单一；明显超长的拆
- **分层边界**：pages 不直接调 api，经 composables/stores；handlers 不写业务逻辑，调 services
  - view 层只调 store/composable，不直接 import platform 或 HTTP client
  - store 内部调 platform.db.xxx 或 api 模块
  - 简单系统能力（窗口/剪贴板/主题）放 composable 封装
  - 好处：换后端只需改 store 内部实现，view 代码不动
- **命名**：kebab-case 文件，PascalCase 组件，camelCase 函数
