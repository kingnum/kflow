---
stage: 归档
skill: kflow-archive
version: 1.0.0
created_at: 2026-05-05
template_for: docs/designs/technical-designs/nfr-baseline.md
---

# NFR 基线文档

> **最后更新**: {YYYY-MM-DD}
> **最后更新来源变更**: {change-name}

---

## 一、性能基准

| 需求项 | 目标值 | 测量方式 | 当前值 | 更新时间 | 来源变更 |
|--------|--------|---------|--------|---------|---------|
| API P95 响应时间 | < 500ms | 接口单元测试 | {value} | {时间} | {change-name} |
| 页面首次加载时间 | < 2s | E2E测试 | {value} | {时间} | {change-name} |
| 数据库查询时间 | < 100ms | 单元测试 | {value} | {时间} | {change-name} |
| 并发用户数 | ≥ {n} | 压测 | {value} | {时间} | {change-name} |

## 二、安全基准

| 需求项 | 要求 | 当前状态 | 更新时间 | 来源变更 |
|--------|------|---------|---------|---------|
| 认证机制 | JWT + Refresh Token | {状态} | {时间} | {change-name} |
| 权限控制 | RBAC 角色权限 | {状态} | {时间} | {change-name} |
| 数据加密 | 敏感字段 AES-256 | {状态} | {时间} | {change-name} |
| SQL注入防护 | 参数化查询 | {状态} | {时间} | {change-name} |
| XSS防护 | 输出编码 | {状态} | {时间} | {change-name} |

## 三、可用性基准

| 需求项 | 目标值 | 当前值 | 更新时间 | 来源变更 |
|--------|--------|--------|---------|---------|
| 服务可用率 | 99.9% | {value} | {时间} | {change-name} |
| 故障恢复时间 | < 30min | {value} | {时间} | {change-name} |

## 四、可维护性基准

| 需求项 | 要求 | 当前状态 | 更新时间 | 来源变更 |
|--------|------|---------|---------|---------|
| 日志规范 | 结构化日志 (JSON) + traceId | {状态} | {时间} | {change-name} |
| 代码覆盖率 | ≥ 80% | {value}% | {时间} | {change-name} |
| 文档完整性 | 所有接口有 OpenAPI 描述 | {状态} | {时间} | {change-name} |

---

> **维护说明**: 本文档在变更涉及 NFR 调整时更新。每次更新标注来源变更和更新时间。
> **兼容性**: 本文档与 detailed-design.md §三 NFR 章节保持结构兼容，归档时从 detailed-design.md 对应章节提取并合并。
