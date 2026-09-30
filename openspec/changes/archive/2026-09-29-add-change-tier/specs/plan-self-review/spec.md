# Spec Delta

## ADDED Requirements

### Requirement: 计划阶段档位驱动的子代理自审

系统 SHALL 在 kflow-plan 阶段执行由变更档位决定轮次的子代理串行自循环审查（SELFREV）：轻量 0 轮、标准 2 轮、完整 10 轮。目标轮次大于 0 时，每轮 SHALL 启动独立子代理执行全部 4 个定制维度检查，不允许在达到目标轮次前终止。

#### Scenario: plan SELFREV 步骤位置

- **WHEN** kflow-plan 完成所有子变更 tasks.md 初稿后
- **THEN** 在步骤 8（VERIFY）之后、步骤 9（COMPLETE）之前插入 SELFREV 步骤
- **AND** SELFREV 步骤序号为 8.5，原 COMPLETE 步骤序号顺延为 9

#### Scenario: 轻量档跳过自审

- **WHEN** 变更档位为 `轻量`
- **THEN** kflow-plan SHALL 完全跳过 SELFREV 步骤
- **AND** SHALL NOT 启动任何自审子代理
- **AND** 系统 SHALL 以产物完整性门控替代自审门控

#### Scenario: 目标轮次强制执行

- **WHEN** plan SELFREV 执行中 且 目标轮次大于 0
- **THEN** SHALL 完成全部目标轮次子代理自审（标准 2 轮 / 完整 10 轮）
- **AND** SHALL NOT 因中间某轮无新问题而提前终止
- **AND** 即使连续多轮无新问题也必须完成全部目标轮次

#### Scenario: 子代理串行执行

- **WHEN** 第 N 轮子代理完成
- **THEN** 主 Agent 读取审查报告和修复后的产物
- **AND** 确认修复内容后启动第 N+1 轮子代理
- **AND** SHALL NOT 同时启动多个子代理（禁止并行）

## REMOVED Requirements

### Requirement: 计划阶段 10 轮子代理自审强制执行

**Reason**: 计划阶段自审由固定 10 轮改为由变更档位驱动，与执行类阶段轮次口径统一。固定 10 轮对轻量变更产生与大型变更相同的自审开销。

**Migration**: 改由本能力新增的「计划阶段档位驱动的子代理自审」确定轮次（轻量 0 轮 / 标准 2 轮 / 完整 10 轮）；维度表、报告格式与边审边修规则保持不变。
