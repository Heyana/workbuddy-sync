# Flutter 布局知识库

> Wind + shadcn_flutter 布局踩坑与最佳实践。每次遇到布局报错、样式不生效、组件组合问题，立刻更新。
> 保持精炼——只记结论和关键约束，不记推导过程。

---

## 铁律

- 技术栈：shadcn_flutter + fluttersdk_wind (^1.1.0) + LucideIcons
- ❌ **禁止** material/forui（main.dart 例外）
- 页面 import：shadcn_flutter + fluttersdk_wind + my-wind/div，不 import 其他 UI 库
- shadcn_flutter import 需 `hide Scaffold, NavigationBar, ThemeMode`

---

## Wind 布局核心规则

### WDiv + className（首选布局方式）

```
WDiv(className: 'flex flex-col gap-4 p-4', children: [
  WDiv(className: 'flex-1', children: [...]),
  WDiv(className: 'h-12', children: [...]),
])
```

- ✅ 用 WDiv + Tailwind className，不用 Flutter 原生 Column/Row
- 原因：Wind Column/Row 被 `WindFlexOverflowScope` 包裹，原生 FlexParentData 不兼容

### flex-1 陷阱

- ✅ `WDiv(className: 'flex-1', children: [...])` 可行
- ❌ 嵌套 flex-1：内部 `Expanded` > `Expanded` 冲突 → `Incorrect use of ParentDataWidget`
- 解决：嵌套场景用固定高度或 Stack 替代

### Spacer 替代

- ❌ 禁止 Flutter `Spacer()`
- ✅ 替换为：`WDiv(className: 'flex-1')`

### 可滚动页面（scrollPrimary 陷阱）

- ❌ **`WDiv(className: 'col f', scrollPrimary: true)` 会炸**：`scrollPrimary` 生成 `SingleChildScrollView`，而 `f`/`flex-1` 生成 `Expanded`/`Flexible`，Expanded 不能在 ScrollView 中 → `Incorrect use of ParentDataWidget` + overflow
- ❌ **`WDiv(className: 'col', scrollPrimary: true)` 子内容超出也会 overflow**：scrollPrimary 的 ScrollView 给子 Column 有限高度约束，内容超了就溢出
- ✅ **推荐模式**：原生 `SingleChildScrollView` 包 `WDiv`，ScrollView 给无限高度约束，不会 overflow：
  ```dart
  SingleChildScrollView(
    child: WDiv(className: 'col gap-6 p-6', children: [...]),
  )
  ```
- **教训**：scroll 页面只用 `col` 不用 `col f`；要滚动就直接用原生 `SingleChildScrollView` 替代 `scrollPrimary: true`

### 自定 alias `f` 在 Row 中炸

- ❌ **`WDiv(className: 'f')` 放在 `WDiv(className: 'row')` 内会 `BoxConstraints forces an infinite width`**
- **根因**：若 `f` alias 定义为 `w-full h-full`，`w-full` 生成 `SizedBox(width: double.infinity)`；Row 给非 flex 子 loose 宽度约束（maxWidth=Infinity），两者叠加出 `minWidth=Infinity` 非法约束
- ✅ **Row 内要用 flex 撑满必须用 `flex-1`**（生成 `Flexible`，走 Row 正常布局路线），不能用 `f`
- ⚠️ 检查 `wind_theme.dart` 里自定 alias 的实际展开值，`w-full`/`h-full` 类的 alias 不能用在 Row/Col 的非 flex 子中

### 页面背景色

- ❌ **shadcn `Scaffold` 不要设 `backgroundColor: Colors.transparent`**：Wind 的 `toThemeData()` 设 `canvasColor: Colors.transparent`，Scaffold 透明后一路透到 Flutter canvas 默认黑色
- ✅ **Scaffold 不设 backgroundColor**，走默认 `theme.colorScheme.background`（light: 浅色, dark: 深色）
- ✅ 每个页面可包一层 shadcn `Scaffold`，自动拿到正确的背景色（参考 test_wind_1_1 做法）

### Stack vs WDiv relative

- ❌ `WDiv(className: 'relative')` **不能让 Positioned 工作**——Wind 的 relative 是 CSS 语义，不影响 Flutter 布局
- ✅ 浮动元素必须用 `Stack`：
  ```dart
  Stack(children: [
    Positioned.fill(child: 主内容),
    Positioned(bottom: 0, right: 0, child: 浮动按钮),
  ])
  ```
- ⚠️ Stack 内部用 `Expanded` / `Positioned.fill`（不能用 WDiv 替代 flex-1）

---

## 样式细节

| 项目 | 规则 |
|------|------|
| 动态颜色 | `WText` 用 `foregroundColor:`，不是 `style:` |
| 背景色 | `className: 'bg-[#1a1a2e]'` — Wind 只支持 6 位 hex |
| 字体 | 统一 LucideIcons，camelCase 引用 |
| StatelessWidget | 构造函数加 `const` |
| 字符串插值 | 单变量不加花括号：`$index`，非 `${index}` |

---

## 常见报错速查

| 报错 | 根因 | 修复 |
|------|------|------|
| `Incorrect use of ParentDataWidget` | 嵌套 flex-1 / 混用 Wind 和原生 Flex / scrollPrimary+flex | 去掉嵌套 flex-1；或改用 Stack；scroll 页面去掉 `f` |
| Positioned 不生效 | 父级是 WDiv 而非 Stack | 改用 Stack 包裹 |
| `A RenderFlex overflowed` | 内容超出 flex 容器 / scrollPrimary 有限高度约束 | 加 `overflow-hidden` 或限制高度；或改用原生 `SingleChildScrollView` |
| `BoxConstraints forces an infinite width` | `f`/`w-full` alias 放在 Row 非 flex 子中 | Row 内用 `flex-1` 而非 `f` |
| light 模式背景纯黑 | Scaffold 设了 `Colors.transparent` 透到 Flutter canvas | 删掉 `backgroundColor: Colors.transparent`，走默认 `theme.colorScheme.background` |

---

## 项目特定

### PureRaw (pureraw_flutter)
- liquid_glass_widgets + Wind 混用
- Liquid Glass 效果组件不要放在 WDiv flex-1 内部——玻璃效果依赖特定布局上下文
- （TODO：补充更多 liquid_glass + Wind 混用经验）

### dots (生活追踪)
- Timeline 滚动加载时出现过 `ParentDataWidget` 错误
- 解决：确保 ListView 内部不使用 flex-1，改为固定高度或 `shrinkWrap: true`
- （TODO：补充最终修复方案）

### asset_manager
- （TODO：补充布局相关经验）

### Flowtime (番茄钟)
- shadcn Scaffold 不能设 `backgroundColor: Colors.transparent`，否则透底看到 Flutter canvas 黑色
- 可滚动页面用原生 `SingleChildScrollView(child: WDiv(className: 'col gap-6'))`，不用 `scrollPrimary: true`
- 自定 alias `f`（→ `w-full h-full`）在 Row 非 flex 子中会触发 infinite width，Row 内撑满用 `flex-1`

---

_最后更新：2026-06-25 | 补充 scrollPrimary 陷阱、f alias 在 Row 中炸、页面背景色规则（Flowtime 项目）_
