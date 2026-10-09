# tier-driven-repetition Specification

## Purpose

定义档位驱动的轮次上限模型：执行轮次下限全局统一为 1 轮，轮次上限由变更档位决定（执行类阶段 轻量 1 / 标准 3 / 完整 5；设计自审 轻量 1 / 标准 2 / 完整 5），以**见证轮**为收敛终止判据并在达上限仍未收敛时进入非收敛分支；替代与变更规模无关的固定下限，并规定回退重执行的叠加规则与相应验证门控。

## Requirements

### Requirement: 轮次上限模型与全局下限

系统 SHALL 采用「全局下限 + 档位上限」的轮次模型：全部阶段与全部口径的执行轮次**下限统一为 1 轮，无例外**；轮次上限由变更档位决定（`轻量` 1 / `标准` 2 设计·3 执行 / `完整` 5）。变更档位 SHALL NOT 表示必须完成的固定轮次数。

#### Scenario: 全局下限为 1 轮

- **WHEN** 任一阶段（设计自审 / 执行类重复制 / prototype VERIFY）启动
- **THEN** 执行轮次 SHALL 不低于 1 轮

#### Scenario: 档位不再表示强制完成数

- **WHEN** 阶段启动 且 变更档位为 `完整`
- **THEN** 系统 SHALL NOT 要求完成固定 10 轮
- **AND** 轮次上限 SHALL 为 5，并在收敛时提前结束

#### Scenario: 轻量档不再存在 0 轮豁免

- **WHEN** 变更档位为 `轻量` 且设计类阶段完成产物初稿
- **THEN** SELFREV SHALL 执行 1 轮
- **AND** SHALL NOT 存在 0 轮豁免路径

### Requirement: 收敛终止条件

系统 SHALL 以**见证轮**作为收敛终止判据。见证轮定义为同时满足以下三条的一轮审查：(a) 零新发现问题；(b) 零修复/零修改；(c) 审查报告证明全部审查维度已完成全量遍历。终止条件 SHALL 为「执行轮次 >= 1（全局下限）且最近一轮为见证轮」，或「执行轮次 = 轮次上限」。

达到轮次上限仍未出现见证轮时，系统 SHALL 进入**非收敛分支**：记录到 `skill-suggestion.md`、使用 AskUserQuestion 询问用户，并可将该阶段标记为 ⚠️ 阻塞。阶段终止时系统 SHALL 在 `.status.md` 写入终止原因（取值 `收敛` 或 `达上限`）。

#### Scenario: 见证轮达成即终止

- **WHEN** 某轮同时满足零新发现、零修改且报告证明全维度全量遍历
- **AND** 执行轮次 >= 1
- **THEN** 阶段 SHALL 终止
- **AND** 终止原因 SHALL 记录为 `收敛`

#### Scenario: 未达成见证轮则继续

- **WHEN** 本轮存在新发现或存在修复/修改
- **AND** 执行轮次 < 轮次上限
- **THEN** 系统 SHALL 继续下一轮

#### Scenario: 达上限仍无见证轮进入非收敛分支

- **WHEN** 执行轮次 = 轮次上限 且 无任何一轮为见证轮
- **THEN** 系统 SHALL 记录到 `skill-suggestion.md`
- **AND** SHALL 使用 AskUserQuestion 询问用户
- **AND** 终止原因 SHALL 记录为 `达上限`
- **AND** 系统 MAY 将该阶段标记为 ⚠️ 阻塞

#### Scenario: 见证轮不得为空转轮

- **WHEN** 某轮报告未证明全部审查维度已完成全量遍历
- **THEN** 该轮 SHALL NOT 被判定为见证轮
- **AND** 系统 SHALL 继续下一轮

### Requirement: 执行类阶段轮次上限按档位决定

执行类阶段（编码、代码审查、接口单元测试、E2E测试、集成测试、缺陷修复）的轮次**上限** SHALL 由变更档位决定：`轻量` 为 1，`标准` 为 3，`完整` 为 5。执行轮次 SHALL 不低于全局下限 1 轮；达成收敛终止条件时 SHALL 提前结束，SHALL NOT 为凑满上限而继续执行无增量价值的轮次。

kflow-plan 阶段的迭代循环为**产物自审**（其每轮工作为对 tasks.md 执行 4 维度审查），SHALL 取设计自审口径（`轻量` 1 轮 / `标准` 2 轮 / `完整` 5 轮），SHALL NOT 取本需求列的 1/3/5。

#### Scenario: 轻量档轮次上限为 1

- **WHEN** 变更档位为 `轻量` 且任一执行类阶段（编码/代码审查/接口单元测试/E2E测试/集成测试/缺陷修复）启动
- **THEN** 轮次上限 SHALL 为 1 轮

#### Scenario: 标准档轮次上限为 3

- **WHEN** 变更档位为 `标准` 且任一执行类阶段（编码/代码审查/接口单元测试/E2E测试/集成测试/缺陷修复）启动
- **THEN** 轮次上限 SHALL 为 3 轮

#### Scenario: 完整档轮次上限为 5

- **WHEN** 变更档位为 `完整` 且任一执行类阶段（编码/代码审查/接口单元测试/E2E测试/集成测试/缺陷修复）启动
- **THEN** 轮次上限 SHALL 为 5 轮
- **AND** SHALL NOT 为 10 轮

#### Scenario: plan 阶段取其自审口径

- **WHEN** kflow-plan 阶段的迭代循环启动 且 变更档位为 `轻量`
- **THEN** 轮次上限 SHALL 为 1 轮（设计自审口径）
- **AND** SHALL NOT 为 3 轮

### Requirement: 设计自审轮次上限按档位决定

设计类阶段（kflow-explore、kflow-prototype-design、kflow-design）SELFREV 自审的轮次**上限** SHALL 由变更档位决定：`轻量` 为 1，`标准` 为 2，`完整` 为 5。设计自审 SHALL 至少执行 1 轮，SHALL NOT 存在 0 轮豁免。达成收敛终止条件时 SHALL 提前结束。kflow-prototype-design 阶段 SHALL 仅在该变更选择「子代理自动审查验证」审查方式时执行自审；选择「人工审查」时 SHALL 完全跳过 SELFREV，SHALL NOT 保留兜底轮次。

#### Scenario: 轻量档执行 1 轮自审

- **WHEN** 变更档位为 `轻量` 且设计类阶段完成产物初稿
- **THEN** SELFREV SHALL 执行 1 轮子代理串行自审
- **AND** SHALL NOT 跳过 SELFREV

#### Scenario: 标准档执行至多 2 轮自审

- **WHEN** 变更档位为 `标准` 且设计类阶段完成产物初稿
- **THEN** SELFREV SHALL 至多执行 2 轮子代理串行自审
- **AND** 达成收敛终止条件时 SHALL 提前结束

#### Scenario: 完整档上限 5 轮自审

- **WHEN** 变更档位为 `完整` 且设计类阶段完成产物初稿
- **THEN** SELFREV SHALL 至多执行 5 轮子代理串行自审
- **AND** 达成收敛终止条件时 SHALL 提前结束

#### Scenario: prototype 阶段选择人工审查时跳过自审

- **WHEN** 当前阶段为 kflow-prototype-design 且该变更选择「人工审查」审查方式
- **THEN** SELFREV SHALL NOT 执行，不计算轮次上限、不执行评分底线判定
- **AND** 系统 SHALL 直接进入用户评审 REVIEW 步骤

### Requirement: 废除首次一律最大的轮次下限

系统 SHALL NOT 以「首次执行」或「首次创建」作为轮次决定的依据。执行类阶段首次执行的 10 轮下限，以及设计自审首次创建的固定 10 轮规则，SHALL NOT 存在。

#### Scenario: 首次执行按档位而非固定 10 轮

- **WHEN** 某执行类阶段在变更中首次执行 且 变更档位为 `轻量`
- **THEN** 轮次上限 SHALL 为 1 轮
- **AND** SHALL NOT 为 10 轮

#### Scenario: 项目无设计基础时不触发 10 轮自审

- **WHEN** 项目无设计基础（`docs/CONTEXT.md` 不存在 或 `docs/designs/detailed-designs/` 为空） 且 变更档位为 `轻量`
- **THEN** SELFREV SHALL 执行 1 轮（全局下限）
- **AND** 系统 SHALL NOT 依据项目设计基础状态调整轮次

### Requirement: 回退重执行的轮次上限叠加规则

阶段回退重执行时，轮次**上限** SHALL 取档位上限与影响范围分数映射值的较大者。影响范围分数映射规则统一为：分数 <= 3 映射 1 轮，分数在 4 至 15 之间映射 3 轮，分数 > 15 映射 5 轮。`.status.md` 中无影响范围分数可用时，轮次上限 SHALL 为档位上限。

#### Scenario: 回退重执行取较大者

- **WHEN** 阶段回退重执行 且 变更档位为 `轻量` 且 影响范围分数为 8
- **THEN** 轮次上限 SHALL 为 max(1, 3) = 3 轮
- **AND** 返工验证 SHALL NOT 因低档而放松

#### Scenario: 影响范围分数低于档位上限时维持上限

- **WHEN** 阶段回退重执行 且 变更档位为 `完整` 且 影响范围分数为 1
- **THEN** 轮次上限 SHALL 为 max(5, 1) = 5 轮

#### Scenario: 无影响范围分数时采用档位上限

- **WHEN** 阶段回退重执行 且 `.status.md` 中无影响范围分数
- **THEN** 轮次上限 SHALL 为档位上限

### Requirement: 统一轮次映射口径

影响范围分数到轮次的映射 SHALL 仅在本能力中定义一次。其他能力（kflow-bug-triage 的影响评估、重复制执行模型、设计审查分级）SHALL 引用本映射，SHALL NOT 另行定义数值区间。

#### Scenario: triage 引用统一映射

- **WHEN** kflow-bug-triage 输出影响评估报告的推荐轮次
- **THEN** 推荐轮次 SHALL 取自本能力定义的统一映射

#### Scenario: 各执行类阶段的重复制模型引用统一映射

- **WHEN** 任一执行类阶段的 `references/repetition.md` 描述轮次决策
- **THEN** 轮次规则 SHALL 引用本能力定义的档位上限与叠加规则
- **AND** SHALL NOT 定义自己的分数区间表

### Requirement: 完整档自审评分底线

变更档位为 `完整` 时，SELFREV 每轮 SHALL 输出各维度评分（0-10 量纲），自审通过 SHALL 要求各维度评分均 > 8 **且**达成收敛终止条件；任一维度 <= 8 SHALL 继续补审，直至各维度均 > 8 且收敛，或达到轮次上限 5。

#### Scenario: 各维度达标即通过

- **WHEN** 变更档位为 `完整` 且本轮各维度评分均 > 8 且本轮为见证轮
- **THEN** 自审 SHALL 通过并终止

#### Scenario: 未达标继续补审

- **WHEN** 变更档位为 `完整` 且任一维度评分 <= 8
- **THEN** 系统 SHALL 继续补审
- **AND** 直至各维度均 > 8 且收敛，或达到轮次上限 5

### Requirement: 轻量档一轮自审与产物门控

变更档位为 `轻量` 时，设计自审 SHALL 执行 1 轮（全局下限），SHALL NOT 豁免 SELFREV。产物完整性门控 SHALL 保留为**附加硬门**：阶段产物 SHALL 全部存在，且 SHALL NOT 含 TODO、TBD 或未填充占位符；任一产物缺失或含占位符时 SHALL 阻塞该阶段。

#### Scenario: 轻量档执行 1 轮自审

- **WHEN** 变更档位为 `轻量` 且设计类阶段产出完成
- **THEN** 系统 SHALL 启动 1 轮自审子代理
- **AND** SHALL 产出自审报告

#### Scenario: 轻量档产物门控保留为附加硬门

- **WHEN** 变更档位为 `轻量` 且设计类阶段产出完成
- **THEN** 系统 SHALL 校验产物存在性与占位符
- **AND** 任一产物缺失或含 TODO/TBD/未填充占位符时 SHALL 阻塞该阶段

### Requirement: 目标轮次写入状态文件

系统 SHALL 将轮次上限写入变更级 `.status.md` 的执行轮次字段（形如 `1/3`），并在每轮完成时递增计数器。

#### Scenario: 轮次计数器呈现目标轮次

- **WHEN** 执行类阶段启动 且 变更档位为 `标准`
- **THEN** `.status.md` 的执行轮次 SHALL 呈现为 `1/3` 形式
- **AND** 分母 SHALL 为该档位的轮次上限，SHALL NOT 固定为 10
