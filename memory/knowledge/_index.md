# 技术知识库索引

> 技术深度知识 & 排坑记录（为什么这么干、怎么干对）。
> 主索引见 `~/.workbuddy/MEMORY.md` → 📚 技术知识库。

| 领域 | 文件 | 覆盖内容 |
|------|------|----------|
| Go + SQLite | [go-sqlite.md](go-sqlite.md) | GORM 性能、并发写入、连接池、查询规范、迁移 |
| Flutter 布局 | [flutter-layout.md](flutter-layout.md) | Wind WDiv、Stack/Positioned、flex-1 嵌套、ParentDataWidget 排坑 |
| Vue TSX | [vue-tsx.md](vue-tsx.md) | TSX 优先策略、createApp 函数式组件、h() 禁令、reka-ui 整合 |
| ffmpeg | [ffmpeg.md](ffmpeg.md) | NVENC (RTX 4070) 参数、GPU 管线、C++ 集成 (osvtoolbox) |
| WebDAV 同步 | [webdav-sync.md](webdav-sync.md) | 文件级增量同步、多账号、manifest 设计、冲突处理 |

## 维护规则

1. 每次踩坑、学到模式 → 追加到对应文件
2. 不重复 topics（topics 记规则约定，knowledge 记深层原理和排坑）
3. 保持精炼：结论、约束、关键参数、代码模板
4. TODO 是债务，遇到相关知识立刻填入并移除
5. 新增领域时 → 新建文件 + 更新本索引 + 更新 `MEMORY.md`
