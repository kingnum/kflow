## ADDED Requirements

### Requirement: 审计发现触发回退

系统 SHALL 支持 kflow-audit 审计发现问题时触发阶段回退，作为第 4 种回退触发来源。

#### Scenario: 审计发现问题归属到特定阶段
- **WHEN** kflow-audit 审计发现问题
- **THEN** 系统判断问题归属阶段
- **AND** 对应阶段状态变更为 ⚠️ 需修订
- **AND** 后续阶段状态重置为 ⏳ 待开始

#### Scenario: 审计阻断归档
- **WHEN** 审计发现阻塞级问题
- **THEN** 阻断归档流程
- **AND** 要求按阶段回退修复后重新审计

## MODIFIED Requirements

### Requirement: 阶段回退门控

系统 SHALL 定义阶段回退时的门控规则，支持四种回退触发来源。

#### Scenario: 回退触发来源
- **WHEN** 需要触发阶段回退
- **THEN** 系统判断回退触发来源为以下四种之一：缺陷修复根因（设计错误）、代码审查发现问题、用户需求变更、kflow-audit 审计发现
- **AND** 不同来源使用相同的回退门控规则

#### Scenario: 回退到设计阶段
- **WHEN** 需要回退到详细设计阶段
- **THEN** 详细设计状态: ✅ → ⚠️ 需修订
- **AND** 计划、编码、测试等后续阶段状态: 重置为 ⏳ 待开始
- **AND** 受影响产物标记为"待修订"（不删除，保留参考）

#### Scenario: 仅当前子变更回退
- **WHEN** 回退仅影响单个子变更
- **THEN** 其他子变更不受影响
- **AND** 仅该子变更的阶段状态被重置

#### Scenario: 接口契约变更导致多子变更联动回退
- **WHEN** 回退涉及接口契约变更
- **THEN** 依赖该接口的所有子变更联动回退
- **AND** 评估影响范围后用户确认修订方案

### Requirement: design-explore.md 修订管理

系统 SHALL 支持 functional-design.md（原 design-explore.md）的版本化修订。

#### Scenario: 详细设计阶段修订功能点
- **WHEN** 详细设计阶段发现功能点粒度需调整
- **THEN** 允许修订 functional-design.md 中的功能点清单
- **AND** 更新版本号（如 1.0.0 → 1.1.0）和修订记录

#### Scenario: 编码阶段修订被限制
- **WHEN** 编码阶段尝试修订功能点
- **THEN** 必须走需求变更流程
- **AND** 不允许直接修改 functional-design.md

### Requirement: 需求变更记录

系统 SHALL 在 functional-design.md 中维护需求变更记录。

#### Scenario: 记录需求变更
- **WHEN** 任何阶段发生需求变更
- **THEN** functional-design.md 的需求变更记录表增加一条记录
- **AND** 记录包含变更序号、时间、描述、影响功能点、触发阶段、处理状态
