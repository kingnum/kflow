# Spec Delta

## MODIFIED Requirements

### Requirement: 设计自审按首次/非首次分级

系统 SHALL 依据项目是否已有设计基础决定设计三阶段（kflow-explore、kflow-prototype-design、kflow-design）SELFREV 自审的执行模式：首次创建走完整自审（固定 10 轮），非首次创建走弹性自审（弹性轮次 + 评分底线）。其中 kflow-explore、kflow-design 两阶段的 SELFREV 分级 SHALL 无条件适用；kflow-prototype-design 阶段的 SELFREV 分级 SHALL 仅在该变更选择「子代理自动审查验证」审查方式时适用，该变更选择「人工审查」时 prototype 阶段 SHALL 完全跳过 SELFREV，本节分级规则不适用（SHALL NOT 保留兜底轮次）。

#### Scenario: 首次创建走完整自审
- **WHEN** 项目无设计基础（首次创建）
- **AND** 当前阶段为 kflow-explore、kflow-design 之一，或当前阶段为 kflow-prototype-design 且该变更选择「子代理自动审查验证」审查方式
- **THEN** SELFREV SHALL 固定执行 10 轮自审

#### Scenario: 非首次创建走弹性自审
- **WHEN** 项目已有设计基础（非首次创建）
- **AND** 当前阶段为 kflow-explore、kflow-design 之一，或当前阶段为 kflow-prototype-design 且该变更选择「子代理自动审查验证」审查方式
- **THEN** SELFREV SHALL 按弹性轮次（下限 1 轮）+ 评分底线执行

#### Scenario: prototype 阶段选择人工审查时分级规则不适用
- **WHEN** 当前阶段为 kflow-prototype-design
- **AND** 该变更选择「人工审查」审查方式
- **THEN** 本节 SELFREV 分级规则 SHALL NOT 适用
- **AND** prototype 阶段 SHALL 完全跳过 SELFREV，不计算目标轮次、不执行评分底线判定
