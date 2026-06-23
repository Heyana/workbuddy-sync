# Go + SQLite 知识库

> 高频踩坑和最佳实践。每次遇到新坑、性能优化、模式选择，立刻更新此文件。
> 保持精炼——只记结论和关键约束，不记推导过程。

---

## 项目约定

| 项目 | SQLite 驱动 | ORM | 端口 |
|------|------------|-----|------|
| electron-media-manager | mattn/go-sqlite3 (CGO) | GORM | 23347 |
| （待补充） | | | |

## GORM + SQLite 常见坑

### 写入慢 (>200ms)
- **已观察**：electron-media-manager 中 GORM + SQLite 写入延迟超 200ms
- 可能原因：WAL 模式未开启 / 事务未批量 / GORM 默认关闭 prepared statement cache
- **排查方向**：
  - 开启 WAL：`PRAGMA journal_mode=WAL;`
  - 批量写入用事务包裹：`db.Transaction(func(tx *gorm.DB) error { ... })`
  - 设置 `db.Exec("PRAGMA synchronous=NORMAL;")`
  - 检查是否有不必要的索引或全表扫描
- （TODO：记录最终定位和修复方案）

### 并发写入
- SQLite 写锁是库级（database-level），多 goroutine 并发写会排队
- 若高并发写场景，考虑：
  - 写入通道串行化（chan + 单 writer goroutine）
  - 或切换到支持行级锁的数据库

### 连接池
- GORM + SQLite 的 `SetMaxOpenConns(1)` 是安全底线（SQLite 不适合多连接并发写）
- 读可适当放宽，但写必须在同一连接

## 查询规范

- ❌ 禁止 `WHERE '1'='1'` 这种原始 SQL 拼接
- ✅ 用 GORM 的 proper where 子句：`db.Where("name = ?", name)`
- ✅ 或手动构建参数化查询：`db.Raw("SELECT * FROM t WHERE id = ?", id)`

## 项目结构

```
├── handlers/       # 请求处理器（薄层，仅解析+调用 service）
├── services/       # 业务逻辑
├── models/         # 数据模型
├── middleware/     # 中间件
├── utils/          # 工具函数
└── main.go         # 入口（初始化 + 注册路由）
```

- handlers 不写业务逻辑，只做参数解析/校验/响应
- services 做数据库操作和业务编排
- 好处：换存储/换 ORM 只改 services 层

## 迁移

- electron-media-manager 已从 Prisma 迁移到原生 GORM + SQLite
- 迁移注意事项：
  - 保留数据完整性验证步骤
  - 迁移后做数据对账（行数 / checksum）
- （TODO：补充迁移脚本的最佳实践）

---

_最后更新：2026-06-23 | 初建，含已知坑位，待边用边补_
