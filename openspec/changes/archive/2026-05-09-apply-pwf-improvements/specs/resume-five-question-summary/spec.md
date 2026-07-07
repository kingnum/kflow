## ADDED Requirements

### Requirement: 五问题快速摘要输出

`kflow-resume` Skill 在恢复流程的 SUMMARIZE 步骤中 SHALL 输出五问题快速摘要，使用户在一屏内确认恢复状态。

#### Scenario: 五问题摘要格式
- **WHEN** kflow-resume 执行 SUMMARIZE 步骤
- **THEN** 系统 SHALL 在详细恢复信息前输出「恢复摘要」区块
- **AND** 区块包含以下 5 个字段：
  1. 当前位置：当前阶段 → 当前子变更（如适用）→ 当前功能点（如适用）
  2. 剩余路径：按顺序列出未完成的阶段（用 → 连接，仅显示当前变更剩余阶段）
  3. 变更目标：从 .status.md 的「变更描述」字段获取
  4. 设计依据：指向当前阶段依赖的主要设计文档及章节
  5. 已完成：从 tasks.md checkbox 统计已完成 / 总任务数

#### Scenario: 摘要数据来源
- **WHEN** 系统准备输出摘要
- **THEN** 「当前位置」SHALL 从 .status.md 的「当前阶段」字段和子变更进度矩阵获取
- **AND** 「剩余路径」SHALL 从 .status.md 的阶段状态表获取（筛选 ⏳ 待开始 的阶段）
- **AND** 「变更目标」SHALL 从 .status.md 的「变更描述」字段获取
- **AND** 「设计依据」SHALL 根据当前阶段映射对应的设计文档路径
- **AND** 「已完成」SHALL 从当前子变更 tasks.md 统计 ✅ checkbox 数量

#### Scenario: 设计依据映射
- **WHEN** 当前阶段为编码或测试
- **THEN** 「设计依据」SHALL 指向变更级 detailed-design.md（含章号）
- **WHEN** 当前阶段为详细设计
- **THEN** 「设计依据」SHALL 指向 functional-designs/index.md
- **WHEN** 当前阶段为计划
- **THEN** 「设计依据」SHALL 指向 detailed-design.md 的子变更划分章节

#### Scenario: 摘要与详细恢复信息的关系
- **WHEN** kflow-resume 输出恢复结果
- **THEN** 五问题摘要 SHALL 在详细恢复信息之前展示
- **AND** 摘要 SHALL 控制在 15 行以内，使用简洁格式
- **AND** 详细恢复流程输出（当前阶段、待执行任务等）在摘要之后完整展示
