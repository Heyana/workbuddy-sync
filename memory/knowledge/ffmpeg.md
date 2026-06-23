# ffmpeg 知识库

> 视频编码、GPU 加速、参数调优的实战经验与排坑记录。
> 保持精炼——只记结论和关键约束，不记推导过程。

---

## 硬件环境

- GPU：NVIDIA RTX 4070
- 编码器：NVENC (h264_nvenc / hevc_nvenc)
- 项目：osvtoolbox（C++ 封装 ffmpeg 逻辑）

---

## NVENC 基础

### 可用编码器
```bash
# 列出 NVIDIA 编码器
ffmpeg -encoders | grep nvenc

# 常用：
h264_nvenc    # H.264 硬件编码
hevc_nvenc    # H.265/HEVC 硬件编码
av1_nvenc     # AV1 硬件编码（RTX 40 系列支持）
```

### 基本用法
```bash
# H.264 NVENC
ffmpeg -i input.mp4 -c:v h264_nvenc -preset p4 -cq 23 output.mp4

# HEVC NVENC (H.265)
ffmpeg -i input.mp4 -c:v hevc_nvenc -preset p4 -cq 28 output.mp4
```

---

## 关键参数速查

| 参数 | 说明 | 常用值 |
|------|------|--------|
| `-preset` | 编码速度/质量平衡 | p1(最快) ~ p7(最慢/高质量) |
| `-cq` | 恒定质量 (CQP 模式) | h264: 18-23, hevc: 23-28 |
| `-b:v` | 固定码率 | 如 `-b:v 8M` |
| `-maxrate` / `-bufsize` | VBR 上限和缓冲 | 配合 `-b:v` 使用 |
| `-rc` | 码率控制 | cbr / vbr / constqp |
| `-tune` | 场景优化 | hq / ll (低延迟) / ull (超低延迟) |
| `-profile` | 编码档次 | main / high / rext |

---

## 常见场景

### 高质量存档（文件最小化）
```bash
ffmpeg -i input.mp4 \
  -c:v hevc_nvenc -preset p7 -cq 28 \
  -c:a aac -b:a 128k \
  output.mp4
```

### 快速转码（速度优先）
```bash
ffmpeg -i input.mp4 \
  -c:v h264_nvenc -preset p1 -b:v 8M \
  -c:a copy \
  output.mp4
```

### 全 GPU 管线（解码 + 编码）
```bash
ffmpeg -hwaccel cuda -hwaccel_output_format cuda \
  -i input.mp4 \
  -c:v hevc_nvenc -preset p4 -cq 28 \
  output.mp4
```

---

## 排坑记录

### TODO：记录已知问题
- （TODO：osvtoolbox 中遇到的 ffmpeg 具体坑位）
- （TODO：RTX 4070 特定限制——如最大并发编码流数）
- （TODO：10-bit 编码支持情况）
- （TODO：HDR 元数据传递问题）

---

## C++ 集成 (osvtoolbox)

- （TODO：C++ 调用 ffmpeg libav* API 的最佳实践）
- （TODO：异步编码管线设计）
- （TODO：错误处理和资源释放模式）

---

_最后更新：2026-06-23 | 初建，含 NVENC 基础参数模板，待从 osvtoolbox 实战中补充_
