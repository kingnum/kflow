## MODIFIED Requirements

### Requirement: D3 输入源正确性检查

系统 SHALL 对每个子变更判定其类型（后端/前端），按类型检查输入源。子变更类型 SHALL 从子变更划分结果中读取，输入源检查 SHALL 分为 D3.1 输入源存在性检查和 D3.2 输出越界检查。

#### Scenario: D3.1 输入源存在性检查（原有逻辑）

- **WHEN** 执行输入源存在性诊断
- **THEN** 系统 SHALL 对每个子变更判定其类型（后端/前端）
- **AND** 后端子变更 SHALL 检查 functional-designs/、detailed-design.md、api-tests/、CONTEXT.md、tasks.md 可访问性
- **AND** 前端子变更 SHALL 检查 docs/designs/prototypes/manifest.md、变更级 prototype-changes.md、变更级 element-coverage-tree.md、detailed-design.md 可访问性
- **AND** 前端子变更 SHALL NOT 将 prototype-plan/design-prompt.md 或 design-system/MASTER.md 列为输入
- **AND** 输入源缺失 SHALL 标记为 🔴 阻塞
- **AND** 若 functional-designs/index.md 缺少 FP 类型列，SHALL 标记 🟡 警告（旧版文档兼容）

#### Scenario: D3.2 后端子变更输出越界检查

- **WHEN** D3.2 对后端子变更执行越界检测
- **THEN** 系统 SHALL grep 检测子变更源码目录中：
  - `.tsx`、`.jsx`、`.vue`、`.svelte` 文件 → 🟡 警告
  - 硬编码颜色值（`#[0-9a-fA-F]{3,6}` 或 `rgb(` 模式 ≥ 5 次）→ 🔵 建议
  - `docs/designs/prototypes/` 路径引用 → 🟡 警告
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
