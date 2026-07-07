# subagent-self-review Specification

## Purpose
定义三阶段（explore/prototype/design）SELFREV 步骤的子代理串行执行机制。自审从"当前阶段 Agent 自身执行"改为"独立子代理串行执行"，每轮子代理独立上下文、相同审查范围、边审边修。

## ADDED Requirements

### Requirement: 自审由子代理串行执行

系统 SHALL 在 kflow-explore、kflow-prototype-design、kflow-design 三个阶段的 SELFREV 步骤强制使用子代理（Agent subagent）执行自审，每轮启动独立子代理，10 轮顺序执行。

#### Scenario: 子代理启动
- **WHEN** 阶段产物初稿生成完毕，进入 SELFREV 步骤
- **THEN** 主 Agent 启动第一轮子代理（Agent subagent）
- **AND** 子代理接收该阶段的产物文件路径和审查维度规则作为输入
- **AND** 子代理拥有独立上下文，不共享主 Agent 的对话历史

#### Scenario: 串行执行 10 轮
- **WHEN** 第 N 轮子代理完成并返回审查报告
- **THEN** 主 Agent 读取审查报告和修复后的产物
- **AND** 主 Agent 确认修复内容后启动第 N+1 轮子代理
- **AND** SHALL NOT 同时启动多个子代理（禁止并行）
- **AND** 必须完成全部 10 轮后方可进入下一流程

### Requirement: 每轮子代理审查范围一致

每轮子代理 SHALL 执行该阶段全部审查维度的完整检查，范围与要求与其他轮次完全一致。

#### Scenario: explore 阶段子代理审查范围
- **WHEN** explore 阶段子代理执行自审
- **THEN** SHALL 独立执行完整性、闭环性、必要性、清晰性全部四个维度的完整检查
- **AND** SHALL NOT 将维度分组到不同轮次

#### Scenario: prototype 阶段子代理审查范围
- **WHEN** prototype 阶段子代理执行自审
- **THEN** SHALL 独立执行覆盖性、一致性、可用性、完整性全部四个维度的完整检查
- **AND** 覆盖性为第一优先级

#### Scenario: design 阶段子代理审查范围
- **WHEN** design 阶段子代理执行自审
- **THEN** SHALL 独立执行一致性、完备性、可行性、可测性全部四个维度的完整检查
- **AND** SHALL NOT 按轮次分组分配维度（废除分工制）

### Requirement: 子代理边审边修

子代理在审查过程中发现的问题 SHALL 直接修复产物文件，不限于生成审查报告。

#### Scenario: 发现问题直接修复
- **WHEN** 子代理在审查过程中确认了问题
- **THEN** 直接修复产物文件中的对应内容
- **AND** 在审查报告中记录修复内容

#### Scenario: 修复范围限制
- **WHEN** 子代理执行修复
- **THEN** SHALL 仅修复确认的问题，不做重构或额外改进
- **AND** SHALL NOT 新增功能（遵循"非必要不增加新功能"原则）

### Requirement: 子代理审查报告

每轮子代理完成审查后 SHALL 生成审查报告，内容与现有自审报告规范一致。

#### Scenario: 报告内容
- **WHEN** 子代理完成一轮审查
- **THEN** 生成审查报告，包含审查维度得分表、新发现问题清单、上轮问题修复验证、本轮修复内容、仍存在问题
- **AND** 报告保存路径为 `self-reviews/{phase}/{YYYYMMDD}-{HHMMSS}.md`

#### Scenario: 主 Agent 读取报告
- **WHEN** 子代理返回审查报告路径
- **THEN** 主 Agent 读取报告内容
- **AND** 确认修复内容是否合理
- **AND** 如修复不合理，主 Agent 可补充修复后再启动下一轮子代理
