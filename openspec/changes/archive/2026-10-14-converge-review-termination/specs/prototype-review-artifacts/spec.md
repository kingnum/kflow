# Spec Delta

## MODIFIED Requirements

### Requirement: 审查产物统一存放在 self-reviews/prototype/ 下

系统 SHALL 将原型设计阶段的所有审查和验证产物统一存放在 `self-reviews/prototype/` 目录下，按子目录分类管理。产出的产物范围 SHALL 由审查方式决定。

#### Scenario: 审查产物目录结构

- **WHEN** kflow-prototype-design 执行 BUILD、VERIFY 和 SELFREV 步骤
- **THEN** 产物 SHALL 按以下结构存放：
  - `self-reviews/prototype/{YYYYMMDD}-{HHMMSS}.md` — 按收敛实际轮次产出的自审报告
  - `self-reviews/prototype/nav-check/round-{N}.md` — 导航合理性验证报告（下限 1 轮，轮数由收敛决定，见证轮收敛终止）
  - `self-reviews/prototype/playwright-check/round-{N}.md` — Playwright 验证报告（下限 1 轮，轮数由收敛决定，见证轮收敛终止）
  - `self-reviews/prototype/ux-check/round-{N}.md` — UX 规则审查报告（下限 1 轮，轮数由收敛决定，见证轮收敛终止）
  - `self-reviews/prototype/contrast-check/report.md` — 对比度检测报告
  - `self-reviews/prototype/cdn-crossref-check/report.md` — CDN 扫描 + 交叉引用 + 必检产物 + 清单一致 综合报告
- **AND** SHALL NOT 将验证报告散落在产品级原型目录 `docs/designs/prototypes/` 下

#### Scenario: 审查方式决定产物范围

- **WHEN** 审查方式为"人工审查"
- **THEN** 系统 SHALL 仅产出 `self-reviews/prototype/cdn-crossref-check/report.md`（BUILD 步骤产物）
- **AND** SHALL NOT 产出自审报告、`nav-check/`、`playwright-check/`、`ux-check/` 下的轮次报告与 `contrast-check/report.md`

#### Scenario: 子代理自动审查验证路径产出全部报告

- **WHEN** 审查方式为"子代理自动审查验证"
- **THEN** 系统 SHALL 产出自审报告、导航验证报告、Playwright 验证报告、UX 规则审查报告、对比度检测报告与 BUILD 报告（各验证报告的轮数由收敛决定，无固定轮数上限）

#### Scenario: 目录自动创建

- **WHEN** 某子目录不存在
- **THEN** 系统 SHALL 自动创建所需的子目录
- **AND** 不需要用户手动创建

### Requirement: 导航验证报告路径变更

导航合理性验证报告 SHALL 从 `prototype/nav-check-round-{N}.md` 变更为 `self-reviews/prototype/nav-check/round-{N}.md`，且 SHALL 仅在审查方式为"子代理自动审查验证"时产出。

#### Scenario: 新路径下报告生成

- **WHEN** kflow-prototype-design 执行 VERIFY 步骤 9.1（导航验证）
- **THEN** 每轮子代理 SHALL 保存报告到 `self-reviews/prototype/nav-check/round-{N}.md`（N 为收敛实际轮次）
- **AND** 主 Agent SHALL 从新路径读取报告

#### Scenario: 人工审查路径不产出导航验证报告

- **WHEN** 审查方式为"人工审查"
- **THEN** 系统 SHALL NOT 生成 `self-reviews/prototype/nav-check/round-{N}.md`
- **AND** 系统 SHALL NOT 创建 `nav-check/` 子目录

### Requirement: Playwright 验证报告路径变更

Playwright 全覆盖验证报告 SHALL 从 `prototype/playwright-check-round-{N}.md` 变更为 `self-reviews/prototype/playwright-check/round-{N}.md`，且 SHALL 仅在审查方式为"子代理自动审查验证"时产出。

#### Scenario: 新路径下报告生成

- **WHEN** kflow-prototype-design 执行 VERIFY 步骤 9.2（Playwright 验证）
- **THEN** 每轮子代理 SHALL 保存报告到 `self-reviews/prototype/playwright-check/round-{N}.md`（N 为收敛实际轮次）
- **AND** Playwright 不可用降级报告同样保存到该路径

#### Scenario: 人工审查路径不产出 Playwright 验证报告

- **WHEN** 审查方式为"人工审查"
- **THEN** 系统 SHALL NOT 生成 `self-reviews/prototype/playwright-check/round-{N}.md`
- **AND** 系统 SHALL NOT 创建 `playwright-check/` 子目录

### Requirement: UX 规则审查与对比度检测报告路径

UX 规则审查报告与对比度检测报告 SHALL 统一存放在变更级 `self-reviews/prototype/` 目录下，取自 `prototype/ux-check-round-{N}.md`、`prototype/contrast-check.md` 的产物路径 SHALL 废弃。两者 SHALL 仅在审查方式为"子代理自动审查验证"时产出。

#### Scenario: UX 规则审查报告路径

- **WHEN** kflow-prototype-design 执行 VERIFY 步骤 9.3（UX 规则审查）
- **THEN** 每轮子代理 SHALL 保存报告到 `self-reviews/prototype/ux-check/round-{N}.md`（N 为收敛实际轮次）
- **AND** 主 Agent SHALL 从该路径读取报告

#### Scenario: 对比度检测报告路径

- **WHEN** kflow-prototype-design 执行 VERIFY 步骤 9.4（对比度检测）
- **THEN** 系统 SHALL 保存报告到 `self-reviews/prototype/contrast-check/report.md`
- **AND** 报告 SHALL 包含：所有检测到的颜色对及其对比度值、标记 ⚠️ 不达标的颜色对、建议替代色值

#### Scenario: 人工审查路径不产出 UX 与对比度报告

- **WHEN** 审查方式为"人工审查"
- **THEN** 系统 SHALL NOT 生成 `self-reviews/prototype/ux-check/round-{N}.md` 与 `self-reviews/prototype/contrast-check/report.md`
- **AND** 系统 SHALL NOT 创建 `ux-check/` 与 `contrast-check/` 子目录
