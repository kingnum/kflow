---
stage: 归档
skill: kflow-archive
version: 1.0.0
created_at: 2026-05-06
template_for: docs/changes/index.md
template_description: 变更管理索引模板，记录活跃变更列表和已归档变更列表。由 kflow-archive 在归档操作时更新（从活跃列表移除，添加到已归档列表）。新建变更时由 kflow-explore 在活跃列表中添加。
---

# 变更管理索引

> **更新时间**: {YYYY-MM-DD HH:MM}

## 活跃变更

| 变更名称 | 类型 | 项目类型 | 当前阶段 | 影响文件 | 创建时间 |
|----------|------|---------|----------|---------|----------|
| {change-1} | {产品需求/功能需求/功能缺陷} | {前后端项目/纯后端项目} | {阶段名称} | {影响文件路径} | {YYYY-MM-DD} |
| {change-2} | {产品需求/功能需求/功能缺陷} | {前后端项目/纯后端项目} | {阶段名称} | {影响文件路径} | {YYYY-MM-DD} |

## 已归档变更

| 变更名称 | 归档时间 | 归档状态 | 归档目录 |
|----------|----------|----------|----------|
| {change-old} | {YYYY-MM-DD} | {完成/未完成} | docs/archive/{YYYY-MM-DD}-{change-old}/ |
