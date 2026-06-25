# Capacitor 原生桥接模式

> React/前端项目集成 Capacitor 的标准模式：动态 import + Native 检测 + Web 降级。

## 核心模式

```typescript
// 1. 懒检测 Capacitor 可用性
let _capAvailable = false;
async function isCapacitorAvailable(): Promise<boolean> {
  const { Capacitor } = await import('@capacitor/core');
  return Capacitor.isNativePlatform();
}

// 2. 每个功能：Native 路径 + Web fallback
async function myFeature(): Promise<void> {
  if (await isCapacitorAvailable()) {
    const { SomePlugin } = await import('@capacitor/some-plugin');
    // native implementation
  } else {
    // web fallback
  }
}
```

**关键点**：
- 所有 Capacitor 依赖用 **动态 `import()`**，不在顶层静态引用
- `Capacitor.isNativePlatform()` 返回 false 时整个插件不加载
- Web bundle 中 Capacitor 代码 tree-shake 掉，增量 < 5KB

## 通知（响铃 + 弹窗）

```typescript
const { LocalNotifications } = await import('@capacitor/local-notifications');

// 先请求权限（iOS 必需）
const perm = await LocalNotifications.requestPermissions();
if (perm.display !== 'granted') return;

// 立即触发通知
await LocalNotifications.schedule({
  notifications: [{
    id: Date.now(),
    title: 'Focus Complete',
    body: 'Time to rest',
    sound: 'timer_end.wav',
    schedule: { at: new Date(Date.now() + 100) },
  }],
});
```

## 后台时间追踪

```typescript
// 切后台时保存快照
interface BackgroundCheckpoint {
  timestamp: number;
  timeLeft: number;
  timerMode: 'work' | 'rest';
  timerState: 'running' | 'paused';
}

function saveCheckpoint(cp: BackgroundCheckpoint): void {
  localStorage.setItem('bg_checkpoint', JSON.stringify(cp));
}

// 回前台时计算经过时间
function calculateAdjusted(checkpoint: BackgroundCheckpoint): number {
  const elapsed = Math.floor((Date.now() - checkpoint.timestamp) / 1000);
  return Math.max(0, checkpoint.timeLeft - elapsed);
}
```

## 双通道监听（Capacitor + Web）

```typescript
// Capacitor: App.addListener('appStateChange')
const { App } = await import('@capacitor/app');
App.addListener('appStateChange', (state) => {
  if (state.isActive) { /* 回前台 */ }
});

// Web fallback: visibilitychange
document.addEventListener('visibilitychange', () => {
  if (document.hidden) { /* 切后台 */ }
  else { /* 回前台 */ }
});
```

## 通知栏倒计时（cancel + reschedule）

Capacitor 不支持更新已有通知的文本，变通方案：

```typescript
// 每秒 cancel 旧通知 + reschedule 新通知（文本含剩余秒数）
let remaining = 10;
const interval = setInterval(async () => {
  await LocalNotifications.cancel({ notifications: [{ id: 9999 }] });
  await LocalNotifications.schedule({
    notifications: [{
      id: 9999,
      title: 'Countdown',
      body: `${remaining}s remaining`,
      ongoing: true,
      schedule: { at: new Date(Date.now() + 200) },
    }],
  });
  remaining--;
  if (remaining <= 0) clearInterval(interval);
}, 1000);
```

注意：高频 cancel/reschedule 可能被 Android 限流，不适合生产环境精确计时。
