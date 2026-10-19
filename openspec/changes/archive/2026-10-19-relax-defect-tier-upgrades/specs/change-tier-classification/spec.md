# Spec Delta

## REMOVED Requirements

### Requirement: 档位由影响范围分数派生

**Reason**: 原公式把“受影响接口数”与“修改接口契约数”混为一谈，且保留三档时代的“中分/高分”场景。档位应衡量设计面变更量，而非代码或接口的爆炸半径。

**Migration**: 使用 ADDED「档位由设计面分数派生」。计量口径改为接口契约变更数与 schema/migration 变更数；受影响但未改契约的接口改由 triage 的影响面清单承载。历史变更无需迁移；历史 `完整` 取值仍按 `标准` 读取。

## MODIFIED Requirements

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

## ADDED Requirements

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
