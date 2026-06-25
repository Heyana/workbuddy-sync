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

## Bug #2: setTimeLeft 更新器覆盖

在上面的修复中，`handleTimerCompleteRef.current()` 仍在 `setTimeLeft` 更新器内部被调用。`handleTimerComplete` 内部会调用 `setTimeLeft(新时长)`，但更新器随后 `return 0`。React 批量处理时 `0` 覆盖了 `新时长`，导致只第一轮正常，后续轮 `timeLeft` 被钉在 0。

### 修复：延迟完成标志

```typescript
const shouldCompleteRef = useRef(false);

// 效果1：在更新器外部检测完成
useEffect(() => {
  if (shouldCompleteRef.current && timerState === 'running' && timeLeft === 0) {
    shouldCompleteRef.current = false;
    handleTimerCompleteRef.current();
  }
});

// 效果2：更新器只设标志
useEffect(() => {
  if (timerState === 'running') {
    interval = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) { shouldCompleteRef.current = true; return 0; }
        return prev - 1;
      });
    }, 1000);
  }
  return () => clearInterval(interval);
}, [timerState, timerMode, settings]);
```

确保 `handleTimerComplete` 永远不在 `setTimeLeft` 更新器内部执行，避免返回值覆盖冲突。

## See Also
- [[flowtime-stitch]]
