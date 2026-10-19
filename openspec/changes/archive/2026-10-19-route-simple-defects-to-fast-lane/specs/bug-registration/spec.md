# Spec Delta

## MODIFIED Requirements

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

## ADDED Requirements

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
