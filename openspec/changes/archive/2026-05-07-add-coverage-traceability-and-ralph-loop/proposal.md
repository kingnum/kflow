## Why

当前 Skills 体系缺少从功能点到各阶段产物的全链路覆盖追溯，无法机械化验证"每个功能点是否在所有阶段产物中都有对应落点"，导致覆盖率依赖人工检查。同时，执行类阶段（计划/编码/审查/测试/集成测试/缺陷修复）缺少统一的子代理迭代执行机制，输出质量波动大，缺乏验收闭环。本次变更建立覆盖追溯矩阵和 ralph-loop 子代理执行模型，实现 100% 覆盖可验证 + 迭代验收闭环。

## What Changes

- 新增 `docs/changes/{change}/traceability.md` 覆盖追溯矩阵文件，独立维护，各阶段完成后各自填写对应列
- 新增覆盖率门控规则：每个执行阶段完成时验证 traceability.md 对应列覆盖率 = 100%
- 执行类阶段（计划/编码/审查/测试/集成测试/缺陷修复）统一采用 ralph-loop 子代理执行模式
- 新增子代理复杂度评估机制：按功能点数/接口数/场景数自动计算建议迭代轮次（5-10 次）
- 新增子代理验收流程：主 Agent 验收覆盖率 → 记录 skill-suggestion.md → 询问是否重跑
- 创造性阶段（设计探索/原型设计/详细设计/归档/审计）维持主 Agent 直连，不强制子代理

## Capabilities

### New Capabilities
- `coverage-traceability`: 全链路覆盖追溯矩阵 — traceability.md 文件定义、FP×阶段产物覆盖映射、覆盖率门控规则、缺口自动发现与追踪
- `ralph-loop-subagent-execution`: ralph-loop 子代理执行模型 — 执行类阶段子代理调度、复杂度评估、迭代轮次确定、COMPLETED 完成承诺、主 Agent 验收闭环、验收失败记录与重跑询问

### Modified Capabilities
<!-- 本次为全新机制，无需修改现有 capability 的 spec -->

## Impact

- **新增文件**: `docs/changes/{change}/traceability.md`（变更级产物）、`docs/designs/templates/change/traceability.md`（模板）
- **修改文件**: `docs/designs/core-mechanisms.md`（新增 §十四 覆盖追溯机制、§十五 子代理执行模型、门控规则扩展）、`docs/designs/overview.md`（设计决策表、实施计划更新）
- **修改 Skill 文件**: `kflow-design`（创建 traceability.md）、`kflow-plan`、`kflow-code`、`kflow-code-review`、`kflow-e2e-test`、`kflow-bug-fix`、`kflow-integration-test`（集成 ralph-loop 子代理模式）
- **不涉及**: MCP 工具、外部 API、数据库 schema
