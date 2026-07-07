# hitl-afk-classification Delta Spec

## MODIFIED Requirements

### Requirement: 子变更 HITL/AFK 分类

系统 SHALL 在 kflow-design 阶段划分子变更时，对每个子变更标注执行类型：AFK（Away From Keyboard，可自动执行）或 HITL（Human In The Loop，设计不完整标记）。HITL 子变更 SHALL NOT 进入 plan 阶段，MUST 在设计阶段解决所有未决决策后转为 AFK。

#### Scenario: AFK 子变更判定

- **WHEN** 子变更满足以下条件：无架构选择决策点、无设计方案确认需求、所有实现路径已由设计文档明确
- **THEN** 系统 SHALL 标记该子变更为 AFK
- **AND** Agent 可直接全自动迭代执行
- **AND** 原「无 UI/UX 方向决策」条件移除——UI/UX 决策 SHALL 在原型设计阶段通过用户评审关闭

#### Scenario: HITL 子变更判定

- **WHEN** 子变更涉及以下任一类型：架构选择未裁决、设计方案确认未完成
- **THEN** 系统 SHALL 标记该子变更为 HITL
- **AND** HITL 是设计阶段不完整标记，非执行类型
- **AND** 标注具体的未决决策点和建议关闭方式

#### Scenario: HITL 阻塞 plan 阶段入口

- **WHEN** 子变更标记为 HITL
- **THEN** 系统 SHALL NOT 允许该子变更进入 plan 阶段
- **AND** 门控 SHALL 显示「子变更存在未决设计决策，请先在 design 或 prototype-design 阶段完成决策」
- **AND** 所有进入 plan 的子变更 MUST 是 AFK

#### Scenario: HITL 决策点关闭

- **WHEN** 设计阶段完成未决决策（ADR 创建、用户评审确认、接口契约批准）
- **THEN** 系统 SHALL 将该子变更从 HITL 转为 AFK
- **AND** SHALL 在 detailed-design.md 子变更划分表中更新执行类型
- **AND** 释放 plan 阶段入口门控

## REMOVED Requirements

### Requirement: HITL 子变更执行
**Reason**: HITL 不再作为执行类型。编码阶段不应出现决策点。所有决策在设计阶段完成。
**Migration**: 原 HITL 决策点在编码阶段触发 AskUserQuestion 的机制移除。决策前移到 design 或 prototype-design 阶段的用户评审中完成。

## ADDED Requirements

### Requirement: AFK 判定标准更新

系统 SHALL 使用更新的 AFK 判定标准，移除 UI/UX 方向决策条件。

#### Scenario: AFK 新三条件判定
- **WHEN** 判定子变更是否 AFK
- **THEN** 系统 SHALL 检查：无架构选择决策点、无设计方案确认需求、所有实现路径已明确
- **AND** UI/UX 方向决策 SHALL 视为已在 prototype-design 用户评审阶段解决
- **AND** 三项条件全部满足时标记为 AFK
