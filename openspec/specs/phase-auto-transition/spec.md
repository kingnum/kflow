# phase-auto-transition Specification

## Purpose

定义阶段 Skill 完成后的自动衔接规则——阶段的 COMPLETE 步骤结束后，按变更当前状态直接调度下一阶段 Skill，免除用户手动输入推进指令；并在归档阶段、阻塞状态与各类人工评审门控处正确停止，避免自动流转越过必要的用户确认点。

## Requirements

### Requirement: 阶段完成后自动衔接下一阶段

阶段 Skill SHALL 在其 COMPLETE 步骤完成后执行阶段衔接决策，并按决策结果直接调度目标阶段 Skill。系统 SHALL NOT 将「提示用户输入推进指令（如「继续 {change-name}」）」作为进入下一阶段的必要条件。

#### Scenario: 阶段完成且下一阶段待开始

- **WHEN** 阶段 Skill 的 COMPLETE 步骤完成
- **AND** `docs/changes/{change}/.status.md` 中该阶段的下一阶段状态为 `⏳ 待开始`
- **THEN** 系统 SHALL 直接调度该下一阶段 Skill
- **AND** SHALL NOT 提示用户输入推进指令

#### Scenario: 连续多个阶段已完成

- **WHEN** 阶段 Skill 的 COMPLETE 步骤完成
- **AND** 其后连续多个阶段在 `.status.md` 中均标记为 `✅ 完成`
- **THEN** 系统 SHALL 递归推进至第一个非 `✅ 完成` 的阶段
- **AND** 递归推进 SHALL 在遇到 `⏳ 待开始` 阶段时停止并调度该阶段

#### Scenario: 变更全部阶段完成

- **WHEN** 阶段衔接决策推进至最后阶段且该阶段标记为 `✅ 完成`
- **THEN** 系统 SHALL 停止自动衔接
- **AND** SHALL NOT 自动进入归档

#### Scenario: 子变更级阶段的衔接

- **WHEN** 当前阶段为子变更级阶段（计划、编码、代码审查、接口单元测试、E2E 测试）
- **THEN** 系统 SHALL 在当前子变更内推进至下一阶段
- **AND** 当前子变更全部阶段完成后，SHALL 按子变更遍历顺序推进至下一个子变更的首个未完成阶段

### Requirement: 阶段衔接决策表

系统 SHALL 按目标阶段的 `.status.md` 状态执行衔接决策，判定结果 SHALL 覆盖完成、进行中、需修订、阻塞、待开始五种状态。

#### Scenario: 状态为完成

- **WHEN** 目标阶段状态为 `✅ 完成`
- **THEN** 系统 SHALL 自动推进到下一阶段并重新执行衔接决策

#### Scenario: 状态为进行中

- **WHEN** 目标阶段状态为 `🔄 进行中`
- **THEN** 系统 SHALL 调度该阶段 Skill

#### Scenario: 状态为需修订

- **WHEN** 目标阶段状态为 `⚠️ 需修订`
- **THEN** 系统 SHALL 调度该阶段标注的回退目标阶段 Skill
- **AND** SHALL NOT 调度标注为需修订的阶段本身

#### Scenario: 状态为阻塞

- **WHEN** 目标阶段状态为 `❌ 阻塞`
- **THEN** 系统 SHALL 输出阻碍信息
- **AND** SHALL NOT 调度任何阶段 Skill

#### Scenario: 状态为待开始

- **WHEN** 目标阶段状态为 `⏳ 待开始`
- **THEN** 系统 SHALL 调度该阶段 Skill

### Requirement: 归档阶段禁止自动衔接

系统 SHALL NOT 将归档阶段纳入自动衔接的推进目标。变更全部阶段完成后，系统 SHALL 停止自动衔接并等待用户显式发起归档。

#### Scenario: 审计阶段完成后的衔接

- **WHEN** 审计阶段 COMPLETE 步骤完成，且其后仅剩归档阶段
- **THEN** 系统 SHALL 停止自动衔接
- **AND** SHALL NOT 自动调度 `kflow-archive`
- **AND** 系统 MAY 提示用户可发起归档，但该提示 SHALL NOT 构成自动流转

### Requirement: 人工评审门控与自动衔接共存

阶段自身定义的人工评审门控（原型设计决策门控、用户评审、用户验收门控等）SHALL 在自动衔接过程中正常执行。自动衔接免除的 SHALL 仅为「提示用户输入推进指令」，SHALL NOT 免除阶段自有的人工确认。

#### Scenario: 原型设计决策门控

- **WHEN** 设计探索阶段完成，且变更的 `prototype_decision` 标记未设置
- **THEN** 系统 SHALL 先执行原型设计决策询问
- **AND** 按用户选择进入原型设计阶段或跳过该阶段
- **AND** 无论用户选择如何，衔接 SHALL NOT 要求用户额外输入推进指令

#### Scenario: 用户评审门控

- **WHEN** 阶段定义了用户评审门控（如详细设计的方案评审、原型的用户评审）
- **THEN** 系统 SHALL 执行该评审询问并等待用户确认
- **AND** 用户确认后 SHALL 直接执行衔接决策进入下一阶段

#### Scenario: 用户验收门控

- **WHEN** 审计阶段定义了用户验收门控
- **THEN** 系统 SHALL 执行该验收询问
- **AND** 该门控 SHALL NOT 被自动衔接跳过

### Requirement: 阶段阻断时的用户介入提示

系统在停止自动衔接时 SHALL 向用户说明停止原因与可执行的下一步操作，使用户无需记忆 Skill 名称即可介入。

#### Scenario: 因阻塞停止

- **WHEN** 衔接决策因目标阶段状态为 `❌ 阻塞` 而停止
- **THEN** 系统 SHALL 输出阻碍信息，包含阻塞阶段名称、阻塞原因与解除阻塞的建议操作

#### Scenario: 因归档闸口停止

- **WHEN** 衔接决策因仅剩归档阶段而停止
- **THEN** 系统 SHALL 提示变更已具备归档条件及发起归档的方式
