# round-counter Specification

## Purpose
Defines the execution round counter mechanism that tracks agent iteration progress in change-level and subchange-level .status.md files.

## Requirements
### Requirement: 执行轮次计数器格式与维护

系统 SHALL 在变更级和子变更级 .status.md 的 `## 基本信息` 区维护 `**执行轮次**: {N} / {上限}` 字段，用于追踪当前执行类阶段的迭代轮次进度。`{上限}` SHALL 为变更档位决定的轮次上限（`轻量` 1 / `标准` 2 设计·3 执行 / `完整` 5），SHALL NOT 固定为 10。该字段 SHALL 仅记录审查轮，复检轮 SHALL NOT 计入该字段。

#### Scenario: 子变更级阶段开始时初始化计数器

- **WHEN** 子变更进入新的执行类阶段（计划/编码/代码审查/接口单元测试/E2E测试/缺陷修复）
- **THEN** 主 Agent 在调度 Agent 迭代子代理前，将 `执行轮次` 字段写入 `1 / {上限}`
- **AND** 该字段位于 `## 基本信息` 区，与 `**当前阶段**`、`**执行类型**` 同级

#### Scenario: 变更级阶段开始时初始化计数器

- **WHEN** 变更进入执行类阶段（集成测试/缺陷修复）
- **THEN** 主 Agent 在调度 Agent 迭代子代理前，将变更级 .status.md 中 `执行轮次` 字段写入 `1 / {上限}`
- **AND** 该字段位于变更级 `## 基本信息` 区，与 `**当前阶段**` 同级

#### Scenario: Agent 每轮迭代后递增计数器

- **WHEN** Agent 迭代子代理完成一轮迭代
- **THEN** Agent MUST 更新对应级别 .status.md 中 `执行轮次` 字段为当前轮次号（如 `2 / 3`、`3 / 5`）
- **AND** 递增 MUST 在进入下一轮之前完成

#### Scenario: 阶段切换时重置计数器

- **WHEN** 当前执行类阶段完成，变更或子变更进入下一个执行类阶段
- **THEN** 计数器重置为 `1 / {上限}`，与新阶段生命周期对齐
- **AND** 旧阶段的最终值 `{N} / {上限}` 保留在执行记录中

#### Scenario: 计数器格式和位置固定

- **WHEN** .status.md 被读取或解析
- **THEN** `执行轮次` 字段位于 `## 基本信息` 区
- **AND** 格式固定为 `**执行轮次**: {N} / {上限}`
- **AND** N 为 1 至轮次上限之间的整数

#### Scenario: 复检轮不计入计数器

- **WHEN** 阶段执行复检轮
- **THEN** `.status.md` 的 `执行轮次` 字段 SHALL 保持执行复检轮之前的取值
- **AND** 分母 SHALL NOT 因复检轮而变更

#### Scenario: 非执行类阶段不使用计数器

- **WHEN** 当前阶段为非执行类阶段（设计探索/原型设计/详细设计/审计/归档）
- **THEN** `执行轮次` 字段不存在或标记为 `--`（不适用）
- **AND** 阶段切换至执行类阶段时，主 Agent 创建并初始化为 `1 / {上限}`

### Requirement: 轮次验收判据

系统 SHALL 在 Agent 迭代子代理返回后进行轮次验收。验收通过条件 SHALL 为：`执行轮次 >= 1` 且（最近一轮为见证轮**或** `执行轮次 = 轮次上限`**或**存在通过的复检轮）。因收敛提前返回是合法的，SHALL NOT 仅因未达轮次上限而拒收。

#### Scenario: 收敛终止验收

- **WHEN** 主 Agent 读取 .status.md 发现 `执行轮次 >= 1` 且最近一轮为见证轮
- **AND** 其他验收条件满足（产物齐全、覆盖率达标、无占位符）
- **THEN** 验收通过
- **AND** 更新阶段状态为 ✅ 完成

#### Scenario: 达上限验收

- **WHEN** 主 Agent 读取 .status.md 发现 `执行轮次` = `{上限} / {上限}`
- **AND** 其他验收条件满足（产物齐全、覆盖率达标、无占位符）
- **THEN** 验收通过
- **AND** 终止原因 SHALL 记录为 `达上限`

#### Scenario: 复检轮通过时验收通过

- **WHEN** 主 Agent 读取 .status.md 发现存在通过的复检轮
- **AND** 终止原因记录为 `收敛（复检轮）`
- **AND** 其他验收条件满足（产物齐全、覆盖率达标、无占位符）
- **THEN** 验收通过
- **AND** 更新阶段状态为 ✅ 完成

#### Scenario: 无见证轮且未达上限时拒收

- **WHEN** 主 Agent 读取 .status.md 发现 `执行轮次` < 轮次上限 且 无任何一轮为见证轮
- **THEN** 验收不通过，拒收
- **AND** 主 Agent 要求 Agent 子代理继续执行剩余轮次（不接受无理由的提前返回）
- **AND** 不进入 AskUserQuestion 流程——直接重新启动 Agent 子代理

#### Scenario: 达上限仍无见证轮进入非收敛分支

- **WHEN** `执行轮次` = 轮次上限 且 无任何一轮为见证轮
- **AND** 不存在通过的复检轮
- **AND** 其他验收条件不满足（产物缺失、覆盖率不足、有占位符）
- **THEN** 系统 SHALL 记录到 skill-suggestion.md
- **AND** SHALL 使用 AskUserQuestion 询问用户
