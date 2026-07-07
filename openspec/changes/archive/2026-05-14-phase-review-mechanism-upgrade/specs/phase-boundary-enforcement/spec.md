# phase-boundary-enforcement

## Purpose

定义阶段边界强制规则，包括文档创建白名单模式、标准产物强制生成规则、信息不足溢出路径、阶段内容禁止越界规则，以及越界内容触发阶段回退提醒机制。

## ADDED Requirements

### Requirement: 文档创建白名单模式

系统 SHALL 在每个阶段仅允许创建其输出产物表中列出的文件，禁止创建任何未在输出产物表中列出的文件。

#### Scenario: 白名单内文件允许创建
- **WHEN** 阶段需要创建输出产物表中的文件
- **THEN** 系统允许创建该文件
- **AND** 文件内容遵循阶段任务边界约束

#### Scenario: 白名单外文件禁止创建
- **WHEN** 阶段尝试创建输出产物表中未列出的文件
- **THEN** 系统禁止创建
- **AND** 如内容确有必要，记录到 docs/skill-suggestion.md

### Requirement: 标准产物强制生成

系统 SHALL 无论用户输入来源是什么（口述/文件/URL），都必须生成该阶段完整的标准输出产物。

#### Scenario: 用户以文件提供输入
- **WHEN** 用户以文档文件提供需求输入
- **THEN** 系统仍需生成 functional-designs/ 目录（explore 阶段）
- **AND** 不可直接引用用户文件替代标准产物

#### Scenario: 用户以 URL 提供输入
- **WHEN** 用户以 URL 指向外部需求描述
- **THEN** 系统读取 URL 内容后仍需生成完整的标准输出产物
- **AND** 不可仅保存 URL 引用作为替代

#### Scenario: 用户口述需求
- **WHEN** 用户口头描述需求
- **THEN** 系统基于对话内容生成完整的标准输出产物
- **AND** 产出物质量与文件输入模式一致

### Requirement: 信息不足时的溢出路径

系统 SHALL 当当前文档内容无法满足需求时，记录到 docs/skill-suggestion.md 并在当前阶段文档中扩充，禁止创建额外文档。

#### Scenario: 发现信息不足
- **WHEN** 阶段执行过程中发现需要额外信息
- **THEN** 在当前阶段文档中标记"待补充"并说明缺少什么
- **AND** 记录到 docs/skill-suggestion.md 作为流程改进建议

#### Scenario: 禁止自创新文档
- **WHEN** 阶段发现当前文档无法容纳某类信息
- **THEN** 禁止创建额外文档来填补信息空缺
- **AND** 如需扩展文档结构，通过 skill-suggestion 提议流程改进

### Requirement: 阶段内容禁止越界

系统 SHALL 确保每个阶段仅输出其职责范围内的内容，禁止输出后续阶段的职责内容。

#### Scenario: explore 禁止输出技术设计
- **WHEN** kflow-explore 生成 functional-designs/
- **THEN** 内容聚焦用户视角（页面/操作/表单/规则）
- **AND** 不包含技术架构选型、数据模型设计、接口定义

#### Scenario: prototype 禁止输出业务规则变更
- **WHEN** kflow-prototype-design 生成 prototype.pen
- **THEN** 原型基于 functional-designs/ 的业务规则设计交互
- **AND** 不可以在原型设计过程中修改业务规则

#### Scenario: design 禁止输出功能设计
- **WHEN** kflow-design 生成 detailed-design.md
- **THEN** 内容聚焦技术视角（架构/数据模型/接口/NFR）
- **AND** 不修改 functional-designs/ 中的功能定义

### Requirement: 越界内容触发阶段回退提醒

系统 SHALL 当发现上游阶段产物存在问题时，记录到 skill-suggestion.md 并提示可能的阶段回退，但不可直接修改上游产物。

#### Scenario: design 发现功能设计不完整
- **WHEN** kflow-design 发现 functional-designs/ 缺失关键信息
- **THEN** 记录到 skill-suggestion.md
- **AND** 提示用户是否需要回退到 explore 阶段补充
- **AND** 不直接修改 functional-designs/ 内容

#### Scenario: prototype 发现功能点定义不清晰
- **WHEN** kflow-prototype-design 发现某功能点描述不足以支撑原型设计
- **THEN** 记录到 skill-suggestion.md
- **AND** 在当前能力范围内完成原型
- **AND** 提示用户需要回退 explore 补充功能点描述
