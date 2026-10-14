# design-review-tiering Specification

## Purpose

定义设计多视角审查按变更档位分级执行：轻量档走简化模式（单 Agent 串行综合审查），标准档走两视角并行审查，在保证审查质量的同时降低小变更的审查成本。

## Requirements

### Requirement: 设计审查按变更档位分级

系统 SHALL 依据变更的变更档位（变更级 `.status.md` 基本信息中的 `变更档位` 字段，取值 `{轻量|标准}`）决定设计审查的执行模式。字段缺失或取值为历史遗留的 `完整` 时，系统 SHALL 按 `标准` 档决定执行模式。

#### Scenario: 轻量档走简化模式

- **WHEN** 变更档位为 `轻量`
- **THEN** 设计审查 SHALL 采用简化模式（单视角综合审查）

#### Scenario: 标准档走两视角模式

- **WHEN** 变更档位为 `标准`
- **THEN** 设计审查 SHALL 采用两视角并行审查

#### Scenario: 完整档走完整模式

- **WHEN** 读取到的变更档位为历史遗留的 `完整`
- **THEN** 设计审查 SHALL 采用两视角并行审查
- **AND** SHALL NOT 进入四视角并行路径

### Requirement: 简化模式（单视角综合审查）

轻量档变更 SHALL 使用单个 Agent 串行执行综合审查，覆盖业务/技术/安全/质量四视角的全部检查项，单轮输出单一综合报告，不执行分级重审闭环。

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

### Requirement: 标准档两视角设计审查

变更档位为 `标准` 时，设计审查 SHALL 采用两视角并行审查：视角一覆盖业务与技术，视角二覆盖安全与质量。每个视角 SHALL 由独立 Agent 执行，输出两份视角报告与一份综合报告。

#### Scenario: 标准档审查执行

- **WHEN** 变更档位为 `标准` 且设计审查启动
- **THEN** 系统 SHALL 并行启动两个审查 Agent（业务+技术视角、安全+质量视角）

#### Scenario: 标准档审查产物

- **WHEN** 标准档设计审查完成
- **THEN** `cross-reviews/{timestamp}/` 目录 SHALL 包含 business-technical-review.md、security-quality-review.md、synthesis.md
- **AND** SHALL NOT 生成四份独立视角报告

#### Scenario: 标准档视角检查项覆盖

- **WHEN** 标准档设计审查执行
- **THEN** 业务+技术视角 SHALL 覆盖业务视角与技术视角的全部检查项
- **AND** 安全+质量视角 SHALL 覆盖安全视角与质量视角的全部检查项

### Requirement: 进入计划门控适配审查模式

进入计划阶段的门控 SHALL 接受两种审查模式的产物——两视角模式检查两份视角报告与 synthesis.md，简化模式仅检查单一综合报告。

#### Scenario: 完整模式门控

- **WHEN** 变更档位读取为历史遗留的 `完整`
- **THEN** 门控 SHALL 检查 `cross-reviews/{timestamp}/` 存在两份视角报告且 synthesis.md 标记审查通过
- **AND** SHALL NOT 要求四份独立视角报告存在

#### Scenario: 标准模式门控

- **WHEN** 变更档位为 `标准`
- **THEN** 门控 SHALL 检查 `cross-reviews/{timestamp}/` 存在两份视角报告且 synthesis.md 标记审查通过
- **AND** SHALL NOT 检查四份独立视角报告

#### Scenario: 简化模式门控

- **WHEN** 变更档位为 `轻量`
- **THEN** 门控 SHALL 检查 `cross-reviews/{timestamp}/synthesis.md` 存在且标记审查通过
- **AND** SHALL NOT 检查独立视角报告
