---
title: Android Foreground Service (Capacitor)
type: concept
created: 2026-06-26
updated: 2026-06-26
tags: [android, capacitor, foreground-service, notification]
---

# Android Foreground Service (Capacitor)

使用 `@capawesome-team/capacitor-android-foreground-service` 实现真正的前台服务，替代普通通知。

## 为什么不用 LocalNotifications

| | LocalNotifications | ForegroundService |
|------|------|------|
| 类型 | 普通通知 | 前台服务 |
| Android 杀进程概率 | 中 | **极低** |
| 更新方式 | cancel + reschedule | `updateForegroundService()` 原生 |
| 更新延迟 | 200-500ms | < 50ms |
| 静默更新 | 不支持（每次都响/震） | `silent: true` |

## 安装配置

```bash
npm install @capawesome-team/capacitor-android-foreground-service
```

### AndroidManifest.xml

```xml
<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_SPECIAL_USE" />
<uses-permission android:name="android.permission.WAKE_LOCK" />
<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />

<!-- Inside <application> -->
<receiver android:name="io.capawesome.capacitorjs.plugins.foregroundservice.NotificationActionBroadcastReceiver" />
<service
    android:name="io.capawesome.capacitorjs.plugins.foregroundservice.AndroidForegroundService"
    android:foregroundServiceType="specialUse"
    android:exported="false" />
```

### 通知渠道（一次创建，低优先级静默更新）

```typescript
await ForegroundService.createNotificationChannel({
  id: 'flowtime_timer',
  name: 'Flowtime Timer',
  description: 'Persistent countdown',
  importance: Importance.Low,
});
```

### 启动 + 定时更新

```typescript
await ForegroundService.startForegroundService({
  id: 7777, title: '专注中', body: '25:00',
  smallIcon: 'ic_stat_flowtime', silent: true,
  notificationChannelId: 'flowtime_timer',
});

// 每 3 秒更新
setInterval(async () => {
  await ForegroundService.updateForegroundService({
    id: 7777, title: '专注中', body: '24:57\n████████░░░░',
    smallIcon: 'ic_stat_flowtime', silent: true,
    notificationChannelId: 'flowtime_timer',
  });
}, 3000);
```

### 停止

```typescript
await ForegroundService.stopForegroundService();
```

## 图标

需要 `res/drawable/ic_stat_xxx.xml` 矢量图（白色剪影）。插件用 `smallIcon` 参数引用文件名（无扩展名）。

## See Also
- [[capacitor-android-build]]
- [[capacitor-native-bridge]]
- [[flowtime-stitch]]
