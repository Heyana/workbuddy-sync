---
title: Capacitor Android Build
type: concept
created: 2026-06-26
updated: 2026-06-26
tags: [capacitor, android, build, jdk, gradle]
---

# Capacitor Android Build

从零搭建 Capacitor Android 构建环境的完整流程和排坑记录。

## 环境要求

- JDK 21 (Temurin) — **不是 17**，Capacitor Android 库编译目标 Java 21
- Gradle 8.14.3+ (wrapper)
- Android SDK platforms 34-36, build-tools 35-37

## 国内镜像

### Gradle Wrapper
```properties
distributionUrl=https\://mirrors.cloud.tencent.com/gradle/gradle-8.14.3-all.zip
networkTimeout=60000
```

### Maven 仓库
```groovy
repositories {
    maven { url 'https://mirrors.cloud.tencent.com/nexus/repository/maven-public/' }
    google()
    mavenCentral()
}
```

### SDK 路径
`local.properties` 必须用正斜杠格式：
```
sdk.dir=C:/Users/xxx/AppData/Local/Android/Sdk
```

## 构建命令

```bash
npx vite build
npx cap sync android
cd android && ./gradlew assembleDebug
```

## 排坑

| 错误 | 原因 | 修复 |
|------|------|------|
| `SDK location not found` | local.properties 缺失 | 创建含 sdk.dir |
| `Connect timed out` | Gradle 官方源不可达 | 切腾讯镜像 |
| `invalid source release 21` | JDK < 21 | 安装 JDK 21 |
| 文件名/目录名语法错误 (乱码) | 路径编码问题 | 用正斜杠 |

## See Also
- [[capacitor-native-bridge]]
- [[flowtime-stitch]]
