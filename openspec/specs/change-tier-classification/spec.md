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

### Requirement: 档位由设计面分数派生

系统 SHALL 以设计面分数作为档位判定的唯一量化依据，公式为 `功能点数 x 1 + 接口契约变更数 x 1.5 + 数据模型变更数 x 2`。阈值映射为：分数 <= 3 为 `轻量`，分数 > 3 为 `标准`。

计量口径：

- 功能点数 = 本变更涉及的功能点数量
- 接口契约变更数 = 本变更新增或修改的 API 契约数量；受影响但契约未修改的接口 SHALL NOT 计入
- 数据模型变更数 = 本变更新增或修改的 schema/migration 数量；纯数据修正 SHALL NOT 计入
- 受影响项清单（爆炸半径）由 triage 产出，仅用于定向验证范围与回退判定，SHALL NOT 计入本分数

系统 SHALL NOT 为任何变更类型保留独立于该公式的档位映射。字段名「影响范围分数」在状态文件与既有文档中保留，其语义按本节改为设计面分数。

#### Scenario: 低分映射轻量档

- **WHEN** 设计面分数 <= 3
- **THEN** 档位 SHALL 为 `轻量`

#### Scenario: 分数大于 3 映射标准档

- **WHEN** 设计面分数 > 3
- **THEN** 档位 SHALL 为 `标准`
- **AND** SHALL NOT 存在按分数上探的第三档取值

#### Scenario: 无变更类型例外

- **WHEN** 系统对任一变更类型执行档位判定
- **THEN** SHALL 使用同一设计面分数公式
- **AND** SHALL NOT 存在按变更类型的无条件档位映射

#### Scenario: 受影响接口不计入

- **WHEN** 缺陷修复涉及多个受影响接口 且 未修改任何接口契约
- **THEN** 接口契约变更数 SHALL 为 0
- **AND** 受影响接口清单 SHALL 仅用于定向验证范围

#### Scenario: 纯数据修正不计入

- **WHEN** 缺陷修复只修正数据 且 未修改 schema 或 migration
- **THEN** 数据模型变更数 SHALL 为 0

### Requirement: 设计面与影响面分离

系统 SHALL 区分设计面分数与影响面清单，二者服务于不同目的。

#### Scenario: 两个度量各自使用

- **WHEN** 系统计算档位
- **THEN** SHALL 仅使用设计面分数
- **WHEN** 系统确定定向验证或回退范围
- **THEN** SHALL 仅使用影响面清单
- **AND** 影响面清单 SHALL NOT 用于推导档位

#### Scenario: 影响面较大但设计面较小

- **WHEN** 缺陷影响多个接口或用例 但 未修改任何接口契约或 schema
- **THEN** 设计面分数 SHALL 保持较低
- **AND** 档位 SHALL 按设计面分数判定
- **AND** 定向验证范围 SHALL 按影响面清单覆盖全部受影响项

### Requirement: 产品需求档位下限抬升

变更类型为 `产品需求` 的变更 SHALL 与功能需求、功能缺陷采用相同的影响范围分数映射，SHALL NOT 因变更类型为 `产品需求` 而抬升档位。kflow-design 的复核环节仍适用单向升档安全阀。

#### Scenario: 产品需求分数超过阈值时判为标准档

- **WHEN** 变更级 `.status.md` 的变更类型为 `产品需求` 且其影响范围分数 > 3
- **THEN** 档位 SHALL 为 `标准`
- **AND** SHALL NOT 因变更类型为 `产品需求` 而抬升档位

#### Scenario: 产品需求高分不产生第三档

- **WHEN** 变更级 `.status.md` 的变更类型为 `产品需求` 且其影响范围分数为任意大于 3 的取值
- **THEN** 档位 SHALL 保持为 `标准`
- **AND** SHALL NOT 存在按分数上探的第三档取值

### Requirement: 两段式档位判定时机

档位判定 SHALL 分两段执行：kflow-explore 的 SPLIT 之后执行初判，kflow-design 的 DIVIDE 之后执行复核。初判 SHALL 仅使用初判时可得的信息；复核 SHALL 使用设计面分数公式。两段的映射规则 SHALL 对所有变更类型一致适用，SHALL NOT 因变更类型而分支。

#### Scenario: explore 初判使用可得信息

- **WHEN** kflow-explore 完成 SPLIT 步骤
- **THEN** 系统 SHALL 以变更类型与功能点数执行档位初判
- **AND** SHALL NOT 要求接口数或数据模型变更数（explore 阶段域外内容禁止接口定义与数据模型设计）

#### Scenario: design 复核使用完整公式

- **WHEN** kflow-design 完成 DIVIDE 步骤
- **THEN** 系统 SHALL 以设计面分数公式执行档位复核

#### Scenario: 两段均无变更类型分支

- **WHEN** 任一变更类型执行初判或复核
- **THEN** 系统 SHALL 使用同一映射规则
- **AND** SHALL NOT 存在按变更类型的无条件档位分支

### Requirement: explore 初判映射规则

kflow-explore 初判 SHALL 按以下规则映射档位：`功能缺陷` 且功能点数 <= 3 为 `轻量`；`功能缺陷` 且功能点数 > 3 为 `标准`；`功能需求` 且功能点数 <= 2 为 `轻量`；`功能需求` 且功能点数 > 2 为 `标准`；`产品需求` SHALL 按功能点数比照功能需求的分档规则判定，SHALL NOT 无条件判定为 `标准` 之外的档位。初判结果 SHALL 标注为「初判」，并由 kflow-design 的复核环节用设计面分数公式校正。

#### Scenario: 小规模功能缺陷判为轻量

- **WHEN** 变更类型为 `功能缺陷` 且功能点数 <= 3
- **THEN** 初判档位 SHALL 为 `轻量`

#### Scenario: 中等规模功能需求判为标准

- **WHEN** 变更类型为 `功能需求` 且功能点数在 3 至 10 之间
- **THEN** 初判档位 SHALL 为 `标准`

#### Scenario: 大规模功能需求判为标准

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

kflow-design 的复核阶段 SHALL 仅允许升档，禁止降档。升档分为硬升档与软升档，并按必要性决定是否提示用户。

- **硬升档**：涉及数据迁移、破坏性接口契约变更或跨变更契约影响时触发；不可拒绝，提示 SHALL 说明原因。
- **软升档**：非硬升档且复核档位高于当前档位时触发；默认选项 SHALL 为保持当前档位，用户可主动选择升档。
- **必要性判定**：仅当升档会实际新增至少一个下游测试阶段（该阶段原本会被判定为 `⏭️ 不适用`），或属于硬升档时，系统 SHALL 提示用户；否则 SHALL 维持当前档位并记录“未升档理由”。
- 用户拒绝软升档后，系统 SHALL 保持当前档位、记录理由，SHALL NOT 在后续阶段重复提示。
- 复核档位不高于当前档位时，系统 SHALL 维持原档位，SHALL NOT 降档。
- 升档 SHALL NOT 回退 kflow-explore 阶段。

#### Scenario: 复核发现影响超预估触发升档

- **WHEN** 复核发现数据迁移、破坏性契约变更或跨变更契约影响
- **THEN** 系统 SHALL 执行硬升档
- **AND** SHALL 通过 AskUserQuestion 说明原因
- **AND** SHALL NOT 提供保持轻量的选项

#### Scenario: 软升档默认保持轻量

- **WHEN** 复核档位高于当前档位且不属于硬升档
- **THEN** 系统 SHALL 通过 AskUserQuestion 展示分数构成与影响
- **AND** 默认选项 SHALL 为保持当前档位
- **AND** 用户选择升档后才覆写档位字段

#### Scenario: 用户拒绝软升档

- **WHEN** 用户在软升档提示中选择保持当前档位
- **THEN** 系统 SHALL 保持当前档位
- **AND** SHALL 在 `.status.md` 记录拒绝理由
- **AND** 后续阶段 SHALL NOT 重复提示升档

#### Scenario: 无必要升档时不提示

- **WHEN** 复核档位高于当前档位 但 升档不会新增任何下游测试阶段 且 不属于硬升档
- **THEN** 系统 SHALL 维持当前档位
- **AND** SHALL 记录“未升档理由”
- **AND** SHALL NOT 弹出升档提示

#### Scenario: 复核档位不高于当前档位时禁止降档

- **WHEN** 复核档位不高于当前档位
- **THEN** 系统 SHALL 维持当前档位执行
- **AND** SHALL NOT 降档

#### Scenario: 升档不回退 explore

- **WHEN** 系统执行硬升档或软升档
- **THEN** SHALL NOT 回退 kflow-explore 阶段
- **AND** SHALL 从当前阶段继续执行

### Requirement: 历史变更的档位缺省回退

缺少「变更档位」字段或字段取值不在 `{轻量, 标准}` 枚举内的历史变更 `.status.md`，系统 SHALL 按 `标准` 档处理。

#### Scenario: 无档位字段按标准档处理

- **WHEN** 变更级 `.status.md` 基本信息中不含「变更档位」字段
- **THEN** 系统 SHALL 按 `标准` 档确定审查形态与产出深度

#### Scenario: 非法取值按标准档处理

- **WHEN** 变更级 `.status.md` 的「变更档位」字段取值不在 `{轻量, 标准}` 枚举内
- **THEN** 系统 SHALL 按 `标准` 档处理
- **AND** SHALL 将该异常记录到 `docs/skill-suggestion.md`
