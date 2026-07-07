# design-level-restructure (Delta)

## ADDED Requirements

### Requirement: explore 阶段边界明确化

系统 SHALL 将 kflow-explore 的输出内容限定在用户视角。

#### Scenario: explore 域内内容
- **WHEN** kflow-explore 输出 functional-designs/
- **THEN** 内容聚焦用户能做什么、页面什么样、业务规则是什么
- **AND** 包含页面结构/菜单层级、可执行操作、表单项定义、业务规则
- **AND** 不包含技术架构选型、数据模型设计、接口定义

#### Scenario: explore 域外约束
- **WHEN** kflow-explore 执行需求分析
- **THEN** 禁止讨论技术方案选型
- **AND** 禁止设计数据模型或接口
- **AND** 如用户需求涉及技术实现，转由 design 阶段处理

### Requirement: prototype 阶段边界明确化

系统 SHALL 将 kflow-prototype-design 限定为 UI 视觉和交互原型生成。

#### Scenario: prototype 域内内容
- **WHEN** kflow-prototype-design 生成原型
- **THEN** 基于 functional-designs/ 的页面/操作/表单定义生成 UI 原型
- **AND** 聚焦视觉呈现和交互流程
- **AND** 覆盖所有 FP 对应的页面

#### Scenario: prototype 域外约束
- **WHEN** kflow-prototype-design 执行原型设计
- **THEN** 禁止修改功能点定义或业务规则
- **AND** 禁止在此阶段做技术实现决策
- **AND** 如原型过程发现功能设计不完整，记录 skill-suggestion 并提示回退

### Requirement: design 阶段边界明确化

系统 SHALL 将 kflow-design 限定为技术视角的详细设计。

#### Scenario: design 域内内容
- **WHEN** kflow-design 输出 detailed-design.md
- **THEN** 内容聚焦系统架构、数据模型、接口设计、NFR、子变更划分
- **AND** 包含 api-tests/ 和 e2e-tests/ 测试用例文档

#### Scenario: design 域外约束
- **WHEN** kflow-design 执行技术设计
- **THEN** 禁止修改 functional-designs/ 中的功能定义
- **AND** 禁止修改 prototype.pen 中的 UI 设计
- **AND** 如发现上游设计问题，记录 skill-suggestion 并提示回退

### Requirement: 三阶段数据流向约束

系统 SHALL 确保数据仅从上游流向下游，不反向修改。

#### Scenario: 数据流向
- **WHEN** 变更流程从 explore 到 prototype 到 design
- **THEN** explore 输出 → prototype 输入（只读）
- **AND** explore + prototype 输出 → design 输入（只读）
- **AND** 下游不可修改上游产物

#### Scenario: 发现上游问题时的处理
- **WHEN** 下游阶段发现上游产物存在缺陷
- **THEN** 记录到 skill-suggestion.md
- **AND** 提示用户是否需要阶段回退
- **AND** 禁止直接修改上游产物来"修复"问题

## MODIFIED Requirements

### Requirement: 设计探索输出调整

系统 SHALL 调整设计探索阶段的输出内容，不包含子变更划分，但新增页面/操作/表单/业务规则等用户视角信息。

#### Scenario: 功能设计输出内容
- **WHEN** 设计探索阶段完成
- **THEN** functional-designs/ 目录包含需求描述、项目类型、功能点清单、功能点关联关系
- **AND** 每个功能点包含：用户故事、所属页面与菜单、可执行操作、表单项定义、业务规则（前置条件/校验规则/触发条件/后置结果）、业务流程上下文
- **AND** 不包含数据需求、接口需求（这些属于详细设计）
- **AND** 不包含子变更划分方案
- **AND** 版本号和修订记录在 index.md 和每个 part-NN.md 中维护
