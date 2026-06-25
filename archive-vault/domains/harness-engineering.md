# Harness Engineering

**Summary:** Harness engineering = 把 AI coding agent 的反复错误转为持久化的仓库制品（指令、检查、记忆、治理）。三大生态：ruvnet/ruflo 元工具链（脚手架+评分+审计）、github/awesome-copilot 治理框架（失败记忆+漂移检测）、muratcankoylan 自治系统设计。

## 已安装

| Skill | 来源 | 用途 |
|-------|------|------|
| harness-engineering | github/awesome-copilot | 仓库级 agent harness 治理，失败→持久指令 |

## 搜索结果（2026-06-25，skillsmp.com）

### ruvnet/ruflo MetaHarness 生态
| Skill | 用途 |
|-------|------|
| harness-mint | CLI 脚手架 `metaharness new <name>` |
| harness-genome | 7 维度仓库就绪度报告 |
| harness-score | 5 维度评分卡 (fit/confidence/coverage/safety/memory) |
| harness-mcp-scan | MCP 安全扫描 |
| harness-threat-model | MCP 威胁建模 |
| harness-oia-audit | 复合审计 |
| harness-drift-from-history | 漂移检测 |
| harness-similarity | harness 指纹相似度 |

### 其他
| Skill | 来源 | 用途 |
|-------|------|------|
| harness-engineering | muratcankoylan | 自治 agent harness：研究循环、评估、日志、回滚 |
| harness-eval | HKUDS/OpenHarness | 集成测试（真实 LLM 调用） |
| using-duru-herness | ori-kim/duru | 路由+记忆+网关 |

## 适用场景判断

- **已有项目 => 用 awesome-copilot 版**：扫描现有仓库，往 AGENTS.md / docs/failures/ 加治理层
- **新建项目 => 用 harness-mint**：脚手架生成一套 agent 友好的项目骨架
- **研究型 agent => 用 murat 版**：需要研究循环+人工审批的工作流

## 核心概念

```
Harness = Instructions + Constraints + Feedback + Memory + Evaluation + Governance
```

- 发现 → 选表面 → 写指令 → 加检查 → 录失败记忆 → 漂移检测 → 报告
- 关键：不复制通用模板，基于目标仓库真实证据定制
