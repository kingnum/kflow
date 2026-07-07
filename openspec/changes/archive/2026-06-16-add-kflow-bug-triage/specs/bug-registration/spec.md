## ADDED Requirements

### Requirement: bugs 目录结构

系统 SHALL 在变更目录下创建独立的问题登记目录 `docs/changes/{change}/bugs/`，用于登记和追踪变更过程中发现的所有问题。

#### Scenario: 目录创建时机
- **WHEN** kflow-bug-triage 首次为某变更登记问题
- **THEN** 系统 SHALL 在 `docs/changes/{change}/` 下创建 `bugs/` 目录
- **AND** 创建 `bugs/index.md` 索引文件
- **AND** 创建首个分页详情文件 `bugs/bug-001-020.md`

#### Scenario: 目录生命周期
- **WHEN** 变更归档时
- **THEN** `bugs/` 目录 SHALL 随变更整体归档到 `docs/archive/` 对应目录
- **AND** 归档前 SHALL 检查是否有未关闭的 🔴 阻塞级问题

### Requirement: index 索引文件格式

系统 SHALL 在 `bugs/index.md` 中维护问题索引，包含统计信息和所有问题的摘要列表。

#### Scenario: 索引内容结构
- **WHEN** 系统创建或更新 `bugs/index.md`
- **THEN** 文件 SHALL 包含以下节：
  - 统计：总问题数、按严重度分类计数、按状态分类计数
  - 问题列表：表格形式，每行含 ID、标题、严重度、源头阶段、路由目标、状态、登记时间、详情文件
  - 分页：表格形式，列出每个分页文件及其包含的 BUG ID 范围

#### Scenario: 新增问题时更新索引
- **WHEN** kflow-bug-triage 登记新问题
- **THEN** 系统 SHALL 在 `bugs/index.md` 的问题列表表格中追加一行
- **AND** 更新统计计数
- **AND** 如果当前分页文件已满（20 条），SHALL 创建新的分页文件并更新分页表

### Requirement: 分页详情文件格式

系统 SHALL 使用分页详情文件记录每个问题的完整信息，每个文件最多登记 20 个 BUG。

#### Scenario: 文件命名规则
- **WHEN** 系统创建分页详情文件
- **THEN** 文件 SHALL 命名为 `bug-{NNN}-{NNN}.md`，表示包含的 BUG ID 范围
- **AND** 第一个文件为 `bug-001-020.md`，第二个为 `bug-021-040.md`，以此类推

#### Scenario: 问题详情内容模板
- **WHEN** 系统登记单个问题的详情
- **THEN** 每个问题 SHALL 包含以下节：
  - 基本信息：ID、登记时间、严重度、问题来源（用户反馈/测试发现/审查发现）
  - 问题描述：用户原始反馈、问题现象、复现步骤
  - 诊断结果：四层溯源路径表（每层含检查项、结论、证据）、问题源头层级和判断依据
  - 解决方案：建议方案、路由目标、影响范围、下游影响
  - 处理状态：checkbox 列表（问题登记/诊断完成/用户确认/执行修复/验证修复/关闭）
  - 关联：关联子变更、关联功能点、关联修复报告（修复完成后填写）

#### Scenario: 单个文件上限
- **WHEN** 当前分页文件已包含 20 个问题
- **THEN** 系统 SHALL 创建新的分页文件
- **AND** 新文件名 SHALL 反映新的 ID 范围

### Requirement: 问题状态追踪

系统 SHALL 为每个登记的问题维护完整的生命周期状态。

#### Scenario: 状态流转
- **WHEN** 问题被登记
- **THEN** 初始状态 SHALL 为「待处理」
- **AND** 状态流转 SHALL 遵循：待处理 → 处理中 → 已解决 → 已关闭
- **AND** 任何状态 SHALL 可标记为「已挂起」（用户选择暂缓处理）

#### Scenario: 状态更新时机
- **WHEN** 问题路由到对应阶段并开始修复
- **THEN** 状态 SHALL 更新为「处理中」
- **AND** 当修复验证通过
- **THEN** 状态 SHALL 更新为「已解决」
- **AND** 当用户在 AskUserQuestion 中确认关闭
- **THEN** 状态 SHALL 更新为「已关闭」

#### Scenario: 问题与修复报告关联
- **WHEN** L4 实现问题的 bug-fix 完成修复
- **THEN** 对应问题详情的「关联修复报告」字段 SHALL 填入 fix-report 文件路径
- **AND** 问题状态 SHALL 更新为「已解决」
