# phase-artifact-verification Delta Spec

## MODIFIED Requirements

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

## ADDED Requirements

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
