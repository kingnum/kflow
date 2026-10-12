# Spec Delta

## MODIFIED Requirements

### Requirement: 收敛终止条件

系统 SHALL 以**见证轮**作为收敛终止判据。见证轮定义为同时满足以下三条的一轮审查：(a) 零新发现问题；(b) 零修复/零修改；(c) 审查报告证明全部审查维度已完成全量遍历。

终止判定 SHALL 分两步执行。第一步：主 Agent 判定累积未复核修复清单是否为空。第二步按清单状态分支——清单为空时，终止条件 SHALL 为「执行轮次 >= 1（全局下限）且最近一轮为见证轮」，或「执行轮次 = 轮次上限」；清单非空时，系统 SHALL 追加 1 轮复检轮，该轮 SHALL NOT 消耗档位轮次预算，且在单个阶段内 SHALL 最多追加 1 轮。

复检轮构成见证轮时系统 SHALL 终止该阶段；复检轮未构成见证轮时，系统 SHALL 终止并进入非收敛分支。

达到轮次上限、且不存在通过的复检轮、且无任何一轮为见证轮时，系统 SHALL 进入**非收敛分支**：记录到 `skill-suggestion.md`、使用 AskUserQuestion 询问用户，并可将该阶段标记为 ⚠️ 阻塞。

阶段终止时系统 SHALL 在 `.status.md` 写入终止原因，取值 `收敛`、`收敛（复检轮）` 或 `达上限`。

复检轮的触发条件、预算规则、复核范围、通过判据与结果写入的完整定义见 `recheck-round` 能力，本能力 SHALL NOT 另行定义。

#### Scenario: 见证轮达成即终止

- **WHEN** 某轮同时满足零新发现、零修改且报告证明全维度全量遍历
- **AND** 执行轮次 >= 1
- **THEN** 阶段 SHALL 终止
- **AND** 终止原因 SHALL 记录为 `收敛`

#### Scenario: 未达成见证轮则继续

- **WHEN** 本轮存在新发现或存在修复/修改
- **AND** 执行轮次 < 轮次上限
- **THEN** 系统 SHALL 继续下一轮

#### Scenario: 累积未复核修复清单非空时追加复检轮

- **WHEN** 执行轮次 = 轮次上限
- **AND** 无任何一轮为见证轮
- **AND** 累积未复核修复清单非空
- **THEN** 系统 SHALL 追加 1 轮复检轮
- **AND** 该轮 SHALL NOT 消耗档位轮次预算
- **AND** SHALL NOT 在此时进入非收敛分支

#### Scenario: 复检轮通过后终止

- **WHEN** 复检轮构成见证轮
- **THEN** 阶段 SHALL 终止
- **AND** 终止原因 SHALL 记录为 `收敛（复检轮）`

#### Scenario: 复检轮未通过后进入非收敛分支

- **WHEN** 复检轮未构成见证轮
- **THEN** 阶段 SHALL 终止
- **AND** 终止原因 SHALL 记录为 `达上限`
- **AND** 系统 SHALL 进入非收敛分支

#### Scenario: 达上限仍无见证轮进入非收敛分支

- **WHEN** 执行轮次 = 轮次上限 且 无任何一轮为见证轮
- **AND** 不存在通过的复检轮
- **THEN** 系统 SHALL 记录到 `skill-suggestion.md`
- **AND** SHALL 使用 AskUserQuestion 询问用户
- **AND** 终止原因 SHALL 记录为 `达上限`
- **AND** 系统 MAY 将该阶段标记为 ⚠️ 阻塞

#### Scenario: 见证轮不得为空转轮

- **WHEN** 某轮报告未证明全部审查维度已完成全量遍历
- **THEN** 该轮 SHALL NOT 被判定为见证轮
- **AND** 系统 SHALL 继续下一轮
