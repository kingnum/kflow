# two-level-checkpoint

## ADDED Requirements

### Requirement: Checkpoint 两级存储结构

系统 SHALL 按操作归属级别保存 checkpoint 文件：变更级操作存储在 `docs/changes/{change}/checkpoints/`，子变更级操作存储在 `docs/changes/{change}/subchanges/{subchange}/checkpoints/`。

#### Scenario: 变更级 checkpoint 存储
- **WHEN** 当前阶段为以下之一：设计探索、原型设计、详细设计、集成测试、归档
- **THEN** checkpoint 保存到 `docs/changes/{change}/checkpoints/`
- **AND** checkpoint 文件名格式为 `{YYYYMMDD-HHMMSS}-checkpoint[-auto].md`

#### Scenario: 子变更级 checkpoint 存储
- **WHEN** 当前阶段为以下之一：计划、编码、代码审查、接口单元测试、E2E 测试
- **THEN** checkpoint 保存到 `docs/changes/{change}/subchanges/{subchange}/checkpoints/`
- **AND** checkpoint frontmatter 中包含 `subchange` 字段标识归属

#### Scenario: 缺陷修复归属判断
- **WHEN** 缺陷修复阶段产生 checkpoint
- **THEN** 系统根据触发来源判断：子变更测试失败触发的修复 → 子变更级；集成测试失败触发的修复 → 变更级

### Requirement: 子变更级 checkpoint 格式

系统 SHALL 在子变更级 checkpoint 中增加 `subchange` 标识字段。

#### Scenario: 子变更级 checkpoint frontmatter
- **WHEN** 在子变更操作中保存 checkpoint
- **THEN** checkpoint frontmatter 包含 `subchange: {subchange-name}` 字段
- **AND** 包含 `files_modified` 列出本次会话修改的文件
- **AND** 包含 `status`（in_progress / paused / blocked）

### Requirement: Checkpoint 恢复优先级

系统 SHALL 在恢复时优先读取子变更级 checkpoint，无则回退到变更级。

#### Scenario: 从子变更级恢复
- **WHEN** 系统从中断恢复且存在子变更级 checkpoint
- **THEN** 系统读取最近子变更级 checkpoint
- **AND** 解析 frontmatter 获取子变更名、状态、修改文件列表
- **AND** 恢复该子变更的阶段状态和任务进度

#### Scenario: 从变更级恢复
- **WHEN** 系统从中断恢复且无子变更级 checkpoint
- **THEN** 系统读取最近变更级 checkpoint
- **AND** 解析 frontmatter 获取变更级状态
- **AND** 恢复变更级阶段状态和进度

#### Scenario: 两级 checkpoint 均不存在
- **WHEN** 系统从中断恢复且两级均无 checkpoint
- **THEN** 系统读取 `.status.md` 和 `tasks.md` 推断当前阶段
- **AND** 显示推断结果供用户确认

### Requirement: Checkpoint 过期清理

系统 SHALL 在变更归档后清理所有关联的 checkpoint 文件。

#### Scenario: 归档时清理
- **WHEN** 变更归档操作完成
- **THEN** 系统删除该变更下的所有 checkpoint 文件（变更级 + 所有子变更级）
- **AND** 确保归档目录中不保留 checkpoint 文件

#### Scenario: 手动清理
- **WHEN** 用户请求清理 checkpoint
- **THEN** 系统仅保留最近 3 个 checkpoint（按级别分别保留）
- **AND** 删除更早的 checkpoint 文件
