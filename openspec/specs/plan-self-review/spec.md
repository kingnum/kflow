# plan-self-review Specification

## Purpose
定义 kflow-plan 阶段**收敛驱动**的子代理串行自审机制（执行轮次下限统一为 1 轮、`SHALL NOT` 预设或受限于任何轮数，以见证轮四项判据收敛终止）：每轮由独立子代理按任务覆盖完整性、DoD 验收标准、HITL 标注准确性与任务粒度四个定制维度检查 tasks.md，审查对象集合由主 Agent 按轮冻结、维度集合封闭，边审边修并向 self-reviews/plan/ 输出每轮自审报告。权威定义见 `convergence-driven-repetition` 能力。
## Requirements
### Requirement: 计划阶段审查维度（定制）

kflow-plan 自审 SHALL 覆盖以下 4 个定制维度，每轮子代理 SHALL 执行全部维度检查。

#### Scenario: 任务覆盖完整性检查

- **WHEN** plan 自审执行任务覆盖完整性维度
- **THEN** 检查是否所有 detailed-design.md 中该子变更的功能点都有对应任务
- **AND** 覆盖率必须 = 100%
- **AND** 检查是否所有 api-tests/ 和 e2e-tests/ 中的测试用例在任务清单中有对应的测试编写步骤
- **AND** 标记缺失任务的功能点

#### Scenario: DoD 验收标准正确性检查

- **WHEN** plan 自审执行 DoD 验收标准正确性维度
- **THEN** 检查每功能点是否包含 Happy Path(≥1) + Error Path(≥2) + Edge Case(≥1) + Quality(≥1)
- **AND** 检查每条验收标准是否使用 WHEN/THEN 格式
- **AND** 检查 Happy Path 是否验证正常业务流程
- **AND** 检查 Error Path 是否覆盖至少 2 种异常场景
- **AND** 检查 Edge Case 是否覆盖边界值
- **AND** 检查 Quality 是否验证性能/安全等质量属性
- **AND** 标记格式错误或数量不足的功能点

#### Scenario: HITL 标注准确性检查

- **WHEN** plan 自审执行 HITL 标注准确性维度
- **THEN** 检查所有 HITL 子变更是否包含决策点列表
- **AND** 检查 `[HITL D{n}]` 标注是否在正确的任务位置（Step 2 或 Step 3 之间）
- **AND** 检查每个决策点是否有明确的决策内容和至少 2 个选项
- **AND** 检查默认建议是否标注
- **AND** 检查 AFK 子变更是否不包含 HITL 标注
- **AND** 标记缺失标注或位置不当的决策点

#### Scenario: 任务粒度合理性检查

- **WHEN** plan 自审执行任务粒度合理性维度
- **THEN** 检查每任务是否符合 2-5 分钟可完成的标准
- **AND** 检查 TDD 循环是否完整（Step 1-7：编写测试→RED→实现→GREEN→质量检查→重构→验证）
- **AND** 标记过粗任务（包含多个独立操作）
- **AND** 标记过细任务（实现细节级别）

### Requirement: plan 自审报告

每轮子代理 SHALL 输出自审报告到 `self-reviews/plan/` 目录，报告格式与 explore/design 自审报告一致。

#### Scenario: 报告路径

- **WHEN** plan 子代理完成一轮自审
- **THEN** 报告保存路径为 `self-reviews/plan/{YYYYMMDD}-{HHMMSS}.md`
- **AND** 文件名使用时间戳格式

#### Scenario: 报告内容

- **WHEN** 子代理完成一轮审查
- **THEN** 报告包含审查维度得分表（维度名、本轮得分、上轮得分、变化值）
- **AND** 包含新发现问题清单（序号、问题描述、严重度、状态）
- **AND** 包含上轮问题修复验证
- **AND** 包含本轮改进内容描述
- **AND** 包含仍存在的问题
- **AND** 包含全量遍历证明（4 维度与全部子变更 tasks.md 均已遍历）与本轮判定（是否为见证轮）

### Requirement: 边审边修规则

子代理在审查过程中确认的问题 SHALL 直接修复 tasks.md 文件，不限于生成审查报告。

#### Scenario: 发现问题直接修复

- **WHEN** 子代理在审查过程中确认了 DoD 格式错误或任务缺失
- **THEN** 直接修复对应子变更的 tasks.md 文件
- **AND** 在审查报告中记录修复内容
- **AND** SHALL 仅修复确认的问题，不做额外改进
- **AND** SHALL NOT 新增功能点任务（遵循"非必要不增加新功能"原则）

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
