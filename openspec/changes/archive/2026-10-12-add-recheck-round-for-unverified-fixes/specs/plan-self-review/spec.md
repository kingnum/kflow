# Spec Delta

## MODIFIED Requirements

### Requirement: 计划阶段档位驱动轮次上限的子代理自审

系统 SHALL 在 kflow-plan 阶段执行由变更档位决定轮次上限的子代理串行自循环审查（SELFREV）：`轻量` 1 轮、`标准` 2 轮、`完整` 5 轮。每轮 SHALL 启动独立子代理执行全部 4 个定制维度检查；执行轮次 SHALL 不少于 1 轮，达成收敛终止条件（最近一轮为见证轮）时 SHALL 提前结束，SHALL NOT 为凑满上限而继续执行。审查循环到达终止点且累积未复核修复清单非空时，系统 SHALL 追加 1 轮复检轮，逐项复核清单内全部修复；该轮 SHALL NOT 消耗档位轮次上限，且 SHALL 最多追加 1 轮。

#### Scenario: plan SELFREV 步骤位置

- **WHEN** kflow-plan 完成所有子变更 tasks.md 初稿后
- **THEN** 在步骤 8（VERIFY）之后、步骤 9（COMPLETE）之前插入 SELFREV 步骤
- **AND** SELFREV 步骤序号为 8.5，原 COMPLETE 步骤序号顺延为 9

#### Scenario: 轻量档执行 1 轮自审

- **WHEN** 变更档位为 `轻量`
- **THEN** kflow-plan SHALL 执行 1 轮审查轮 SELFREV
- **AND** SHALL NOT 跳过 SELFREV
- **AND** 该轮产生修复时 SHALL 追加 1 轮复检轮
- **AND** 产物完整性门控 SHALL 保留为附加硬门

#### Scenario: 收敛或达上限终止

- **WHEN** plan SELFREV 执行中
- **THEN** 最近一轮为见证轮（零新发现、零修改、报告证明 4 维度全量遍历）时 SHALL 终止
- **AND** 否则继续下一轮，直至轮次达到上限（轻量 1 / 标准 2 / 完整 5）
- **AND** SHALL NOT 因存在新发现问题而强制走满上限

#### Scenario: 终止点清单非空时追加复检轮

- **WHEN** plan SELFREV 到达终止点（最近一轮为见证轮，或已达到档位轮次上限）
- **AND** 累积未复核修复清单非空
- **THEN** 系统 SHALL 追加 1 轮复检轮
- **AND** 该轮 SHALL NOT 计入档位轮次上限
- **AND** 该轮 SHALL 逐项复核清单内全部修复，并证明 4 维度已完成全量遍历

#### Scenario: 复检轮通过后终止

- **WHEN** 复检轮零新发现、零修改、证明 4 维度全量遍历且清单内全部修复逐项复核通过
- **THEN** 系统 SHALL 终止 plan SELFREV
- **AND** 终止原因 SHALL 记录为 `收敛（复检轮）`

#### Scenario: 复检轮未通过后终止

- **WHEN** 复检轮未满足通过判据
- **THEN** 系统 SHALL 终止 plan SELFREV
- **AND** 终止原因 SHALL 记录为 `达上限`
- **AND** 系统 SHALL 进入非收敛分支

#### Scenario: 子代理串行执行

- **WHEN** 第 N 轮子代理完成
- **THEN** 主 Agent 读取审查报告和修复后的产物
- **AND** 确认修复内容后启动第 N+1 轮子代理
- **AND** SHALL NOT 同时启动多个子代理（禁止并行）
