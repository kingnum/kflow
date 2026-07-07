## Context

`kflow-code` 设计文档包含共享文件冲突预防和前后端文件隔离规则，未在 SKILL.md 中体现。多子变更并行编码时，缺少这些规则可能导致文件冲突和域越界。

## Goals / Non-Goals

**Goals:**
- SKILL.md 补齐共享文件冲突预防规则（4 条）
- SKILL.md 补齐前后端文件隔离规则（域目录定义 + FP>10 策略）

**Non-Goals:**
- 不修改设计文档

## Decisions

### D1: 共享文件冲突预防

从设计文档同步 4 条规则：
1. 识别共享文件（shared-types/、service-guide.md 等）
2. Agent 禁止直接修改共享文件
3. wait-for-all 模式（所有子变更编码完成后由主 Agent 统一处理共享文件）
4. 冲突回滚规则

### D2: 前后端文件隔离

从设计文档同步：
- 前端域目录范围：src/pages, components, router, store, styles, layouts
- 后端域目录范围：src/api, services, models, db, middleware
- 前端 FP>10 时的骨架子变更 + 页面组子变更策略

### D3: 插入位置

在执行流程的编码步骤之前添加（作为约束前置检查）。

## Risks / Trade-offs

无显著风险。
