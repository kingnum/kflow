## ADDED Requirements

### Requirement: 执行类阶段统一使用 Agent 迭代执行

系统 SHALL 要求所有执行类阶段（计划/编码/代码审查/接口单元测试/E2E测试/集成测试/缺陷修复）通过 Agent 工具的原生迭代能力执行。创造性阶段（设计探索/原型设计/详细设计/归档/审计）不强制使用 Agent 迭代执行。

#### Scenario: 计划阶段启动 Agent 迭代执行

- **WHEN** 进入计划阶段（`kflow-plan`）
- **THEN** 系统评估复杂度后确定迭代策略
- **AND** 构建阶段专属 prompt（包含输入要求、迭代指令、输出产物、完成标准）
- **AND** 使用 `Agent(description, prompt, run_in_background)` 启动子代理

#### Scenario: 编码阶段启动 Agent 迭代执行

- **WHEN** 进入编码阶段（`kflow-code`）且当前子变更无依赖或依赖已完成
- **THEN** 系统启动 Agent 子代理
- **AND** prompt 包含 TDD 流程要求（Red → Green → Refactor）、功能点清单、DoD 验收标准
- **AND** prompt 包含迭代指令：「如有测试失败，修复后重新运行，重复直到全部通过」

#### Scenario: 测试阶段启动 Agent 迭代执行

- **WHEN** 进入接口单元测试或 E2E 测试阶段
- **THEN** 系统启动 Agent 子代理
- **AND** prompt 包含测试用例清单、服务地址、期望覆盖率 100%
- **AND** prompt 包含迭代指令：「测试失败时分析根因并修复，重复直到全部通过」

#### Scenario: 创造性阶段不启动 Agent 迭代执行

- **WHEN** 进入设计探索、原型设计、详细设计、归档或审计阶段
- **THEN** 系统维持主 Agent 直连执行模式
- **AND** 不启动 Agent 迭代子代理

### Requirement: 复杂度评估机制

系统 SHALL 在启动 Agent 迭代子代理前评估任务复杂度，并将其作为 prompt 中的节奏指引。

#### Scenario: 基于可量化指标计算复杂度

- **WHEN** 评估阶段复杂性
- **THEN** 系统 MUST 按以下公式计算复杂度分：功能点数 × 1 + 接口数 × 1.5 + 场景数 × 2
- **AND** 将结果转化为 prompt 中的节奏指引：低复杂度 (< 20) →「预计 3-5 轮验证」；中复杂度 (20-50) →「预计 5-8 轮验证」；高复杂度 (> 50) →「预计 8-12 轮验证」
- **AND** 不硬性限制迭代次数，Agent 根据实际进展自行判断

#### Scenario: Agent 提前返回但未完成

- **WHEN** Agent 子代理返回但主 Agent 验收发现产物不合格
- **THEN** 主 Agent 记录当前进度到 skill-suggestion.md
- **AND** 询问用户是否重新启动 Agent 子代理

### Requirement: Agent 迭代子代理 prompt 规范

系统 SHALL 为 Agent 迭代子代理构建包含完整上下文的 prompt。

#### Scenario: prompt 内容要求

- **WHEN** 构建 Agent 迭代子代理 prompt
- **THEN** prompt MUST 包含：
  - 当前阶段目标与产物要求
  - 输入文档引用（functional-designs/、detailed-design.md 等）
  - traceability.md 中待填充的列和覆盖率目标
  - 迭代指令：「验证产物合格后返回验收报告，若验证失败则修复后重新验证」
- **AND** prompt SHOULD 包含分阶段目标以引导迭代方向
- **AND** prompt SHOULD 包含复杂度评估结果作为节奏指引

#### Scenario: prompt 引用现有文档

- **WHEN** 子代理需要读取设计文档作为输入
- **THEN** prompt 中使用文档路径引用（非复制完整内容）
- **AND** 子代理通过 Read 工具自行读取所需文档

### Requirement: 主 Agent 验收

系统 SHALL 在 Agent 迭代子代理完成后由主 Agent 执行验收。

#### Scenario: 验收通过

- **WHEN** 主 Agent 检查以下条件全部满足：
  - 阶段产物文件存在且格式正确
  - traceability.md 对应列覆盖率 = 100%
  - 无 TODO/TBD/{待填写} 等占位符
- **THEN** 验收通过
- **AND** 更新 .status.md 中对应阶段状态为 ✅ 完成
- **AND** 门控释放，可进入下一阶段

#### Scenario: 验收不通过

- **WHEN** 主 Agent 检查发现任一条件不满足
- **THEN** 验收不通过
- **AND** 系统记录到 skill-suggestion.md（包含阶段、复杂度、覆盖率缺口、建议）
- **AND** 使用 AskUserQuestion 询问用户：「验收不通过，是否重新启动 Agent 迭代子代理？」
- **AND** 用户选择「是」→ 调整 prompt 后重新启动 Agent 子代理
- **AND** 用户选择「否」→ 标记 .status.md 为 ⚠️ 需修订，阻塞当前阶段

#### Scenario: 验收记录格式

- **WHEN** 验收不通过并记录到 skill-suggestion.md
- **THEN** 记录 MUST 包含以下字段：发现时间、发现阶段（Agent 验收）、触发场景、覆盖缺口详情、复杂度信息、改进建议、状态（待重跑）、优先级
