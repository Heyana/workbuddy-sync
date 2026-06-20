# shadcn-vue MCP Server 深度分析

> 源码位置：`D:\hxy\github\shadcn-vue`（`unovue/shadcn-vue`, v2.7.4, MIT）
> 
> MCP 核心代码：`packages/cli/src/mcp/index.ts`（~465 行）

---

## 1. 架构概览

```
npx shadcn-vue@latest mcp       # 启动 MCP server（stdio 传输）
npx shadcn-vue@latest mcp init  # 生成编辑器配置文件
```

**传输层**：stdio（标准 MCP 协议），所有通信通过 stdin/stdout JSON-RPC。

**依赖**：
- `@modelcontextprotocol/sdk` ^1.24.3 — 核心 MCP SDK
- `zod` + `zod-to-json-schema` — 参数校验与工具 schema 生成
- `commander` ^14.0.2 — CLI 命令解析
- `fuzzysort` — 模糊搜索（registry 内搜索组件）
- `@dotenvx/dotenvx` — `.env.local` 环境变量加载（私有 registry 认证）

---

## 2. 提供的 7 个 MCP 工具

| 工具名 | 输入 | 功能 | 安全关注 |
|--------|------|------|---------|
| `get_project_registries` | 无 | 读取 `components.json` 返回 registry 列表 | 只读本地文件 |
| `list_items_in_registries` | registries[], limit?, offset? | 列出 registry 的全部组件 | fetch 外部 registry URL |
| `search_items_in_registries` | registries[], query, limit?, offset? | 模糊搜索组件 | fetch + fuzzysort |
| `view_items_in_registries` | items[] | 查看组件详情（含文件内容） | fetch 外部资源 |
| `get_item_examples_from_registries` | registries[], query | 搜索示例/demo 源码 | fetch, 返回含代码 |
| `get_add_command_for_items` | items[] | 返回 npx 安装命令 | 纯本地计算，无网络 |
| `get_audit_checklist` | 无 | 返回组件验证清单 | 纯静态文本 |

### 工具工作流

```
get_project_registries → list_items / search_items
                       → view_items（含文件内容、依赖、示例代码）
                       → get_add_command_for_items（生成 CLI 命令）
```

### 审计清单内容

`get_audit_checklist` 返回的验证项：
- import 路径、组件依赖（dependencies/devDependencies）
- ESLint 检查、TypeScript 类型检查
- Tailwind CSS 配置验证

---

## 3. Registry 机制

### 内置 Registry

`@shadcn` — 始终可用，无需配置，指向 shadcn-vue 官方组件仓库。

### 自定义 Registry（`components.json`）

```json
{
  "registries": {
    "@acme": "https://acme.com/r/{name}.json",
    "@private": {
      "url": "https://private.com/r/{name}.json",
      "headers": {
        "Authorization": "Bearer ${REGISTRY_TOKEN}"
      }
    }
  }
}
```

- 命名空间必须以 `@` 开头
- URL 必须含 `{name}` 占位符
- `${VAR}` 环境变量引用：从 `.env.local` 或系统环境变量解析
- 私有 registry 通过 `headers` 实现认证

### 数据获取

- 使用 `ofetch` 发起 HTTP 请求到 registry URL
- 响应数据用 zod schema 校验（`registryItemSchema`、`searchResultsSchema`）
- 支持分页（offset/limit），默认 limit=10

---

## 4. 支持的 MCP 客户端

| 客户端 | 配置文件 | `init` 自动生成 |
|--------|---------|:---:|
| Claude Code | `.mcp.json` | ✅ |
| Cursor | `.cursor/mcp.json` | ✅ |
| VS Code (Copilot) | `.vscode/mcp.json` | ✅ |
| Opencode | `opencode.json` | ✅ |
| Codex | `~/.codex/config.toml` | ❌ 手动 |

所有客户端的 MCP 配置格式相同：
```json
{
  "mcpServers": {
    "shadcn": {
      "command": "npx",
      "args": ["shadcn-vue@latest", "mcp"]
    }
  }
}
```
（Opencode 略有不同，`"type": "local"`，command 是数组格式）

---

## 5. 安全分析

### ✅ 安全点

- **stdio 传输**：不监听网络端口，无远程攻击面
- **输入校验**：所有工具输入通过 zod schema 严格校验
- **环境变量注入**：`${VAR}` 语法由 `@dotenvx/dotenvx` 安全解析，不会执行任意命令
- **无持久化状态**：MCP 服务器无状态，每次请求独立
- **审计清单纯静态**：`get_audit_checklist` 仅返回硬编码文本，无文件系统操作
- **安装命令纯计算**：`get_add_command_for_items` 仅拼接本地命令字符串，不执行

### ⚠️ 需注意

- **Registry URL 无白名单**：`components.json` 中配置的任何 registry URL 都会被请求。AI 可能通过 `list_items_in_registries` 等工具触发外部 HTTP 请求到任意域名
- **文件内容返回**：`view_items_in_registries` 和 `get_item_examples_from_registries` 会返回 registry 返回的完整文件内容，如果 registry 返回恶意代码片段，AI 可能被误导
- **`.env.local` 读取**：自动加载项目根目录的 `.env.local`，如果项目被污染，可能暴露 token

### 评分

| 维度 | 评分 | 说明 |
|------|:---:|------|
| 攻击面 | 🟢 低 | stdio 传输，无网络监听 |
| 输入安全 | 🟢 低 | zod schema 校验 |
| 数据外发 | 🟡 中 | 可触发 HTTP 请求到 registry（由 `components.json` 控制） |
| 代码执行 | 🟢 低 | 无 eval/exec，仅返回命令字符串 |
| 依赖安全 | 🟢 低 | 核心依赖成熟，无高危 CVE 记录 |
| 综合风险 | 🟢 **低** | 可安全接入 WorkBuddy |

---

## 6. 与 WorkBuddy 集成方案

### 配置方式

添加到 `~/.workbuddy/mcp.json`：
```json
{
  "mcpServers": {
    "shadcn-vue": {
      "command": "npx",
      "args": ["shadcn-vue@latest", "mcp"]
    }
  }
}
```

### 前置条件

- 目标项目必须有 `components.json`（否则 `get_project_registries` 报错）
- Node.js >= 18
- 项目需安装 shadcn-vue 依赖（`reka-ui` 等）

### 适用场景

- Vue3/Nuxt 项目需要快速添加 shadcn 组件
- 通过 AI 对话直接搜索和安装组件，无需手动记忆 CLI 命令
- 浏览 registry 中的可用组件和示例

---

## 7. 项目结构关键路径

```
packages/cli/
├── src/
│   ├── index.ts           # CLI 入口，注册 mcp/mcp init 命令
│   ├── mcp/
│   │   ├── index.ts       # MCP server 核心（工具注册 + stdio 传输）
│   │   └── utils.ts       # 格式化函数（搜索结果、组件详情、示例）
│   ├── commands/
│   │   ├── mcp.ts         # `mcp` 命令：启动 stdio server
│   │   └── registry/mcp.ts # `mcp init` 命令：生成编辑器配置
│   ├── registry/
│   │   └── api.ts         # Registry HTTP 请求（ofetch）
│   └── schema/            # Zod schema 定义
├── skills/shadcn-vue/
│   └── mcp.md             # AI skill 文件（用于 Claude Code 等）
└── package.json           # 依赖清单
```

---

## 8. 维护信息

- **仓库**：`https://github.com/unovue/shadcn-vue`
- **本地克隆**：`D:\hxy\github\shadcn-vue`
- **当前版本**：2.7.4
- **分支**：dev（开发主分支）
- **包管理器**：pnpm 10.25.0
- **构建**：`pnpm build:cli`（tsdown 打包）
- **发布**：`pnpm pub:release`（build + npm publish）
- **协议**：MIT
