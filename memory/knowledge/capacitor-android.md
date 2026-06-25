# Capacitor Android 构建

> 从零搭建 Capacitor Android 构建环境，含国内镜像配置。

## 环境要求

| 组件 | 版本 | 来源 |
|------|------|------|
| JDK | **21** (不是 17!) | Eclipse Temurin, `adoptium.net` |
| Gradle | 8.14.3 (wrapper) | `gradle-wrapper.properties` |
| Android SDK | platforms 34-36, build-tools 35-37 | `%LOCALAPPDATA%/Android/Sdk/` |

- JDK 17 报错：`error: invalid source release 21` — Capacitor Android 库编译目标 Java 21。

## 构建流程

```bash
# 1. Web 构建
npx vite build

# 2. 同步 web 产物到 Android
npx cap sync android

# 3. Android APK
cd android
$env:JAVA_HOME = "D:\path\to\jdk-21"
.\gradlew assembleDebug
```

APK 输出：`android/app/build/outputs/apk/debug/app-debug.apk`

## 国内镜像配置

### Gradle Wrapper (`gradle-wrapper.properties`)
```properties
distributionUrl=https\://mirrors.cloud.tencent.com/gradle/gradle-8.14.3-all.zip
networkTimeout=60000
```

### Maven (`build.gradle`)
```groovy
repositories {
    maven { url 'https://mirrors.cloud.tencent.com/nexus/repository/maven-public/' }
    google()
    mavenCentral()
}
```

### SDK 路径 (`local.properties`)
```
sdk.dir=C:/Users/xxx/AppData/Local/Android/Sdk
```
注意：使用正斜杠，不要反斜杠。

## 常见问题

| 错误 | 原因 | 修复 |
|------|------|------|
| `SDK location not found` | `local.properties` 缺失 | 创建文件写入 `sdk.dir=...` |
| `Connect timed out` | Gradle 官方源不可达 | 切腾讯镜像 |
| `invalid source release 21` | JDK 版本太低 | 安装 JDK 21 |
| `文件名称、目录名称或卷标语法不正确` | local.properties 路径编码问题 | 用正斜杠路径格式 |
