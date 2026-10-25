# Spec Delta

## MODIFIED Requirements

### Requirement: 阶段内容禁止越界

系统 SHALL 确保每个阶段仅输出其职责范围内的内容，禁止输出后续阶段的职责内容。

#### Scenario: explore 禁止输出技术设计
- **WHEN** kflow-explore 生成 functional-designs/
- **THEN** 内容聚焦用户视角（页面/操作/表单/规则/非功能期望/页面清单）
- **AND** 不包含技术架构选型、数据模型设计、接口定义
- **AND** 非功能期望 SHALL 为业务语言输入，SHALL NOT 定义技术目标值（技术指标由 design 阶段 NFR 章节定义）
- **AND** 页面清单 SHALL 为区块级文字结构描述，SHALL NOT 输出视觉稿或交互原型（由 prototype 阶段承接）

#### Scenario: prototype 禁止输出业务规则变更
- **WHEN** kflow-prototype-design 生成 HTML 原型产物（直写产品级 `docs/designs/prototypes/`）
- **THEN** 原型基于 functional-designs/ 的业务规则设计交互
- **AND** 不可以在原型设计过程中修改业务规则

#### Scenario: design 禁止输出功能设计
- **WHEN** kflow-design 生成 detailed-design.md
- **THEN** 内容聚焦技术视角（架构/数据模型/接口/NFR）
- **AND** 不修改 functional-designs/ 中的功能定义
