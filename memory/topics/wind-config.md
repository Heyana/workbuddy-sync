# Wind 配置规范

- 包名：fluttersdk_wind（非 wind）
- 版本：^1.1.0
- 主题配置：WindTheme + WindThemeData
  - light theme 用 WindThemeData(brightness: Brightness.light, syncWithSystem: true, ...)
  - dark theme 用 light.copyWith(brightness: Brightness.dark, colors: {...})
  - MaterialApp 放在 WindTheme.builder 内，用 controller.toThemeData() 转 Material ThemeData
- baseSpacingUnit：默认 4，设计系统用 8 时设为 8（p-1=8px）
- aliases 字段配置缩写类名（见下方别名表）
- 颜色：colors 字段用 MaterialColor（_swatch() 辅助函数从单色生成 50-950 shades）
- 字体：fontFamilies: {'sans': '字体名'}，applyDefaultFontFamily: true

## 常用别名（aliases）
在 WindThemeData(aliases: {...}) 中配置：
- w=w-full, h=h-full, f=w-full h-full
- row=flex flex-row, col=flex flex-col
- aic=items-center, ais=items-start, aie=items-end
- jcc=justify-center, jcb=justify-between, jce=justify-end, jcs=justify-start
- center=flex items-center justify-center
- row-c=flex flex-row items-center justify-center
- col-c=flex flex-col items-center justify-center
- row-aic=flex flex-row items-center
- col-aic=flex flex-col items-center
- bgc-f=bg-white（背景色别名，按设计系统自定义）
