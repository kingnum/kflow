# agent-iteration-execution Specification

## Purpose

定义执行类阶段的执行与验收机制：单轮类阶段（接口单元测试 / E2E 测试 / 集成测试）执行单轮全量、失败项走定向重验（有界重试），重复制类阶段（编码 / 代码审查 / 缺陷修复）沿用重复制子代理循环逐轮遍历全部工作项；涵盖复杂度评估、子代理 prompt 规范、审查范围冻结与主 Agent 迭代验收规则，确保执行充分、产物质量受控且不以轮次数量作为通过判据。权威定义见 `convergence-driven-repetition` 与 `signed-checklist-verification` 能力。

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

- **WHEN** Agent 子代理返回但主 Agent 验收发现执行报告缺失或不完整
- **THEN** 主 Agent 记录当前进度到 skill-suggestion.md
- **AND** 直接要求 Agent 子代理继续迭代（验收通过是唯一的正常返回条件），不进入 AskUserQuestion
- **AND** 若子代理同时报告命中升级判定 → 进入升级分支，询问用户是否重新启动 Agent 子代理

### Requirement: 重复制子代理 prompt 规范

系统 SHALL 为子代理构建包含完整上下文的 prompt。Prompt SHALL 区分两类阶段的执行指令：单轮类阶段 SHALL 含单轮执行指令；重复制类阶段 SHALL 含重复制遍历指令。Prompt SHALL 包含审查范围冻结要求，SHALL NOT 包含节奏指引或按轮次分段分配工作重点的指令。

#### Scenario: prompt 内容要求

- **WHEN** 构建子代理 prompt
- **THEN** prompt MUST 包含：
  - 当前阶段目标与产物要求
  - 输入文档引用（functional-designs/、detailed-design.md 等）
  - traceability.md 中待填充的列和覆盖率目标
  - **审查对象清单**：由主 Agent 从阶段产物既有内容生成的审查范围（冻结，子代理 SHALL NOT 扩大）
  - **单轮类阶段（接口单元测试 / E2E 测试 / 集成测试）的单轮执行指令**：「在一轮内遍历全部工作项执行完整流程，完成后返回执行报告。发现失败项时按定向重验处理——仅重跑失败用例，不重跑全量。审查对象集合已冻结，SHALL NOT 审查清单之外的文件或内容、SHALL NOT 新增审查维度、SHALL NOT 借审查之名新增功能点/字段/章节/分支。」
  - **重复制类阶段（编码 / 代码审查 / 缺陷修复）的重复制遍历指令**：「每轮遍历全部工作项独立执行完整流程。更新 .status.md 中执行轮次计数器为当前轮次号。禁止按轮次分段分配工作重点——每轮均须对全部工作项执行完整检查。审查对象集合已冻结，SHALL NOT 审查清单之外的文件或内容、SHALL NOT 新增审查维度。」
  - **范围外发现降级指令**：「在冻结范围之外发现的问题 SHALL NOT 计入执行发现数；SHALL 记为『范围外观察』写入执行报告的『范围外观察』小节。」
  - 轮间摘要（仅重复制类阶段自第 2 轮起注入，格式见 `inter-round-summary` 能力）
- **AND** prompt SHALL NOT 包含任何轮数上限数值
- **AND** prompt SHALL NOT 包含「前 N 轮重点执行/中间 N 轮细节优化/后 N 轮验证」等分段分配指令
- **AND** 复杂度评估结果可出现在 prompt 中但必须附带标注「仅供参考，不驱动执行行为」

#### Scenario: prompt 引用现有文档

- **WHEN** 子代理需要读取设计文档作为输入
- **THEN** prompt 中使用文档路径引用（非复制完整内容）
- **AND** 子代理通过 Read 工具自行读取所需文档

### Requirement: 执行类阶段迭代至收敛

执行类阶段 SHALL 按两类型执行。(a) **单轮类阶段**（接口单元测试 / E2E 测试 / 集成测试）：SHALL 执行单轮全面执行，SHALL NOT 执行第二轮全量审查；发现失败项时 SHALL 走定向重验——仅重跑失败用例，属有界重试，SHALL NOT 使用收敛循环或见证轮判据。(b) **重复制类阶段**（编码 / 代码审查 / 缺陷修复）：SHALL 沿用重复制子代理循环，每轮遍历全部工作项执行完整流程。kflow-plan 阶段的产物自审由 `plan-self-review` 能力承载，不适用本需求。

#### Scenario: 执行类阶段不预置轮数

- **WHEN** 任一执行类阶段启动子代理
- **THEN** 系统 SHALL NOT 向子代理传递轮数上限数值
- **AND** 单轮类阶段 SHALL 执行一轮全量
- **AND** 重复制类阶段 SHALL 执行不少于 1 轮，每轮完成时更新 .status.md 中 `执行轮次` 计数器

#### Scenario: 有实际工作时正常迭代

- **WHEN** 重复制类阶段的子代理在当前轮次发现需要执行的工作（代码编写、代码审查、缺陷修复等）
- **THEN** 子代理执行该工作
- **AND** 记录执行结果
- **AND** 递增轮次计数器并进入下一轮

#### Scenario: 无实际工作时按收敛判定

- **WHEN** 重复制类阶段的子代理在当前轮次无新发现且无可执行工作
- **THEN** 子代理 SHALL 返回执行报告
- **AND** 执行报告 SHALL 证明全部工作项已完成全量遍历
- **AND** SHALL NOT 为凑轮次而执行无增量价值的轮次

#### Scenario: 收敛后返回

- **WHEN** 重复制类阶段的子代理完成全部可执行工作
- **THEN** 子代理 SHALL 准备执行报告
- **AND** 报告 SHALL 记录执行结果 `执行完成`
- **AND** 返回主 Agent

#### Scenario: 不收敛时按判定升级

- **WHEN** 重复制类阶段的子代理连续 3 轮无实质进展（同一问题项反复出现）
- **THEN** 子代理 SHALL 返回执行报告并标注停滞缘由
- **AND** 主 Agent SHALL 记录到 `docs/skill-suggestion.md`
- **AND** SHALL 使用 AskUserQuestion 询问用户是否重新启动子代理
- **AND** 用户选择「否」时 MAY 将该阶段标记为 ⚠️ 阻塞

### Requirement: 主 Agent 迭代验收

系统 SHALL 在子代理完成后由主 Agent 执行验收。验收 SHALL 以「执行报告完整 + 阶段产物齐全 + 覆盖率达标 + 无占位符」为通过条件；单轮类阶段另须「定向重验全部通过」。系统 SHALL NOT 存在以轮次数量作为通过或拒收依据的路径。

#### Scenario: 验收通过

- **WHEN** 主 Agent 检查以下条件全部满足：
  - 执行报告已产出且内容完整（含全量遍历证明）
  - 阶段产物文件存在且格式正确
  - traceability.md 对应列覆盖率 = 100%
  - 无 TODO/TBD/{待填写} 等占位符
  - 单轮类阶段的定向重验全部通过
- **THEN** 验收通过
- **AND** 更新 .status.md 中对应阶段状态为 ✅ 完成
- **AND** 门控释放，可进入下一阶段

#### Scenario: 验收不通过——无见证轮

- **WHEN** 主 Agent 检查发现执行报告缺失、不完整、或覆盖率未达标
- **THEN** 验收不通过
- **AND** 系统记录到 `docs/skill-suggestion.md`（包含阶段、缺失项、建议）
- **AND** 直接重新启动子代理执行剩余工作，不询问用户

#### Scenario: 验收不通过——引入范围外新内容

- **WHEN** 主 Agent 验收发现子代理引入了冻结审查范围之外的新内容（范围外文件、新增审查维度、新增功能点或章节）
- **THEN** 主 Agent SHALL 拒收
- **AND** SHALL 要求子代理在冻结范围内重新执行
- **AND** 系统记录到 `docs/skill-suggestion.md`（包含阶段、越界详情）

#### Scenario: 验收不通过——未收敛

- **WHEN** 单轮类阶段的定向重验连续 3 次仍未通过
- **THEN** 验收不通过
- **AND** 系统记录到 `docs/skill-suggestion.md`（包含阶段、轮次、失败用例清单、建议）
- **AND** 使用 AskUserQuestion 询问用户：「定向重验连续失败，是否调整修复方案后重试？」
- **AND** 用户选择「否」时 MAY 标记 .status.md 为 ⚠️ 阻塞并终止当前阶段

#### Scenario: 验收记录格式

- **WHEN** 验收不通过并记录到 `docs/skill-suggestion.md`
- **THEN** 记录 MUST 包含以下字段：发现时间、发现阶段（Agent 验收）、触发场景、覆盖缺口详情、轮次信息（当前轮次）、执行结果（`执行完成` / `定向重验失败` / `停滞`）、复杂度信息、改进建议、状态（待重跑）、优先级
