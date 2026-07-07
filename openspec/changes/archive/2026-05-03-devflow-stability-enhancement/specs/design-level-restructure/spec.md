## ADDED Requirements

### Requirement: 详细设计在变更级执行

系统 SHALL 将详细设计阶段（kflow-design）从子变更级提升到变更级，在设计探索完成后、子变更划分前执行。

#### Scenario: 变更级统一设计
- **WHEN** 设计探索阶段完成（design-explore.md 已创建，含完整功能点清单）
- **THEN** 系统在变更级执行详细设计
- **AND** 输出单一 design.md 包含所有功能点的详细设计
- **AND** 子变更划分在 design.md 完成后基于完整设计认知执行

#### Scenario: 功能缺陷级走简化流程
- **WHEN** 变更类型为功能缺陷级
- **THEN** design.md 简化输出（仅包含受影响的功能点设计）
- **AND** 子变更划分可跳过（单变更内直接编码）

### Requirement: 子变更职责简化为执行单元

系统 SHALL 将子变更职责限制为计划、编码、测试等执行工作，不再包含设计职责。

#### Scenario: 子变更目录结构
- **WHEN** 子变更创建
- **THEN** 子变更目录仅包含 .status.md、tasks.md、test-reports/
- **AND** 不包含 design.md、api-tests.md、e2e-tests.md（已移至变更级）

#### Scenario: 子变更计划引用变更级设计
- **WHEN** kflow-plan 为子变更创建任务清单
- **THEN** 输入为变更级 design.md 中属于该子变更的章节
- **AND** 任务拆分基于变更级设计中的功能点描述和数据模型

## MODIFIED Requirements

### Requirement: 设计探索输出调整

系统 SHALL 调整设计探索阶段的输出内容，不再包含子变更划分。

#### Scenario: design-explore.md 内容
- **WHEN** 设计探索阶段完成
- **THEN** design-explore.md 包含需求描述、项目类型、功能点清单、功能点关联关系
- **AND** design-explore.md 包含版本号和修订记录区
- **AND** design-explore.md 不再包含子变更划分方案

### Requirement: architecture.md 合并到 design.md

系统 SHALL 将 architecture.md 的内容合并到变更级 design.md 的架构章节中。

#### Scenario: design.md 包含架构内容
- **WHEN** 详细设计阶段执行
- **THEN** design.md 开头章节包含系统架构、技术选型、模块划分
- **AND** 不再单独生成 architecture.md 文件
