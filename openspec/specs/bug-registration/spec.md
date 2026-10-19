## Purpose

Define the bug registration mechanism — `bugs/` directory structure, `index.md` format, paginated detail file format (≤20 bugs per file), severity grading, and status tracking for issue lifecycle management.

## Requirements

### Requirement: bugs 目录结构

系统 SHALL 支持两种问题登记工作区：变更级 `docs/changes/{change}/bugs/` 用于测试阶段自动发现的缺陷（B 路径）；项目级 `docs/bugs/` 用于用户反馈的缺陷（A 路径）以及不属于任何活跃变更的缺陷。kflow-bug-triage SHALL 在登记前确定工作区。

#### Scenario: 目录创建时机

- **WHEN** kflow-bug-triage 为某变更登记测试阶段自动发现的缺陷
- **THEN** 系统 SHALL 在 `docs/changes/{change}/` 下创建 `bugs/` 目录
- **AND** 创建 `bugs/index.md` 索引文件
- **AND** 创建首个分页详情文件 `bugs/bug-001-020.md`

#### Scenario: 项目级目录创建时机

- **WHEN** kflow-bug-triage 登记用户反馈的缺陷且该缺陷不属于任何活跃变更
- **THEN** 系统 SHALL 在项目根创建 `docs/bugs/` 目录
- **AND** 创建 `docs/bugs/index.md` 索引文件
- **AND** 创建首个分页详情文件 `docs/bugs/bug-001-020.md`

#### Scenario: 项目级目录生命周期

- **WHEN** 项目级缺陷快速收口完成
- **THEN** `docs/bugs/` 下的问题详情与 `fix/{BUG-ID}/` 状态文件 SHALL 保留为历史记录
- **AND** SHALL NOT 随任何变更归档而移动或删除

#### Scenario: 目录生命周期

- **WHEN** 变更归档时
- **THEN** 变更级 `bugs/` 目录 SHALL 随变更整体归档到 `docs/archive/` 对应目录
- **AND** 归档前 SHALL 检查该变更是否存在未关闭的 🔴 阻塞级问题

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
- **THEN** 文件 SHALL 命名为 `bug-{start}-{end}.md`，表示包含的 BUG ID 范围
- **AND** 第一个文件为 `bug-001-020.md`，第二个为 `bug-021-040.md`，以此类推
- **AND** SHALL NOT 使用非标准命名（如 `bug-001-005.md` 表示"BUG-001 到 BUG-005"以外的语义）

#### Scenario: 追加优先、满额新建
- **WHEN** 系统登记新问题
- **THEN** SHALL 将新问题的详情追加到当前分页文件末尾
- **AND** SHALL NOT 每次登记新问题时创建新的分页文件
- **AND** 仅当当前分页文件已包含 20 个问题时，SHALL 创建新的分页文件
- **AND** 新文件名 SHALL 反映新的 ID 范围（如 `bug-021-040.md`）

#### Scenario: 问题详情内容模板
- **WHEN** 系统登记单个问题的详情
- **THEN** 每个问题 SHALL 按以下顺序包含以下节（SHALL NOT 省略任何节）：
  - 基本信息：ID、登记时间、严重度、问题来源
  - 问题描述：用户原始反馈、问题现象、复现步骤
  - 诊断结果：四层溯源路径表、问题源头层级、判断依据
  - 解决方案：建议方案、路由目标、影响范围、下游影响
  - 处理状态：checkbox 列表（问题登记/诊断完成/用户确认/执行修复/验证修复/关闭）
  - 修复记录：占位，由 bug-fix 回写（含修复日期、根因分类、修复文件、验证结果、修复内容、Post-mortem）
  - 关联：关联子变更、关联功能点
- **AND** SHALL NOT 包含 YAML frontmatter（`stage`、`skill`、`template_for` 字段）

### Requirement: BUG-ID 编号规范

系统 SHALL 使用纯序号格式 `BUG-{NNN}` 作为问题唯一标识，严重度作为独立字段。项目级与变更级工作区各自维护独立的递增序号。

#### Scenario: BUG-ID 分配

- **WHEN** 系统向任一缺陷工作区登记新问题
- **THEN** SHALL 分配该工作区下一个可用的递增序号 `BUG-{NNN}`（首个为 BUG-001）
- **AND** 项目级与变更级工作区 SHALL 各自独立维护序号
- **AND** SHALL NOT 在 BUG-ID 中编码严重度前缀

#### Scenario: 严重度独立表示

- **WHEN** 系统记录问题的严重度
- **THEN** 严重度 SHALL 作为独立字段记录（`🔴 阻塞`、`🟡 警告`、`🔵 建议`）
- **AND** SHALL NOT 将严重度前缀编码到 BUG-ID 中

#### Scenario: 跨工作区引用

- **WHEN** 问题详情引用另一工作区的缺陷
- **THEN** SHALL 使用“工作区路径 + BUG-ID”形式标识
- **AND** SHALL NOT 仅使用 BUG-ID 造成跨工作区歧义

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

系统 SHALL 通过「修复记录」节在 bug 详情中记录修复执行信息，而非使用独立的 fix-report 文件（A 路径场景）。

##### Scenario: A 路径修复记录回写
- **WHEN** L4 实现问题的 bug-fix 完成修复（A 路径：用户反馈 → triage → L4 → bug-fix）
- **THEN** bug-fix SHALL 将修复记录追加到 `bugs/bug-NNN-NNN.md` 对应 BUG 的「修复记录」节
- **AND** SHALL 填写：修复日期、根因分类（实现错误/测试错误）、修复文件、验证结果、修复内容、Post-mortem
- **AND** SHALL NOT 在 `bugs/` 目录下创建独立的 fix-report 文件

##### Scenario: B 路径修复报告位置
- **WHEN** bug-fix 完成修复（B 路径：测试阶段自动发现）
- **THEN** fix-report SHALL 输出到 `subchanges/{subchange}/test-reports/fix-reports/fix-{timestamp}.md`
- **AND** 若该 bug 已在 `bugs/` 目录登记，SHALL 同步在 `bugs/bug-NNN-NNN.md` 对应 BUG 的「修复记录」节追加摘要
- **AND** 摘要 SHALL 包含：修复日期、根因分类、fix-report 文件路径引用

##### Scenario: 状态更新联动
- **WHEN** bug-fix 修复验证通过
- **THEN** SHALL 将对应 bug 的状态更新为「已解决」
- **AND** SHALL 更新 `bugs/index.md` 中对应条目的状态列

### Requirement: 项目级缺陷工作区

系统 SHALL 在项目根提供 `docs/bugs/` 工作区，承载用户反馈的缺陷（A 路径）以及不属于任何活跃变更的缺陷。该工作区 SHALL 与变更级 `bugs/` 同构，但不参与变更归档。

#### Scenario: 项目级工作区结构

- **WHEN** 项目级缺陷工作区首次创建
- **THEN** 目录 SHALL 包含：
  - `index.md` 问题索引
  - `bug-{start}-{end}.md` 分页详情文件
  - `fix/{BUG-ID}/bugfix-status.md` 缺陷级状态文件（L4 快车道缺陷）
  - `fix/{BUG-ID}/verify-report.md` 定向验证报告（L4 快车道缺陷）

#### Scenario: 项目级索引格式

- **WHEN** 系统创建或更新 `docs/bugs/index.md`
- **THEN** 文件 SHALL 包含统计、问题列表与分页表
- **AND** 问题列表每行 SHALL 含 ID、标题、严重度、源头阶段、处理路径、状态、登记时间、详情文件、关联变更

#### Scenario: 项目级工作区不参与变更归档

- **WHEN** 任一变更归档
- **THEN** `docs/bugs/` SHALL NOT 被移动、合并或删除
- **AND** 归档门控 SHALL 单独读取 `docs/bugs/index.md` 判定阻塞级缺陷
