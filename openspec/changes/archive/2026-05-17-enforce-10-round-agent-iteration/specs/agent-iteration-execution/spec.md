## MODIFIED Requirements

### Requirement: 复杂度评估机制

系统 SHALL 在启动 Agent 迭代子代理前评估任务复杂度，并将其作为 prompt 中的节奏指引。复杂度评估结果用于指导各轮次的迭代深度，不影响强制10轮下限。

#### Scenario: 基于可量化指标计算复杂度

- **WHEN** 评估阶段复杂性
- **THEN** 系统 MUST 按以下公式计算复杂度分：功能点数 × 1 + 接口数 × 1.5 + 场景数 × 2
- **AND** 将结果转化为 prompt 中的节奏指引：低复杂度 (< 20) →「前 6 轮重点执行，后 4 轮验证和边界检查」；中复杂度 (20-50) →「前 4 轮重点执行，中间 3 轮细节优化，后 3 轮验证和边界检查」；高复杂度 (> 50) →「前 3 轮重点执行，中间 4 轮细节优化，后 3 轮验证和边界检查」
- **AND** 无论复杂度高低，MUST 完成全部 10 轮迭代后方可返回

#### Scenario: Agent 提前返回但未完成

- **WHEN** Agent 子代理返回但主 Agent 验收发现产物不合格或轮次不足
- **THEN** 主 Agent 记录当前进度到 skill-suggestion.md
- **AND** 若轮次不足 10/10 → 直接要求 Agent 子代理继续执行剩余轮次，不进入 AskUserQuestion
- **AND** 若轮次已达 10/10 但产物不合格 → 询问用户是否重新启动 Agent 子代理

### Requirement: Agent 迭代子代理 prompt 规范

系统 SHALL 为 Agent 迭代子代理构建包含完整上下文的 prompt。

#### Scenario: prompt 内容要求

- **WHEN** 构建 Agent 迭代子代理 prompt
- **THEN** prompt MUST 包含：
  - 当前阶段目标与产物要求
  - 输入文档引用（functional-designs/、detailed-design.md 等）
  - traceability.md 中待填充的列和覆盖率目标
  - 迭代指令：「每完成一轮迭代，更新 .status.md 中执行轮次计数器为当前轮次号。必须完成全部 10 轮迭代后才可返回验收报告，禁止在第 10 轮前返回。若当前轮次无新发现且无可执行工作，仍须递增计数器并继续。」
- **AND** prompt SHOULD 包含分阶段目标以引导迭代方向
- **AND** prompt SHOULD 包含复杂度评估结果作为节奏指引（按轮次阶段分布：重点执行 → 细节优化 → 验证边界检查）

#### Scenario: prompt 引用现有文档

- **WHEN** 子代理需要读取设计文档作为输入
- **THEN** prompt 中使用文档路径引用（非复制完整内容）
- **AND** 子代理通过 Read 工具自行读取所需文档

### Requirement: 主 Agent 验收

系统 SHALL 在 Agent 迭代子代理完成后由主 Agent 执行验收。

#### Scenario: 验收通过

- **WHEN** 主 Agent 检查以下条件全部满足：
  - .status.md 中 `执行轮次` = `10 / 10`
  - 阶段产物文件存在且格式正确
  - traceability.md 对应列覆盖率 = 100%
  - 无 TODO/TBD/{待填写} 等占位符
- **THEN** 验收通过
- **AND** 更新 .status.md 中对应阶段状态为 ✅ 完成
- **AND** 门控释放，可进入下一阶段

#### Scenario: 验收不通过——轮次不足

- **WHEN** 主 Agent 检查发现 .status.md 中 `执行轮次` < `10 / 10`
- **THEN** 验收不通过
- **AND** 轮次不足为硬性拒收条件，不接受 Agent 子代理任何理由的提前返回
- **AND** 系统记录到 skill-suggestion.md（包含阶段、当前轮次、缺失轮次数、建议：继续执行剩余轮次）
- **AND** 直接重新启动 Agent 子代理继续执行，不询问用户

#### Scenario: 验收不通过——产物不合格

- **WHEN** 主 Agent 检查发现轮次已达 10/10 但产物条件不满足（文件缺失、覆盖率不足、有占位符）
- **THEN** 验收不通过
- **AND** 系统记录到 skill-suggestion.md（包含阶段、复杂度、覆盖率缺口、建议）
- **AND** 使用 AskUserQuestion 询问用户：「验收不通过，是否重新启动 Agent 迭代子代理？」
- **AND** 用户选择「是」→ 调整 prompt 后重新启动 Agent 子代理
- **AND** 用户选择「否」→ 标记 .status.md 为 ⚠️ 需修订，阻塞当前阶段

#### Scenario: 验收记录格式

- **WHEN** 验收不通过并记录到 skill-suggestion.md
- **THEN** 记录 MUST 包含以下字段：发现时间、发现阶段（Agent 验收）、触发场景、覆盖缺口详情、轮次信息（当前轮次/最大轮次）、复杂度信息、改进建议、状态（待重跑）、优先级

## ADDED Requirements

### Requirement: 执行类阶段强制10轮迭代

所有执行类阶段（计划/编码/代码审查/接口单元测试/E2E测试/集成测试/缺陷修复）SHALL 通过 Agent 迭代子代理完成强制10轮迭代，不允许在第10轮前返回验收报告。

#### Scenario: 执行类阶段设定10轮下限

- **WHEN** 任一执行类阶段启动 Agent 迭代子代理
- **THEN** Agent MUST 执行完整 10 轮迭代
- **AND** 每轮完成时更新 .status.md 中 `执行轮次` 计数器
- **AND** 第 10 轮完成后才可返回验收报告

#### Scenario: 有实际工作时正常迭代

- **WHEN** Agent 在当前轮次发现需要执行的工作（代码编写、测试执行、缺陷修复等）
- **THEN** Agent 执行该工作
- **AND** 记录执行结果
- **AND** 递增轮次计数器并进入下一轮

#### Scenario: 无实际工作时仍完成轮次

- **WHEN** Agent 在当前轮次无新发现且无可执行工作
- **THEN** Agent 执行验证检查（复验已有产物、确认无遗漏）
- **AND** 递增轮次计数器
- **AND** 在执行记录中标注「第 N 轮：无新发现」
- **AND** 继续下一轮（如果 N < 10）

#### Scenario: 第10轮完成后方可返回

- **WHEN** Agent 完成第 10 轮迭代
- **THEN** Agent 确认 `执行轮次` = `10 / 10`
- **AND** 准备验收报告
- **AND** 返回主 Agent
