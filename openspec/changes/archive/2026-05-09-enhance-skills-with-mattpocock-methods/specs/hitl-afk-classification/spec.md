## ADDED Requirements

### Requirement: 子变更 HITL/AFK 分类

系统 SHALL 在 kflow-design 阶段划分子变更时，对每个子变更标注执行类型：AFK（Away From Keyboard，可自动执行）或 HITL（Human In The Loop，需人工决策）。

#### Scenario: AFK 子变更判定

- **WHEN** 子变更满足以下条件：无架构选择决策点、无设计方案确认需求、无 UI/UX 方向决策、所有实现路径已由设计文档明确
- **THEN** 系统 SHALL 标记该子变更为 AFK
- **AND** ralph-loop 可直接全自动迭代执行

#### Scenario: HITL 子变更判定

- **WHEN** 子变更涉及以下任一类型：架构选择（如"选 Redis 还是 Memcached"）、设计方案确认（接口契约需用户批准）、UI/UX 方向（布局/交互需确认）
- **THEN** 系统 SHALL 标记该子变更为 HITL
- **AND** 标注具体的决策点位置和触发条件

#### Scenario: HITL 子变更执行

- **WHEN** ralph-loop 执行 HITL 子变更到达决策点
- **THEN** 系统 SHALL 暂停执行并通过 AskUserQuestion 请求用户决策
- **AND** 用户确认后继续执行
- **AND** 不跳过决策点

### Requirement: 子变更划分表格增加执行类型列

子变更划分结果表格 SHALL 增加"执行类型"列。

#### Scenario: 子变更划分表格格式

- **WHEN** kflow-design 输出子变更划分结果
- **THEN** 表格 SHALL 包含以下列：子变更名称、功能点数、包含功能点ID、依赖子变更、优先级、**执行类型（AFK/HITL）**
- **AND** HITL 子变更 SHALL 附带决策点说明（在备注或单独字段）

### Requirement: AFK 并行执行策略

AFK 子变更 SHALL 支持并行执行，HITL 子变更 SHALL 顺序执行以避免多个决策点并发导致混乱。

#### Scenario: 并行 AFK 执行

- **WHEN** 存在多个无依赖的 AFK 子变更
- **THEN** 系统 SHALL 可并行启动 ralph-loop 子代理
- **AND** 每个 Agent 仅修改分配的子变更目录

#### Scenario: HITL 顺序执行

- **WHEN** 存在 HITL 子变更
- **THEN** 系统 SHALL 顺序执行 HITL 子变更
- **AND** 前一个 HITL 子变更的决策点全部解决后，才开始下一个 HITL 子变更
