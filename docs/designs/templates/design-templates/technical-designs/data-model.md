---
stage: 归档
skill: kflow-archive
version: 1.0.0
created_at: 2026-05-05
template_for: docs/designs/technical-designs/data-model.md
---

# 全景数据模型文档

> **最后更新**: {YYYY-MM-DD}
> **最后更新来源变更**: {change-name}

---

## 一、实体总览

| 实体 | 所属域 | 表名 | 简述 | 来源变更 |
|------|--------|------|------|---------|
| {Entity} | {domain} | {table} | {简述} | {change-name} |

## 二、实体关系图

{实体关系描述，标注 1:1 / 1:N / N:M 关系}

## 三、实体详细定义

### {实体名称}

> 来源变更: {change-name} | 更新时间: {YYYY-MM-DD}

| 字段 | 类型 | 约束 | 默认值 | 说明 |
|------|------|------|--------|------|
| {field} | {type} | {constraint} | {default} | {说明} |

**索引**:

| 索引名 | 字段 | 类型 | 说明 |
|--------|------|------|------|
| {index} | {fields} | {UNIQUE/BTREE/...} | {说明} |

**关联**:

| 关联实体 | 关系 | 外键 | 说明 |
|---------|------|------|------|
| {Entity} | {1:1/1:N/N:M} | {fk} | {说明} |

---

> **维护说明**: 本文档在变更涉及新增或修改数据实体时更新。每次更新标注来源变更和更新时间。
> **兼容性**: 本文档与 detailed-design.md §二设计域章节（数据模型部分）保持结构兼容，归档时从 detailed-design.md 对应章节提取并合并。
