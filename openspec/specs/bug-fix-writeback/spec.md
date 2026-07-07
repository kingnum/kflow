## Purpose

定义 kflow-bug-fix 对 bugs/ 目录的回写职责——在修复完成后，将修复记录追加到问题详情文件，并更新问题索引状态。区分 A 路径（用户反馈路由）和 B 路径（测试阶段发现）的不同处理方式。

## Requirements

### Requirement: A 路径修复记录回写

系统 SHALL 在 A 路径（用户反馈 → triage → L4 → bug-fix）的修复完成后，将修复记录回写到 bugs/ 目录对应问题的详情文件。

#### Scenario: A 路径修复完成后回写
- **WHEN** bug-fix 完成 A 路径问题的修复（来自 kflow-bug-triage L4 路由）
- **AND** 本地验证通过
- **THEN** bug-fix SHALL 在 `bugs/bug-NNN-NNN.md` 对应 BUG 的「修复记录」节追加以下内容：
  - 修复日期
  - 根因分类（实现错误/测试错误）
  - 修复文件（逗号分隔的文件路径）
  - 验证结果（✅ 通过 / ❌ 失败）
  - 修复内容（具体变更描述）
  - Post-mortem（什么可以防止此类缺陷）
- **AND** SHALL NOT 修改 triage 登记的其他节（基本信息、问题描述、诊断结果、解决方案）
- **AND** SHALL NOT 在 `bugs/` 目录下创建独立的 fix-report 文件

#### Scenario: 修复记录节追加规则
- **WHEN** 同一 BUG 需要多次修复（如修复后验证失败）
- **THEN** 每次修复 SHALL 追加新的「修复记录」节（不覆盖之前的记录）
- **AND** 追加顺序按修复日期排列

### Requirement: B 路径同步回写

系统 SHALL 在 B 路径（测试阶段自动发现 → bug-fix）的修复完成后，若对应 bug 已在 bugs/ 登记，则同步回写修复记录。

#### Scenario: B 路径修复后同步回写
- **WHEN** bug-fix 完成 B 路径问题的修复
- **AND** 该问题已在 `bugs/` 目录登记（由 triage 之前登记，或同时登记）
- **THEN** bug-fix SHALL 在 `bugs/bug-NNN-NNN.md` 对应 BUG 的「修复记录」节追加摘要
- **AND** 摘要 SHALL 包含：修复日期、根因分类、fix-report 文件路径引用（指向 `subchanges/{sc}/test-reports/fix-reports/fix-{timestamp}.md`）
- **AND** 完整修复详情 SHALL 保留在 fix-report 文件中，摘要节仅做引用

#### Scenario: B 路径问题未登记
- **WHEN** bug-fix 完成 B 路径问题的修复
- **AND** 该问题未在 `bugs/` 目录登记
- **THEN** SHALL NOT 创建新的 bugs/ 条目（B 路径的修复报告仅在子变更目录维护）

### Requirement: 问题状态更新联动

系统 SHALL 在 bug-fix 修复验证通过后，更新 bugs/ 目录中对应问题的状态。

#### Scenario: 修复通过后状态更新
- **WHEN** bug-fix 修复验证通过（本地验证 + 原始场景验证）
- **THEN** SHALL 将 `bugs/bug-NNN-NNN.md` 对应 BUG 的处理状态 checkbox 更新：
  - 勾选「执行修复」
  - 勾选「验证修复」
- **AND** SHALL 将 BUG 状态字段从「处理中」更新为「已解决」
- **AND** SHALL 更新 `bugs/index.md` 对应行的状态列为「已解决」

#### Scenario: 修复失败不更新状态
- **WHEN** bug-fix 修复验证失败
- **THEN** SHALL NOT 更新 bugs/ 目录中的状态
- **AND** SHALL 在修复记录节记录失败信息（修复日期 + ❌ 验证失败 + 失败原因）
