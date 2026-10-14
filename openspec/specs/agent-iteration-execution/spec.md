# agent-iteration-execution Specification

## Purpose

定义执行类阶段的**收敛驱动**迭代机制：执行轮次下限统一为 1 轮、**不预设轮数上限**（轮数由收敛实际发生在第几轮决定），以**见证轮**（零新发现 + 零修复零修改 + 报告证明全维全量遍历 + 累积未复核修复清单内全部条目逐项复核通过）为唯一成功终止条件，以不收敛判定（无进展 / 振荡 / 安全丝）为失败终止路径，涵盖复杂度评估、重复制子代理 prompt 规范、审查范围冻结与主 Agent 迭代验收规则，确保执行类阶段迭代充分且产物质量受控。权威定义见 `convergence-driven-repetition` 能力。

## Requirements

### Requirement: 复杂度评估机制

系统 SHALL 在启动重复制子代理前评估任务复杂度，并将结果仅作为信息展示写入 .status.md 备注列。复杂度评估结果不驱动子代理执行行为——禁止将分级转化为按轮次分段分配工作重点的节奏指引。

#### Scenario: 基于可量化指标计算复杂度

- **WHEN** 评估阶段复杂性
- **THEN** 系统 MUST 按以下公式计算复杂度分：功能点数 × 1 + 接口数 × 1.5 + 场景数 × 2
- **AND** 将结果写入 .status.md 备注列作为背景信息，附带标注「仅供参考，不驱动执行行为」
- **AND** 分级阈值保留（低 <20 / 中 20-50 / 高 >50）但仅用于信息分类
- **AND** MUST NOT 将分级转化为节奏指引传递给子代理

#### Scenario: Agent 提前返回但未完成

- **WHEN** Agent 子代理返回但主 Agent 验收发现无任何一轮为见证轮
- **THEN** 主 Agent 记录当前进度到 skill-suggestion.md
- **AND** 直接要求 Agent 子代理继续迭代（见证轮是唯一的正常返回条件），不进入 AskUserQuestion
- **AND** 若子代理同时报告命中不收敛判定 → 进入非收敛分支，询问用户是否重新启动 Agent 子代理

### Requirement: 重复制子代理 prompt 规范

系统 SHALL 为重复制子代理构建包含完整上下文的 prompt。Prompt SHALL 包含重复制遍历指令，SHALL 包含审查范围冻结要求，SHALL NOT 包含节奏指引或按轮次分段分配工作重点的指令。

#### Scenario: prompt 内容要求

- **WHEN** 构建重复制子代理 prompt
- **THEN** prompt MUST 包含：
  - 当前阶段目标与产物要求
  - 输入文档引用（functional-designs/、detailed-design.md 等）
  - traceability.md 中待填充的列和覆盖率目标
  - **审查对象清单**：由主 Agent 从阶段产物既有内容生成的本轮审查范围（冻结，子代理 SHALL NOT 扩大）
  - 重复制遍历指令：「每轮遍历全部工作项独立执行完整流程。更新 .status.md 中执行轮次计数器为当前轮次号。禁止按轮次分段分配工作重点——每轮均须对全部工作项执行完整检查。审查对象集合已冻结，SHALL NOT 审查清单之外的文件或内容、SHALL NOT 新增审查维度、SHALL NOT 借审查之名新增功能点/字段/章节/分支。当某轮零新发现且零修改、且报告证明全部工作项已完成全量遍历、且清单内全部未复核修复逐项复核通过时，该轮构成见证轮，SHALL 提前返回验收报告。达成收敛或命中不收敛判定之前 SHALL NOT 无理由返回。」
  - **范围外发现降级指令**：「在冻结范围之外发现的问题 SHALL NOT 在本轮修复、SHALL NOT 计入本轮新发现数、SHALL NOT 阻断收敛；SHALL 记为『范围外观察』写入本轮审查报告的『范围外观察』小节。」
  - 轮间摘要（第 2 轮起注入，格式见 `inter-round-summary` 能力）
- **AND** prompt SHALL NOT 包含任何轮数上限数值
- **AND** prompt SHALL NOT 包含「前 N 轮重点执行/中间 N 轮细节优化/后 N 轮验证」等分段分配指令
- **AND** 复杂度评估结果可出现在 prompt 中但必须附带标注「仅供参考，不驱动执行行为」

#### Scenario: prompt 引用现有文档

- **WHEN** 子代理需要读取设计文档作为输入
- **THEN** prompt 中使用文档路径引用（非复制完整内容）
- **AND** 子代理通过 Read 工具自行读取所需文档

### Requirement: 执行类阶段迭代至收敛

所有执行类阶段（编码/代码审查/接口单元测试/E2E测试/集成测试/缺陷修复）SHALL 通过重复制子代理迭代**至收敛**，SHALL 不少于全局下限 1 轮，SHALL NOT 预置或受限于任何轮数上限。收敛终止条件 SHALL 为**见证轮**——同时满足 (a) 零新发现、(b) 零修复零修改、(c) 报告证明全部审查维度与全部审查对象已完成全量遍历、(d) 累积未复核修复清单内全部条目逐项复核通过。kflow-plan 阶段的迭代循环为产物自审，与本需求同口径（轮数由收敛决定，SHALL NOT 取任何档位口径的上限）。不收敛的判定与升级见 `convergence-driven-repetition` 能力。

#### Scenario: 执行类阶段不预置轮数

- **WHEN** 任一执行类阶段启动重复制子代理
- **THEN** 系统 SHALL NOT 向子代理传递轮数上限数值
- **AND** 执行轮次 SHALL 不少于 1 轮
- **AND** 每轮完成时更新 .status.md 中 `执行轮次` 计数器
- **AND** 仅在达成见证轮或命中不收敛判定后方可返回验收报告

#### Scenario: 有实际工作时正常迭代

- **WHEN** Agent 在当前轮次发现需要执行的工作（代码编写、测试执行、缺陷修复等）
- **THEN** Agent 执行该工作
- **AND** 记录执行结果
- **AND** 递增轮次计数器并进入下一轮

#### Scenario: 无实际工作时按收敛判定

- **WHEN** Agent 在当前轮次无新发现且无可执行工作
- **THEN** 该轮 SHALL 被判定为**见证轮候选**——须同时满足「零修改」「报告证明全部工作项已完成全量遍历」「清单内全部条目逐项复核通过」
- **AND** 满足见证轮条件时 Agent SHALL 终止并返回验收报告
- **AND** 不满足见证轮条件时 Agent SHALL 递增计数器并继续下一轮
- **AND** SHALL NOT 为凑满轮次而执行无增量价值的轮次

#### Scenario: 收敛后返回

- **WHEN** Agent 在某轮达成见证轮
- **THEN** Agent SHALL 准备验收报告
- **AND** 报告 SHALL 记录终止结果 `收敛`
- **AND** 返回主 Agent

#### Scenario: 不收敛时按判定升级

- **WHEN** Agent 命中无进展（连续 2 轮「本轮新发现数」与「累积未复核修复清单长度」双双无改善）、振荡（同一问题项「修复 → 重新发现」累计 ≥ 2 次）或安全丝（该阶段审查轮数达到 10 轮）任一情形
- **THEN** Agent SHALL 返回验收报告并标注不收敛缘由
- **AND** 主 Agent SHALL 按 `convergence-driven-repetition` 能力的「不收敛判定与升级」Requirement 处理

### Requirement: 主 Agent 迭代验收

系统 SHALL 在重复制子代理完成后由主 Agent 执行验收。验收 SHALL 以「最近一轮为见证轮」为通过前提，SHALL NOT 存在以轮次数量达标替代见证轮的通过路径。

#### Scenario: 验收通过

- **WHEN** 主 Agent 检查以下条件全部满足：
  - .status.md 中 `执行轮次` >= 1 且最近一轮为见证轮
  - 累积未复核修复清单为空（见证轮的第 (d) 项条件已保证）
  - 阶段产物文件存在且格式正确
  - traceability.md 对应列覆盖率 = 100%
  - 无 TODO/TBD/{待填写} 等占位符
- **THEN** 验收通过
- **AND** 更新 .status.md 中对应阶段状态为 ✅ 完成
- **AND** 门控释放，可进入下一阶段

#### Scenario: 验收不通过——无见证轮

- **WHEN** 主 Agent 检查发现无任何一轮为见证轮，且子代理未报告命中不收敛判定
- **THEN** 验收不通过
- **AND** 无见证轮为硬性拒收条件，不接受 Agent 子代理任何理由的提前返回
- **AND** 系统记录到 skill-suggestion.md（包含阶段、当前轮次、建议：继续迭代）
- **AND** 直接重新启动 Agent 子代理继续迭代，不询问用户

#### Scenario: 验收不通过——引入范围外新内容

- **WHEN** 主 Agent 验收发现某轮引入了冻结审查范围之外的新内容（范围外文件、新增审查维度、新增功能点或章节）
- **THEN** 该轮 SHALL NOT 被判定为见证轮
- **AND** 主 Agent SHALL 拒收该轮并要求子代理在冻结范围内重新审查
- **AND** 系统记录到 skill-suggestion.md（包含阶段、当前轮次、越界详情）

#### Scenario: 验收不通过——未收敛

- **WHEN** 子代理报告命中不收敛判定（无进展 / 振荡 / 安全丝）
- **THEN** 验收不通过，进入非收敛分支
- **AND** 系统记录到 skill-suggestion.md（包含阶段、当前轮数、不收敛缘由、覆盖率缺口、建议）
- **AND** 使用 AskUserQuestion 询问用户：「验收不通过，是否重新启动重复制子代理？」
- **AND** 用户选择「是」→ 调整 prompt 后重新启动 Agent 子代理
- **AND** 用户选择「否」→ 标记 .status.md 为 ⚠️ 需修订，阻塞当前阶段

#### Scenario: 验收记录格式

- **WHEN** 验收不通过并记录到 skill-suggestion.md
- **THEN** 记录 MUST 包含以下字段：发现时间、发现阶段（Agent 验收）、触发场景、覆盖缺口详情、轮次信息（当前轮次）、终止结果（`收敛` / `未收敛`，未收敛时含缘由）、复杂度信息、改进建议、状态（待重跑）、优先级
