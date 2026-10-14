# convergence-driven-repetition Specification

## Purpose

定义设计类阶段 SELFREV 与测试类阶段审查的统一终止模型：审查循环固定单轮（不预置轮数上限、不执行第二轮、无 0 轮豁免），以**审查范围冻结**封闭审查边界，以范围外观察降级保证单轮内可达完整遍历；终止结果为 `验证通过` 或 `验证发现问题({N})`。签署清单自证、打假契约与修复责任见 `signed-checklist-verification` 能力。

## Requirements

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

变更档位 SHALL 决定审查的**审查形态**（`轻量` 单 Agent 串行覆盖全部视角 / `标准` 两视角并行）与产出深度，以及验证报告的输出深度。档位 SHALL NOT 决定审查轮数——全部档位的审查轮数恒为单轮。系统 SHALL NOT 存在四视角并行等第三形态。

#### Scenario: 档位不决定轮数

- **WHEN** 任一阶段的单轮验证启动
- **THEN** 系统 SHALL NOT 因变更档位而调整审查轮数
- **AND** 审查轮数 SHALL 恒为 1

#### Scenario: 档位决定每轮审查强度

- **WHEN** 变更档位为 `轻量`
- **THEN** 审查 SHALL 由单个 Agent 串行覆盖全部视角的检查项
- **AND** 检查项 SHALL NOT 因单 Agent 而缩减

#### Scenario: 标准档两视角审查

- **WHEN** 变更档位为 `标准`
- **THEN** 审查 SHALL 由两个 Agent 并行执行（业务+技术视角 / 安全+质量视角）
- **AND** 检查项 SHALL NOT 因合并为两个 Agent 而缩减

#### Scenario: 档位缺失时的处理

- **WHEN** 变更级 `.status.md` 不含 `变更档位` 字段，或读取到的历史取值为 `完整`
- **THEN** 系统 SHALL 按 `标准` 档确定审查形态与产出深度

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
