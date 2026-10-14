# Spec Delta

## MODIFIED Requirements

### Requirement: 每轮子代理审查维度完整且审查对象冻结

单轮验证子代理 SHALL 执行该阶段全部审查维度的完整检查，维度集合 SHALL 为封闭枚举、SHALL NOT 新增；审查对象集合 SHALL 由主 Agent 从阶段产物既有内容生成并冻结，子代理 SHALL NOT 扩大。审查对象集合 MAY 因阶段输入变化（如回退重执行新增受影响项）由主 Agent 更新。

#### Scenario: explore 阶段子代理审查范围

- **WHEN** explore 阶段的验证子代理执行单轮验证
- **THEN** SHALL 独立执行完整性、闭环性、必要性、清晰性全部四个维度的完整检查
- **AND** SHALL NOT 新增任何维度

#### Scenario: prototype 阶段子代理审查范围

- **WHEN** prototype 阶段的验证子代理执行单轮验证
- **AND** 该变更选择「子代理自动审查验证」审查方式
- **THEN** SHALL 独立执行覆盖性、一致性、可用性、完整性全部四个维度的完整检查
- **AND** 覆盖性为第一优先级

#### Scenario: design 阶段子代理审查范围

- **WHEN** design 阶段的验证子代理执行单轮验证
- **THEN** SHALL 独立执行一致性、完备性、可行性、可测性全部四个维度的完整检查
- **AND** SHALL NOT 减少维度或检查项

#### Scenario: plan 阶段子代理审查范围（新增）

- **WHEN** plan 阶段的验证子代理执行单轮验证
- **THEN** SHALL 独立执行任务覆盖完整性、DoD 验收标准正确性、HITL 标注准确性、任务粒度合理性全部四个维度的完整检查

#### Scenario: 审查对象集合由主 Agent 冻结注入

- **WHEN** 主 Agent 构建验证子代理的 prompt
- **THEN** prompt SHALL 包含由阶段产物既有内容生成的审查对象清单
- **AND** 子代理 SHALL NOT 审查该清单之外的产物或文件

### Requirement: 子代理边审边修

验证子代理 SHALL NOT 修改任何阶段产物，仅将发现的问题记入验证报告。全部发现项 SHALL 由主 Agent 在单轮验证完成后统一修复并生成「本阶段修复清单」。

#### Scenario: 发现问题直接修复

- **WHEN** 验证子代理在验证过程中确认了问题
- **THEN** SHALL NOT 修改任何产物文件
- **AND** SHALL 将该问题记入验证报告的发现问题清单
- **AND** 主 Agent SHALL 在验证完成后统一修复产物文件

#### Scenario: 修复范围限制

- **WHEN** 主 Agent 在验证完成后执行统一修复
- **THEN** SHALL 仅修复验证报告确认的问题，不做重构或额外改进
- **AND** SHALL NOT 新增功能（遵循「非必要不增加新功能」原则）
- **AND** SHALL NOT 新增冻结审查对象集合之外的产物内容（功能点、字段、章节、分支）

#### Scenario: 范围外发现降级为范围外观察

- **WHEN** 子代理在冻结审查对象集合之外发现问题
- **THEN** SHALL NOT 将其计入验证发现数
- **AND** SHALL 记为「范围外观察」写入验证报告的「范围外观察」小节

### Requirement: 子代理审查报告

单轮验证子代理完成验证后 SHALL 生成一份验证报告，且 SHALL 足以判定验证结果与签署是否属实。报告 SHALL 证明全部审查维度与全部审查对象已完成遍历。

#### Scenario: 报告内容

- **WHEN** 子代理完成单轮验证
- **THEN** 生成验证报告，包含签署清单打假结果、独立发现问题清单、范围外观察、全量遍历证明与验证结论
- **AND** 报告 SHALL 证明已完成全部审查维度与全部审查对象的全量遍历
- **AND** 报告保存路径为 `self-reviews/{phase}/report.md`
- **AND** 「范围外观察」小节为空时 SHALL 记为「（空）」

#### Scenario: 主 Agent 读取报告

- **WHEN** 子代理返回验证报告路径
- **THEN** 主 Agent 读取报告内容
- **AND** 统一修复报告确认的全部问题并生成「本阶段修复清单」
- **AND** 校验审查对象是否超出冻结范围；超出时 SHALL 要求子代理在冻结范围内重新验证，并记录越界事实到 `docs/skill-suggestion.md`
- **AND** 汇总「范围外观察」条目，在阶段终止时向用户提示
- **AND** SHALL NOT 为验证修复结果追加确认轮

### Requirement: 自审由子代理串行执行至收敛

系统 SHALL 在 kflow-explore、kflow-prototype-design、kflow-design、kflow-plan 四个阶段的 SELFREV 步骤使用子代理（Agent subagent）执行单轮验证，SHALL NOT 执行第二轮。SHALL NOT 存在 0 轮豁免；验证完成后系统 SHALL 结束该环节。其中 kflow-explore、kflow-design、kflow-plan 三阶段 SHALL 无条件执行 SELFREV；kflow-prototype-design 阶段 SHALL 仅在该变更选择「子代理自动审查验证」审查方式时执行 SELFREV，选择「人工审查」时 SHALL 完全跳过 SELFREV，SHALL NOT 保留兜底轮次。子代理意外停止时，主代理 MUST 重新创建子代理，SHALL NOT 接管执行。签署清单结构、打假契约、终止结果取值与写入位置见 `signed-checklist-verification` 能力。

#### Scenario: 子代理启动

- **WHEN** 阶段产物初稿生成完毕且主 Agent 已完成签署自证，进入 SELFREV 步骤
- **AND** 当前阶段为 kflow-explore、kflow-design、kflow-plan 之一，或当前阶段为 kflow-prototype-design 且该变更选择「子代理自动审查验证」审查方式
- **THEN** 主 Agent 启动验证子代理（Agent subagent）
- **AND** 子代理接收该阶段的产物文件路径、审查维度规则与审查对象清单作为输入
- **AND** 子代理拥有独立上下文，不共享主 Agent 的对话历史

#### Scenario: 轻量档执行至少 1 轮自审

- **WHEN** 变更档位为 `轻量`
- **THEN** 系统 SHALL 执行 SELFREV 单轮验证
- **AND** SHALL NOT 跳过 SELFREV，SHALL NOT 存在 0 轮豁免路径
- **AND** 轮数 SHALL 恒为 1，SHALL NOT 执行第二轮
- **AND** 产物完整性门控 SHALL 保留为附加硬门

#### Scenario: 串行执行至收敛

- **WHEN** 验证子代理完成并返回验证报告
- **THEN** 主 Agent 读取验证报告与产物差异
- **AND** 统一修复报告确认的全部问题并生成「本阶段修复清单」
- **AND** 将终止结果写入变更级 `.status.md`，取值 `验证通过` 或 `验证发现问题({N})`
- **AND** SHALL NOT 启动第二轮验证子代理

#### Scenario: 不收敛时升级用户

- **WHEN** 验证子代理意外停止、报错退出或返回不完整结果
- **THEN** 主代理 MUST 分析原因后重新创建新的子代理
- **AND** SHALL NOT 在主 Agent 上下文中接管子代理未完成的工作
- **AND** 最多重试 3 次，全部失败后标记 ⚠️ 阻塞并提示用户

#### Scenario: 原型阶段选择人工审查时跳过 SELFREV

- **WHEN** 当前阶段为 kflow-prototype-design
- **AND** 该变更选择「人工审查」审查方式
- **THEN** 系统 SHALL 完全跳过 SELFREV 步骤
- **AND** SHALL NOT 启动任何验证子代理，SHALL NOT 保留兜底轮次
- **AND** 系统 SHALL 直接进入用户评审 REVIEW 步骤

#### Scenario: 子代理异常时主代理禁止接管

- **WHEN** 子代理意外停止、报错退出或返回要求重做/继续
- **THEN** 主代理 MUST 分析原因后重新创建新的子代理
- **AND** SHALL NOT 在主 Agent 上下文中接管子代理未完成的工作
- **AND** 新子代理的 prompt 包含已完成的验证范围与待验证说明
