# plan-self-review Specification

## Purpose
定义 kflow-plan 阶段档位驱动的子代理串行自审机制（执行轮次下限统一为 1 轮、上限 轻量 1 / 标准 2 / 完整 5，以见证轮收敛终止）：每轮由独立子代理按任务覆盖完整性、DoD 验收标准、HITL 标注准确性与任务粒度四个定制维度检查 tasks.md，边审边修并向 self-reviews/plan/ 输出每轮自审报告。
## Requirements
### Requirement: 计划阶段档位驱动轮次上限的子代理自审

系统 SHALL 在 kflow-plan 阶段执行由变更档位决定轮次上限的子代理串行自循环审查（SELFREV）：`轻量` 1 轮、`标准` 2 轮、`完整` 5 轮。每轮 SHALL 启动独立子代理执行全部 4 个定制维度检查；执行轮次 SHALL 不少于 1 轮，达成收敛终止条件（最近一轮为见证轮）时 SHALL 提前结束，SHALL NOT 为凑满上限而继续执行。审查循环到达终止点且累积未复核修复清单非空时，系统 SHALL 追加 1 轮复检轮，逐项复核清单内全部修复；该轮 SHALL NOT 消耗档位轮次上限，且 SHALL 最多追加 1 轮。

#### Scenario: plan SELFREV 步骤位置

- **WHEN** kflow-plan 完成所有子变更 tasks.md 初稿后
- **THEN** 在步骤 8（VERIFY）之后、步骤 9（COMPLETE）之前插入 SELFREV 步骤
- **AND** SELFREV 步骤序号为 8.5，原 COMPLETE 步骤序号顺延为 9

#### Scenario: 轻量档执行 1 轮自审

- **WHEN** 变更档位为 `轻量`
- **THEN** kflow-plan SHALL 执行 1 轮审查轮 SELFREV
- **AND** SHALL NOT 跳过 SELFREV
- **AND** 该轮产生修复时 SHALL 追加 1 轮复检轮
- **AND** 产物完整性门控 SHALL 保留为附加硬门

#### Scenario: 收敛或达上限终止

- **WHEN** plan SELFREV 执行中
- **THEN** 最近一轮为见证轮（零新发现、零修改、报告证明 4 维度全量遍历）时 SHALL 终止
- **AND** 否则继续下一轮，直至轮次达到上限（轻量 1 / 标准 2 / 完整 5）
- **AND** SHALL NOT 因存在新发现问题而强制走满上限

#### Scenario: 终止点清单非空时追加复检轮

- **WHEN** plan SELFREV 到达终止点（最近一轮为见证轮，或已达到档位轮次上限）
- **AND** 累积未复核修复清单非空
- **THEN** 系统 SHALL 追加 1 轮复检轮
- **AND** 该轮 SHALL NOT 计入档位轮次上限
- **AND** 该轮 SHALL 逐项复核清单内全部修复，并证明 4 维度已完成全量遍历

#### Scenario: 复检轮通过后终止

- **WHEN** 复检轮零新发现、零修改、证明 4 维度全量遍历且清单内全部修复逐项复核通过
- **THEN** 系统 SHALL 终止 plan SELFREV
- **AND** 终止原因 SHALL 记录为 `收敛（复检轮）`

#### Scenario: 复检轮未通过后终止

- **WHEN** 复检轮未满足通过判据
- **THEN** 系统 SHALL 终止 plan SELFREV
- **AND** 终止原因 SHALL 记录为 `达上限`
- **AND** 系统 SHALL 进入非收敛分支

#### Scenario: 子代理串行执行

- **WHEN** 第 N 轮子代理完成
- **THEN** 主 Agent 读取审查报告和修复后的产物
- **AND** 确认修复内容后启动第 N+1 轮子代理
- **AND** SHALL NOT 同时启动多个子代理（禁止并行）

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
