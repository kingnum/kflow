# Spec Delta

## MODIFIED Requirements

### Requirement: A 路径修复记录回写

系统 SHALL 在 A 路径（用户反馈 → triage → L4 → bug-fix）的修复完成后，将修复记录回写到缺陷工作区对应问题的详情文件。

#### Scenario: A 路径修复完成后回写

- **WHEN** bug-fix 完成 A 路径问题的修复（来自 kflow-bug-triage L4 路由）
- **AND** 本地验证通过
- **THEN** bug-fix SHALL 在 triage 选定的缺陷工作区的 `bug-NNN-NNN.md` 对应 BUG 的「修复记录」节追加以下内容：
  - 修复日期
  - 根因分类（实现错误/测试错误）
  - 修复文件（逗号分隔的文件路径）
  - 验证结果（✅ 通过 / ❌ 失败）
  - 修复内容（具体变更描述）
  - Post-mortem（什么可以防止此类缺陷）
- **AND** SHALL NOT 修改 triage 登记的其他节（基本信息、问题描述、诊断结果、解决方案）
- **AND** SHALL NOT 在缺陷工作区下创建独立的 fix-report 文件

#### Scenario: 修复记录节追加规则

- **WHEN** 同一 BUG 需要多次修复（如修复后验证失败）
- **THEN** 每次修复 SHALL 追加新的「修复记录」节（不覆盖之前的记录）
- **AND** 追加顺序按修复日期排列

#### Scenario: 项目级 A 路径回写

- **WHEN** A 路径缺陷登记在项目级 `docs/bugs/`
- **THEN** 修复记录 SHALL 写入 `docs/bugs/bug-NNN-NNN.md`
- **AND** SHALL NOT 写入任何变更级 `bugs/` 目录

### Requirement: 快车道模式回写

系统 SHALL 在快车道缺陷的定向验证通过并完成快速收口后，将收口信息回写到缺陷级状态文件与选定工作区的索引。

#### Scenario: 快车道收口后回写

- **WHEN** 快车道缺陷的定向验证通过且快速收口校验项全部满足
- **THEN** 系统 SHALL 在 `bugfix-status.md` 的收口结论区写入收口时间与校验项逐项结论
- **AND** SHALL 在工作区的 `bug-NNN-NNN.md` 对应 BUG 的「修复记录」节追加修复摘要（修复日期、根因分类、修复文件、验证结果、修复内容、Post-mortem）
- **AND** SHALL 更新工作区 `index.md` 对应行状态为「已解决」
- **AND** SHALL 在缺陷详情文件中标记快车道收口完成

#### Scenario: 项目级快车道回写

- **WHEN** 项目级快车道缺陷完成收口
- **THEN** 回写路径 SHALL 为 `docs/bugs/index.md`、`docs/bugs/bug-NNN-NNN.md` 与 `docs/bugs/fix/{BUG-ID}/bugfix-status.md`
- **AND** SHALL NOT 创建或修改任何变更级产物

#### Scenario: 快车道回写不改变更级状态

- **WHEN** 快车道收口后执行回写
- **THEN** 系统 SHALL NOT 修改变更级 `.status.md` 的任何阶段状态字段
- **AND** 回写范围 SHALL 限于缺陷级状态文件与选定工作区

#### Scenario: 定向验证失败时的回写

- **WHEN** 快车道缺陷的定向验证未通过
- **THEN** SHALL NOT 更新工作区 `index.md` 状态
- **AND** SHALL 在 `bugfix-status.md` 的定向验证区记录失败信息（验证时间、失败目标、失败原因）
- **AND** SHALL 在定向验证通过后按本 Requirement 的正向路径重新回写

#### Scenario: 多次定向验证的追加规则

- **WHEN** 同一快车道缺陷经历多次定向验证
- **THEN** 每次验证 SHALL 在 `bugfix-status.md` 的定向验证区追加新的验证记录（不覆盖之前的记录）
- **AND** 追加顺序 SHALL 按验证时间排列

### Requirement: 问题状态更新联动

系统 SHALL 在 bug-fix 修复验证通过后，更新缺陷工作区中对应问题的状态。快车道缺陷的状态更新 SHALL 以定向验证通过且快速收口校验项全部满足为条件。

#### Scenario: 修复通过后状态更新

- **WHEN** bug-fix 修复验证通过（本地验证 + 原始场景验证），或快车道缺陷的定向验证通过且快速收口校验项全部满足
- **THEN** SHALL 将工作区 `bug-NNN-NNN.md` 对应 BUG 的处理状态 checkbox 更新：
  - 勾选「执行修复」
  - 勾选「验证修复」
- **AND** SHALL 将 BUG 状态字段从「处理中」更新为「已解决」
- **AND** SHALL 更新工作区 `index.md` 对应行的状态列为「已解决」

#### Scenario: 修复失败不更新状态

- **WHEN** bug-fix 修复验证失败，或快车道缺陷的定向验证未通过
- **THEN** SHALL NOT 更新缺陷工作区中的状态
- **AND** SHALL 在修复记录节记录失败信息（修复日期 + ❌ 验证失败 + 失败原因）
- **AND** BUG 状态 SHALL 保持「处理中」
