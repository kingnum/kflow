# prototype-review-artifacts Specification

## Purpose
定义原型设计阶段所有审查与验证产物的存放位置、命名规则与目录结构：统一收敛到 self-reviews/prototype/ 下，存放 SELFREV 单轮验证报告 report.md、VERIFY 单轮合并验证报告 verify-report.md，以及 BUILD 步骤的 CDN 扫描与交叉引用综合检查报告 cdn-crossref-check/report.md。
## Requirements
### Requirement: 审查产物统一存放在 self-reviews/prototype/ 下

系统 SHALL 将原型设计阶段的所有审查和验证产物统一存放在 `self-reviews/prototype/` 目录下，按子目录分类管理。产出的产物范围 SHALL 由审查方式决定。

#### Scenario: 审查产物目录结构

- **WHEN** kflow-prototype-design 执行 BUILD、VERIFY 和 SELFREV 步骤
- **THEN** 产物 SHALL 按以下结构存放：
  - `self-reviews/prototype/report.md` — SELFREV 单轮验证报告（签署清单打假结果 + 独立发现 + 范围外观察 + 全量遍历证明 + 验证结论）
  - `self-reviews/prototype/verify-report.md` — VERIFY 单轮合并验证报告（「导航合理性」「Playwright 全覆盖」「UX 规则审查」「对比度检测」四分区 + 「验证结论」分区）
  - `self-reviews/prototype/cdn-crossref-check/report.md` — CDN 扫描 + 交叉引用 + 必检产物 + 清单一致 综合报告（BUILD 步骤产物）
- **AND** SHALL NOT 将验证报告散落在产品级原型目录 `docs/designs/prototypes/` 下
- **AND** SHALL NOT 产出按轮次编号的多份报告

#### Scenario: 审查方式决定产物范围

- **WHEN** 审查方式为"人工审查"
- **THEN** 系统 SHALL 仅产出 `self-reviews/prototype/cdn-crossref-check/report.md`（BUILD 步骤产物）
- **AND** SHALL NOT 产出 `self-reviews/prototype/report.md` 与 `self-reviews/prototype/verify-report.md`

#### Scenario: 子代理自动审查验证路径产出全部报告

- **WHEN** 审查方式为"子代理自动审查验证"
- **THEN** 系统 SHALL 产出 `self-reviews/prototype/report.md`、`self-reviews/prototype/verify-report.md` 与 `cdn-crossref-check/report.md`
- **AND** 各报告的份数 SHALL 恒为 1，SHALL NOT 因轮次而增加

#### Scenario: 目录自动创建

- **WHEN** 某子目录不存在
- **THEN** 系统 SHALL 自动创建所需的子目录
- **AND** 不需要用户手动创建

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

### Requirement: CDN 扫描和交叉引用生成独立报告

BUILD 步骤中的 CDN 外部依赖扫描和交叉引用完整性检查 SHALL 生成独立验证报告，作为 BUILD 步骤的产物，且 SHALL 在两种审查方式下均产出。

#### Scenario: CDN 扫描报告

- **WHEN** 主 Agent 执行 BUILD 步骤的 CDN 外部依赖扫描
- **THEN** SHALL 生成 CDN 扫描报告到 `self-reviews/prototype/cdn-crossref-check/report.md`
- **AND** 报告包含：扫描范围（文件列表）、发现的外部引用（文件/引用 URL/类型）、扫描结果（通过/不通过）

#### Scenario: 交叉引用检查报告

- **WHEN** 主 Agent 执行 BUILD 步骤的交叉引用完整性检查
- **THEN** SHALL 将检查结果合并到 `self-reviews/prototype/cdn-crossref-check/report.md`
- **AND** 报告包含：引用完整性矩阵（源文件/引用路径/目标文件是否存在）、断链清单

#### Scenario: CDN 扫描不通过时交叉引用仍执行

- **WHEN** CDN 外部依赖扫描不通过
- **THEN** CDN 扫描结果 SHALL 记录到报告
- **AND** 交叉引用完整性检查 SHALL 继续执行并记录结果
- **AND** 所有问题汇总在同一份 `report.md` 中
- **AND** 系统 SHALL 修复问题后重跑 BUILD 的全部四项静态检查

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
