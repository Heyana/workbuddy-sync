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
| `Incorrect use of ParentDataWidget` | 嵌套 flex-1 / 混用 Wind 和原生 Flex | 去掉嵌套 flex-1；或改用 Stack |
| Positioned 不生效 | 父级是 WDiv 而非 Stack | 改用 Stack 包裹 |
| `A RenderFlex overflowed` | 内容超出 flex 容器 | 加 `overflow-hidden` 或限制高度 |

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

---

_最后更新：2026-06-23 | 初建，从 flutter.md 提取核心规则 + 补充项目特定经验_
