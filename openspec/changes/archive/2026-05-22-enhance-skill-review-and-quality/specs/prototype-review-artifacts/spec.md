## ADDED Requirements

### Requirement: 审查产物统一存放在 self-reviews/prototype/ 下

系统 SHALL 将原型设计阶段的所有审查和验证产物统一存放在 `self-reviews/prototype/` 目录下，按子目录分类管理。

#### Scenario: 审查产物目录结构

- **WHEN** kflow-prototype-design 执行 VERIFY 和 SELFREV 步骤
- **THEN** 产物 SHALL 按以下结构存放：
  - `self-reviews/prototype/{YYYYMMDD}-{HHMMSS}.md` — 10 轮自审报告
  - `self-reviews/prototype/nav-check/round-{1..5}.md` — 5 轮导航合理性验证报告
  - `self-reviews/prototype/playwright-check/round-{1..5}.md` — 5 轮 Playwright 验证报告
  - `self-reviews/prototype/cdn-crossref-check/report.md` — CDN 扫描 + 交叉引用检查综合报告
- **AND** SHALL NOT 将验证报告散落在 `prototype/` 目录下

#### Scenario: 目录自动创建

- **WHEN** 某子目录不存在
- **THEN** 系统 SHALL 自动创建所需的子目录
- **AND** 不需要用户手动创建

### Requirement: 导航验证报告路径变更

导航合理性验证报告 SHALL 从 `prototype/nav-check-round-{N}.md` 变更为 `self-reviews/prototype/nav-check/round-{N}.md`。

#### Scenario: 新路径下报告生成

- **WHEN** kflow-prototype-design 执行 VERIFY 步骤 6.3（导航验证）
- **THEN** 每轮子代理 SHALL 保存报告到 `self-reviews/prototype/nav-check/round-{N}.md`（N 为轮次 1-5）
- **AND** 主 Agent SHALL 从新路径读取报告

### Requirement: Playwright 验证报告路径变更

Playwright 全覆盖验证报告 SHALL 从 `prototype/playwright-check-round-{N}.md` 变更为 `self-reviews/prototype/playwright-check/round-{N}.md`。

#### Scenario: 新路径下报告生成

- **WHEN** kflow-prototype-design 执行 VERIFY 步骤 6.4（Playwright 验证）
- **THEN** 每轮子代理 SHALL 保存报告到 `self-reviews/prototype/playwright-check/round-{N}.md`（N 为轮次 1-5）
- **AND** Playwright 不可用降级报告同样保存到该路径

### Requirement: CDN 扫描和交叉引用生成独立报告

CDN 外部依赖扫描和交叉引用完整性检查 SHALL 生成独立验证报告。

#### Scenario: CDN 扫描报告

- **WHEN** kflow-prototype-design 执行 VERIFY 步骤 6.1（CDN 扫描）
- **THEN** SHALL 生成 CDN 扫描报告到 `self-reviews/prototype/cdn-crossref-check/report.md`
- **AND** 报告包含：扫描范围（文件列表）、发现的外部引用（文件/引用 URL/类型）、扫描结果（通过/不通过）

#### Scenario: 交叉引用检查报告

- **WHEN** kflow-prototype-design 执行 VERIFY 步骤 6.2（交叉引用检查）
- **THEN** SHALL 将检查结果合并到 `self-reviews/prototype/cdn-crossref-check/report.md`
- **AND** 报告包含：引用完整性矩阵（源文件/引用路径/目标文件是否存在）、断链清单

#### Scenario: CDN 扫描不通过时交叉引用仍执行

- **WHEN** CDN 扫描不通过
- **THEN** CDN 扫描结果 SHALL 记录到报告
- **AND** 交叉引用检查 SHALL 继续执行并记录结果
- **AND** 所有问题汇总在同一份 `report.md` 中
- **AND** 返回 DESIGN 步骤修复后重新执行 VERIFY
