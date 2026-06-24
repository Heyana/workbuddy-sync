# 中文字体方案

## 阿里巴巴普惠体 3.0

- **来源**: https://www.alibabafonts.com/ (永久免费商用)
- **字符集**: 9 字重 Thin→Black（35/45/55/65/75/85/95/105/115），覆盖 GB18030-2022 约 5 万汉字
- **格式**: 官方提供 TTF + WOFF + WOFF2 + EOT + OTF
- **无 VF**: 阿里巴巴普惠体没有可变字体（Variable Font）版本，只有静态多字重文件。CJK 字体不同字重字形轮廓不兼容，fonttools varLib 无法合成

## Web 字体压缩策略

### 1. 字符集裁剪 (pyftsubset)
```bash
# 安装 fonttools
pip install fonttools[woff] brotli

# 裁剪到常用字符集 + 输出 woff2
pyftsubset font.ttf \
  --text-file=charset.txt \
  --output-file=font-subset.woff2 \
  --flavor=woff2 \
  --no-hinting \
  --layout-features=*
```

### 2. 常用字符集大小参考
- 4200 字（CJK 基本区前 3600 + ASCII + 标点）覆盖日常中文 99.9%+
- 全量中文字体 ~8MB/字重 → 裁剪后 ~460KB/字重（woff2）
- Thin/Bold/Heavy/Black 等字重字符集更小，裁剪后 ~200KB

### 3. CSS @font-face 多字重方案
虽然没有 VF 文件，但用标准 font-weight 映射多字重文件，CSS 层行为和 VF 一致：
```css
@font-face {
  font-family: 'Alibaba PuHuiTi';
  src: url('./AlibabaPuHuiTi-3-55-Regular-subset.woff2') format('woff2');
  font-weight: 400;
  font-display: swap;
}
/* 使用时: font-family: 'Alibaba PuHuiTi'; font-weight: 600; → 自动匹配 SemiBold */
```

### 4. 官方下载参考
- 完整包: `https://fonts.alibabadesign.com/AlibabaPuHuiTi-3.zip` (266MB)
- 需要 Referer: `https://www.alibabafonts.com/`
- 单个字重 ZIP: `https://fonts.alibabadesign.com/AlibabaPuHuiTi-3/AlibabaPuHuiTi-3-55-Regular.zip`

### 5. 字体体积控制原则
- 优先 woff2（比 ttf 小 30-40%），ttf 做 fallback
- 按需裁剪：项目用多少字就裁多少，不要拉全量
- font-display: swap 避免 FOIT
