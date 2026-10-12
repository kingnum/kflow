# Spec Delta

## MODIFIED Requirements

### Requirement: 自审由子代理按档位轮次上限串行执行

系统 SHALL 在 kflow-explore、kflow-prototype-design、kflow-design、kflow-plan 四个阶段的 SELFREV 步骤使用子代理（Agent subagent）执行自审，每轮启动独立子代理，串行执行**不少于 1 轮、不超过档位轮次上限**的轮次（上限由变更档位决定：`轻量` 1 轮、`标准` 2 轮、`完整` 5 轮）。SHALL NOT 存在 0 轮豁免；达成收敛终止条件（最近一轮为见证轮）时 SHALL 提前结束。审查循环到达终止点且累积未复核修复清单非空时，系统 SHALL 追加 1 轮复检轮——复检轮同样由独立子代理串行执行，SHALL NOT 消耗档位轮次预算，且单个阶段 SHALL 最多追加 1 轮。其中 kflow-explore、kflow-design、kflow-plan 三阶段 SHALL 无条件执行 SELFREV；kflow-prototype-design 阶段 SHALL 仅在该变更选择「子代理自动审查验证」审查方式时执行 SELFREV，选择「人工审查」时 SHALL 完全跳过 SELFREV，SHALL NOT 保留兜底轮次。子代理意外停止时，主代理 MUST 重新创建子代理，SHALL NOT 接管执行。

#### Scenario: 子代理启动

- **WHEN** 阶段产物初稿生成完毕，进入 SELFREV 步骤
- **AND** 当前阶段为 kflow-explore、kflow-design、kflow-plan 之一，或当前阶段为 kflow-prototype-design 且该变更选择「子代理自动审查验证」审查方式
- **THEN** 主 Agent 启动第一轮子代理（Agent subagent）
- **AND** 子代理接收该阶段的产物文件路径和审查维度规则作为输入
- **AND** 子代理拥有独立上下文，不共享主 Agent 的对话历史

#### Scenario: 轻量档执行 1 轮自审

- **WHEN** 变更档位为 `轻量`
- **THEN** 系统 SHALL 执行 1 轮审查轮 SELFREV
- **AND** SHALL NOT 跳过 SELFREV，SHALL NOT 存在 0 轮豁免路径
- **AND** 该轮产生修复时 SHALL 追加 1 轮复检轮
- **AND** 产物完整性门控 SHALL 保留为附加硬门

#### Scenario: 串行执行至收敛或达上限

- **WHEN** 第 N 轮子代理完成并返回审查报告
- **THEN** 主 Agent 读取审查报告和修复后的产物
- **AND** 若第 N 轮为见证轮（零新发现、零修改、报告证明全维度全量遍历）→ 终止
- **AND** 否则确认修复内容后启动第 N+1 轮子代理（若 N < 轮次上限）
- **AND** SHALL NOT 同时启动多个子代理（禁止并行）
- **AND** SHALL NOT 为凑满轮次上限而继续执行

#### Scenario: 轻量档第 1 轮含修复时追加复检轮

- **WHEN** 变更档位为 `轻量`
- **AND** 第 1 轮审查轮产生修复
- **THEN** 系统 SHALL 追加 1 轮复检轮
- **AND** SHALL NOT 因执行轮次达到档位上限 1 而直接进入非收敛分支

#### Scenario: 复检轮通过后终止

- **WHEN** 复检轮构成见证轮
- **THEN** 系统 SHALL 终止该阶段
- **AND** 终止原因 SHALL 记录为 `收敛（复检轮）`

#### Scenario: 复检轮未通过后进入非收敛分支

- **WHEN** 复检轮未构成见证轮
- **THEN** 系统 SHALL 终止该阶段
- **AND** 终止原因 SHALL 记录为 `达上限`
- **AND** 系统 SHALL 进入非收敛分支

#### Scenario: 原型阶段选择人工审查时跳过 SELFREV

- **WHEN** 当前阶段为 kflow-prototype-design
- **AND** 该变更选择「人工审查」审查方式
- **THEN** 系统 SHALL 完全跳过 SELFREV 步骤
- **AND** SHALL NOT 启动任何自审子代理，SHALL NOT 保留兜底轮次
- **AND** SHALL NOT 追加复检轮
- **AND** 系统 SHALL 直接进入用户评审 REVIEW 步骤

#### Scenario: 子代理异常时主代理禁止接管

- **WHEN** 子代理意外停止、报错退出或返回要求重做/继续
- **THEN** 主代理 MUST 分析原因后重新创建新的子代理
- **AND** SHALL NOT 在主 Agent 上下文中接管子代理未完成的工作
- **AND** 新子代理的 prompt 包含上一轮的上下文和未完成的工作说明
