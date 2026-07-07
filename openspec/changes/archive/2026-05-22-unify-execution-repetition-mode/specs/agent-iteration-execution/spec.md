## MODIFIED Requirements

### Requirement: 复杂度评估机制

系统 SHALL 在启动 Agent 迭代子代理前评估任务复杂度，并将结果仅作为信息展示写入 .status.md 备注列。复杂度评估结果不驱动子代理执行行为——禁止将分级转化为按轮次分段分配工作重点的节奏指引。

#### Scenario: 基于可量化指标计算复杂度

- **WHEN** 评估阶段复杂性
- **THEN** 系统 MUST 按以下公式计算复杂度分：功能点数 × 1 + 接口数 × 1.5 + 场景数 × 2
- **AND** 将结果写入 .status.md 备注列作为背景信息，附带标注「仅供参考，不驱动执行行为」
- **AND** 分级阈值保留（低 <20 / 中 20-50 / 高 >50）但仅用于信息分类
- **AND** MUST NOT 将分级转化为节奏指引传递给子代理

#### Scenario: Agent 提前返回但未完成

- **WHEN** Agent 子代理返回但主 Agent 验收发现产物不合格或轮次不足
- **THEN** 主 Agent 记录当前进度到 skill-suggestion.md
- **AND** 若轮次不足 10/10 → 直接要求 Agent 子代理继续执行剩余轮次，不进入 AskUserQuestion
- **AND** 若轮次已达 10/10 但产物不合格 → 询问用户是否重新启动 Agent 子代理

### Requirement: Agent 迭代子代理 prompt 规范

系统 SHALL 为 Agent 迭代子代理构建包含完整上下文的 prompt。Prompt SHALL 包含重复制遍历指令，SHALL NOT 包含节奏指引或按轮次分段分配工作重点的指令。

#### Scenario: prompt 内容要求

- **WHEN** 构建 Agent 迭代子代理 prompt
- **THEN** prompt MUST 包含：
  - 当前阶段目标与产物要求
  - 输入文档引用（functional-designs/、detailed-design.md 等）
  - traceability.md 中待填充的列和覆盖率目标
  - 重复制遍历指令：「每轮遍历全部工作项独立执行完整流程。更新 .status.md 中执行轮次计数器为当前轮次号。禁止按轮次分段分配工作重点——每轮均须对全部工作项执行完整检查。必须完成全部 10 轮迭代后才可返回验收报告，禁止在第 10 轮前返回。若当前轮次无新发现且无可执行工作，仍须递增计数器并继续。」
- **AND** prompt SHALL NOT 包含「前 N 轮重点执行/中间 N 轮细节优化/后 N 轮验证」等分段分配指令
- **AND** 复杂度评估结果可出现在 prompt 中但必须附带标注「仅供参考，不驱动执行行为」

#### Scenario: prompt 引用现有文档

- **WHEN** 子代理需要读取设计文档作为输入
- **THEN** prompt 中使用文档路径引用（非复制完整内容）
- **AND** 子代理通过 Read 工具自行读取所需文档
