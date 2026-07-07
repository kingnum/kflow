# resume-skill

## Purpose

定义中断恢复 Skill（kflow-resume）的精确恢复流程——通过变更标识名称定位变更、读取状态文件和 checkpoint 定位断点、输出恢复摘要、直接调度对应阶段 Skill 继续执行。

## ADDED Requirements

### Requirement: 变更存在性验证

kflow-resume SHALL 在恢复执行前验证目标变更存在且未归档。

#### Scenario: 变更存在且未归档

- **WHEN** 用户指定变更名称 `add-user-auth` 且 `docs/changes/add-user-auth/` 目录存在且不在 `docs/archive/` 下
- **THEN** 系统通过验证，继续恢复流程

#### Scenario: 变更目录不存在

- **WHEN** 用户指定变更名称 `nonexistent-change` 且 `docs/changes/nonexistent-change/` 目录不存在
- **THEN** 系统报错：变更不存在，请检查变更名称

#### Scenario: 变更已归档

- **WHEN** 用户指定变更名称 `old-change` 且该变更已位于 `docs/archive/` 下
- **THEN** 系统报错：变更已归档，无法恢复。如需继续工作请创建新变更

### Requirement: 状态读取优先级链

kflow-resume SHALL 按优先级链读取状态文件以定位最精确的恢复断点。

#### Scenario: checkpoint 文件存在

- **WHEN** `docs/changes/{change}/checkpoints/` 或子变更级 `checkpoints/` 目录存在 checkpoint 文件
- **THEN** 系统读取最近时间的 checkpoint 作为首选断点信息
- **AND** 优先读取子变更级 checkpoint 再回退到变更级 checkpoint

#### Scenario: 无 checkpoint 但有 .status.md

- **WHEN** checkpoint 文件不存在但 `.status.md` 文件存在
- **THEN** 系统从 `.status.md` 的「当前阶段」字段获取恢复阶段
- **AND** 从子变更进度矩阵获取子变更级状态

#### Scenario: 仅有 tasks.md

- **WHEN** checkpoint 和 .status.md 均缺失
- **THEN** 系统从 tasks.md 的 checkbox 完成状态反推当前阶段和待执行任务

### Requirement: 断点定位

kflow-resume SHALL 精确定位恢复断点，确定当前阶段、当前子变更、待执行任务。

#### Scenario: 变更级阶段断点（设计探索、详细设计等）

- **WHEN** 当前阶段为变更级阶段（设计探索、详细设计等）
- **THEN** 系统定位到该阶段的未完成任务
- **AND** 从变更级 tasks.md 获取待执行列表

#### Scenario: 子变更级断点（计划、编码、测试等）

- **WHEN** 当前阶段为子变更级阶段（计划、编码、接口单元测试等）
- **THEN** 系统定位到当前活跃子变更
- **AND** 从子变更 tasks.md 获取未勾选的功能点任务

#### Scenario: 阶段回退状态（⚠️ 需修订）

- **WHEN** 当前阶段状态为 `⚠️ 需修订`
- **THEN** 系统定位到回退目标阶段
- **AND** 将回退目标阶段作为调度目标

### Requirement: 恢复摘要输出

kflow-resume SHALL 在调度阶段 Skill 前输出恢复摘要供用户确认上下文。

#### Scenario: 输出恢复摘要

- **WHEN** 断点定位完成
- **THEN** 系统输出恢复摘要，包含变更描述、类型、当前阶段、进度概览、待执行任务列表、下一步操作
- **AND** 摘要格式为 Markdown 表格+列表

### Requirement: 直接调度阶段 Skill

kflow-resume SHALL 输出恢复摘要后直接调用对应阶段 Skill（使用 Skill 工具）。

#### Scenario: 调度编码阶段

- **WHEN** 恢复断点定位为编码阶段（子变更 `user-auth`）
- **THEN** 系统直接调用 `kflow-code` Skill 并传入子变更上下文

#### Scenario: 调度详细设计阶段

- **WHEN** 恢复断点定位为详细设计阶段（变更级）
- **THEN** 系统直接调用 `kflow-design` Skill 并传入变更上下文

#### Scenario: 阶段被阻塞

- **WHEN** 当前阶段状态为 `❌ 阻塞`
- **THEN** 系统输出阻碍信息和建议解决方案
- **AND** 不调度阶段 Skill，让用户决定如何处理

### Requirement: 调度映射

kflow-resume SHALL 按阶段到 Skill 的映射表调度正确的 Skill。

#### Scenario: 阶段映射正确性

- **WHEN** 当前阶段确定
- **THEN** 系统按以下映射调度 Skill：
  - 设计探索 → `kflow-explore`
  - 原型设计 → `kflow-prototype-design`
  - 详细设计 → `kflow-design`
  - 计划 → `kflow-plan`
  - 编码 → `kflow-code`
  - 代码审查 → `kflow-code-review`
  - 接口单元测试 → `kflow-e2e-qa`
  - E2E测试 → `kflow-e2e-qa`
  - 集成测试 → `kflow-integration-test`
  - 审计 → `kflow-audit`
  - 归档 → `kflow-archive`
