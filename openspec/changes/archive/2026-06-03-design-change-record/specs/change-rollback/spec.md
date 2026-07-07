## ADDED Requirements

### Requirement: .status.md 设计修订同步追踪

系统 SHALL 在变更级 .status.md 中维护"设计修订同步追踪"节，以表格追踪每次设计修订在各受影响阶段的同步状态。每阶段使用独立确认列。

#### Scenario: 回退时追加同步追踪行

- **WHEN** 阶段回退被用户确认执行
- **THEN** .status.md 的"设计修订同步追踪"表 SHALL 追加一行
- **AND** 行包含：序号、修订时间、修订目标（functional-designs/prototype/detailed-design）、变更简述、影响范围
- **AND** 所有受影响阶段列初始为 ⏳ 待同步
- **AND** 不受影响的阶段列标记为 —

#### Scenario: 各阶段独立确认同步状态

- **WHEN** 受影响阶段重新执行并完成
- **THEN** 该阶段 SHALL 在 POST_HOOK 中将本阶段列从 ⏳ 更新为 ✅
- **AND** 仅更新本阶段列，不影响其他阶段列

#### Scenario: 多次修订时各行独立追踪

- **WHEN** 存在多次设计修订（多行追踪记录）
- **THEN** 每行各自的阶段列独立追踪
- **AND** 新修订追加新行，不修改已有行的状态

## MODIFIED Requirements

### Requirement: 需求变更记录

系统 SHALL 在 functional-designs/index.md 和其他设计目录 index.md 中维护统一的修订记录。原"需求变更记录"和"修订记录"合并为一张"修订记录"表。

#### Scenario: 记录需求变更

- **WHEN** 任何阶段发生需求变更
- **THEN** 目标设计目录 index.md 的修订记录表增加一条记录
- **AND** 记录包含：版本、日期、修订类型、修订内容、影响功能点、触发阶段
- **AND** .status.md 的设计修订同步追踪表追加对应的追踪行
