# shadcn-vue CLI 内部机制 — init 与 apply

> 源码：`D:\hxy\github\shadcn-vue\packages\cli\src\commands\init.ts` (938行) / `apply.ts` (336行)
> 
> 版本：v2.7.4

---

## 1. init 完整流程

### 1.1 阶段一：预设解析

```
npx shadcn-vue@latest init --preset a2QcktPc --yes
                          ├── preset 参数有 5 种形式
```

| 预设形式 | 示例 | 解析方式 |
|---------|------|---------|
| 预设码（base62） | `a2QcktPc` | `decodePreset()` 位解码 → 风格/主题/字体/图标/基色/圆角/图表色 |
| URL | `https://shadcn-vue.com/create?...` | 直接用作 init URL |
| 命名预设名 | `nova` `vega` `maia` `lyra` `mira` `luma` `sera` | `DEFAULT_PRESETS` 查找，内部有预设七种风格 |
| `true`（无值） | `--preset` | 交互选择：展示 7 种风格，或选 Custom 打开浏览器到 `/create` |
| `false` | 不传 | 使用 `--defaults`（nova + geist-sans + nuxt + reka） |

### 1.2 PresetCode 编码结构

base62 字符串，前缀 `"a"` 表示 v1。39 bits 完整编码 11 个设计参数：

```
menuColor (3bit) → menuAccent (2bit) → radius (3bit) →
font (5bit, 12种) → fontHeading (5bit, 13种) → iconLibrary (3bit, 5种) →
theme (5bit, 24种) → baseColor (3bit, 7种) → style (3bit, 7种) →
base (2bit, 仅reka) → chartColor (5bit, 24种)
```

> 兼容铁律：永不对值列表重排 — 只追加。新字段默认值必须在 index 0。总位数 < 53。

### 1.3 阶段二：获取 registry 配置

```
preset → resolveInitUrl() → https://shadcn-vue.com/init?base=reka&style=nova&...
                           └── GET 请求获取 registry:base item
                              └── 提取 config 对象（合并到 components.json）
```

`config` 对象包含：base、style、font、fontHeading、iconLibrary、baseColor、theme、radius、rtl、pointer、registries。

### 1.4 阶段三：预检 `preFlightInit()`

```
检查项：
  ✅ package.json 存在
  ✅ components.json 不存在（或 --force）
  ✅ 框架检验：Nuxt/Vite/Astro/Laravel
  ✅ Tailwind CSS v3/v4 配置存在
  ✅ tsconfig import alias 配置正确
```

### 1.5 阶段四：新项目 vs 已有项目

```
项目目录为空？
  ├── YES → createProject()
  │         ├── giget 下载模板（github:unovue/shadcn-vue/templates/<框架>#dev）
  │         ├── git init
  │         └── 安装依赖（检测包管理器）
  └── NO  → 交互式配置向导
            ├── 已有 components.json → promptForMinimalConfig()
            └── 无 components.json → promptForConfig()
              选项：TypeScript、框架、base、style、iconLibrary、font、baseColor、
                    CSS 文件路径、CSS 变量、tailwind prefix、组件别名、utils 别名
```

### 1.6 阶段五：写入与安装

```
1. 写入 components.json（key 配置）

2. 组装 components 列表：
   baseStyle=true → ["style-index", ...preset组件]
   baseStyle=false → [...preset组件]

3. addComponents() 按顺序执行 6 步：
   ┌─────────────────────────────────────────────┐
   │ ① updateTailwindConfig()  → tailwind 配置    │
   │ ② updateCssVars()         → CSS 变量注入     │
   │ ③ updateCss()             → 基础 CSS 写入    │
   │ ④ updateEnvVars()         → .env.local       │
   │ ⑤ updateDependencies()    → package.json     │
   │ ⑥ updateFiles()           → .vue 组件文件    │
   └─────────────────────────────────────────────┘
```

### 1.7 init 期间修改的文件汇总

| 文件 | 操作 | 说明 |
|------|:--:|------|
| `components.json` | 创建 | 含 base/style/font/iconLibrary/tailwind/aliases/rtl/registries |
| `package.json` | 更新 | 安装 reka-ui、class-variance-authority、lucide-vue 等 |
| `assets/css/tailwind.css` | 创建/覆盖 | 含 `@import "shadcn-vue/tailwind.css"` + CSS 变量 |
| `tailwind.config.*` | 更新 | 添加 plugin、content paths |
| `components/ui/*.vue` | 创建 | 所有组件文件 |
| `lib/utils.ts` | 创建 | `cn()` 工具函数 |
| `.env.local` | 更新 | registry 认证 token |

---

## 2. apply 完整流程

### 2.1 与 init 的本质区别

**apply 是对已有项目的"换皮"操作。** 保留组件库基础（reka）、保留 RTL 设置、保留所有已安装组件，只替换视觉层（CSS 变量、字体、图标库、风格）。

### 2.2 执行流程

```
npx shadcn-vue@latest apply --preset a2QcktPc --yes

1. preFlightApply() — 轻量预检：
   ✅ package.json 必须存在
   ✅ components.json 必须存在且有效
   ❌ 不检验框架/tailwind/alias（init 时已验证）

2. resolveApplyInitUrl():
   - 强制 base = 当前项目 base（从 components.json 读）
   - 强制 rtl  = 当前项目 rtl
   - 其他参数（style/font/theme/iconLibrary）来自预设

3. getProjectComponents() — 列出所有已安装 UI 组件

4. 用户确认：
   ⚠️ "Applying a new preset will overwrite existing
      UI components, fonts, and CSS variables"
   显示所有将被重新安装的组件名

5. withFileCopyBackup() 事务包裹 runInit():
   ├── 备份 components.json → components.json.apply.bak
   ├── 注册 process.on('exit', restoreOnExit) 回滚监听器
   ├── 执行 runInit({
   │     skipPreflight: true,     # 跳过全部预检
   │     reinstall: true,         # 标记重装
   │     force: false,
   │     base: currentBase,       # 强制保持当前 base
   │     rtl: currentRtl,         # 强制保持当前 rtl
   │     components: [initUrl, ...全部已有组件]  # 预设 + 全量重装
   │   })
   ├── 成功 → 移除监听器，删除备份
   └── 失败 → exit listener 恢复 components.json.apply.bak
```

### 2.3 为什么用 exit listener 而不是 try/catch？

`addComponents()` 内部出错时调用 `handleError()`，后者执行 `process.exit(1)`。`process.exit()` 不触发 try/catch，但会触发 `process.on('exit')` 监听器。apply 用这个监听器实现 **原子性保证**：失败时完整恢复 `components.json`。

### 2.4 apply vs init 对照表

| | init | apply |
|---|------|-------|
| **前置条件** | 无严格要求 | 必须有 package.json + components.json |
| **预检** | 全量（框架/tailwind/alias） | 轻量（仅两项） |
| **base 处理** | 用户可选 | 强制继承当前项目 |
| **rtl 处理** | 用户可选 | 强制继承当前项目 |
| **组件处理** | 仅预设中的组件 | 预设 + 重新安装全部已有组件 |
| **回滚** | 无 | `withFileCopyBackup()` exit listener |
| **跳过预检** | 不跳过 | `skipPreflight: true` |
| **交互提示** | 完整配置向导 | 仅确认 + 组件列表 |

---

## 3. add 流程（补充）

```bash
npx shadcn-vue@latest add button dialog card
```

```
1. 解析组件名 → resolveTree() 构建依赖树
2. 下载每个组件的 registry JSON
3. 写入文件 → .vue 到 components/ui/
4. 更新依赖 → package.json（如果组件有额外 npm 依赖）
5. 合并 CSS 变量（增量添加，不覆盖已有 token）
```

**与 init/apply 关键区别**：add 只做第⑥步 + 增量依赖更新，**不覆盖** CSS 变量、tailwind 配置、或 components.json 结构。

---

## 4. 迁移命令（migrate）

v2.7.x 支持从旧版迁移：
```bash
npx shadcn-vue@latest migrate --preset a2QcktPc --yes
```
内部调用 apply 流程，但额外的：更新 RTL 配置、更新 pointer 配置、清理旧文件。
