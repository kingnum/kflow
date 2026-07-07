## Context

`kflow-resume` SKILL.md frontmatter 缺少 version 字段。此变更的处理取决于 `unified-version-management` 的最终决策。

## Goals / Non-Goals

**Goals:**
- 确保 kflow-resume 版本定义与体系统一

**Non-Goals:**
- 如果统一方案是移除 version 字段，本变更为空操作

## Decisions

### D1: 条件处理

- 若 `unified-version-management` 已先行完成：确认 kflow-resume 无 version 字段即可
- 若 `unified-version-management` 未先行：本变更标记为"待 unified-version-management 完成后确认"

## Risks / Trade-offs

无风险。
