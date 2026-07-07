# kflow-verify（产物诊断阶段）

> **版本**: 参见仓库根目录 `VERSION` 文件
> **类型**: 独立诊断 Skill（非流程阶段）
> **创建时间**: 2026-06-03

---

## 基本信息

```yaml
name: kflow-verify
description: 产物诊断 - 七维度全阶段产物诊断、严重度分级、修复路由到对应阶段 REVISION 模式。独立诊断 Skill（非流程阶段），可随时手动调用 + 归档前自动触发。不写入 .status.md 阶段状态表。
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
```

---

## 定位

kflow-verify 是独立诊断 Skill，非流程阶段。触发时机：手动调用 + 归档前自动触发（integration-test 通过后）。不阻塞阶段流转（诊断报告是信息输出，修复由用户决策驱动）。

### 与 kflow-audit 的关系

```
kflow-verify (独立诊断)               kflow-audit (流程阶段)
├── 全阶段产物诊断                       ├── 归档门控
├── 输入源完整性检查                     ├── 七维度评分
├── 交叉引用一致性                       ├── 效率统计
├── 修复路由建议                         └── 阻断归档
└── 不影响 .status.md
```

---

## 输入要求

| 产物 | 图例 | 说明 |
|------|------|------|
| .status.md | ✅ 必须 | 变更级状态文件，获取阶段完成状态 |
| 变更目录（docs/changes/{change}/） | ✅ 必须 | 变更的完整产物目录 |

---

## 输出产物

| 产物 | 文件 | 图例 | 说明 |
|------|------|------|------|
| 诊断报告 | docs/changes/{change}/verify-report.md | ✅ 必须 | 七维度诊断结果、严重度分级、修复路由 |

---

## 执行流程

```
诊断流程:

┌─────────────────────────────────────────────────────────────┐
│                    VERIFY WORKFLOW                           │
├─────────────────────────────────────────────────────────────┤
│  1. LOAD      → 读取 .status.md，确认变更信息                │
│  2. D1        → 产物存在性检查                               │
│  3. D2        → 产物内容完整性检查                           │
│  4. D3        → 输入源正确性检查                             │
│  5. D4        → 交叉引用一致性检查                           │
│  6. D5        → 设计决策完整性检查                           │
│  7. D6        → 门控合规性检查                               │
│  8. D7        → 审查闭环检查                                 │
│  9. REPORT    → 生成诊断报告到 verify-report.md              │
│  10. ASK      → AskUserQuestion 询问修复策略                 │
│      ├── 确认全部修复 → 按路由逐一修复                       │
│      ├── 仅修复阻塞项 → 修复 🔴 阻塞级问题                   │
│      └── 暂不修复 → 报告保留，用户自行处理                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 七维度诊断体系

### D1 产物存在性检查

对 .status.md 中标记为「✅ 完成」的每个阶段，检查其关键产物文件是否存在。条件产物（🔶）根据项目类型和子变更类型判定是否缺失。

- 缺失的必须产物 → 🔴 阻塞
- 条件产物基于上下文缺失 → 🔴 阻塞
- 条件产物基于上下文不适用 → 跳过

### D2 产物内容完整性检查

检查每个产物文件是否非空、是否无占位符（TODO/TBD/{待填写}/...等）、必填章节是否存在。

- 文件为空 → 🔴 阻塞
- 发现占位符 → 🟡 警告
- 必填章节缺失 → 🟡 警告

### D3 输入源正确性检查

对每个子变更判定其类型（后端/前端），按类型检查输入源。

后端子变更 SHALL 检查：
- functional-designs/、detailed-design.md、api-tests/、CONTEXT.md、tasks.md 可访问性

前端子变更 SHALL 检查：
- prototype/index.md（含 entry 角色文件）、detailed-design.md 可访问性
- SHALL NOT 将 prototype/design-prompt.md 或 design-system/MASTER.md 列为输入

- 输入源缺失 → 🔴 阻塞
- 前端子变更引用了过程产物（design-prompt.md、design-system/*）→ 🟡 警告

### D4 交叉引用一致性检查

验证跨文档引用的一致性。

- traceability.md 中 FP 清单与 functional-designs/index.md 一致
- detailed-design.md 中的 FP 引用与 functional-designs/ 一致
- api-tests/ 接口数与 detailed-design.md §接口设计 匹配
- element-coverage-tree.md 🎯 状态节点的 TC-ID 覆盖率与 traceability.md E2E测试列一致

- 不一致 → 🟡 警告

### D5 设计决策完整性检查

检查是否存在未决设计决策。

- 是否存在 HITL 标记的子变更 → 🟡 警告（说明设计不完整）
- detailed-design.md 中是否有「待定」「TBD」等未决决策 → 🟡 警告
- ADR 是否有已过期的记录 → 🔵 建议

### D6 门控合规性检查

检查阶段流转是否符合规则。

- .status.md 阶段顺序是否正确（无跳阶段）→ 🔴 阻塞
- 前置阶段状态是否为 ✅ 完成 → 🔴 阻塞
- 回退后后续阶段是否已正确重置为 ⏳ 待开始 → 🔴 阻塞

### D7 审查闭环检查

检查审查问题是否已关闭。

- cross-reviews/ 最新批次 synthesis.md 中所有高/中严重度问题是否已关闭 → 🔴 阻塞
- 代码审查（test-reports/review/code-review.md）中高严重度问题是否已修复 → 🔴 阻塞
- traceability.md 各列覆盖率是否达标（设计阶段列 = 100%）→ 🔴 阻塞

---

## 严重度分级

| 严重度 | 编号前缀 | 判定标准 | 建议处理 |
|--------|---------|---------|---------|
| 🔴 阻塞 | B- | 必须产物缺失、阶段跳转、输入源严重缺漏、审查问题未关闭 | 进入下一阶段前修复 |
| 🟡 警告 | W- | 内容不完整（含占位符）、交叉引用不一致、覆盖率不足、HITL 未决议 | 合适时机修复 |
| 🔵 建议 | S- | 文档格式不规范、版本号滞后、ADR 过期 | 不阻塞流程，可自行决定 |

---

## 修复路由

### 设计阶段问题路由

诊断问题归属于 explore/prototype-design/design 阶段时，修复路由指向对应 Skill 的 REVISION 模式：

- `→ kflow-explore REVISION`
- `→ kflow-prototype-design REVISION`
- `→ kflow-design REVISION`

### 执行阶段问题路由

诊断问题归属于 plan/code/code-review/api-test/e2e-test/integration-test 阶段时，修复路由指向对应 Skill 的重新执行：

- `→ kflow-plan (重新执行)`
- `→ kflow-code (重新执行)`
- `→ kflow-code-review (重新执行)`
- `→ kflow-api-test (重新执行)`
- `→ kflow-e2e-test (重新执行)`
- `→ kflow-integration-test (重新执行)`

### 修复策略选择

诊断报告输出后，SHALL 使用 AskUserQuestion 询问用户：「诊断报告已生成。是否按修复路由执行修复？」

选项：
1. 确认全部修复
2. 仅修复阻塞项
3. 暂不修复

SHALL NOT 自动执行修复，修复由用户决策驱动。

---

## 诊断报告格式

诊断报告输出到 `docs/changes/{change}/verify-report.md`，包含：

1. 生成时间
2. 诊断范围（变更名、子变更列表）
3. 问题总览表（按严重度统计：🔴阻塞 / 🟡警告 / 🔵建议 各数量）
4. 分级问题清单（每条问题含编号、维度、阶段、描述、影响说明、修复路由、关联GAP）
5. 修复路由建议汇总

### 问题条目格式

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

---

## 触发时机

| 触发方式 | 说明 |
|---------|------|
| 手动调用 | 用户直接调用 `/kflow-verify {change-name}` |
| 归档前自动触发 | kflow-integration-test 完成后，变更下存在至少一个子变更时自动触发 |

---

## 约束

- SHALL NOT 修改 .status.md 的阶段状态
- SHALL NOT 写入 traceability.md
- SHALL NOT 自动执行修复
- SHALL NOT 阻塞阶段流转

---

## 与其他 Skill 的关系

- **独立 Skill**：非流程阶段，可随时调用
- **与 kflow-audit 互补**：verify 是诊断工具（发现问题+路由），audit 是流程阶段（门控+评分）
- **与 kflow-guide 集成**：通过 guide 路由入口触发

---

## 反馈机制

如果在使用本 Skill 过程中发现问题或有优化建议，请记录到 `docs/skill-suggestion.md` 文件中。
