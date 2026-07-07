# phase-artifact-verification Specification

## Purpose
定义 kflow-verify 独立诊断 Skill 的功能规格——全阶段产物诊断、严重度分级、修复路由和诊断报告格式。

## Requirements

### Requirement: kflow-verify 独立诊断 Skill 存在
系统 SHALL 提供 kflow-verify Skill 作为独立诊断工具，非流程阶段，不写入 .status.md 阶段状态表。

#### Scenario: Skill 定义
- **WHEN** kflow-verify 被调用
- **THEN** 系统 SHALL 执行七维度全阶段产物诊断
- **AND** SHALL NOT 修改 .status.md 的阶段状态
- **AND** SHALL NOT 写入 traceability.md

#### Scenario: 手动调用
- **WHEN** 用户直接调用 /kflow-verify {change-name}
- **THEN** 系统 SHALL 对指定变更执行全阶段诊断
- **AND** 输出诊断报告到 `docs/changes/{change}/verify-report.md`

#### Scenario: 归档前自动触发
- **WHEN** kflow-integration-test 阶段完成
- **AND** 变更下存在至少一个子变更
- **THEN** 系统 SHALL 自动触发 kflow-verify 诊断
- **AND** 诊断报告在 audit 阶段之前完成

### Requirement: 七维度诊断体系
系统 SHALL 对每个变更执行以下七个维度的诊断检查。

#### Scenario: D1 产物存在性检查
- **WHEN** 执行产物存在性诊断
- **THEN** 系统 SHALL 对 .status.md 中标记为「✅ 完成」的每个阶段，检查其关键产物文件是否存在
- **AND** 条件产物（🔶）SHALL 根据项目类型和子变更类型判定是否缺失
- **AND** 缺失的必须产物 SHALL 标记为 🔴 阻塞

#### Scenario: D2 产物内容完整性检查
- **WHEN** 执行内容完整性诊断
- **THEN** 系统 SHALL 检查每个产物文件是否非空
- **AND** SHALL 检查是否无占位符（TODO/TBD/{待填写}/...等）
- **AND** SHALL 检查必填章节是否存在（如 functional-designs/index.md 的版本号和修订记录、detailed-design.md 的 NFR 章节）
- **AND** 发现占位符 SHALL 标记为 🟡 警告

### Requirement: D3 输入源正确性检查

系统 SHALL 对每个子变更判定其类型（后端/前端），按类型检查输入源。子变更类型 SHALL 从子变更划分结果中读取，输入源检查 SHALL 分为 D3.1 输入源存在性检查和 D3.2 输出越界检查。

#### Scenario: D3.1 输入源存在性检查（原有逻辑）

- **WHEN** 执行输入源存在性诊断
- **THEN** 系统 SHALL 对每个子变更判定其类型（后端/前端）
- **AND** 后端子变更 SHALL 检查 functional-designs/、detailed-design.md、api-tests/、CONTEXT.md、tasks.md 可访问性
- **AND** 前端子变更 SHALL 检查 prototype/index.html、prototype/design-tokens.css、prototype/element-coverage-tree.md、detailed-design.md 可访问性
- **AND** 前端子变更 SHALL NOT 将 prototype/design-prompt.md 或 design-system/MASTER.md 列为输入
- **AND** 输入源缺失 SHALL 标记为 🔴 阻塞
- **AND** 若 functional-designs/index.md 缺少 FP 类型列，SHALL 标记 🟡 警告（旧版文档兼容）

#### Scenario: D3.2 后端子变更输出越界检查

- **WHEN** D3.2 对后端子变更执行越界检测
- **THEN** 系统 SHALL grep 检测子变更源码目录中：
  - `.tsx`、`.jsx`、`.vue`、`.svelte` 文件 → 🟡 警告
  - 硬编码颜色值（`#[0-9a-fA-F]{3,6}` 或 `rgb(` 模式 ≥ 5 次）→ 🔵 建议
  - `prototype/` 路径引用 → 🟡 警告
- **AND** 排除 `node_modules/`、`.next/`、`dist/`、`build/`、`.git/`、`*.d.ts`、`*.test.*`、`*.spec.*`、`__tests__/`、`mocks/`、`__mocks__/`

#### Scenario: D3.2 前端子变更输出越界检查

- **WHEN** D3.2 对前端子变更执行越界检测
- **THEN** 系统 SHALL grep 检测子变更源码目录中：
  - 数据库迁移脚本（`migrations/` 或 `schema.sql` 或 `*.prisma`）→ 🟡 警告
  - ORM 模型定义（`@Entity`、`@Table`、`prisma.model`、`mongoose.Schema`）→ 🟡 警告
  - 服务端路由注册（`app.use(`、`app.post(`、`router.get(`、`@PostMapping`、`@GetMapping`）→ 🟡 警告
- **AND** 排除规则同后端子变更

#### Scenario: D3.2 严重度不阻塞

- **WHEN** D3.2 越界检测发现问题
- **THEN** 🟡 警告 SHALL NOT 阻塞阶段流转
- **AND** 🔵 建议 SHALL NOT 阻塞阶段流转
- **AND** 问题 SHALL 在诊断报告中醒目展示

#### Scenario: D4 交叉引用一致性检查
- **WHEN** 执行交叉引用一致性诊断
- **THEN** 系统 SHALL 验证 traceability.md 中 FP 清单与 functional-designs/index.md 一致
- **AND** SHALL 验证 detailed-design.md 中的 FP 引用与 functional-designs/ 一致
- **AND** SHALL 验证 api-tests/ 接口数与 detailed-design.md §接口设计 匹配
- **AND** SHALL 验证 element-coverage-tree.md 🎯 状态节点的 TC-ID 覆盖率与 traceability.md E2E测试列一致
- **AND** 不一致 SHALL 标记为 🟡 警告

#### Scenario: D5 设计决策完整性检查
- **WHEN** 执行设计决策完整性诊断
- **THEN** 系统 SHALL 检查是否存在 HITL 标记的子变更（说明设计不完整）
- **AND** SHALL 检查 detailed-design.md 中是否有「待定」「TBD」等未决决策
- **AND** SHALL 检查 ADR 是否有已过期的记录
- **AND** HITL 子变更存在 SHALL 标记为 🟡 警告

#### Scenario: D6 门控合规性检查
- **WHEN** 执行门控合规性诊断
- **THEN** 系统 SHALL 检查 .status.md 阶段顺序是否正确（无跳阶段）
- **AND** SHALL 检查前置阶段状态是否为 ✅ 完成
- **AND** SHALL 检查回退后后续阶段是否已正确重置为 ⏳ 待开始
- **AND** 跳阶段或状态矛盾 SHALL 标记为 🔴 阻塞

#### Scenario: D7 审查闭环检查
- **WHEN** 执行审查闭环诊断
- **THEN** 系统 SHALL 检查 cross-reviews/ 最新批次 synthesis.md 中所有高/中严重度问题是否已关闭
- **AND** SHALL 检查代码审查（test-reports/review/code-review.md）中高严重度问题是否已修复
- **AND** SHALL 检查 traceability.md 各列覆盖率是否达标（设计阶段列 = 100%）
- **AND** 审查问题未关闭 SHALL 标记为 🔴 阻塞

### Requirement: 严重度分级
系统 SHALL 对诊断问题按三级严重度分级输出。

#### Scenario: 🔴 阻塞级判定
- **WHEN** 问题属于必须产物缺失、阶段跳转、输入源严重缺漏、审查问题未关闭
- **THEN** 系统 SHALL 标记为 🔴 阻塞
- **AND** 建议在进入下一阶段前修复

#### Scenario: 🟡 警告级判定
- **WHEN** 问题属于内容不完整（含占位符）、交叉引用不一致、覆盖率不足、HITL 未决议
- **THEN** 系统 SHALL 标记为 🟡 警告
- **AND** 建议在合适时机修复

#### Scenario: 🔵 建议级判定
- **WHEN** 问题属于文档格式不规范、版本号滞后、ADR 过期
- **THEN** 系统 SHALL 标记为 🔵 建议
- **AND** 不阻塞流程，可自行决定是否修复

### Requirement: 修复路由
系统 SHALL 为每个诊断问题提供修复路由，指向对应阶段的 REVISION 模式或重新执行。

#### Scenario: 设计阶段问题路由
- **WHEN** 诊断问题归属于 explore/prototype-design/design 阶段
- **THEN** 修复路由 SHALL 指向对应 Skill 的 REVISION 模式
- **AND** 输出格式：`→ kflow-{phase} REVISION`

#### Scenario: 执行阶段问题路由
- **WHEN** 诊断问题归属于 plan/code/code-review/api-test/e2e-test/integration-test 阶段
- **THEN** 修复路由 SHALL 指向对应 Skill 的重新执行
- **AND** 输出格式：`→ kflow-{phase} (重新执行)`

#### Scenario: 用户决策修复策略
- **WHEN** 诊断报告输出后
- **THEN** 系统 SHALL 使用 AskUserQuestion 询问用户：「诊断报告已生成。是否按修复路由执行修复？」
- **AND** 选项包含：确认全部修复 / 仅修复阻塞项 / 暂不修复
- **AND** SHALL NOT 自动执行修复

### Requirement: 诊断报告格式
系统 SHALL 输出结构化诊断报告到 `docs/changes/{change}/verify-report.md`。

#### Scenario: 报告基本结构
- **WHEN** 诊断完成
- **THEN** 报告 SHALL 包含：生成时间、诊断范围、问题总览表（按严重度统计）、分级问题清单、修复路由建议
- **AND** 报告 SHALL 包含「关联 GAP」字段，标注该问题对应的门控缺口编号（如有）

#### Scenario: 问题条目格式
- **WHEN** 输出诊断问题
- **THEN** 每条问题 SHALL 包含：编号（B/W/S-前缀）、阶段、描述、影响说明、修复路由
- **AND** 🔴 阻塞使用 B-编号，🟡 警告使用 W-编号，🔵 建议使用 S-编号

## ADDED by subchange-type-enforcement

### Requirement: FP 类型列存在性检查

verify D2 内容完整性检查 SHALL 增加对 functional-designs/index.md FP 清单「类型」列的检查。

#### Scenario: 类型列缺失警告

- **WHEN** verify D2 检查 functional-designs/index.md 内容完整性
- **AND** FP 清单缺少「类型」列（旧版文档）
- **THEN** 系统 SHALL 标记 🟡 警告：「功能点清单缺少类型列，建议重新执行 kflow-explore REVISION 补充」
- **AND** SHALL NOT 标记为 🔴 阻塞（向后兼容）

#### Scenario: 类型列存在且完整

- **WHEN** verify D2 检查 functional-designs/index.md
- **AND** FP 清单「类型」列存在且每行均已填写
- **THEN** 检查通过
