# archive-manual-entry Specification

## Purpose
归档阶段禁止自动流转，MUST 用户显式确认后方可进入。

## Requirements

### Requirement: 归档阶段禁止自动流转

归档阶段 SHALL NOT 被任何前置阶段自动调度进入。审计（kflow-audit）通过后 MUST 通过 AskUserQuestion 获取用户显式确认后方可进入归档阶段。

#### Scenario: 审计通过后不自动进入归档

- **WHEN** kflow-audit 阶段完成且审计通过
- **THEN** 系统 SHALL NOT 自动调度进入 kflow-archive 阶段
- **AND** 系统 SHALL 通过 AskUserQuestion 询问用户：「审计已通过，是否进入归档阶段？」
- **AND** 选项包含：确认归档 / 暂时不归档 / 需要进一步验证

#### Scenario: 用户确认后进入归档

- **WHEN** 用户在 AskUserQuestion 中选择「确认归档」
- **THEN** 系统 SHALL 进入 kflow-archive 阶段
- **AND** 按现有归档流程执行（设计合并 → 目录移动 → 索引更新）

#### Scenario: 用户拒绝归档时保持当前状态

- **WHEN** 用户在 AskUserQuestion 中选择「暂时不归档」或「需要进一步验证」
- **THEN** 系统 SHALL NOT 进入归档阶段
- **AND** 变更保持在 audit 完成状态
- **AND** 用户可在验证后手动调用 kflow-archive

### Requirement: Archive 是唯一禁止自动流转的阶段

归档阶段 SHALL 是 KFlow 体系中唯一禁止自动流转的阶段。其他阶段（explore → prototype-design → design → plan → code → code-review → api-test → e2e-test → integration-test → audit）的流转可在门控通过后自动或半自动调度。

#### Scenario: 其他阶段允许自动流转

- **WHEN** 非归档阶段的门控检查通过
- **THEN** 后续阶段可按现有机制自动或半自动调度进入
- **AND** 归档阶段为此规则的唯一例外

#### Scenario: 归档阶段标记为手动入口

- **WHEN** kflow-archive 的 SKILL.md 定义触发条件
- **THEN** 触发语义 SHALL 强调用户主动调用（如「用户确认归档」「手动进入归档」）
- **AND** SHALL NOT 包含「自动」「自动调度」等语义

### Requirement: 归档确认前的信息展示

系统 SHALL 在询问用户是否进入归档前，展示完整的决策所需信息。

#### Scenario: 展示归档决策信息

- **WHEN** kflow-audit 完成且审计通过
- **THEN** 系统 SHALL 在 AskUserQuestion 中展示：变更名称、所有子变更完成状态、集成测试结果摘要、E2E 测试覆盖率、审计结论摘要
- **AND** 用户可据此做出是否归档的决策
