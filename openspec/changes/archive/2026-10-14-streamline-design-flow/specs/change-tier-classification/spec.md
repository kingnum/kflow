# Spec Delta

## MODIFIED Requirements

### Requirement: 档位由影响范围分数派生

系统 SHALL 以影响范围分数作为档位判定的唯一量化依据，公式为 `功能点数 x 1 + 接口数 x 1.5 + 数据模型变更数 x 2`。阈值映射为：分数 <= 3 为 `轻量`，分数在 4 至 15 之间为 `标准`，分数 > 15 为 `完整`。系统 SHALL NOT 为任何变更类型保留独立于该公式的档位映射。

#### Scenario: 低分映射轻量档

- **WHEN** 影响范围分数 <= 3
- **THEN** 档位 SHALL 为 `轻量`

#### Scenario: 中分映射标准档

- **WHEN** 影响范围分数在 4 至 15 之间
- **THEN** 档位 SHALL 为 `标准`

#### Scenario: 高分映射完整档

- **WHEN** 影响范围分数 > 15
- **THEN** 档位 SHALL 为 `完整`

#### Scenario: 无变更类型例外

- **WHEN** 系统对任一变更类型执行档位判定
- **THEN** SHALL 使用同一影响范围分数公式
- **AND** SHALL NOT 存在按变更类型的无条件档位映射

### Requirement: 产品需求档位下限抬升

变更类型为 `产品需求` 的变更 SHALL 与功能需求、功能缺陷采用相同的影响范围分数映射，SHALL NOT 因变更类型为 `产品需求` 而抬升档位。kflow-design 的复核环节仍适用单向升档安全阀。

#### Scenario: 产品需求强制完整档

- **WHEN** 变更级 `.status.md` 的变更类型为 `产品需求` 且其影响范围分数在 4 至 15 之间
- **THEN** 档位 SHALL 为 `标准`
- **AND** SHALL NOT 因变更类型为 `产品需求` 而强制判定为 `完整`

#### Scenario: 产品需求分数高时仍为完整档

- **WHEN** 变更级 `.status.md` 的变更类型为 `产品需求` 且其影响范围分数 > 15
- **THEN** 档位 SHALL 为 `完整`

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

kflow-explore 初判 SHALL 按以下规则映射档位：`功能缺陷` 且功能点数 <= 3 为 `轻量`；`功能缺陷` 且功能点数 > 3 为 `标准`；`功能需求` 且功能点数 <= 2 为 `轻量`；`功能需求` 且功能点数在 3 至 10 之间为 `标准`；`功能需求` 且功能点数 > 10 为 `完整`；`产品需求` SHALL 按功能点数比照功能需求的分档规则判定，SHALL NOT 无条件判定为 `完整`。初判结果 SHALL 标注为「初判」，并由 kflow-design 的复核环节用完整影响范围分数公式校正。

#### Scenario: 小规模功能缺陷判为轻量

- **WHEN** 变更类型为 `功能缺陷` 且功能点数 <= 3
- **THEN** 初判档位 SHALL 为 `轻量`

#### Scenario: 中等规模功能需求判为标准

- **WHEN** 变更类型为 `功能需求` 且功能点数在 3 至 10 之间
- **THEN** 初判档位 SHALL 为 `标准`

#### Scenario: 大规模功能需求判为完整

- **WHEN** 变更类型为 `功能需求` 且功能点数 > 10
- **THEN** 初判档位 SHALL 为 `完整`

#### Scenario: 产品需求按功能点数初判

- **WHEN** 变更类型为 `产品需求` 且功能点数为 5
- **THEN** 初判档位 SHALL 为 `标准`
- **AND** SHALL NOT 无条件判定为 `完整`
