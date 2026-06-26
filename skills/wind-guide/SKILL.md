---
name: wind-guide
description: >
  Flutter Wind (fluttersdk_wind v1.1.0) layout system reference for all Flutter projects using
  shadcn_flutter + Wind. Consult before writing any Flutter UI that imports WDiv, WText, or uses
  className-based layout. Documents correct/incorrect patterns for flex, scrolling, positioning, colors,
  aliases, cx(), and StyleProvider. Triggers: any .dart file using WDiv / className / Wind layout.
agent_created: true
---

# Wind Guide — Flutter Projects

Technical stack: shadcn_flutter + fluttersdk_wind (^1.1.0) + LucideIcons + project my-wind helpers.

## Core Rules

### ⛔ BANNED: flutter/material.dart

`package:flutter/material.dart` is FORBIDDEN in all UI files. The only exception is `main.dart` (MaterialApp.router requires it). All other files must NOT import it.

**Consequence**: Never use these Material widgets — always use shadcn equivalents:

| ❌ Material (banned) | ✅ shadcn (use this) |
|---------------------|---------------------|
| `Slider` / `SliderTheme` | `ControlledSlider` with `SliderController` |
| `TextField` | `TextField` (from shadcn) |
| `TextFormField` | `TextField` (from shadcn) |
| `TextButton` | `TextButton` (from shadcn) or `Button.text()` |
| `AlertDialog` | `AlertDialog` (from shadcn) |
| `Spacer` / `Flexible` / `Expanded` | `WDiv(className: 'flex-1')` (**exception**: `Stack` 内部允许 `Expanded` / `Positioned.fill`) |
| `Navigator.pop(context)` | `Navigator.pop(context)` (ok — from widgets) |

### Imports

Every UI file must use this exact import pattern:

```dart
import 'package:fluttersdk_wind/fluttersdk_wind.dart';
import 'package:lucide_icons_flutter/lucide_icons.dart';
import 'package:shadcn_flutter/shadcn_flutter.dart'
    hide ThemeMode, LucideIcons, Stack, Positioned;
import 'package:signals/signals_flutter.dart';
```

If a file truly needs a Flutter widget that shadcn doesn't provide (eg. `Stack`, `Positioned`), import `package:flutter/widgets.dart` instead — never `material.dart`.

Never import `material.dart` outside `main.dart`. Never use Material/Forui components.

### Casing & Code Style

- All `StatelessWidget` subclass constructors must be `const`.
- LucideIcons use camelCase: `LucideIcons.timer`, `LucideIcons.play`, `LucideIcons.barChart3`.
- String interpolation: single variable → no braces: `'$index'` not `'${index}'`.
- `WText` dynamic color uses `foregroundColor:`, not `style:`.

---

## Layout System

### WDiv — the only layout primitive

Use project `Div` (from `my-wind/div.dart`) — it pre-expands aliases and resolves style sheets before handing to WDiv.

```dart
// Function shorthand
div('col gap-4', [child1, child2])  // children
div('w-full', singleChild)          // single child
div('w-full')                       // empty

// Class-based (preferred for clarity)
WDiv(className: 'col gap-4', children: [...])
```

Use the **project alias table** from `my-wind/aliases.dart`:

| Alias | Expands to |
|-------|-----------|
| `w` | `w-full` |
| `h` | `h-full` |
| `f` | `w-full h-full` |
| `row` | `flex flex-row` |
| `col` | `flex flex-col` |
| `aic` | `items-center` |
| `ais` | `items-start` |
| `aie` | `items-end` |
| `jcc` | `justify-center` |
| `jcb` | `justify-between` |
| `jce` | `justify-end` |
| `jcs` | `justify-start` |
| `center` | `flex items-center justify-center` |
| `row-c` | `flex flex-row items-center justify-center` |
| `col-c` | `flex flex-col items-center justify-center` |
| `row-aic` | `flex flex-row items-center` |
| `col-aic` | `flex flex-col items-center` |
| `wrow` | `wrap` |
| `wrow-c` | `wrap align-content-center` |
| `wrow-b` | `wrap align-content-between` |
| `bgc-f` | `bg-white` |

### Conditional className — use `cx()`

From `my-wind/cx.dart`. Combines strings, ignores null/false/bool:

```dart
// ✅ correct
cx(['w-full', isActive && 'bg-primary', !isActive && 'bg-muted', null])

// ❌ wrong — manual string interpolation
'w-full ${isActive ? "bg-primary" : "bg-muted"}'  // cx is cleaner, handles nulls
```

### StyleProvider — inject stylesheets

From `my-wind/style_provider.dart`. Wrap the tree once, child Divs use `id` to reference:

```dart
StyleProvider(
  styleSheet: myStyleMap,
  child: WDiv(className: 'col gap-4', children: [
    WDiv(id: 'card_header'),
    WDiv(id: 'card_body'),
  ]),
)
```

---

## Layout Anti-Patterns (MUST NOT DO)

### ❌ Never use Flutter Spacer / Flexible / Expanded

Wind's Column/Row are wrapped by `WindFlexOverflowScope` — native FlexParentData conflicts.

```dart
// ❌ WRONG — will crash or misbehave
Row(children: [Expanded(child: ...), Spacer()])

// ✅ CORRECT
WDiv(className: 'row', children: [
  WDiv(className: 'flex-1', child: ...),
  WDiv(className: 'flex-1'),  // acts as Spacer
])
```

**Exception**: Inside `Stack`, use `Expanded` / `Positioned.fill` — WDiv(className: 'flex-1') does NOT work there.

### ❌ Never nest flex-1

Inner Expanded inside outer Expanded = conflict.

```dart
// ❌ WRONG
WDiv(className: 'flex-1', children: [
  WDiv(className: 'flex-1', child: ...),  // nested flex-1
])

// ✅ CORRECT — use column layout instead
WDiv(className: 'flex-1 col', children: [...])
```

### ❌ Never use WDiv relative + Positioned

Wind's `relative` doesn't make Positioned children work.

```dart
// ❌ WRONG
WDiv(className: 'relative', children: [
  Positioned(bottom: 0, child: ...),  // won't work
])

// ✅ CORRECT
Stack(children: [
  Positioned.fill(child: mainContent),
  Positioned(bottom: 8, child: floatingWidget),
])
```

### ❌ Never use `f` alias in Row children

`f` expands to `w-full h-full`. In a Row non-flex child, `w-full` = infinite width → overflow.

```dart
// ❌ WRONG
WDiv(className: 'row', children: [
  WDiv(className: 'f', child: ...),  // infinite width in row
])

// ✅ CORRECT
WDiv(className: 'row', children: [
  WDiv(className: 'flex-1', child: ...),  // flex-1 expands correctly
])
```

---

## Scrolling

### ❌ Never use scrollPrimary + flex together

`scrollPrimary: true` with flex children causes overflow and layout explosion.

```dart
// ❌ WRONG
WDiv(scrollPrimary: true, className: 'col gap-6', children: [...])

// ✅ CORRECT — use native SingleChildScrollView
SingleChildScrollView(
  child: WDiv(className: 'col gap-6', children: [...]),
)
```

### Page with scroll + padding

```dart
SingleChildScrollView(
  padding: const EdgeInsets.all(24),
  child: WDiv(className: 'col gap-8', children: [...]),
)
```

---

## Colors

### hex colors in className — 6 digits only

```dart
// ✅ CORRECT — 6 hex digits
WDiv(className: 'bg-[#b3272e]')     // Focus Red
WDiv(className: 'bg-[#006d3e]')     // Rest Green
WDiv(className: 'bg-[#f9f9f9]')     // Background

// ❌ WRONG — 8 hex digits (alpha) not supported
WDiv(className: 'bg-[#ff5f5f80]')
```

### Color tokens from Wind theme

```dart
WDiv(className: 'bg-primary text-surface')
WDiv(className: 'bg-secondary text-on-secondary')
WText(className: 'text-onsurfacevariant')
```

---

## Background & Page

### shadcn Scaffold background

```dart
// ❌ WRONG — transparent shows black Flutter canvas
Scaffold(backgroundColor: Colors.transparent, ...)

// ✅ CORRECT — let shadcn theme handle it
Scaffold(...)  // uses theme.colorScheme.background by default
```

---

## React-like UI → Flutter Wind Translation

| React (Tailwind) | Flutter Wind |
|-----------------|-------------|
| `<div className="flex gap-4">` | `WDiv(className: 'row gap-4')` |
| `<div className="flex flex-col">` | `WDiv(className: 'col')` |
| `<div className="items-center justify-center">` | `WDiv(className: 'center')` |
| `className="flex-1"` in row | `WDiv(className: 'flex-1')` |
| `className="rounded-full"` | `WDiv(className: 'rounded-full')` |
| `className="p-4"` | `WDiv(className: 'p-4')` |
| `className="text-sm font-bold"` | `WText(className: 'text-sm font-bold')` |
| `<span>` | `WText` |
| CSS `var(--primary)` | Wind theme color token `text-primary` |
| absolute positioning | `Stack` + `Positioned` |
| `overflow-auto` | `SingleChildScrollView` |

---

## Working Example

See `lib/presentation/timer/timer_screen.dart` for a complete, correct pattern:

```dart
class TimerScreen extends StatelessWidget {
  const TimerScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Watch((context) {
      return SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: WDiv(className: 'col-c gap-8', children: [
          // ... nested widgets using WDiv, WText, icons
        ]),
      );
    });
  }
}
```

Key patterns:
1. `const` constructor
2. `Watch()` wrapper for signals reactivity
3. `SingleChildScrollView` outside, `WDiv(className: 'col...')` inside
4. `EdgeInsets.all(24)` for page padding (not Wind p-6)
5. Nested layout only uses WDiv/WText — no Flutter layout primitives
