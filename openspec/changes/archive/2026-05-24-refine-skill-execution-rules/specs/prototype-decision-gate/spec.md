## ADDED Requirements

### Requirement: 原型设计决策门控

系统 SHALL 在 explore 完成后，对前后端项目强制询问是否进入原型设计阶段，使用 prototype_decision 标记控制幂等，避免重复询问。

#### Scenario: 前后端项目探索完成后询问

- **WHEN** kflow-explore 完成且项目类型为前后端项目
- **AND** functional-designs/ 中包含至少一个 UI 功能点
- **AND** .status.md 中不存在 prototype_decision 标记
- **THEN** 系统执行 AskUserQuestion: "检测到 {n} 个 UI 功能点，是否进入原型设计阶段？"
- **AND** 选项包含"确认创建原型"（推荐）和"跳过原型设计"

#### Scenario: 用户确认创建原型

- **WHEN** 用户在 AskUserQuestion 中选择"确认创建原型"
- **THEN** 系统在 .status.md 中写入 prototype_decision=已选择原型设计
- **AND** 调度 kflow-prototype-design 阶段

#### Scenario: 用户跳过原型设计

- **WHEN** 用户在 AskUserQuestion 中选择"跳过原型设计"
- **THEN** 系统在 .status.md 中写入 prototype_decision=已跳过
- **AND** 调度 kflow-design 阶段
- **AND** 记录跳过原因到 .status.md 备注列

#### Scenario: 已有决策标记时不重复询问

- **WHEN** kflow-explore 完成或 kflow-guide 路由到 explore
- **AND** .status.md 中已存在 prototype_decision 标记
- **THEN** 系统跳过询问，直接进入下一阶段
- **AND** 若 prototype_decision=已选择原型设计 → 进入 kflow-prototype-design
- **AND** 若 prototype_decision=已跳过 → 进入 kflow-design

#### Scenario: 纯后端项目自动跳过

- **WHEN** 项目类型为纯后端项目
- **THEN** 系统自动跳过原型设计询问
- **AND** 直接进入 kflow-design 阶段
- **AND** 不在 .status.md 中写入 prototype_decision 标记

#### Scenario: 用户后续明确需要原型

- **WHEN** prototype_decision=已跳过 已存在
- **AND** 用户明确表达"现在想要原型"或"我想看原型"
- **THEN** 系统调度 kflow-prototype-design
- **AND** 不删除已有 prototype_decision 标记
- **AND** 原型通过后可选更新 prototype_decision=已选择原型设计

### Requirement: guide RESUME 路由不触发原型询问

系统 SHALL 确保通过 kflow-guide 的 RESUME 路由进入变更时，不触发原型设计决策询问。

#### Scenario: RESUME 路由到已有变更

- **WHEN** 用户输入匹配「继续/恢复/resume + 变更名」
- **THEN** kflow-guide 路由到 kflow-resume
- **AND** kflow-resume 读取 .status.md 定位断点
- **AND** 按断点调度对应阶段，不执行 explore COMPLETE 步骤
- **AND** 不触发原型设计决策询问
