# Spec Delta

## MODIFIED Requirements

### Requirement: 导航验证报告路径变更

导航合理性验证的检查结果 SHALL 内联于 `self-reviews/prototype/verify-report.md` 的「导航合理性」分区，`self-reviews/prototype/nav-check/` 路径及其轮次报告 SHALL 废弃。该结果 SHALL 仅在审查方式为「子代理自动审查验证」时产出。

#### Scenario: 新路径下报告生成

- **WHEN** kflow-prototype-design 执行单轮合并验证
- **THEN** 导航合理性的 5 项检查结果 SHALL 写入 `self-reviews/prototype/verify-report.md` 的「导航合理性」分区
- **AND** 主 Agent SHALL 从该路径读取导航检查结果

#### Scenario: 人工审查路径不产出导航验证报告

- **WHEN** 审查方式为「人工审查」
- **THEN** 系统 SHALL NOT 生成 `self-reviews/prototype/verify-report.md`
- **AND** 系统 SHALL NOT 创建 `nav-check/` 子目录

### Requirement: Playwright 验证报告路径变更

Playwright 全覆盖验证的检查结果 SHALL 内联于 `self-reviews/prototype/verify-report.md` 的「Playwright 全覆盖」分区，`self-reviews/prototype/playwright-check/` 路径及其轮次报告 SHALL 废弃。该结果 SHALL 仅在审查方式为「子代理自动审查验证」时产出。

#### Scenario: 新路径下报告生成

- **WHEN** kflow-prototype-design 执行单轮合并验证
- **THEN** Playwright 的 5 项检查结果 SHALL 写入 `self-reviews/prototype/verify-report.md` 的「Playwright 全覆盖」分区
- **AND** Playwright 不可用降级报告同样写入该分区

#### Scenario: 人工审查路径不产出 Playwright 验证报告

- **WHEN** 审查方式为「人工审查」
- **THEN** 系统 SHALL NOT 生成 `self-reviews/prototype/verify-report.md`
- **AND** 系统 SHALL NOT 创建 `playwright-check/` 子目录

### Requirement: UX 规则审查与对比度检测报告路径

UX 规则审查结果与对比度检测结果 SHALL 内联于 `self-reviews/prototype/verify-report.md` 的「UX 规则审查」与「对比度检测」分区，`prototype/ux-check-round-{N}.md`、`self-reviews/prototype/ux-check/`、`self-reviews/prototype/contrast-check/` 路径 SHALL 废弃。两者 SHALL 仅在审查方式为「子代理自动审查验证」时产出。

#### Scenario: UX 规则审查报告路径

- **WHEN** kflow-prototype-design 执行单轮合并验证
- **THEN** UX 规则审查的逐项结论 SHALL 写入 `self-reviews/prototype/verify-report.md` 的「UX 规则审查」分区
- **AND** 主 Agent SHALL 从该路径读取 UX 审查结果

#### Scenario: 对比度检测报告路径

- **WHEN** kflow-prototype-design 执行单轮合并验证
- **THEN** 对比度检测结果 SHALL 写入 `self-reviews/prototype/verify-report.md` 的「对比度检测」分区
- **AND** 报告 SHALL 包含：所有检测到的颜色对及其对比度值、标记 ⚠️ 不达标的颜色对、建议替代色值

#### Scenario: 人工审查路径不产出 UX 与对比度报告

- **WHEN** 审查方式为「人工审查」
- **THEN** 系统 SHALL NOT 生成 `self-reviews/prototype/verify-report.md`
- **AND** 系统 SHALL NOT 创建 `ux-check/` 与 `contrast-check/` 子目录
