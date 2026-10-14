# Spec Delta

## ADDED Requirements

### Requirement: 计划阶段收敛驱动的子代理自审

系统 SHALL 在 kflow-plan 阶段以独立子代理串行执行收敛驱动的自审（SELFREV）。审查轮数 SHALL 由收敛实际发生在第几轮决定，SHALL NOT 预置或受限于任何档位轮数上限，SHALL NOT 少于 1 轮且 SHALL NOT 存在 0 轮豁免路径。每轮 SHALL 启动独立子代理执行全部 4 个定制维度检查；某轮同时满足零新发现、零修改、报告证明 4 个维度与全部子变更 tasks.md 已完成全量遍历、累积未复核修复清单内全部条目逐项复核通过（即构成见证轮）时，系统 SHALL 终止并写入终止结果 `收敛`；命中不收敛判定时系统 SHALL 终止并写入终止结果 `未收敛`。见证轮 4 项判据、累积未复核修复清单与复核义务、不收敛判定与升级的权威定义见 `convergence-driven-repetition` 能力。

#### Scenario: plan SELFREV 步骤位置

- **WHEN** kflow-plan 完成所有子变更 tasks.md 初稿后
- **THEN** 在步骤 8（VERIFY）之后、步骤 9（COMPLETE）之前插入 SELFREV 步骤
- **AND** SELFREV 步骤序号为 8.5，原 COMPLETE 步骤序号顺延为 9

#### Scenario: 轻量档执行至少 1 轮自审

- **WHEN** 变更档位为 `轻量`
- **THEN** kflow-plan SHALL 执行 SELFREV，轮数不少于 1 轮
- **AND** SHALL NOT 跳过 SELFREV，SHALL NOT 存在 0 轮豁免路径
- **AND** 轮数 SHALL 由收敛实际发生在第几轮决定，SHALL NOT 因变更档位而限制轮数
- **AND** 产物完整性门控 SHALL 保留为附加硬门

#### Scenario: 串行执行至收敛

- **WHEN** 第 N 轮子代理完成并返回自审报告
- **THEN** 主 Agent 读取自审报告与修复后的 tasks.md
- **AND** 该轮构成见证轮时 SHALL 终止并写入终止结果 `收敛`
- **AND** 否则确认修复内容后启动第 N+1 轮子代理
- **AND** SHALL NOT 为凑轮数而继续执行

#### Scenario: 子代理串行执行

- **WHEN** 第 N 轮子代理完成
- **THEN** 主 Agent 读取审查报告和修复后的产物
- **AND** 确认修复内容后启动第 N+1 轮子代理
- **AND** SHALL NOT 同时启动多个子代理（禁止并行）

#### Scenario: 不收敛时升级用户

- **WHEN** 自审循环命中不收敛判定（无进展 / 振荡 / 安全丝）
- **THEN** 系统 SHALL 终止并写入终止结果 `未收敛`
- **AND** SHALL 按 `convergence-driven-repetition` 能力的「不收敛判定与升级」升级用户
- **AND** 具体缘由 SHALL 写入 `docs/skill-suggestion.md`

### Requirement: 计划阶段审查对象冻结与范围外观察

主 Agent SHALL 在每轮开始时从阶段产物既有内容（各子变更 tasks.md）生成本轮审查对象集合并冻结，审查维度 SHALL 限于本阶段的 4 个定制维度；子代理 SHALL NOT 扩大审查对象集合、SHALL NOT 新增审查维度、SHALL NOT 借审查之名新增功能点或任务。冻结范围之外的发现 SHALL 记为「范围外观察」，SHALL NOT 在本轮修复、SHALL NOT 计入本轮新发现数、SHALL NOT 阻断收敛，并 SHALL 写入该轮自审报告的「范围外观察」小节。引入范围外新内容的轮次 SHALL NOT 被判定为见证轮，主 Agent SHALL 拒收该轮并要求子代理在冻结范围内重新审查。主 Agent SHALL 在阶段终止时汇总范围外观察条目并向用户提示。

#### Scenario: 审查对象集合冻结

- **WHEN** 主 Agent 构建某轮自审子代理的 prompt
- **THEN** prompt SHALL 包含由阶段产物既有内容生成的本轮审查对象清单
- **AND** 子代理 SHALL NOT 审查该清单之外的文件或内容

#### Scenario: 审查维度封闭

- **WHEN** 某轮 plan 自审执行
- **THEN** 审查维度 SHALL 限于任务覆盖完整性、DoD 验收标准正确性、HITL 标注准确性、任务粒度合理性这 4 个定制维度
- **AND** 子代理 SHALL NOT 新增审查维度

#### Scenario: 范围外发现降级为范围外观察

- **WHEN** 子代理在冻结范围之外发现问题
- **THEN** SHALL NOT 在本轮修改任何阶段产物
- **AND** SHALL NOT 将该问题计入本轮新发现数
- **AND** SHALL 记为「范围外观察」写入该轮自审报告的「范围外观察」小节

#### Scenario: 引入范围外新内容的轮次不得判为见证轮

- **WHEN** 某轮的新发现或修改落在冻结的审查对象集合之外
- **THEN** 该轮 SHALL NOT 被判定为见证轮
- **AND** 主 Agent SHALL 拒收该轮并要求子代理在冻结范围内重新审查

## REMOVED Requirements

### Requirement: 计划阶段档位驱动轮次上限的子代理自审

**Reason**: 该需求以「按变更档位取轮次上限（轻量 1 / 标准 2 / 完整 5）」作为终止依据，并配套复检轮与 `收敛（复检轮）` / `达上限` 三值终止原因。本变更删除全部档位轮次上限，收敛成为唯一成功终止条件，复检轮的复核义务上提为见证轮第 (d) 项。

**Migration**: 迁移至本能力新增的「计划阶段收敛驱动的子代理自审」——轮数由收敛实际发生在第几轮决定，仅保留不小于 1 轮的下限；终止结果改二值 `收敛` / `未收敛`。见证轮判据、累积未复核修复清单与复核义务、不收敛判定与升级、审查范围冻结的权威定义见 `convergence-driven-repetition` 能力。复检轮段落随机制一并移除（复核义务并入见证轮第 (d) 项）。
