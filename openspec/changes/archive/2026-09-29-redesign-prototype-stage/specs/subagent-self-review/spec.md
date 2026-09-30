# Spec Delta

## MODIFIED Requirements

### Requirement: 自审由子代理串行执行

系统 SHALL 在 kflow-explore、kflow-prototype-design、kflow-design、kflow-plan 四个阶段的 SELFREV 步骤使用子代理（Agent subagent）执行自审，每轮启动独立子代理，N 轮顺序执行（N 由 design-review-tiering 决定：explore/prototype/design 三阶段首次创建固定 10 轮、非首次创建弹性轮次下限 1 轮；kflow-plan 维持 10 轮）。其中 kflow-explore、kflow-design、kflow-plan 三阶段 SHALL 无条件执行 SELFREV；kflow-prototype-design 阶段 SHALL 仅在该变更选择「子代理自动审查验证」审查方式时执行 SELFREV，选择「人工审查」时 SHALL 完全跳过 SELFREV，SHALL NOT 保留兜底轮次。子代理意外停止时，主代理 MUST 重新创建子代理，SHALL NOT 接管执行。

#### Scenario: 子代理启动
- **WHEN** 阶段产物初稿生成完毕，进入 SELFREV 步骤
- **AND** 当前阶段为 kflow-explore、kflow-design、kflow-plan 之一，或当前阶段为 kflow-prototype-design 且该变更选择「子代理自动审查验证」审查方式
- **THEN** 主 Agent 启动第一轮子代理（Agent subagent）
- **AND** 子代理接收该阶段的产物文件路径和审查维度规则作为输入
- **AND** 子代理拥有独立上下文，不共享主 Agent 的对话历史

#### Scenario: 串行执行 10 轮
- **WHEN** 第 N 轮子代理完成并返回审查报告
- **AND** 当前阶段 SHALL 执行 SELFREV（kflow-explore、kflow-design、kflow-plan 无条件适用；kflow-prototype-design 仅在该变更选择「子代理自动审查验证」审查方式时适用）
- **THEN** 主 Agent 读取审查报告和修复后的产物
- **AND** 主 Agent 确认修复内容后启动第 N+1 轮子代理
- **AND** SHALL NOT 同时启动多个子代理（禁止并行）
- **AND** 必须完成全部目标轮次（首次创建 10 轮、非首次创建弹性轮次，kflow-plan 固定 10 轮）后方可进入下一流程

#### Scenario: 原型阶段选择人工审查时跳过 SELFREV
- **WHEN** 当前阶段为 kflow-prototype-design
- **AND** 该变更选择「人工审查」审查方式
- **THEN** 系统 SHALL 完全跳过 SELFREV 步骤
- **AND** SHALL NOT 启动任何自审子代理，SHALL NOT 保留兜底轮次
- **AND** 系统 SHALL 直接进入用户评审 REVIEW 步骤

#### Scenario: 子代理异常时主代理禁止接管（新增）
- **WHEN** 子代理意外停止、报错退出或返回要求重做/继续
- **THEN** 主代理 MUST 分析原因后重新创建新的子代理
- **AND** SHALL NOT 在主 Agent 上下文中接管子代理未完成的工作
- **AND** 新子代理的 prompt 包含上一轮的上下文和未完成的工作说明

### Requirement: 每轮子代理审查范围一致

每轮子代理 SHALL 执行该阶段全部审查维度的完整检查，范围与要求与其他轮次完全一致。

#### Scenario: explore 阶段子代理审查范围
- **WHEN** explore 阶段子代理执行自审
- **THEN** SHALL 独立执行完整性、闭环性、必要性、清晰性全部四个维度的完整检查
- **AND** SHALL NOT 将维度分组到不同轮次

#### Scenario: prototype 阶段子代理审查范围
- **WHEN** prototype 阶段子代理执行自审
- **AND** 该变更选择「子代理自动审查验证」审查方式
- **THEN** SHALL 独立执行覆盖性、一致性、可用性、完整性全部四个维度的完整检查
- **AND** 覆盖性为第一优先级

#### Scenario: design 阶段子代理审查范围
- **WHEN** design 阶段子代理执行自审
- **THEN** SHALL 独立执行一致性、完备性、可行性、可测性全部四个维度的完整检查
- **AND** SHALL NOT 按轮次分组分配维度（废除分工制）

#### Scenario: plan 阶段子代理审查范围（新增）
- **WHEN** plan 阶段子代理执行自审
- **THEN** SHALL 独立执行任务覆盖完整性、DoD 验收标准正确性、HITL 标注准确性、任务粒度合理性全部四个维度的完整检查
- **AND** SHALL NOT 将维度分组到不同轮次
