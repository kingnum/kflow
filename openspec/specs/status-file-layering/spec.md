# status-file-layering Specification

## Purpose

定义变更级状态文件的分层结构——把仅需当前判定所需的状态与需要长期留存的历史记录分离到两个文件，使状态文件在长流程中不随阶段推进而无限增长，从而降低其被反复读取时的上下文占用。

## Requirements

### Requirement: 当前状态文件与历史日志文件分离

变更级状态 SHALL 拆分为两个文件：`.status.md` 仅承载当前有效状态，`status-log.md` 承载历史记录。两者 SHALL 均位于变更目录下。

#### Scenario: 文件职责划分

- **WHEN** 变更目录的状态文件被创建
- **THEN** `.status.md` SHALL 承载：当前阶段、阶段状态表、变更档位、执行轮次、终止结果、当前未决事项
- **AND** `status-log.md` SHALL 承载：各阶段完成时间与耗时、历史轮次记录、回退与重执行记录、阶段状态变更轨迹

#### Scenario: 当前状态文件的行数约束

- **WHEN** `.status.md` 被写入
- **THEN** 其内容 SHALL 保持在 100 行以内
- **AND** 超出该约束的内容 SHALL 改为写入 `status-log.md`

### Requirement: 历史记录在阶段完成时写入日志文件

每次阶段完成、回退或重执行时，主 Agent SHALL 将该次事件追加写入 `status-log.md`，并同步刷新 `.status.md` 中的当前状态字段。

#### Scenario: 阶段完成时追加日志

- **WHEN** 任一阶段完成
- **THEN** `status-log.md` SHALL 追加该阶段的完成记录（阶段名、轮次、完成时间、耗时、终止结果）
- **AND** `.status.md` 的当前阶段字段 SHALL 更新为下一阶段

#### Scenario: 回退时追加日志

- **WHEN** 发生阶段回退或重执行
- **THEN** `status-log.md` SHALL 追加该次回退的原因与目标阶段
- **AND** `.status.md` 的当前阶段字段 SHALL 更新为回退目标阶段

### Requirement: 日志文件仅在恢复与审计场景读取

`status-log.md` SHALL 仅在中断恢复与审计场景被读取；常规阶段推进与门控判定 SHALL 仅读取 `.status.md`。

#### Scenario: 常规推进不读日志

- **WHEN** 阶段推进、门控判定、子代理构造时读取状态
- **THEN** 读取目标 SHALL 仅为 `.status.md`
- **AND** SHALL NOT 读取 `status-log.md`

#### Scenario: 恢复场景读取日志

- **WHEN** kflow-resume 执行断点定位
- **THEN** SHALL 读取 `status-log.md` 以还原阶段轨迹与回退记录
- **AND** SHALL 读取 `.status.md` 以获取当前状态

#### Scenario: 审计场景读取日志

- **WHEN** kflow-audit 执行耗时数据汇总
- **THEN** SHALL 读取 `status-log.md` 以获取各阶段耗时记录

### Requirement: 历史状态文件格式的向后兼容

读取侧 SHALL 兼容既有变更目录中的单文件 `.status.md`（未分层形态）。

#### Scenario: 历史变更的状态读取

- **WHEN** 变更目录中不存在 `status-log.md`
- **THEN** 读取侧 SHALL 按既有单文件口径解析 `.status.md`
- **AND** SHALL NOT 因缺失 `status-log.md` 报错或阻塞

#### Scenario: 历史变更不回填

- **WHEN** 对已完成或进行中的历史变更执行阶段推进
- **THEN** 系统 SHALL NOT 强制拆分其 `.status.md`
- **AND** 新结构 SHALL 自下一个新建变更起适用
