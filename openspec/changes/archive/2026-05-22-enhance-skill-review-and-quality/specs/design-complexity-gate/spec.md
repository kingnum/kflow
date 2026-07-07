## ADDED Requirements

### Requirement: 功能点复杂度评估

系统 SHALL 在 kflow-design 步骤 4（DESIGN）中对每个功能点评估实现复杂度，分为低/中/高三级。

#### Scenario: 复杂度分级标准

- **WHEN** kflow-design 为每个功能点编写详细设计
- **THEN** 按以下标准评估复杂度：
  - **低复杂度**：标准 CRUD 操作、简单数据展示、单表查询
  - **中复杂度**：多条件组合查询、表单校验链（≥3 字段联动）、状态机（≤3 状态）、多表关联查询
  - **高复杂度**：多系统外部集成、分布式事务、非平凡算法（如推荐/匹配/排程）、性能敏感路径（高并发/大数据量）、安全敏感操作（支付/鉴权/加密）、业务规则模糊或存在多种合理实现方式
- **AND** 评估结果记录在设计文档中（design-complexity-gate spec 的复杂度分布表）

#### Scenario: 复杂度分布记录

- **WHEN** 所有功能点复杂度评估完成
- **THEN** 在 detailed-design.md（或 detailed-design/index.md）中生成复杂度分布表
- **AND** 表格包含：复杂度等级、数量、涉及 FP 列表

### Requirement: 高复杂度功能点必须用户确认

系统 SHALL 对高复杂度功能点，在详细设计完成后、子变更划分前，逐项通过 AskUserQuestion 与用户确认实现细节。

#### Scenario: 高复杂度 FP 逐项确认

- **WHEN** 存在 ≥1 个高复杂度功能点
- **THEN** 主 Agent SHALL 对每个高复杂度 FP 发起 AskUserQuestion
- **AND** 展示该 FP 的设计方案摘要（不超过 10 行）
- **AND** 明确关键决策点和可选方案
- **AND** 用户确认后进入下一个高复杂度 FP
- **AND** 所有高复杂度 FP 确认完毕后进入 NFR 步骤

#### Scenario: 无高复杂度 FP

- **WHEN** 所有功能点均为低或中复杂度
- **THEN** 跳过逐项确认
- **AND** 在复杂度分布表中标注 "无需逐项确认"
- **AND** 中复杂度 FP 的关键决策点在设计文档中标注，APPROVAL 步骤统一确认

#### Scenario: 用户提出修订

- **WHEN** 用户对高复杂度 FP 的确认回复为 "需要修订"
- **THEN** 收集用户反馈
- **AND** 回到该 FP 的设计步骤修订设计
- **AND** 修订后重新发起确认
- **AND** 不影响已确认的其他高复杂度 FP

### Requirement: 中复杂度功能点决策标注

系统 SHALL 对中复杂度功能点，在详细设计文档中标注关键决策点和设计假设，供 APPROVAL 步骤统一确认。

#### Scenario: 中复杂度 FP 标注

- **WHEN** 功能点复杂度评估为中
- **THEN** 在 detailed-design.md 该 FP 的设计章节末尾标注 "💡 关键决策" 模块
- **AND** 列出该 FP 的关键设计选择和假设
- **AND** 标注可能的替代方案（如有）
