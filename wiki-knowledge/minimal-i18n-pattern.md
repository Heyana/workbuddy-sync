---
title: Minimal i18n Pattern
type: concept
created: 2026-06-26
updated: 2026-06-26
tags: [react, i18n, pattern, typescript]
---

# Minimal i18n Pattern

零依赖的 React i18n 方案，适合 < 200 key 的小型项目。

## 核心设计

```typescript
// 模块级状态，locale 变更即时生效
let _locale: Locale = localStorage.getItem('locale') || 'zh';
let _listeners: Array<() => void> = [];

export function getLocale() { return _locale; }
export function setLocale(l: Locale) {
  _locale = l;
  localStorage.setItem('locale', l);
  _listeners.forEach(fn => fn());
}

// 翻译字典
const zh: Record<string, string> = { 'app.hello': '你好', ... };
const en: Record<string, string> = { 'app.hello': 'Hello', ... };

export function t(key: string): string {
  return _locale === 'zh' ? zh[key] : en[key];
}
```

## 组件集成

```tsx
// Settings 页切换语言
const [locale, setLocalLocale] = useState(getLocale());
useEffect(() => onLocaleChange(() => setLocalLocale(getLocale())), []);

// 任何组件直接调
<h1>{t('app.title')}</h1>
```

## 优势

- 零 npm 依赖
- 模块级反应，不依赖 React context
- key 即原文，可读性好
- `< 50 行核心代码`

## 局限

- 不支持参数插值 (`t('hello {name}')`)
- 无复数/日期格式化
- 适合小型个人项目，不适合 SaaS 多语言

## See Also
- [[flowtime-stitch]]
