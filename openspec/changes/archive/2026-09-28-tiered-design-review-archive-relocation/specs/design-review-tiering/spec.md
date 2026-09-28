# Spec Delta

## Purpose

定义设计四视角审查按变更类型分级执行：功能缺陷级走简化模式（单视角综合审查），功能需求级/产品需求级走完整模式（四视角并行审查），在保证审查质量的同时降低小变更的审查成本。

## ADDED Requirements

### Requirement: 设计审查按变更类型分级

系统 SHALL 依据变更的变更类型（`.status.md` 基本信息中的 `{产品需求|功能需求|功能缺陷}`）决定设计四视角审查的执行模式。

#### Scenario: 功能缺陷级走简化模式
- **WHEN** 变更类型为功能缺陷级
- **THEN** 设计审查 SHALL 采用简化模式（单视角综合审查）

#### Scenario: 功能需求级走完整模式
- **WHEN** 变更类型为功能需求级
- **THEN** 设计审查 SHALL 采用完整模式（四视角并行审查）

#### Scenario: 产品需求级走完整模式
- **WHEN** 变更类型为产品需求级
- **THEN** 设计审查 SHALL 采用完整模式（四视角并行审查）

### Requirement: 简化模式（单视角综合审查）

功能缺陷级变更 SHALL 使用单个 Agent 串行执行综合审查，覆盖业务/技术/安全/质量四视角的全部检查项，单轮输出单一综合报告，不执行分级重审闭环。

#### Scenario: 简化模式审查执行
- **WHEN** 简化模式设计审查启动
- **THEN** 系统 SHALL 使用单个 Agent 串行检查业务/技术/安全/质量四视角的全部检查项

#### Scenario: 简化模式产物
- **WHEN** 简化模式审查完成
- **THEN** 系统 SHALL 输出单一综合报告到 `cross-reviews/{timestamp}/synthesis.md`
- **AND** SHALL NOT 生成 business-review.md、technical-review.md、security-review.md、quality-review.md 四份独立视角报告

#### Scenario: 简化模式无分级重审
- **WHEN** 简化模式审查发现高严重度问题
- **THEN** 修复后 SHALL 仍走单视角单轮复检
- **AND** SHALL NOT 执行 review-closed-loop 的分级重审闭环（高/中/低差异化的多批次验证）

### Requirement: 完整模式（四视角并行审查）

功能需求级/产品需求级变更 SHALL 使用四个并行 Agent 分别执行业务/技术/安全/质量四视角审查，输出四份视角报告与综合报告，并执行 review-closed-loop 的分级重审闭环。

#### Scenario: 完整模式审查执行
- **WHEN** 完整模式设计审查启动
- **THEN** 系统 SHALL 并行启动四个审查 Agent（业务/技术/安全/质量）

#### Scenario: 完整模式产物
- **WHEN** 完整模式审查完成
- **THEN** 系统 SHALL 输出 `cross-reviews/{timestamp}/` 目录
- **AND** 目录 SHALL 包含 business-review.md、technical-review.md、security-review.md、quality-review.md、synthesis.md

#### Scenario: 完整模式闭环
- **WHEN** 完整模式审查发现高/中/低严重度问题
- **THEN** 系统 SHALL 执行 review-closed-loop 的分级重审闭环

### Requirement: 进入计划门控适配审查模式

进入计划阶段的门控 SHALL 接受两种审查模式的产物——完整模式检查四份视角报告与 synthesis.md，简化模式仅检查单一综合报告。

#### Scenario: 完整模式门控
- **WHEN** 变更类型为功能需求级或产品需求级
- **THEN** 门控 SHALL 检查 `cross-reviews/` 存在四份视角报告且 synthesis.md 标记审查通过

#### Scenario: 简化模式门控
- **WHEN** 变更类型为功能缺陷级
- **THEN** 门控 SHALL 检查 `cross-reviews/{timestamp}/synthesis.md` 存在且标记审查通过
- **AND** SHALL NOT 检查四份独立视角报告

### Requirement: 审计审查维度适配审查模式

kflow-audit 的「审查 20%」维度 SHALL 按审查模式分别给分，简化模式不算缺项、不因产物少而误扣。

#### Scenario: 简化模式审计
- **WHEN** 审计变更采用简化模式审查
- **THEN** 「审查」维度 SHALL 依据单一综合报告给分
- **AND** SHALL NOT 因缺少四份视角报告而判为缺项或扣分

#### Scenario: 完整模式审计
- **WHEN** 审计变更采用完整模式审查
- **THEN** 「审查」维度 SHALL 依据四份视角报告与 synthesis.md 给分
