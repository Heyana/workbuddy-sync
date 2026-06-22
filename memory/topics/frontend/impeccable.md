# Impeccable — 前端设计工具集

> marketplace skillId: `skill_2053082862415904768`
> 新电脑安装：在 WorkBuddy 中说「安装 impeccable skill」或通过 marketplace 搜索安装

## 用途

生成前端 UI 时加载此 skill，遵循其设计原则，避免 AI Slop（紫蓝渐变、Inter 字体、毛玻璃滥用、圆角+通用阴影等）。

## 核心约束

- **字体**：禁止 Inter/Roboto/Arial/Open Sans，用独特展示字体+精致正文字体
- **色彩**：禁止纯黑 #000、纯白 #fff；禁止青+紫+霓虹点缀配色；用 oklch/color-mix
- **空间**：禁止卡片套卡片、万物居中；用变化间距创造节奏
- **动效**：禁止 bounce/elastic 缓动；用 expo/ease-out-quart；禁止动画化布局属性
- **设计方向**：每次选一个明确的美学极端（极简/混沌/复古未来/有机/野兽派/杂志风……），有意图而非安全中庸

## 使用方式

做前端 UI 时先 `Skill: impeccable`，然后按指引先确认设计上下文（用户、品牌、美学方向），再产出代码。

## 参考

- 官网：https://impeccable.style
- GitHub：https://github.com/pbakaus/impeccable
