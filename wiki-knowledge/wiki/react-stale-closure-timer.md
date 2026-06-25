---
title: React Stale Closure Timer Bug
type: concept
created: 2026-06-26
updated: 2026-06-26
tags: [react, bug, timer, useeffect, useref, closure]
---

# React Stale Closure Timer Bug

在 React 中使用 `useEffect` + `setInterval` 实现倒计时时，回调函数可能捕获旧的 state/props 值导致状态转换失败。

## 问题

```typescript
// ❌ handleTimerComplete 在 effect 中产生 stale closure
useEffect(() => {
  const interval = setInterval(() => {
    setTimeLeft((prev) => {
      if (prev <= 1) {
        handleTimerComplete(); // 可能读到旧 settings.autoStartBreaks
        return 0;
      }
      return prev - 1;
    });
  }, 1000);
  return () => clearInterval(interval);
}, [timerState, timerMode, settings]);
```

## 修复

```typescript
// 1. handleTimerComplete 用 useCallback 管理依赖
const handleTimerComplete = useCallback(() => {
  // ... 使用最新的 settings, timerMode 等
}, [timerMode, settings, taskTitle, totalDuration]);

// 2. 通过 ref 桥接
const handleTimerCompleteRef = useRef(handleTimerComplete);
useEffect(() => {
  handleTimerCompleteRef.current = handleTimerComplete;
}, [handleTimerComplete]);

// 3. effect 中通过 ref 调用
useEffect(() => {
  const interval = setInterval(() => {
    setTimeLeft((prev) => {
      if (prev <= 1) {
        handleTimerCompleteRef.current(); // 始终是最新的
        return 0;
      }
      return prev - 1;
    });
  }, 1000);
  return () => clearInterval(interval);
}, [timerState, timerMode, settings]);
```

## 症状

Rest 5 分钟倒计时视觉正确但实际不启动 → `settings.autoStartBreaks` 在旧闭包中为 `false`，新设置值被忽略。

## See Also
- [[flowtime-stitch]]
