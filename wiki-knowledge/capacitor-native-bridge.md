---
title: Capacitor Native Bridge Pattern
type: concept
created: 2026-06-26
updated: 2026-06-26
tags: [capacitor, react, pattern, native, notifications, background]
---

# Capacitor Native Bridge Pattern

React 项目集成 Capacitor 原生能力的标准模式。

## 核心原则

```typescript
// 1. 懒检测是否在原生环境
async function isNative(): Promise<boolean> {
  const { Capacitor } = await import('@capacitor/core');
  return Capacitor.isNativePlatform();
}

// 2. 动态 import 插件，Web 端零开销
async function myFeature(): Promise<void> {
  if (await isNative()) {
    const { SomePlugin } = await import('@capacitor/some-plugin');
    // native path
  } else {
    // web fallback
  }
}
```

## 三大能力

### 通知（响铃 + 弹窗）
- `LocalNotifications.schedule()` 立即触发
- 先 `requestPermissions()`（iOS 必需）
- 不同 mode 使用不同 sound 文件

### 后台时间追踪
- 切后台存 checkpoint `{timestamp, timeLeft, timerMode, timerState}`
- Capacitor: `App.addListener('appStateChange')`
- Web: `document.addEventListener('visibilitychange')`
- 回前台算 `timeLeft - elapsed`

### 通知栏倒计时

**优先方案**：使用 [[android-foreground-service]]（真正前台服务），`updateForegroundService()` 原生速度更新。

**降级方案**（不推荐）：使用 `LocalNotifications` 的 cancel + reschedule 模式。

## See Also
- [[android-foreground-service]]
- [[capacitor-android-build]]
- [[flowtime-stitch]]
