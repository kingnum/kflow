# subagent-self-review Specification

## Purpose

定义三阶段（explore/prototype/design）SELFREV 步骤的子代理串行执行机制。自审从"当前阶段 Agent 自身执行"改为"独立子代理串行执行"，每轮子代理独立上下文、审查维度完整且审查对象集合按轮冻结、边审边修；终止口径为收敛驱动（见证轮四项判据为唯一成功终止条件，不收敛时升级用户）。

## Requirements

### Requirement: 每轮子代理审查维度完整且审查对象冻结

每轮子代理 SHALL 执行该阶段全部审查维度的完整检查，维度集合 SHALL 为封闭枚举、SHALL NOT 新增；审查对象集合 SHALL 由主 Agent 在每轮开始时从阶段产物既有内容生成并冻结，子代理 SHALL NOT 扩大。跨轮审查对象集合 MAY 因阶段输入变化（如回退重执行新增受影响项）由主 Agent 更新。

#### Scenario: explore 阶段子代理审查范围

- **WHEN** explore 阶段子代理执行自审
- **THEN** SHALL 独立执行完整性、闭环性、必要性、清晰性全部四个维度的完整检查
- **AND** SHALL NOT 将维度分组到不同轮次
- **AND** SHALL NOT 新增任何维度

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

#### Scenario: 审查对象集合由主 Agent 冻结注入

- **WHEN** 主 Agent 构建某轮自审子代理的 prompt
- **THEN** prompt SHALL 包含由阶段产物既有内容生成的本轮审查对象清单
- **AND** 子代理 SHALL NOT 审查该清单之外的产物或文件

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
- **AND** SHALL NOT 新增冻结审查对象集合之外的产物内容（功能点、字段、章节、分支）

#### Scenario: 范围外发现降级为范围外观察

- **WHEN** 子代理在冻结审查对象集合之外发现问题
- **THEN** SHALL NOT 在本轮修复该问题
- **AND** SHALL NOT 将其计入本轮新发现数
- **AND** SHALL 记为「范围外观察」写入本轮审查报告的「范围外观察」小节

### Requirement: 子代理审查报告

每轮子代理完成审查后 SHALL 生成审查报告，内容与自审报告规范一致，且 SHALL 足以判定该轮是否为见证轮。

#### Scenario: 报告内容

- **WHEN** 子代理完成一轮审查
- **THEN** 生成审查报告，包含审查维度得分表、新发现问题清单、上轮问题修复验证、本轮修复内容、仍存在问题、**范围外观察**
- **AND** 报告 SHALL 证明本轮已完成全部审查维度与全部审查对象的全量遍历
- **AND** 报告保存路径为 `self-reviews/{phase}/{YYYYMMDD}-{HHMMSS}.md`
- **AND** 「新发现问题清单」为空、「本轮修复内容」为空、报告证明全维度全量遍历、且累积未复核修复清单内全部条目逐项复核通过时，SHALL 判定该轮为见证轮
- **AND** 「范围外观察」小节为空时 SHALL 记为「（空）」

#### Scenario: 主 Agent 读取报告

- **WHEN** 子代理返回审查报告路径
- **THEN** 主 Agent 读取报告内容
- **AND** 确认修复内容是否合理
- **AND** 判定该轮是否为见证轮
- **AND** 校验本轮审查对象是否超出冻结范围；超出时 SHALL 拒收该轮并要求子代理在冻结范围内重审
- **AND** 汇总「范围外观察」条目，在阶段终止时向用户提示
- **AND** 如修复不合理，主 Agent 可补充修复后再启动下一轮子代理

### Requirement: 自审由子代理串行执行至收敛

系统 SHALL 在 kflow-explore、kflow-prototype-design、kflow-design、kflow-plan 四个阶段的 SELFREV 步骤使用子代理（Agent subagent）执行自审，每轮启动独立子代理，串行执行**不少于 1 轮**的轮次，SHALL NOT 预置或受限于任何轮数上限。SHALL NOT 存在 0 轮豁免；达成收敛终止条件（最近一轮为见证轮）时 SHALL 结束。其中 kflow-explore、kflow-design、kflow-plan 三阶段 SHALL 无条件执行 SELFREV；kflow-prototype-design 阶段 SHALL 仅在该变更选择「子代理自动审查验证」审查方式时执行 SELFREV，选择「人工审查」时 SHALL 完全跳过 SELFREV，SHALL NOT 保留兜底轮次。子代理意外停止时，主代理 MUST 重新创建子代理，SHALL NOT 接管执行。见证轮的判据、累积未复核修复清单的复核义务、不收敛判定与升级、终止结果的写入，均见 `convergence-driven-repetition` 能力。

#### Scenario: 子代理启动

- **WHEN** 阶段产物初稿生成完毕，进入 SELFREV 步骤
- **AND** 当前阶段为 kflow-explore、kflow-design、kflow-plan 之一，或当前阶段为 kflow-prototype-design 且该变更选择「子代理自动审查验证」审查方式
- **THEN** 主 Agent 启动第一轮子代理（Agent subagent）
- **AND** 子代理接收该阶段的产物文件路径、审查维度规则与本轮审查对象清单作为输入
- **AND** 子代理拥有独立上下文，不共享主 Agent 的对话历史

#### Scenario: 轻量档执行至少 1 轮自审

- **WHEN** 变更档位为 `轻量`
- **THEN** 系统 SHALL 执行 SELFREV，轮数不少于 1 轮
- **AND** SHALL NOT 跳过 SELFREV，SHALL NOT 存在 0 轮豁免路径
- **AND** 轮数 SHALL 由收敛实际发生在第几轮决定，SHALL NOT 因档位而限制为 1 轮
- **AND** 产物完整性门控 SHALL 保留为附加硬门

#### Scenario: 串行执行至收敛

- **WHEN** 第 N 轮子代理完成并返回审查报告
- **THEN** 主 Agent 读取审查报告和修复后的产物
- **AND** 若第 N 轮为见证轮（零新发现、零修改、报告证明全维度全量遍历、清单内全部条目逐项复核通过）→ 终止
- **AND** 否则确认修复内容后启动第 N+1 轮子代理
- **AND** SHALL NOT 同时启动多个子代理（禁止并行）
- **AND** SHALL NOT 为凑轮数而继续执行

#### Scenario: 不收敛时升级用户

- **WHEN** 自审循环命中不收敛判定（无进展 / 振荡 / 安全丝）
- **THEN** 系统 SHALL 终止并记录终止结果 `未收敛`
- **AND** SHALL 按 `convergence-driven-repetition` 能力的「不收敛判定与升级」Requirement 升级用户
- **AND** 具体缘由 SHALL 写入 `docs/skill-suggestion.md`

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
