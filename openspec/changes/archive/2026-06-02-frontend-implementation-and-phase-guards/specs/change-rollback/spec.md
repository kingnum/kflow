## MODIFIED Requirements

### Requirement: 阶段回退门控

系统 SHALL 定义阶段回退时的门控规则，支持六种回退触发来源，回退目标包含 explore、design、prototype-design 三种阶段。

#### Scenario: 回退触发来源

- **WHEN** 需要触发阶段回退
- **THEN** 系统判断回退触发来源为以下六种之一：缺陷修复根因（设计错误）、代码审查发现问题、用户需求变更、kflow-audit 审计发现、编码发现原型交互/视觉/状态问题、编码发现功能点/业务规则问题
- **AND** 不同来源使用相同的回退门控规则

#### Scenario: 回退到设计阶段

- **WHEN** 需要回退到详细设计阶段
- **THEN** 详细设计状态: ✅ → ⚠️ 需修订
- **AND** 计划、编码、测试等后续阶段状态: 重置为 ⏳ 待开始
- **AND** 受影响产物标记为"待修订"（不删除，保留参考）

#### Scenario: 回退到原型设计阶段

- **WHEN** 编码阶段发现原型交互流程/视觉设计/状态覆盖存在问题
- **THEN** 原型设计状态: ✅ → ⚠️ 需修订
- **AND** 进入 prototype-design REVISION 模式（加载已有原型 + 用户修订需求 → 修订 → 验证 → 用户确认）
- **AND** design、plan、code 等后续阶段状态: 重置为 ⏳ 待开始

#### Scenario: 仅当前子变更回退

- **WHEN** 回退仅影响单个子变更
- **THEN** 其他子变更不受影响
- **AND** 仅该子变更的阶段状态被重置

#### Scenario: 接口契约变更导致多子变更联动回退

- **WHEN** 回退涉及接口契约变更
- **THEN** 依赖该接口的所有子变更联动回退
- **AND** 评估影响范围后用户确认修订方案

## ADDED Requirements

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
