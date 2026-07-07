# doc-naming-convention (Delta)

## ADDED Requirements

### Requirement: self-reviews 目录命名规范

系统 SHALL 使用 `self-reviews/` 作为自循环审查记录的根目录。

#### Scenario: self-reviews 目录创建
- **WHEN** 变更目录首次执行设计阶段自审
- **THEN** 创建 `self-reviews/` 根目录
- **AND** 按阶段创建子目录 explore/、prototype/、design/

#### Scenario: self-reviews 子目录结构
- **WHEN** explore 阶段执行自审
- **THEN** 自审报告保存到 `self-reviews/explore/`
- **AND** prototype 阶段保存到 `self-reviews/prototype/`
- **AND** design 阶段保存到 `self-reviews/design/`

### Requirement: cross-reviews 目录命名规范

系统 SHALL 使用 `cross-reviews/` 作为四视角交叉审查记录的根目录。

#### Scenario: cross-reviews 目录创建
- **WHEN** kflow-design 首次执行四视角审查
- **THEN** 创建 `cross-reviews/` 根目录
- **AND** 每次审查（含重审）创建独立的 `{YYYYMMDD}-{HHMMSS}/` 子目录

#### Scenario: cross-reviews 取代 review-reports
- **WHEN** kflow-design 执行四视角审查
- **THEN** 审查报告保存到 `cross-reviews/{timestamp}/`
- **AND** 不再使用 `review-reports/` 目录
- **AND** 旧变更目录中的 `review-reports/` 保持兼容读取

### Requirement: 时间戳命名格式统一

系统 SHALL 对所有审查记录文件/目录使用统一的 `{YYYYMMDD}-{HHMMSS}` 时间戳命名。

#### Scenario: 单文件时间戳命名
- **WHEN** 自审报告为单文件
- **THEN** 文件名为 `{YYYYMMDD}-{HHMMSS}.md`
- **AND** 时间戳为审查开始的本地时间

#### Scenario: 多文件时间戳命名
- **WHEN** 四视角审查涉及多个文件
- **THEN** 目录名为 `{YYYYMMDD}-{HHMMSS}/`
- **AND** 时间戳为审查开始的本地时间
- **AND** 目录内文件保持原有命名（business-review.md 等）

#### Scenario: 自然排序即时间序
- **WHEN** 读取 self-reviews/{phase}/ 或 cross-reviews/
- **THEN** 条目按名称自然排序即为执行时间序
- **AND** 无需额外的排序逻辑或元数据

## MODIFIED Requirements

### Requirement: 门控检查使用新命名

系统 SHALL 在阶段门控检查中使用新的审查目录路径和新的命名格式。

#### Scenario: design 阶段自审完成检查
- **WHEN** 门控检查 design 阶段自审是否完成
- **THEN** 检查 `self-reviews/design/` 是否存在且包含 10 个时间戳命名的 .md 文件

#### Scenario: 四视角审查完成检查
- **WHEN** 门控检查 design 阶段四视角审查是否完成
- **THEN** 检查 `cross-reviews/` 是否存在且至少有一个批次目录
- **AND** 最新批次的 synthesis.md 标记为 ✅ 关闭
