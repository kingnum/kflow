---
name: kflow-verify
version: 0.16.0
description: Use when user needs artifact diagnosis/诊断、验证产物、检查产物、产物完整性、输入源检查、verify, or before archive to check all artifacts. 独立诊断 Skill（非流程阶段），七维度全阶段产物诊断、严重度分级（🔴阻塞/🟡警告/🔵建议）、修复路由到对应阶段 REVISION 模式。可随时手动调用 + 归档前自动触发。不写入 .status.md 阶段状态表。
license: MIT
triggers:
  - 诊断
  - 验证产物
  - 检查产物
  - 产物完整性
  - 输入源检查
  - verify
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - AskUserQuestion
---

# 角色

产物诊断器（独立工具，非流程阶段）。对变更执行七维度全阶段产物诊断，输出诊断报告和修复路由建议。不修改 .status.md，不阻塞阶段流转。

# 任务

读取 .status.md 和变更产物 → 执行七维度诊断（D1-D7）→ 严重度分级 → 生成诊断报告 → AskUserQuestion 询问修复策略 → 根据用户选择执行修复路由。

# 触发时机

| 触发方式 | 说明 |
|---------|------|
| 手动调用 | 用户直接调用 `/kflow-verify {change-name}` |
| kflow-guide 路由 | guide 识别诊断/验证/verify 等关键词后路由到此 |
| 归档前自动触发 | integration-test 完成后自动触发 |

# 七维度诊断

## D1 产物存在性检查

对 .status.md 中标记为「✅ 完成」的每个阶段，检查其关键产物文件是否存在。

| 阶段 | 关键产物 | 条件 |
|------|---------|------|
| 设计探索 | functional-designs/index.md, CONTEXT.md | — |
| 原型设计 | prototype/index.md | 前后端项目 + 未跳过 |
| 详细设计 | detailed-design.md, api-tests/index.md, traceability.md | e2e-tests/ 仅前后端 |
| 计划 | subchanges/*/tasks.md | — |
| 编码 | (代码变更) | — |
| 代码审查 | test-reports/review/code-review.md | — |
| 接口单元测试 | test-reports/api/summary.md | — |
| E2E测试 | test-reports/e2e/summary.md | 仅前后端 |
| 集成测试 | test-reports/integration/summary.md | — |

- 缺失的必须产物 → 🔴 阻塞
- 条件产物基于上下文缺失 → 🔴 阻塞
- 条件产物基于上下文不适用 → 跳过

## D2 产物内容完整性检查

- 产物文件非空
- 无占位符（TODO/TBD/{待填写}/...等）
- 必填章节存在（functional-designs/index.md 版本号和修订记录、detailed-design.md NFR 章节）

- 文件为空 → 🔴 阻塞
- 发现占位符 → 🟡 警告
- 必填章节缺失 → 🟡 警告

## D3 输入源正确性检查

对每个子变更判定类型（后端/前端），按类型检查输入源。

**后端子变更 SHALL 检查**：
- functional-designs/、detailed-design.md、api-tests/、CONTEXT.md、tasks.md

**前端子变更 SHALL 检查**：
- prototype/index.md、detailed-design.md
- SHALL NOT 将 prototype/design-prompt.md 或 design-system/MASTER.md 列为输入

- 输入源缺失 → 🔴 阻塞
- 前端子变更引用了过程产物 → 🟡 警告

## D4 交叉引用一致性检查

- traceability.md FP 清单与 functional-designs/index.md 一致
- detailed-design.md 中的 FP 引用与 functional-designs/ 一致
- api-tests/ 接口数与 detailed-design.md §接口设计 匹配
- element-coverage-tree.md 🎯 状态节点的 TC-ID 覆盖率

- 不一致 → 🟡 警告

## D5 设计决策完整性检查

- 是否存在 HITL 标记的子变更 → 🟡 警告
- detailed-design.md 中是否有「待定」「TBD」等 → 🟡 警告
- ADR 是否有已过期记录 → 🔵 建议

## D6 门控合规性检查

- .status.md 阶段顺序是否正确（无跳阶段）→ 🔴 阻塞
- 前置阶段状态是否为 ✅ 完成 → 🔴 阻塞
- 回退后后续阶段是否已正确重置 → 🔴 阻塞

## D7 审查闭环检查

- cross-reviews/ 最新批次 synthesis.md 所有高/中严重度问题已关闭 → 🔴 阻塞
- 代码审查高严重度问题已修复 → 🔴 阻塞
- traceability.md 设计阶段列覆盖率 = 100% → 🔴 阻塞

# 严重度分级

| 严重度 | 编号前缀 | 含义 | 建议处理 |
|--------|---------|------|---------|
| 🔴 阻塞 | B- | 必须产物缺失、阶段跳转、输入源严重缺漏、审查问题未关闭 | 进入下一阶段前修复 |
| 🟡 警告 | W- | 内容不完整（含占位符）、交叉引用不一致、覆盖率不足、HITL 未决议 | 合适时机修复 |
| 🔵 建议 | S- | 文档格式不规范、版本号滞后、ADR 过期 | 不阻塞流程 |

# 修复路由

| 问题归属阶段 | 路由格式 |
|-------------|---------|
| explore / prototype-design / design | `→ kflow-{phase} REVISION` |
| plan / code / code-review / api-test / e2e-test / integration-test | `→ kflow-{phase} (重新执行)` |

# 执行流程

```
1. LOAD    → 读取 .status.md，确认变更信息（项目类型、子变更列表、阶段状态）
2. D1      → 产物存在性检查（逐个阶段检查关键产物文件）
3. D2      → 产物内容完整性检查（读取产物文件，检查非空/占位符/必填章节）
4. D3      → 输入源正确性检查（按子变更类型检查输入源）
5. D4      → 交叉引用一致性检查（验证跨文档引用）
6. D5      → 设计决策完整性检查（检查 HITL 标记、未决决策、ADR 过期）
7. D6      → 门控合规性检查（检查阶段顺序和状态一致性）
8. D7      → 审查闭环检查（检查审查问题关闭状态和覆盖率）
9. REPORT  → 汇总诊断结果，按严重度分级输出，写入 verify-report.md
10. ASK    → AskUserQuestion 询问修复策略：
    ├── 确认全部修复
    ├── 仅修复阻塞项
    └── 暂不修复
11. ROUTE  → 根据用户选择，按修复路由执行修复（不自动执行）
```

# 约束

- SHALL NOT 修改 .status.md 的阶段状态
- SHALL NOT 写入 traceability.md
- SHALL NOT 自动执行修复（修复由用户决策驱动）
- SHALL NOT 阻塞阶段流转
- 诊断报告写入 `docs/changes/{change}/verify-report.md`

# 输出格式

诊断报告模板参考 `docs/designs/templates/changes/{change}/verify-report.md`。

问题条目格式：
```markdown
### 🔴 B-001: {问题简述}

| 属性 | 值 |
|------|-----|
| **维度** | D1 产物存在性 |
| **阶段** | plan |
| **描述** | CONTEXT.md 文件缺失 |
| **影响** | plan 阶段无法对齐领域词汇表进行任务描述 |
| **修复路由** | → kflow-explore REVISION（构建 CONTEXT.md） |
| **关联GAP** | GAP-1 |
```

# 与其他 Skill 的关系

- **独立 Skill**：非流程阶段，可随时调用
- **与 kflow-audit 互补**：verify 诊断问题+路由，audit 门控+评分
- **与 kflow-guide 集成**：通过 guide 路由入口触发
