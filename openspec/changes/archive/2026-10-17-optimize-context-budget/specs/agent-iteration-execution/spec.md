# Spec Delta

## ADDED Requirements

### Requirement: 子代理任务粒度上限

执行类阶段的单个子代理 SHALL NOT 承担超过 3 个功能点或 10 个 TDD 步骤。超出该上限的工作 SHALL 被拆分为多个子代理按序执行，前一个子代理返回并落盘后由主 Agent 启动后一个子代理。

#### Scenario: 子代理任务超出上限时拆分

- **WHEN** 一个子变更包含的功能点数量超过 3 个
- **THEN** 主 Agent SHALL 按功能点将其划分为多个子代理任务
- **AND** 每个子代理承担的功能点数量 SHALL 不超过 3 个
- **AND** 各子代理按功能点顺序串行执行，前者的落盘结果作为后者的输入

#### Scenario: 子代理达到上限后返回

- **WHEN** 子代理完成其分配的工作量上限
- **THEN** 子代理 SHALL 更新阶段产物与状态文件后返回执行报告
- **AND** 主 Agent SHALL 启动新的子代理承接剩余工作

#### Scenario: 上限与轮数上限的口径区分

- **WHEN** 构造子代理 prompt
- **THEN** prompt SHALL 包含按功能点或 TDD 步骤计的工作量范围
- **AND** prompt SHALL NOT 包含任何轮数上限数值
- **AND** 工作量上限 SHALL NOT 被表述为「最多执行 N 轮」或任何等价的轮次约束

#### Scenario: 子代理自主要求续做

- **WHEN** 子代理在完成其分配工作量前判断剩余工作需另行承接
- **THEN** 子代理 SHALL 落盘当前进度并返回，说明剩余工作范围
- **AND** 主 Agent SHALL 启动新子代理承接，SHALL NOT 在主 Agent 上下文中继续

### Requirement: 工作量分片与全量遍历的关系

工作量分片 SHALL NOT 改变重复制类阶段「每轮遍历全部工作项」的既有要求；分片仅决定单次子代理调用的工作量边界，轮次遍历范围仍以阶段工作项全集为准。

#### Scenario: 分片不缩减轮内遍历范围

- **WHEN** 重复制类阶段的一轮执行被分片为多个子代理
- **THEN** 该轮次的遍历范围 SHALL 仍为阶段工作项全集
- **AND** 各分片子代理 SHALL 在其所属轮次内完成分配部分的全量流程

#### Scenario: 审查范围冻结继续适用

- **WHEN** 子代理在分片后的范围内执行
- **THEN** 审查对象集合冻结规则 SHALL 继续适用
- **AND** 分片 SHALL NOT 成为扩大审查对象集合或新增审查维度的依据
