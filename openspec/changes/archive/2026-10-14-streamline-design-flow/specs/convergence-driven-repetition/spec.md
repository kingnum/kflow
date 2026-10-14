# Spec Delta

## MODIFIED Requirements

### Requirement: 审查范围冻结

主 Agent SHALL 在单轮验证启动前从阶段产物既有内容生成**审查对象集合**并冻结，审查维度 SHALL 限于该阶段既有的固定维度枚举。验证子代理 SHALL NOT 扩大审查对象集合、SHALL NOT 新增审查维度、SHALL NOT 借审查之名新增功能点、字段、章节或分支。审查对象集合 SHALL 由主 Agent 在阶段回退重执行产生新受影响项时更新。

#### Scenario: 审查对象集合冻结

- **WHEN** 主 Agent 构建验证子代理的 prompt
- **THEN** prompt SHALL 包含由阶段产物生成的审查对象清单
- **AND** 子代理 SHALL NOT 审查该清单之外的文件、代码或内容

#### Scenario: 审查维度封闭

- **WHEN** 单轮验证执行
- **THEN** 审查维度 SHALL 限于该阶段固定的维度枚举
- **AND** 子代理 SHALL NOT 新增审查维度

#### Scenario: 轮内不得扩大范围

- **WHEN** 验证子代理认为存在值得一并处理的范围外内容
- **THEN** 子代理 SHALL NOT 将其纳入审查对象或修改范围

#### Scenario: 跨轮由主 Agent 更新范围

- **WHEN** 阶段经历回退重执行并产生新的受影响项
- **THEN** 主 Agent SHALL 更新审查对象集合以纳入这些受影响项
- **AND** 该更新 SHALL NOT 由子代理自行发起

### Requirement: 范围外发现降级为范围外观察

验证子代理在冻结范围之外发现的问题 SHALL NOT 触发产物修改、SHALL NOT 计入验证发现数；SHALL 记为「**范围外观察**」写入验证报告的「范围外观察」小节。主 Agent SHALL 在阶段终止时汇总范围外观察条目并向用户提示。

#### Scenario: 范围外发现不改产物

- **WHEN** 子代理在冻结范围之外发现问题
- **THEN** 系统 SHALL NOT 修改任何阶段产物
- **AND** SHALL NOT 将该问题计为需要修复的项

#### Scenario: 范围外发现不计入发现数

- **WHEN** 验证子代理仅存在范围外发现而无范围内发现
- **THEN** 该阶段的验证发现数 SHALL 记为 0
- **AND** 终止结果 MAY 为 `验证通过`（其余条件同时满足时）

#### Scenario: 范围外观察写入报告并由主 Agent 汇总提示

- **WHEN** 单轮验证产生范围外观察条目
- **THEN** 验证报告 SHALL 在「范围外观察」小节记录这些条目
- **AND** 主 Agent SHALL 在阶段终止时汇总全部范围外观察条目并向用户提示

### Requirement: 终止结果写入

阶段终止时系统 SHALL 在 `.status.md` 写入**终止结果**字段，取值 `验证通过` 或 `验证发现问题({N})`。`验证通过` SHALL 当且仅当该阶段零发现且无签署不成立项；`验证发现问题({N})` SHALL 用于存在发现项或签署不成立项的情形，N 为该阶段发现总数。读取侧遇到历史变更遗留的 `收敛` 取值 SHALL 归并为 `验证通过`，其余历史取值 SHALL 归并为 `验证发现问题`。

#### Scenario: 以见证轮终止写入收敛

- **WHEN** 单轮验证零发现且无签署不成立项
- **THEN** 终止结果 SHALL 为 `验证通过`

#### Scenario: 不收敛升级写入未收敛

- **WHEN** 单轮验证存在发现项或签署不成立项
- **THEN** 终止结果 SHALL 为 `验证发现问题({N})`
- **AND** N SHALL 为该阶段发现总数

#### Scenario: 终止结果与实际终止路径一致

- **WHEN** 审计或门控读取终止结果字段
- **THEN** 该取值 SHALL 与该阶段的实际终止路径一致
- **AND** 读取侧遇到历史变更遗留的 `收敛` 取值时 SHALL 归并为 `验证通过`，其余历史取值 SHALL 归并为 `验证发现问题`

### Requirement: 档位决定每轮审查强度而非轮数

变更档位 SHALL 决定审查的**审查形态**（`轻量` 单 Agent 串行覆盖全部视角 / `标准` 两视角并行 / `完整` 四视角并行）与产出深度，以及验证报告的输出深度。档位 SHALL NOT 决定审查轮数——全部档位的审查轮数恒为单轮。

#### Scenario: 档位不决定轮数

- **WHEN** 任一阶段的单轮验证启动
- **THEN** 系统 SHALL NOT 因变更档位而调整审查轮数
- **AND** 审查轮数 SHALL 恒为 1

#### Scenario: 档位决定每轮审查强度

- **WHEN** 变更档位为 `轻量`
- **THEN** 审查 SHALL 由单个 Agent 串行覆盖全部视角的检查项
- **AND** 检查项 SHALL NOT 因单 Agent 而缩减

#### Scenario: 档位缺失时的处理

- **WHEN** 变更级 `.status.md` 不含 `变更档位` 字段
- **THEN** 系统 SHALL 按 `完整` 档确定审查形态与产出深度

### Requirement: 回退重执行不预置轮数

阶段回退重执行时，系统 SHALL NOT 预置或提高审查轮数——回退重执行后的单轮验证轮数 SHALL 恒为 1。验证门控 SHALL 要求受影响项 100% 覆盖：系统 SHALL 从 `.status.md` 「最近修订信息」读取受影响项清单，每个受影响项 SHALL 接受完整的阶段专属验证。

#### Scenario: 回退不预置轮数

- **WHEN** 某阶段因缺陷回退而重执行
- **THEN** 系统 SHALL NOT 因回退而提高或预置审查轮数
- **AND** 审查轮数 SHALL 恒为 1

#### Scenario: 受影响项 100% 覆盖门控

- **WHEN** 阶段处于回退重执行且 `.status.md` 存在受影响项清单
- **THEN** 每个受影响项 SHALL 接受完整的阶段专属验证
- **AND** 验证结果 SHALL 记录在阶段产物中

## ADDED Requirements

### Requirement: 审查循环固定单轮

设计类阶段（kflow-explore / kflow-prototype-design / kflow-design / kflow-plan）的 SELFREV 与测试类阶段（接口单元测试 / E2E 测试 / 集成测试）的审查 SHALL 固定执行单轮。系统 SHALL NOT 预置轮数上限，SHALL NOT 执行第二轮审查，SHALL NOT 存在 0 轮豁免路径。

#### Scenario: 设计类阶段单轮自审

- **WHEN** 任一设计类阶段完成产物初稿并完成签署自证
- **THEN** 该阶段 SHALL 执行单轮验证
- **AND** SHALL NOT 因该轮发现问题而自动执行第二轮

#### Scenario: 测试类阶段单轮审查

- **WHEN** 接口单元测试、E2E 测试或集成测试阶段启动
- **THEN** 该阶段 SHALL 执行单轮全面执行
- **AND** SHALL NOT 执行第二轮全量审查

#### Scenario: 无 0 轮豁免路径

- **WHEN** 任一适用本能力的阶段完成产物初稿
- **THEN** 单轮验证 SHALL 执行
- **AND** SHALL NOT 存在跳过该轮的通路

#### Scenario: prototype 人工审查跳过验证

- **WHEN** kflow-prototype-design 选择「人工审查」审查方式
- **THEN** 系统 SHALL NOT 执行验证环节
- **AND** 该跳过 SHALL NOT 被视为 0 轮豁免

#### Scenario: 编码与代码审查不适用本能力

- **WHEN** 编码阶段或代码审查阶段执行
- **THEN** 该阶段 SHALL 沿用其自身的重复制循环
- **AND** SHALL NOT 适用本能力的单轮验证模型

## REMOVED Requirements

### Requirement: 收敛为唯一成功终止条件

**Reason**: 该 Requirement 以「见证轮四项判据为唯一成功终止条件、无轮数上限」为终止模型。本次变更将审查改为固定单轮，「第二轮」不存在，见证轮与轮数上限均失去载体。单轮下的成功终止条件为「验证报告完整且全量遍历已证明」，由 `signed-checklist-verification` 能力的「验证报告与终止结果」Requirement 承载。

**Migration**: 终止条件改为单轮验证的报告完整性判定；终止结果取值由 `收敛` / `未收敛` 改为 `验证通过` / `验证发现问题({N})`，见本能力「终止结果写入」Requirement。审查范围冻结与范围外观察两条规则保留并按单轮改写。

### Requirement: 累积未复核修复清单与复核义务

**Reason**: 该机制的存在前提是多轮循环——清单跨轮累加、见证轮候选逐项复核。单轮验证模型下循环不存在，清单无处累积，复核义务失去载体。

**Migration**: 复核义务下沉至下游环节。主 Agent SHALL 生成「本阶段修复清单」随产物交付，设计类阶段的修复结果由交叉审查验证，测试类阶段的失败项走定向重验。清单结构与流转见 `signed-checklist-verification` 能力。

### Requirement: 引入范围外新内容的轮次不得判为见证轮

**Reason**: 该 Requirement 的失败判据是「不得判定为见证轮」，以见证轮存在为前提。单轮下该判据失去载体。

**Migration**: 越界处置改为：主 Agent SHALL 拒收该轮验证，要求子代理在冻结范围内重新验证，并将越界事实记录到 `docs/skill-suggestion.md`。该处置已并入 `signed-checklist-verification` 能力的验证契约。

### Requirement: 不收敛判定与升级

**Reason**: 不收敛判定（无进展 / 振荡 / 安全丝）是轮次循环的失败终止路径。单轮验证模型下不存在第二轮，无收敛性可判，三条判据全部失去意义；安全丝所依赖的「审查轮数达到全局 10 轮」在轮次恒为 1 时不可达。

**Migration**: 单轮验证的失败路径改为「验证发现问题({N})」并由主 Agent 统一修复。验证子代理自身执行异常（崩溃、报错、返回不完整）时按既有子代理隔离规则重试，最多 3 次，全部失败后标记 ⚠️ 阻塞并提示用户。

### Requirement: 全局轮次下限

**Reason**: 该 Requirement 的作用是禁止 0 轮豁免并声明下限为 1 轮。单轮模型中轮数恒为 1，「下限」概念不再成立。

**Migration**: 「无 0 轮豁免路径」的约束迁移至本能力新增的「审查循环固定单轮」Requirement；prototype 阶段选择「人工审查」时跳过验证属流程分支（非 0 轮豁免）的规则同样迁移至该 Requirement。

### Requirement: 完整档评分并入收敛判据

**Reason**: 该 Requirement 把「各维度评分 > 8」并入见证轮判定，以「评分 ≤ 8 等价于存在新发现，该轮不构成见证轮」为机制。单轮下无「继续下一轮」的去处，评分底线作为终止必要条件失去意义。

**Migration**: 评分语义保留为验证报告的输出深度（`完整` 档要求各维度评分与评分不达标时的具体问题项清单），但不再作为终止判据——单轮验证无论评分高低均在单轮结束时终止，发现项由主 Agent 统一修复。档位与产出深度的对应关系见本能力「档位决定每轮审查强度而非轮数」Requirement。
