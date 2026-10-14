# Spec Delta

## MODIFIED Requirements

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

## REMOVED Requirements

### Requirement: 完整模式（四视角并行审查）

**Reason**: 变更档位枚举由三档收敛为 `{轻量, 标准}` 二档，`完整` 取值废除，四视角并行审查不再有触发档位。该模式与两视角模式的检查项集合完全相同（检查项不得随并行度缩减），其唯一差异为并行度，不再支撑独立的审查模式。

**Migration**: 原 `完整` 档变更按 `标准` 档执行两视角并行审查（业务+技术 / 安全+质量），检查项覆盖不变。历史 `cross-reviews/{timestamp}/` 下已产出的四份独立视角报告保留为历史记录，读取侧 SHALL NOT 要求其存在，亦 SHALL NOT 因其存在而阻塞门控。

### Requirement: 审计审查维度适配审查模式

**Reason**: 审计已无评分维度——`devflow-audit` 的四项记账职责不包含四维度评分，本要求的前提（按档位对应的审查形态给分）已不存在，且与「审计报告 SHALL NOT 包含四维度评分表与加权总分」直接矛盾。

**Migration**: 审计对设计审查产物的校验改由 `devflow-audit` 的门控校验职责承担——按本能力与门控规则检查该档位要求的视角报告与 synthesis.md 是否存在且标记通过；不再产生「审查」维度得分。
