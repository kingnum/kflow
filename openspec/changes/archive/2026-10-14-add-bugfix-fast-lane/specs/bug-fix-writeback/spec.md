# Spec Delta

## ADDED Requirements

### Requirement: 快车道模式回写

系统 SHALL 在快车道缺陷的定向验证通过并完成快速收口后，将收口信息回写到缺陷级状态文件与 `bugs/` 目录。

#### Scenario: 快车道收口后回写

- **WHEN** 快车道缺陷的定向验证通过且快速收口校验项全部满足
- **THEN** 系统 SHALL 在 `bugfix-status.md` 的收口结论区写入收口时间与校验项逐项结论
- **AND** SHALL 在 `bugs/bug-NNN-NNN.md` 对应 BUG 的「修复记录」节追加修复摘要（修复日期、根因分类、修复文件、验证结果、修复内容、Post-mortem）
- **AND** SHALL 更新 `bugs/index.md` 对应行状态为「已解决」
- **AND** SHALL 在缺陷详情文件中标记快车道收口完成

#### Scenario: 快车道回写不改变更级状态

- **WHEN** 快车道收口后执行回写
- **THEN** 系统 SHALL NOT 修改变更级 `.status.md` 的任何阶段状态字段
- **AND** 回写范围 SHALL 限于缺陷级状态文件与 `bugs/` 目录

#### Scenario: 定向验证失败时的回写

- **WHEN** 快车道缺陷的定向验证未通过
- **THEN** SHALL NOT 更新 `bugs/index.md` 状态
- **AND** SHALL 在 `bugfix-status.md` 的定向验证区记录失败信息（验证时间、失败用例、失败原因）
- **AND** SHALL 在定向验证通过后按本 Requirement 的正向路径重新回写

#### Scenario: 多次定向验证的追加规则

- **WHEN** 同一快车道缺陷经历多次定向验证
- **THEN** 每次验证 SHALL 在 `bugfix-status.md` 的定向验证区追加新的验证记录（不覆盖之前的记录）
- **AND** 追加顺序 SHALL 按验证时间排列

## MODIFIED Requirements

### Requirement: 问题状态更新联动

系统 SHALL 在 bug-fix 修复验证通过后，更新 bugs/ 目录中对应问题的状态。快车道缺陷的状态更新 SHALL 以定向验证通过且快速收口校验项全部满足为条件。

#### Scenario: 修复通过后状态更新

- **WHEN** bug-fix 修复验证通过（本地验证 + 原始场景验证），或快车道缺陷的定向验证通过且快速收口校验项全部满足
- **THEN** SHALL 将 `bugs/bug-NNN-NNN.md` 对应 BUG 的处理状态 checkbox 更新：
  - 勾选「执行修复」
  - 勾选「验证修复」
- **AND** SHALL 将 BUG 状态字段从「处理中」更新为「已解决」
- **AND** SHALL 更新 `bugs/index.md` 对应行的状态列为「已解决」

#### Scenario: 修复失败不更新状态

- **WHEN** bug-fix 修复验证失败，或快车道缺陷的定向验证未通过
- **THEN** SHALL NOT 更新 bugs/ 目录中的状态
- **AND** SHALL 在修复记录节记录失败信息（修复日期 + ❌ 验证失败 + 失败原因）
- **AND** BUG 状态 SHALL 保持「处理中」
