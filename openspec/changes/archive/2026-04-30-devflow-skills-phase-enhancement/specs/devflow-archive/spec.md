## ADDED Requirements

### Requirement: 变更归档执行

系统 SHALL 支持将已完成或未完成的变更进行归档操作。

#### Scenario: 归档已完成变更
- **WHEN** 用户请求归档一个所有阶段已完成的变更
- **THEN** 系统将变更目录移动到 docs/archive/{YYYY-MM-DD}-{change}/
- **AND** 更新 .status.md 添加归档记录
- **AND** 更新 docs/changes/index.md 归档记录

#### Scenario: 归档未完成变更
- **WHEN** 用户请求归档一个未完成的变更
- **THEN** 系统允许归档并记录归档状态为"未完成"
- **AND** 记录归档原因

### Requirement: 归档后禁止操作

系统 SHALL 禁止对已归档变更进行任何修改操作。

#### Scenario: 尝试继续已归档变更
- **WHEN** 用户尝试继续已归档的变更
- **THEN** 系统拒绝操作并提示创建新变更

### Requirement: 归档索引更新

系统 SHALL 在归档时更新 docs/changes/index.md 文件。

#### Scenario: 更新归档索引
- **WHEN** 变更归档完成
- **THEN** index.md 中活跃变更列表移除该变更
- **AND** 已归档变更列表添加该变更记录

### Requirement: 归档条件检查

系统 SHALL 在归档前检查主变更状态文件。

#### Scenario: 检查归档条件
- **WHEN** 用户请求归档
- **THEN** 系统读取 .status.md 检查所有阶段状态
- **AND** 所有需要开展的阶段均标记完成或跳过时允许归档
