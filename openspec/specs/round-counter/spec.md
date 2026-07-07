# round-counter Specification

## Purpose
Defines the execution round counter mechanism that tracks agent iteration progress in change-level and subchange-level .status.md files.

## Requirements
### Requirement: .status.md 维护执行轮次计数器

系统 SHALL 在变更级和子变更级 .status.md 的 `## 基本信息` 区维护 `**执行轮次**: {N} / 10` 字段，用于追踪当前执行类阶段的迭代轮次进度。

#### Scenario: 子变更级阶段开始时初始化计数器

- **WHEN** 子变更进入新的执行类阶段（计划/编码/代码审查/接口单元测试/E2E测试/缺陷修复）
- **THEN** 主 Agent 在调度 Agent 迭代子代理前，将 `执行轮次` 字段写入 `1 / 10`
- **AND** 该字段位于 `## 基本信息` 区，与 `**当前阶段**`、`**执行类型**` 同级

#### Scenario: 变更级阶段开始时初始化计数器

- **WHEN** 变更进入执行类阶段（集成测试/缺陷修复）
- **THEN** 主 Agent 在调度 Agent 迭代子代理前，将变更级 .status.md 中 `执行轮次` 字段写入 `1 / 10`
- **AND** 该字段位于变更级 `## 基本信息` 区，与 `**当前阶段**` 同级

#### Scenario: Agent 每轮迭代后递增计数器

- **WHEN** Agent 迭代子代理完成一轮迭代
- **THEN** Agent MUST 更新对应级别 .status.md 中 `执行轮次` 字段为当前轮次号（如 `2 / 10`、`3 / 10`）
- **AND** 递增 MUST 在进入下一轮之前完成

#### Scenario: 阶段切换时重置计数器

- **WHEN** 当前执行类阶段完成，变更或子变更进入下一个执行类阶段
- **THEN** 计数器重置为 `1 / 10`，与新阶段生命周期对齐
- **AND** 旧阶段的最终值 `10 / 10` 保留在执行记录中

#### Scenario: 计数器格式和位置固定

- **WHEN** .status.md 被读取或解析
- **THEN** `执行轮次` 字段位于 `## 基本信息` 区
- **AND** 格式固定为 `**执行轮次**: {N} / 10`
- **AND** N 为 1-10 的整数

#### Scenario: 非执行类阶段不使用计数器

- **WHEN** 当前阶段为非执行类阶段（设计探索/原型设计/详细设计/审计/归档）
- **THEN** `执行轮次` 字段不存在或标记为 `--`（不适用）
- **AND** 阶段切换至执行类阶段时，主 Agent 创建并初始化为 `1 / 10`

### Requirement: 主 Agent 验收时检查轮次计数器

系统 SHALL 在 Agent 迭代子代理返回后进行轮次计数验收，轮次不足 10/10 视为验收不通过。

#### Scenario: 轮次达标验收

- **WHEN** 主 Agent 读取 .status.md 发现 `执行轮次` = `10 / 10`
- **AND** 其他验收条件满足（产物齐全、覆盖率达标、无占位符）
- **THEN** 验收通过
- **AND** 更新阶段状态为 ✅ 完成

#### Scenario: 轮次不足拒收

- **WHEN** 主 Agent 读取 .status.md 发现 `执行轮次` < `10 / 10`
- **THEN** 验收不通过，拒收
- **AND** 主 Agent 要求 Agent 子代理继续执行剩余轮次（不允许接受"已完成"的理由）
- **AND** 不进入 AskUserQuestion 流程——直接重新启动 Agent 子代理

#### Scenario: 无实际工作可执行时轮次仍递增

- **WHEN** Agent 迭代子代理在当前轮次中无新发现且无可执行工作
- **THEN** Agent 仍 MUST 递增轮次计数器
- **AND** 可在执行记录中注明「第 N 轮：无新发现，验证已通过内容」
- **AND** 不因无工作而跳过轮次或提前返回
