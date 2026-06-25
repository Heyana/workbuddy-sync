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
- 不支持更新已有通知 → cancel + reschedule 变通
- 每秒更新 body 文本显示剩余秒数
- 高频操作可能被 Android 限流

## 双铃声模式
- Work 完成: 上行 C5→E5→G5（明亮、有力）
- Rest 完成: 下行 G4→E4→C4（柔和、沉静）

## See Also
- [[capacitor-android-build]]
- [[flowtime-stitch]]
