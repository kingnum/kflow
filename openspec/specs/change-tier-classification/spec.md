# change-tier-classification Specification

## Purpose

定义变更档位的判定与记录机制：以影响范围分数将变更划分为轻量、标准两档，分两段判定并持久化到变更级状态文件，承载用户覆盖与单向升档安全阀；历史变更遗留的 `完整` 取值在读取侧归并为 `标准`。

## Requirements

### Requirement: 变更档位字段持久化

变更级 `.status.md` 的基本信息 SHALL 包含「变更档位」字段，取值为 `轻量` 或 `标准`。该字段 SHALL 由 kflow-explore 在确定档位后写入，并由 kflow-design 复核后更新。

#### Scenario: explore 阶段写入档位

- **WHEN** kflow-explore 完成档位判定
- **THEN** 系统 SHALL 将档位写入变更级 `.status.md` 基本信息的「变更档位」字段
- **AND** 写入值 SHALL 为 `轻量` 或 `标准`

#### Scenario: design 复核后更新档位

- **WHEN** kflow-design 的 DIVIDE 之后复核档位并确认升档
- **THEN** 系统 SHALL 用新档位覆写变更级 `.status.md` 的「变更档位」字段

#### Scenario: 历史变更的完整档取值归并

- **WHEN** 读取侧遇到历史变更 `.status.md` 中遗留的 `变更档位 = 完整`
- **THEN** 系统 SHALL 将该取值归并为 `标准` 后使用
- **AND** SHALL NOT 要求用户手工修改历史状态文件

### Requirement: 档位由影响范围分数派生

系统 SHALL 以影响范围分数作为档位判定的唯一量化依据，公式为 `功能点数 x 1 + 接口数 x 1.5 + 数据模型变更数 x 2`。阈值映射为：分数 <= 3 为 `轻量`，分数 > 3 为 `标准`。系统 SHALL NOT 为任何变更类型保留独立于该公式的档位映射。

#### Scenario: 低分映射轻量档

- **WHEN** 影响范围分数 <= 3
- **THEN** 档位 SHALL 为 `轻量`

#### Scenario: 中分映射标准档

- **WHEN** 影响范围分数大于 3 且不超过 15
- **THEN** 档位 SHALL 为 `标准`

#### Scenario: 高分映射完整档

- **WHEN** 影响范围分数 > 15
- **THEN** 档位 SHALL 为 `标准`
- **AND** SHALL NOT 存在按分数上探的第三档取值

#### Scenario: 无变更类型例外

- **WHEN** 系统对任一变更类型执行档位判定
- **THEN** SHALL 使用同一影响范围分数公式
- **AND** SHALL NOT 存在按变更类型的无条件档位映射

### Requirement: 产品需求档位下限抬升

变更类型为 `产品需求` 的变更 SHALL 与功能需求、功能缺陷采用相同的影响范围分数映射，SHALL NOT 因变更类型为 `产品需求` 而抬升档位。kflow-design 的复核环节仍适用单向升档安全阀。

#### Scenario: 产品需求强制完整档

- **WHEN** 变更级 `.status.md` 的变更类型为 `产品需求` 且其影响范围分数在 4 至 15 之间
- **THEN** 档位 SHALL 为 `标准`
- **AND** SHALL NOT 因变更类型为 `产品需求` 而抬升档位

#### Scenario: 产品需求分数高时仍为完整档

- **WHEN** 变更级 `.status.md` 的变更类型为 `产品需求` 且其影响范围分数 > 15
- **THEN** 档位 SHALL 为 `标准`

### Requirement: 两段式档位判定时机

档位判定 SHALL 分两段执行：kflow-explore 的 SPLIT 之后执行初判，kflow-design 的 DIVIDE 之后执行复核。初判 SHALL 仅使用初判时可得的信息；复核 SHALL 使用完整影响范围分数公式。两段的映射规则 SHALL 对所有变更类型一致适用，SHALL NOT 因变更类型而分支。

#### Scenario: explore 初判使用可得信息

- **WHEN** kflow-explore 完成 SPLIT 步骤
- **THEN** 系统 SHALL 以变更类型与功能点数执行档位初判
- **AND** SHALL NOT 要求接口数或数据模型变更数（explore 阶段域外内容禁止接口定义与数据模型设计）

#### Scenario: design 复核使用完整公式

- **WHEN** kflow-design 完成 DIVIDE 步骤
- **THEN** 系统 SHALL 以完整影响范围分数公式执行档位复核

#### Scenario: 两段均无变更类型分支

- **WHEN** 任一变更类型执行初判或复核
- **THEN** 系统 SHALL 使用同一映射规则
- **AND** SHALL NOT 存在按变更类型的无条件档位分支

### Requirement: explore 初判映射规则

kflow-explore 初判 SHALL 按以下规则映射档位：`功能缺陷` 且功能点数 <= 3 为 `轻量`；`功能缺陷` 且功能点数 > 3 为 `标准`；`功能需求` 且功能点数 <= 2 为 `轻量`；`功能需求` 且功能点数 > 2 为 `标准`；`产品需求` SHALL 按功能点数比照功能需求的分档规则判定，SHALL NOT 无条件判定为 `标准` 之外的档位。初判结果 SHALL 标注为「初判」，并由 kflow-design 的复核环节用完整影响范围分数公式校正。

#### Scenario: 小规模功能缺陷判为轻量

- **WHEN** 变更类型为 `功能缺陷` 且功能点数 <= 3
- **THEN** 初判档位 SHALL 为 `轻量`

#### Scenario: 中等规模功能需求判为标准

- **WHEN** 变更类型为 `功能需求` 且功能点数在 3 至 10 之间
- **THEN** 初判档位 SHALL 为 `标准`

#### Scenario: 大规模功能需求判为完整

- **WHEN** 变更类型为 `功能需求` 且功能点数 > 10
- **THEN** 初判档位 SHALL 为 `标准`
- **AND** SHALL NOT 存在按功能点数上探的第三档

#### Scenario: 产品需求按功能点数初判

- **WHEN** 变更类型为 `产品需求` 且功能点数为 5
- **THEN** 初判档位 SHALL 为 `标准`

### Requirement: 用户覆盖档位

用户在 kflow-explore 的确认环节 SHALL 能够上调或下调档位判定结果。用户覆盖结果 SHALL 被记录到变更级 `.status.md`，并优先于初判结果用于后续阶段。

#### Scenario: 用户上调档位

- **WHEN** 初判档位为 `轻量` 且用户在确认环节选择上调
- **THEN** 系统 SHALL 将档位改为 `标准`
- **AND** 后续阶段 SHALL 按用户选择的档位执行

#### Scenario: 用户下调档位

- **WHEN** 初判档位为 `标准` 且用户在确认环节选择下调
- **THEN** 系统 SHALL 将档位改为 `轻量`
- **AND** 后续阶段 SHALL 按新档位执行

### Requirement: 单向升档安全阀

kflow-design 的复核阶段 SHALL 仅允许升档，禁止降档。复核档位高于初判档位时，系统 SHALL 经用户确认后升档并按新档位执行后续阶段，SHALL NOT 回退 kflow-explore 阶段。复核档位不高于初判档位时，系统 SHALL 维持原档位。

#### Scenario: 复核发现影响超预估触发升档

- **WHEN** 复核档位高于当前档位
- **THEN** 系统 SHALL 通过 AskUserQuestion 请求用户确认升档
- **AND** 用户确认后 SHALL 按新档位执行后续阶段
- **AND** SHALL NOT 回退 kflow-explore 阶段

#### Scenario: 复核档位不高于当前档位时禁止降档

- **WHEN** 复核档位不高于当前档位
- **THEN** 系统 SHALL 维持当前档位执行
- **AND** SHALL NOT 降档

### Requirement: 历史变更的档位缺省回退

缺少「变更档位」字段或字段取值不在 `{轻量, 标准}` 枚举内的历史变更 `.status.md`，系统 SHALL 按 `标准` 档处理。

#### Scenario: 无档位字段按完整档处理

- **WHEN** 变更级 `.status.md` 基本信息中不含「变更档位」字段
- **THEN** 系统 SHALL 按 `标准` 档确定审查形态与产出深度

#### Scenario: 非法取值按标准档处理

- **WHEN** 变更级 `.status.md` 的「变更档位」字段取值不在 `{轻量, 标准}` 枚举内
- **THEN** 系统 SHALL 按 `标准` 档处理
- **AND** SHALL 将该异常记录到 `docs/skill-suggestion.md`
