# Spec Delta

## Purpose

定义档位驱动的轮次决策：以变更档位确定执行类阶段与设计自审的目标轮次，替代与变更规模无关的固定下限，并规定回退重执行的叠加规则与相应验证门控。

## ADDED Requirements

### Requirement: 执行类阶段轮次按档位决定

执行类阶段（编码、代码审查、接口单元测试、E2E测试、集成测试、缺陷修复）的目标轮次 SHALL 由变更档位决定：`轻量` 为 1 轮，`标准` 为 3 轮，`完整` 为 10 轮。

kflow-plan 阶段的迭代循环为**产物自审**（其每轮工作为对 tasks.md 执行 4 维度审查），SHALL 取设计自审口径（`轻量` 0 轮 / `标准` 2 轮 / `完整` 10 轮），SHALL NOT 取本需求列的 1/3/10。

#### Scenario: 轻量档执行 1 轮

- **WHEN** 变更档位为 `轻量` 且任一执行类阶段（编码/代码审查/接口单元测试/E2E测试/集成测试/缺陷修复）启动
- **THEN** 目标轮次 SHALL 为 1 轮

#### Scenario: 标准档执行 3 轮

- **WHEN** 变更档位为 `标准` 且任一执行类阶段（编码/代码审查/接口单元测试/E2E测试/集成测试/缺陷修复）启动
- **THEN** 目标轮次 SHALL 为 3 轮

#### Scenario: 完整档执行 10 轮

- **WHEN** 变更档位为 `完整` 且任一执行类阶段（编码/代码审查/接口单元测试/E2E测试/集成测试/缺陷修复）启动
- **THEN** 目标轮次 SHALL 为 10 轮

#### Scenario: plan 阶段取其自审口径

- **WHEN** kflow-plan 阶段的迭代循环启动 且 变更档位为 `轻量`
- **THEN** 目标轮次 SHALL 为 0 轮（以产物完整性门控替代迭代）
- **AND** SHALL NOT 为 1 轮

### Requirement: 设计自审轮次按档位决定

设计类阶段（kflow-explore、kflow-prototype-design、kflow-design）SELFREV 自审的目标轮次 SHALL 由变更档位决定：`轻量` 为 0 轮，`标准` 为 2 轮，`完整` 为 10 轮。kflow-prototype-design 阶段 SHALL 仅在该变更选择「子代理自动审查验证」审查方式时执行自审；选择「人工审查」时 SHALL 完全跳过 SELFREV，SHALL NOT 保留兜底轮次。

#### Scenario: 轻量档跳过自审

- **WHEN** 变更档位为 `轻量` 且设计类阶段完成产物初稿
- **THEN** SELFREV SHALL NOT 执行
- **AND** 系统 SHALL NOT 创建自审报告
- **AND** 阶段 SHALL 直接进入下一门控

#### Scenario: 标准档执行 2 轮自审

- **WHEN** 变更档位为 `标准` 且设计类阶段完成产物初稿
- **THEN** SELFREV SHALL 执行 2 轮子代理串行自审

#### Scenario: 完整档执行 10 轮自审

- **WHEN** 变更档位为 `完整` 且设计类阶段完成产物初稿
- **THEN** SELFREV SHALL 执行 10 轮子代理串行自审

#### Scenario: prototype 阶段选择人工审查时跳过自审

- **WHEN** 当前阶段为 kflow-prototype-design 且该变更选择「人工审查」审查方式
- **THEN** SELFREV SHALL NOT 执行，不计算目标轮次、不执行评分底线判定
- **AND** 系统 SHALL 直接进入用户评审 REVIEW 步骤

### Requirement: 废除首次一律最大的轮次下限

系统 SHALL NOT 以「首次执行」或「首次创建」作为轮次决定的依据。执行类阶段首次执行的 10 轮下限，以及设计自审首次创建的固定 10 轮规则，SHALL NOT 存在。

#### Scenario: 首次执行按档位而非固定 10 轮

- **WHEN** 某执行类阶段在变更中首次执行 且 变更档位为 `轻量`
- **THEN** 目标轮次 SHALL 为 1 轮
- **AND** SHALL NOT 为 10 轮

#### Scenario: 项目无设计基础时不触发 10 轮自审

- **WHEN** 项目无设计基础（`docs/CONTEXT.md` 不存在 或 `docs/designs/detailed-designs/` 为空） 且 变更档位为 `轻量`
- **THEN** SELFREV SHALL NOT 执行
- **AND** 系统 SHALL NOT 依据项目设计基础状态调整轮次

### Requirement: 回退重执行的轮次叠加规则

阶段回退重执行时，目标轮次 SHALL 取档位基线与影响范围分数映射值的较大者。影响范围分数映射规则统一为：分数 <= 3 映射 1 轮，分数在 4 至 15 之间映射 3 轮，分数 > 15 映射 10 轮。`.status.md` 中无影响范围分数可用时，目标轮次 SHALL 为档位基线。

#### Scenario: 回退重执行取较大者

- **WHEN** 阶段回退重执行 且 变更档位为 `轻量` 且 影响范围分数为 8
- **THEN** 目标轮次 SHALL 为 max(1, 3) = 3 轮

#### Scenario: 影响范围分数低于档位基线时维持基线

- **WHEN** 阶段回退重执行 且 变更档位为 `完整` 且 影响范围分数为 1
- **THEN** 目标轮次 SHALL 为 max(10, 1) = 10 轮

#### Scenario: 无影响范围分数时采用档位基线

- **WHEN** 阶段回退重执行 且 `.status.md` 中无影响范围分数
- **THEN** 目标轮次 SHALL 为档位基线

### Requirement: 统一轮次映射口径

影响范围分数到轮次的映射 SHALL 仅在本能力中定义一次。其他能力（kflow-bug-triage 的影响评估、重复制执行模型、设计审查分级）SHALL 引用本映射，SHALL NOT 另行定义数值区间。

#### Scenario: triage 引用统一映射

- **WHEN** kflow-bug-triage 输出影响评估报告的推荐轮次
- **THEN** 推荐轮次 SHALL 取自本能力定义的统一映射

#### Scenario: 各执行类阶段的重复制模型引用统一映射

- **WHEN** 任一执行类阶段的 `references/repetition.md` 描述轮次决策
- **THEN** 轮次规则 SHALL 引用本能力定义的档位基线与叠加规则
- **AND** SHALL NOT 定义自己的分数区间表

### Requirement: 完整档自审评分底线

变更档位为 `完整` 时，SELFREV 每轮 SHALL 输出各维度评分（0-10 量纲），自审通过 SHALL 要求各维度评分均 > 8；任一维度 <= 8 SHALL 继续补审，直至各维度均 > 8 或达到 10 轮上限。

#### Scenario: 各维度达标即通过

- **WHEN** 变更档位为 `完整` 且本轮各维度评分均 > 8
- **THEN** 自审 SHALL 通过

#### Scenario: 未达标继续补审

- **WHEN** 变更档位为 `完整` 且任一维度评分 <= 8
- **THEN** 系统 SHALL 继续补审
- **AND** 直至各维度均 > 8 或达到 10 轮上限

### Requirement: 轻量档零轮自审的产物门控

变更档位为 `轻量` 时，SELFREV 豁免 SHALL 以产物完整性门控替代。阶段产物 SHALL 全部存在，且 SHALL NOT 含 TODO、TBD 或未填充占位符。产物门控不通过时阶段 SHALL 阻塞。

#### Scenario: 轻量档以产物门控替代自审

- **WHEN** 变更档位为 `轻量` 且设计类阶段产出完成
- **THEN** 系统 SHALL 校验产物存在性与占位符
- **AND** SHALL NOT 执行 SELFREV
- **AND** 任一产物缺失或含占位符时 SHALL 阻塞该阶段

### Requirement: 目标轮次写入状态文件

系统 SHALL 将目标轮次写入变更级 `.status.md` 的执行轮次字段（形如 `1/3`），并在每轮完成时递增计数器。

#### Scenario: 轮次计数器呈现目标轮次

- **WHEN** 执行类阶段启动 且 变更档位为 `标准`
- **THEN** `.status.md` 的执行轮次 SHALL 呈现为 `1/3` 形式
