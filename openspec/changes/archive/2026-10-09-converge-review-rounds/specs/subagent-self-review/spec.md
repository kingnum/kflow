# Spec Delta

## MODIFIED Requirements

### Requirement: 子代理审查报告

每轮子代理完成审查后 SHALL 生成审查报告，内容与自审报告规范一致，且 SHALL 足以判定该轮是否为见证轮。

#### Scenario: 报告内容

- **WHEN** 子代理完成一轮审查
- **THEN** 生成审查报告，包含审查维度得分表、新发现问题清单、上轮问题修复验证、本轮修复内容、仍存在问题
- **AND** 报告保存路径为 `self-reviews/{phase}/{YYYYMMDD}-{HHMMSS}.md`
- **AND** 「新发现问题清单」为空、「本轮修复内容」为空且报告证明全维度全量遍历时，SHALL 可判定该轮为见证轮

#### Scenario: 主 Agent 读取报告

- **WHEN** 子代理返回审查报告路径
- **THEN** 主 Agent 读取报告内容
- **AND** 确认修复内容是否合理
- **AND** 判定该轮是否为见证轮
- **AND** 如修复不合理，主 Agent 可补充修复后再启动下一轮子代理

## ADDED Requirements

### Requirement: 自审由子代理按档位轮次上限串行执行

系统 SHALL 在 kflow-explore、kflow-prototype-design、kflow-design、kflow-plan 四个阶段的 SELFREV 步骤使用子代理（Agent subagent）执行自审，每轮启动独立子代理，串行执行**不少于 1 轮、不超过档位轮次上限**的轮次（上限由变更档位决定：`轻量` 1 轮、`标准` 2 轮、`完整` 5 轮）。SHALL NOT 存在 0 轮豁免；达成收敛终止条件（最近一轮为见证轮）时 SHALL 提前结束。其中 kflow-explore、kflow-design、kflow-plan 三阶段 SHALL 无条件执行 SELFREV；kflow-prototype-design 阶段 SHALL 仅在该变更选择「子代理自动审查验证」审查方式时执行 SELFREV，选择「人工审查」时 SHALL 完全跳过 SELFREV，SHALL NOT 保留兜底轮次。子代理意外停止时，主代理 MUST 重新创建子代理，SHALL NOT 接管执行。

#### Scenario: 子代理启动

- **WHEN** 阶段产物初稿生成完毕，进入 SELFREV 步骤
- **AND** 当前阶段为 kflow-explore、kflow-design、kflow-plan 之一，或当前阶段为 kflow-prototype-design 且该变更选择「子代理自动审查验证」审查方式
- **THEN** 主 Agent 启动第一轮子代理（Agent subagent）
- **AND** 子代理接收该阶段的产物文件路径和审查维度规则作为输入
- **AND** 子代理拥有独立上下文，不共享主 Agent 的对话历史

#### Scenario: 轻量档执行 1 轮自审

- **WHEN** 变更档位为 `轻量`
- **THEN** 系统 SHALL 执行 1 轮 SELFREV
- **AND** SHALL NOT 跳过 SELFREV，SHALL NOT 存在 0 轮豁免路径
- **AND** 产物完整性门控 SHALL 保留为附加硬门

#### Scenario: 串行执行至收敛或达上限

- **WHEN** 第 N 轮子代理完成并返回审查报告
- **THEN** 主 Agent 读取审查报告和修复后的产物
- **AND** 若第 N 轮为见证轮（零新发现、零修改、报告证明全维度全量遍历）→ 终止
- **AND** 否则确认修复内容后启动第 N+1 轮子代理（若 N < 轮次上限）
- **AND** SHALL NOT 同时启动多个子代理（禁止并行）
- **AND** SHALL NOT 为凑满轮次上限而继续执行

#### Scenario: 原型阶段选择人工审查时跳过 SELFREV

- **WHEN** 当前阶段为 kflow-prototype-design
- **AND** 该变更选择「人工审查」审查方式
- **THEN** 系统 SHALL 完全跳过 SELFREV 步骤
- **AND** SHALL NOT 启动任何自审子代理，SHALL NOT 保留兜底轮次
- **AND** 系统 SHALL 直接进入用户评审 REVIEW 步骤

#### Scenario: 子代理异常时主代理禁止接管

- **WHEN** 子代理意外停止、报错退出或返回要求重做/继续
- **THEN** 主代理 MUST 分析原因后重新创建新的子代理
- **AND** SHALL NOT 在主 Agent 上下文中接管子代理未完成的工作
- **AND** 新子代理的 prompt 包含上一轮的上下文和未完成的工作说明

## REMOVED Requirements

### Requirement: 自审由子代理按档位轮次串行执行

**Reason**: 轮次由「0/2/10 目标轮次」改为「下限 1、上限 1/2/5」，并引入见证轮收敛终止；轻量档不再存在 0 轮豁免。

**Migration**: 由新增的「自审由子代理按档位轮次上限串行执行」替代。
