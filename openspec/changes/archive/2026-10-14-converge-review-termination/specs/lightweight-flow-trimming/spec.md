# Spec Delta

## MODIFIED Requirements

### Requirement: 功能点类型混合时的升档

轻量档的单一子变更前提在功能点类型混合时不成立（子变更类型严格二分为后端子变更或前端子变更）。此时系统 SHALL 将变更档位升为 `标准` 后按标准档流程重新划分子变更，SHALL NOT 直接阻塞。

#### Scenario: 类型混合触发升档

- **WHEN** 变更档位为 `轻量` 且 所含功能点同时存在「后端」与「前端」类型
- **THEN** 系统 SHALL 将变更档位升为 `标准`
- **AND** SHALL 按标准档流程执行子变更划分
- **AND** SHALL NOT 以类型混合为由阻塞变更

#### Scenario: 升档后重跑受影响的阶段行为

- **WHEN** 轻量档因功能点类型混合升档为 `标准`
- **THEN** 后续阶段 SHALL 按标准档的审查形态与产出深度执行
- **AND** 阶段适用性声明 SHALL NOT 生成
