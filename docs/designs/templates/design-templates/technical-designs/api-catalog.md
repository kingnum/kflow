---
stage: 归档
skill: kflow-archive
version: 1.0.0
created_at: 2026-05-05
template_for: docs/designs/technical-designs/api-catalog.md
---

# 全景 API 目录

> **最后更新**: {YYYY-MM-DD}
> **最后更新来源变更**: {change-name}

---

## 一、接口总览

| 接口ID | 方法 | 路径 | 所属模块 | 简述 | 认证 | 来源变更 |
|--------|------|------|---------|------|------|---------|
| API-001 | GET | /api/{path} | {module} | {简述} | JWT | {change-name} |
| API-002 | POST | /api/{path} | {module} | {简述} | JWT | {change-name} |

## 二、接口详细定义

### API-{id}: {接口名称}

> 来源变更: {change-name} | 更新时间: {YYYY-MM-DD}

- **方法**: {GET/POST/PUT/DELETE/PATCH}
- **路径**: /api/{path}
- **认证**: {JWT / 无 / API Key}
- **权限**: {ROLE_ADMIN / ROLE_USER / 公开}

**请求参数**:

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| {param} | {query/body/path} | {type} | {是/否} | {说明} |

**响应**:

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

**错误码**:

| 错误码 | HTTP状态 | 说明 |
|--------|---------|------|
| {code} | {status} | {说明} |

---

> **维护说明**: 本文档在变更涉及新增或修改 API 接口时更新。每次更新标注来源变更和更新时间。
> **兼容性**: 本文档与 detailed-design.md §二设计域章节（接口设计部分）保持结构兼容，归档时从 detailed-design.md 对应章节提取并合并。
