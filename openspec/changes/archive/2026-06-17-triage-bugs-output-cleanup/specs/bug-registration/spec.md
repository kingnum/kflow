## MODIFIED Requirements

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

系统 SHALL 使用纯序号格式 `BUG-{NNN}` 作为问题唯一标识，严重度作为独立字段。

#### Scenario: BUG-ID 分配
- **WHEN** 系统登记新问题
- **THEN** SHALL 分配下一个可用的递增序号 `BUG-{NNN}`（首个为 BUG-001）
- **AND** SHALL NOT 在 BUG-ID 中编码严重度前缀（如 `B-`、`W-`、`S-`）

#### Scenario: 严重度独立表示
- **WHEN** 系统记录问题的严重度
- **THEN** 严重度 SHALL 作为独立字段记录（`🔴 阻塞`、`🟡 警告`、`🔵 建议`）
- **AND** SHALL NOT 将严重度前缀编码到 BUG-ID 中

### Requirement: 问题与修复报告关联

系统 SHALL 通过「修复记录」节在 bug 详情中记录修复执行信息，而非使用独立的 fix-report 文件（A 路径场景）。

#### Scenario: A 路径修复记录回写
- **WHEN** L4 实现问题的 bug-fix 完成修复（A 路径：用户反馈 → triage → L4 → bug-fix）
- **THEN** bug-fix SHALL 将修复记录追加到 `bugs/bug-NNN-NNN.md` 对应 BUG 的「修复记录」节
- **AND** SHALL 填写：修复日期、根因分类（实现错误/测试错误）、修复文件、验证结果、修复内容、Post-mortem
- **AND** SHALL NOT 在 `bugs/` 目录下创建独立的 fix-report 文件

#### Scenario: B 路径修复报告位置
- **WHEN** bug-fix 完成修复（B 路径：测试阶段自动发现）
- **THEN** fix-report SHALL 输出到 `subchanges/{subchange}/test-reports/fix-reports/fix-{timestamp}.md`
- **AND** 若该 bug 已在 `bugs/` 目录登记，SHALL 同步在 `bugs/bug-NNN-NNN.md` 对应 BUG 的「修复记录」节追加摘要
- **AND** 摘要 SHALL 包含：修复日期、根因分类、fix-report 文件路径引用

#### Scenario: 状态更新联动
- **WHEN** bug-fix 修复验证通过
- **THEN** SHALL 将对应 bug 的状态更新为「已解决」
- **AND** SHALL 更新 `bugs/index.md` 中对应条目的状态列
