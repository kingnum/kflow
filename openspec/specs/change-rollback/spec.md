## Requirements

### Requirement: ⚠️ 需修订 状态值

系统 SHALL 在状态体系中新增 `⚠️ 需修订` 状态值，表示阶段产物因需求变更或设计错误需修订。

#### Scenario: 需求变更触发标记
- **WHEN** 编码或测试阶段发现需求变更（功能点新增/修改/删除）
- **THEN** 当前阶段状态标记为 ❌ 阻塞
- **AND** 受影响的设计阶段状态从 ✅ 完成 变更为 ⚠️ 需修订

#### Scenario: 设计错误触发标记
- **WHEN** 缺陷修复阶段根因分析判定为设计错误
- **THEN** 设计阶段状态变更为 ⚠️ 需修订
- **AND** 受影响的后续阶段状态重置为 ⏳ 待开始

### Requirement: 阶段回退门控

系统 SHALL 定义阶段回退时的门控规则，确保回退合规且产物联动处理。

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

系统 SHALL 支持 design-explore.md 的版本化修订。

#### Scenario: 详细设计阶段修订功能点
- **WHEN** 详细设计阶段发现功能点粒度需调整
- **THEN** 允许修订 design-explore.md 中的功能点清单
- **AND** 更新版本号（如 1.0.0 → 1.1.0）和修订记录

#### Scenario: 编码阶段修订被限制
- **WHEN** 编码阶段尝试修订功能点
- **THEN** 必须走需求变更流程
- **AND** 不允许直接修改 design-explore.md

### Requirement: 需求变更记录

系统 SHALL 在 design-explore.md 中维护需求变更记录。

#### Scenario: 记录需求变更
- **WHEN** 任何阶段发生需求变更
- **THEN** design-explore.md 的需求变更记录表增加一条记录
- **AND** 记录包含变更序号、时间、描述、影响功能点、触发阶段、处理状态

## ADDED by devflow-v1-5-0-upgrade

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

## MODIFIED by devflow-v1-5-0-upgrade

### Requirement: 阶段回退门控

系统 SHALL 定义阶段回退时的门控规则，支持七种回退触发来源，回退目标包含 explore、design、prototype-design 三种阶段。

> **变更说明**：新增第七种回退触发来源——kflow-bug-triage 诊断路由。triage 的四层诊断结果可直接触发回退到 explore（L1 需求问题）、prototype-design（L2 原型问题）或 design（L3 设计问题），路由逻辑与现有六种来源使用相同的回退门控规则。

#### Scenario: 回退触发来源
- **WHEN** 需要触发阶段回退
- **THEN** 系统判断回退触发来源为以下七种之一：缺陷修复根因（设计错误，仅三次尝试升级后用户选择）、代码审查发现问题、用户需求变更、kflow-audit 审计发现、编码发现原型交互/视觉/状态问题、编码发现功能点/业务规则问题、kflow-bug-triage 诊断路由
- **AND** 不同来源使用相同的回退门控规则

#### Scenario: triage 诊断触发回退到 explore
- **WHEN** kflow-bug-triage 诊断确定问题源头为 L1 需求定义
- **THEN** explore 阶段状态: ✅ → ⚠️ 需修订
- **AND** prototype-design、design、plan、code、test 等后续阶段状态: 重置为 ⏳ 待开始
- **AND** 受影响产物标记为"待修订"（不删除，保留参考）
- **AND** 回退后 SHALL 进入 explore 的 REVISION 模式

#### Scenario: triage 诊断触发回退到 prototype-design
- **WHEN** kflow-bug-triage 诊断确定问题源头为 L2 原型设计
- **THEN** prototype-design 阶段状态: ✅ → ⚠️ 需修订
- **AND** design、plan、code、test 等后续阶段状态: 重置为 ⏳ 待开始
- **AND** 受影响产物标记为"待修订"（不删除，保留参考）
- **AND** 回退后 SHALL 进入 prototype-design 的 REVISION 模式

#### Scenario: triage 诊断触发回退到 design
- **WHEN** kflow-bug-triage 诊断确定问题源头为 L3 详细设计
- **THEN** design 阶段状态: ✅ → ⚠️ 需修订
- **AND** plan、code、test 等后续阶段状态: 重置为 ⏳ 待开始
- **AND** 受影响产物标记为"待修订"（不删除，保留参考）
- **AND** 回退后 SHALL 进入 design 的 REVISION 模式

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

### Requirement: 编码阶段发现上游问题的标准化决策流程

系统 SHALL 在编码阶段发现上游产物存在问题时，执行标准化的 AskUserQuestion 决策流程。

#### Scenario: 判断根因归属
- **WHEN** 编码阶段发现上游产物问题
- **THEN** 系统 SHALL 判定根因归属：原型交互/视觉/状态问题 → 回退目标 prototype-design；功能点/业务规则问题 → 回退目标 explore（功能性）或 design（技术性）；纯实现层面可修复 → 不触发回退
- **AND** 记录根因判定结果和影响范围到 skill-suggestion.md

#### Scenario: AskUserQuestion 确认回退决策
- **WHEN** 根因判定为需要回退
- **THEN** 系统 SHALL 通过 AskUserQuestion 询问用户：「发现上游设计需要调整：[具体问题描述]。如何处理？」
- **AND** 选项包含：确认回退到 [目标阶段] / 暂缓此功能点（标记 ⏸️）/ 记录为已知问题继续
- **AND** 用户选择「确认回退」后 SHALL 执行回退流程
- **AND** 用户选择「暂缓」后 SHALL 标记该 FP 为 ⏸️ 暂缓，继续处理其他 FP

## ADDED by design-change-record

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

## MODIFIED by design-change-record

### Requirement: 需求变更记录

系统 SHALL 在 functional-designs/index.md 和其他设计目录 index.md 中维护统一的修订记录。原"需求变更记录"和"修订记录"合并为一张"修订记录"表。

#### Scenario: 记录需求变更

- **WHEN** 任何阶段发生需求变更
- **THEN** 目标设计目录 index.md 的修订记录表增加一条记录
- **AND** 记录包含：版本、日期、修订类型、修订内容、影响功能点、触发阶段
- **AND** .status.md 的设计修订同步追踪表追加对应的追踪行
