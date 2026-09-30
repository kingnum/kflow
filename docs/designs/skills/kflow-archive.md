# kflow-archive（变更归档阶段）

> **版本**: 参见仓库根目录 `VERSION` 文件（统一版本管理，18 个运行时 Skills 共享版本号）
> **阶段**: 归档（必须阶段，变更级，含设计合并）

---

## 基本信息

```yaml
name: kflow-archive
description: 变更归档阶段 - 将已完成的变更进行归档操作。必须阶段，增加集成测试门控、审计门控和所有子变更各阶段完成检查。归档时执行设计合并：提取功能设计和详细设计合并到产品级文档；原型改动登记到产品级 docs/designs/prototypes/manifest.md（原型已在原型设计阶段直写产品级，归档不做文件级原型合并）。更新状态文件和索引文件。归档后禁止对变更进行任何修改操作。阶段钩子引用 `skills/kflow-archive/references/hooks.md`（不需要服务，RELOAD：全量产物, .status.md）。
license: MIT
triggers:
  - 归档
  - 完成
  - 变更结束
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
```

---

## 门控检查

> **机制说明**：门控规则定义在 [core-mechanisms/04-gates-and-transitions.md](../core-mechanisms/04-gates-and-transitions.md#63-归档条件)

进入归档阶段前检查：
- 主变更 .status.md 存在
- 主变更 .status.md 中所有阶段标记完成（✅ 完成 或 ⏭️ 跳过）
- 所有子变更各阶段完成检查（计划、编码、代码审查、接口单元测试、E2E测试）
- 集成测试通过检查（test-reports/integration/summary.md 存在且标记"集成测试通过"；集成测试阶段被合法裁剪时视为满足，不要求该文件存在，见下方档位适配）
- **裁剪合法性检查**：标记 `⏭️ 不适用` 的阶段均须在变更级 `.status.md` 的「阶段适用性声明」区有对应判定依据（无依据的 `⏭️` SHALL 阻塞归档）
- **审计门控通过**（kflow-audit 七维度评估通过，无阻塞/严重问题）
- **用户验收确认通过**（.status.md 中「用户验收确认」状态 = ✅ 已确认 或 ⏭️ 用户跳过）
- **用户显式确认进入归档**（审计通过后 MUST 通过 AskUserQuestion 获取用户显式确认，Archive 是唯一禁止自动流转的阶段，见 §自动流转禁止规则）

**档位适配**（判定基准为变更级 `.status.md` 的 `变更档位` 字段；字段缺失时按 `完整` 档处理）：

| 门控项 | 档位适配规则 |
|--------|-------------|
| 自审记录存在性 | 变更档位为 `轻量` 时设计自审目标轮次为 0 → 不创建 `self-reviews/{phase}/` 目录、不产生自审报告。此为**合法状态**，SHALL NOT 因自审记录缺失阻塞归档 |
| 审查报告数量 | 变更档位为 `轻量` 时设计审查仅 1 份 `cross-reviews/synthesis.md`（无独立视角报告）、代码审查为单 Agent 单轮（不产生多份视角报告）。此为**合法状态**，SHALL NOT 因报告数量少于完整档阻塞归档 |
| 执行轮次 | 门控按档位基线检查（执行类阶段：轻量 1 / 标准 3 / 完整 10），SHALL NOT 以固定 10 轮判定轻量档或标准档未达轮次 |
| 裁剪阶段 | 某阶段标记 `⏭️ 不适用` 且变更级 `.status.md` 的「阶段适用性声明」区存在对应判定依据时，归档门控 SHALL 视为满足，SHALL NOT 因该阶段无产物而阻塞；无声明依据的 `⏭️` SHALL 阻塞归档，并提示缺失裁剪依据 |
| 条件产物 | 变更档位为 `轻量` 时裁剪掉的产物同属合法状态，按档位适用性声明判定，不判缺项 |

---

## 输入要求

| 产物 | 图例 | 说明 |
|------|------|------|
| 变更名称 | ✅ 必须 | 要归档的变更 |
| 用户确认 | ✅ 必须 | 确认归档操作 |
| test-reports/integration/summary.md | ✅ 必须 | 集成测试通过证明 |
| 审计报告 | ✅ 必须 | kflow-audit 审计通过证明 |
| functional-designs/ | ✅ 必须 | 功能设计（用于设计合并） |
| detailed-design.md | ✅ 必须 | 详细设计（用于设计合并） |

---

## 输出产物

| 产物 | 文件 | 模板 | 图例 | 内容要求 |
|------|------|------|------|---------|
| 归档变更目录 | docs/changes/archive/{YYYY-MM-DD}-{change}/ | N/A（目录移动） | ✅ 必须 | 变更整体移动 |
| 状态文件更新 | docs/changes/archive/{YYYY-MM-DD}-{change}/.status.md | [变更级状态文件](../../templates/changes/{change}/change-status.md) | ✅ 必须 | 添加归档记录 |
| 索引文件更新 | docs/changes/index.md | [变更管理索引](../../templates/changes/{change}/change-index.md) | ✅ 必须 | 活跃列表移除，归档列表添加 |
| 产品级功能设计文档（合并） | docs/designs/functional-designs/{menu}/index.md + {menu}/part-NN.md（前后端）或 {domain}.md（纯后端） | [功能模块目录](../../templates/design-templates/functional-designs/index.md)、[产品级分册](../../templates/design-templates/functional-designs/part-NN.md)、[纯后端简化](../../templates/design-templates/functional-designs/backend-domain.md) | ✅ 必须 | 设计合并后的产品级功能设计，按 FP-ID 追加/替换，更新 index.md 分册总览 |
| 详细设计全景文档更新 | docs/designs/detailed-designs/{architecture,data-model,api-catalog,nfr-baseline,config-items,error-handling}.md | [全景架构](../../templates/design-templates/detailed-designs/architecture.md)、[数据模型](../../templates/design-templates/detailed-designs/data-model.md)、[API目录](../../templates/design-templates/detailed-designs/api-catalog.md)、[NFR基线](../../templates/design-templates/detailed-designs/nfr-baseline.md)、[配置项](../../templates/design-templates/detailed-designs/config-items.md)、[错误处理](../../templates/design-templates/detailed-designs/error-handling.md) | 🔶 条件 | 涉及跨模块变更时按类型分散更新至 6 文件 |
| 变更日志更新 | docs/designs/changelog.md | [变更日志](../../templates/design-templates/changelog.md) | 🔶 条件 | 新增功能模块或结构变更时更新 |
| 功能模块摘要更新 | docs/designs/functional-designs/module-summary.md | [模块摘要](../../templates/design-templates/functional-designs/module-summary.md) | ✅ 必须 | 设计合并后更新模块摘要（模块名+核心功能+FP-ID范围+文档位置） |

---

## 执行流程

```
归档阶段流程:

┌─────────────────────────────────────────────────────────────┐
│                    ARCHIVE WORKFLOW                          │
├─────────────────────────────────────────────────────────────┤
│  1. PRE_HOOK  → 引用 `skills/kflow-archive/references/hooks.md` archive 阶段 PRE_HOOK (轻量) │
│  │   ├── CHECK_STATE → 验证前置阶段状态                       │
│  │   ├── RELOAD → 重读全量产物, .status.md                    │
│  │   └── 不需要服务                                            │
│  2. CHECK     → 门控检查（含集成测试+审计门控+所有子变更阶段） │
│  3. ACCEPTANCE→ 用户验收确认（如未确认）                      │
│  │   ├── 检查 .status.md 用户验收确认状态                     │
│  │   ├── 已确认/已跳过 → 直接进入 CONFIRM                    │
│  │   └── 未确认 → 启动服务 + AskUserQuestion 用户验收        │
│  │       ├── 按 docs/service-guide.md 启动服务               │
│  │       ├── 健康检查通过 → 展示服务地址和测试摘要            │
│  │       ├── 确认通过 → 标记 ✅ 已确认 → CONFIRM              │
│  │       ├── 还有问题 → 收集问题描述 → 路由到 kflow-bug-fix │
│  │       └── 跳过确认 → 标记 ⏭️ 用户跳过 → CONFIRM           │
│  4. CONFIRM   → 用户确认归档                                 │
│  │   ├── 已完成变更 → 确认归档                               │
│  │   └── 未完成变更 → 询问归档原因，记录                     │
│  5. MERGE     → 执行设计合并到产品级                          │
│  │   ├── EXTRACT: 提取 functional-designs/ 功能设计            │
│  │   ├── EXTRACT: 提取 detailed-design.md 详细设计            │
│  │   ├── MATCH: 匹配合并目标 functional-designs/{module}.md   │
│  │   │   ├── 检测目标文档是否含「由 AI 逆向分析生成」草稿标记  │
│  │   │   └── 含草稿标记 → 首次合并，替换为正式来源标注         │
│  │   ├── MERGE: 按功能模块合并功能设计（按 FP-ID 追加/替换）   │
│  │   ├── MERGE: 按类型更新 detailed-designs/*.md             │
│  │   ├── ANNOTATE: 标注来源变更和归档时间                     │
│  │   ├── CONFLICT: 检测冲突，默认替换更新，结构性冲突人工裁决  │
│  │   └── CHANGELOG: 更新 docs/designs/changelog.md           │
│  5.4 REGISTER→ 登记原型改动到产品级 manifest.md               │
│  │   ├── 原型设计阶段为 ⏭️ 跳过 → 跳过本步（不修改 manifest.md）│
│  │   ├── 读取变更级 prototype-changes.md 的改动清单            │
│  │   ├── 更新 docs/designs/prototypes/manifest.md：            │
│  │   │   ├── 受影响产物的「来源变更」列                        │
│  │   │   ├── 清单版本号与「修订记录」追加一条                  │
│  │   │   └── 最后更新时间                                     │
│  │   └── SHALL NOT 复制或覆盖 docs/designs/prototypes/ 下文件  │
│  5.5 ADR     → ADR 索引更新检查（如有新增 ADR）               │
│  │   ├── 检查 docs/adr/ 目录是否有新创建的 ADR                  │
│  │   └── 有新增 → 更新 docs/adr/index.md（如有遗漏）            │
│  5.6 SUMMARY → 更新功能模块摘要                                │
│  │   ├── 扫描合并后的 functional-designs/ 目录                  │
│  │   ├── 按模块生成 2-3 行摘要（模块名+核心功能+FP-ID范围+位置）│
│  │   └── 更新 docs/designs/functional-designs/module-summary.md │
│  6. MOVE      → 移动变更目录到 archive/                      │
│  │   └── docs/changes/{change}/ →                            │
│  │       docs/changes/archive/{YYYY-MM-DD}-{change}/                 │
│  7. UPDATE    → 更新归档变更的状态文件                       │
│  │   └── 添加归档时间、归档状态                               │
│  8. INDEX     → 更新 docs/changes/index.md                   │
│  │   ├── 活跃变更列表移除该变更                               │
│  │   └── 已归档变更列表添加该变更记录                         │
│  9. COMPLETE  → 输出归档完成信息                             │
│ 10. ANALYZE   → 分析归档内容                                  │
│  │   ├── 从归档目录读取变更摘要                                │
│  │   ├── 从 functional-designs/ 提取功能设计关键词             │
│  │   └── 从 detailed-design.md 提取受影响的设计域              │
│ 11. COMMIT    → 询问是否 git commit（AskUserQuestion）        │
│  │   ├── 生成提交信息（`归档变更 {name}: {一行摘要}`）         │
│  │   ├── AskUserQuestion: 确认提交/修改提交信息/跳过           │
│  │   ├── 确认 → git add -A && git commit                      │
│  │   └── 提交失败不阻塞归档流程                               │
│ 12. POST_HOOK → 引用 `skills/kflow-archive/references/hooks.md` archive 阶段 POST_HOOK (轻量) │
│  │   └── UPDATE_STATE → 更新 .status.md（归档完成）            │
└─────────────────────────────────────────────────────────────┘
```

---

## 设计合并流程

> 完整规范参见 `skills/kflow-archive/references/archive-rules.md` §2

归档时不仅移动文件，还将设计知识沉淀到产品级文档。合并流程包含 8 步：提取 → 匹配 → 合并 → 溯源标注 → 冲突处理 → 变更日志 → 模块摘要更新 → 完成。

**审查来源的档位适配**：合并设计时若需引用审查报告作为设计定稿依据，SHALL 按变更档位适配审查来源——完整档为四份视角报告 + `synthesis.md`，标准档为两份视角报告 + `synthesis.md`，轻量档为**单一 `cross-reviews/synthesis.md`（唯一审查来源）**。轻量档无独立视角报告、自审 0 轮（无 `self-reviews/` 目录）均属**合法状态**，SHALL NOT 阻塞设计合并或要求补齐审查产物。

**原型产物的处理**：原型在产品设计阶段已**直写产品级** `docs/designs/prototypes/`，归档时**不再执行文件级原型合并**——同一份内容被搬运两次会重复应用。归档只做**登记**：把变更级 `prototype-changes.md` 记录的改动登记到产品级 `docs/designs/prototypes/manifest.md`（更新受影响产物的来源变更与最后更新时间），`prototype-backup/` 随变更目录进 `archive/` 保留。原型设计阶段为 ⏭️ 跳过时，不修改 `manifest.md`，也不读取该变更的 `prototype-changes.md`。

---

## 自动流转禁止规则

> 完整规范参见 `skills/kflow-archive/references/archive-rules.md` §4

归档阶段 SHALL 是 KFlow 体系中唯一禁止自动流转的阶段。审计通过后 MUST 通过 AskUserQuestion 获取用户显式确认后方可进入归档。设计理由：归档是不可逆操作，涉及设计合并到产品级文档，需用户确认。

---

## 归档条件

> 完整规范参见 `skills/kflow-archive/references/archive-rules.md` §1

归档前检查清单：所有阶段完成、所有子变更各阶段完成、测试通过、审计门控通过、用户验收确认通过、ADR 索引已更新（如有新增）、无遗留阻碍记录、用户确认归档。

**按档位适配**（判定基准为变更级 `.status.md` 的 `变更档位`，缺省按 `完整` 档）：

- **自审记录与审查报告数量**：轻量档零轮自审（无 `self-reviews/` 目录、无自审报告）与设计审查仅 1 份 `synthesis.md`（无独立视角报告）、代码审查单 Agent 单轮（无多份视角报告）均为**合法状态**，SHALL NOT 因这些产物缺失或数量不足阻塞归档，亦 SHALL NOT 将其计入「无遗留阻碍记录」的检查项。
- **阶段轮次**：按目标轮次（档位基线）判定，即「达目标轮次 / 目标轮次」（执行类阶段轻量 1 / 标准 3 / 完整 10），SHALL NOT 要求轻量档或标准档达到完整档的 10 轮。
- **裁剪阶段（接受有声明依据的裁剪）**：某阶段标记 `⏭️ 不适用` 且变更级 `.status.md` 的「阶段适用性声明」区存在对应判定依据时，归档门控 SHALL 视为满足，SHALL NOT 因该阶段无产物而阻塞。具体落点：
  - **集成测试门控**：集成测试阶段被合法裁剪时视为满足，SHALL NOT 要求 `test-reports/integration/summary.md` 存在。
  - **归档前最终覆盖检查**：`traceability.md` 中具有声明依据的 `⏭️ 不适用` 列视为满足，SHALL NOT 参与覆盖率判定、SHALL NOT 产生缺口记录。
  - **覆盖率分母**：裁剪列 SHALL 整列填 `⏭️`，覆盖率 = 已填充格数 / (总格数 - 不适用格数)。
- **无声明依据的 `⏭️`（阻塞）**：某阶段标记 `⏭️ 不适用` 但「阶段适用性声明」区无对应判定依据时，SHALL 阻塞归档，并提示缺失裁剪依据。裁剪仅适用于 `轻量` 档；`标准` 与 `完整` 档的归档条件维持既有规则。
- **条件产物**：轻量档按阶段适用性声明裁剪掉的阶段产物属合法状态，不判缺项。

---

## 归档后禁止操作

> 完整规范参见 `skills/kflow-archive/references/archive-rules.md` §3

已归档的变更禁止继续、修改文件、重新测试。如需继续相关工作应创建新变更。

---

## 未完成变更归档

允许归档未完成的变更，但需记录原因：

```markdown
## 归档记录

- **归档时间**: {YYYY-MM-DD HH:MM}
- **归档状态**: 未完成
- **归档原因**: {用户提供的归档原因}
- **完成进度**: {完成的阶段和进度}
```

---

## 归档后 git commit

### 触发时机

在归档流程的 COMPLETE 步骤之后（第 9-10 步 ANALYZE → COMMIT）。

### 执行流程

```
归档后 commit 流程:

1. ANALYZE   → 分析归档内容
   ├── 从归档目录 docs/changes/archive/{YYYY-MM-DD}-{change}/ 读取变更摘要
   ├── 从 functional-designs/ 提取功能设计关键词
   └── 从 detailed-design.md 提取受影响的设计域

2. SUMMARIZE → 生成提交信息
   ├── 格式: 归档变更 {name}: {一行摘要}
   ├── 已完成变更 → "归档变更 {name}: {核心功能摘要}"
   └── 未完成变更 → "归档变更 {name}(未完成): {归档原因摘要}"

3. COMMIT    → AskUserQuestion 询问
   ├── 展示提交信息预览
   ├── AskUserQuestion: 确认提交/修改提交信息/跳过
   ├── 确认 → git add -A && git commit -m "{提交信息}"
   └── 跳过 → 输出提醒"归档内容尚未提交"

4. VERIFY    → 验证提交成功
   └── git status 确认干净
```

### 失败处理

| 场景 | 处理方式 |
|------|---------|
| git commit 失败（无变更内容） | 提示"无内容需要提交"，不阻塞归档 |
| git commit 失败（git 配置问题） | 提示失败原因，建议手动提交，不影响已完成的归档操作 |
| 用户明确要求不提交 | 跳过 COMMIT 步骤，输出提醒"归档内容尚未提交" |

### 提交信息示例

```
归档变更 add-2fa: 新增双因素认证，更新认证域文档
归档变更 fix-payment-callback: 修复支付回调签名验证异常
归档变更 refactor-user-module(未完成): 用户模块重构中途归档，已完成60%
```

---

## 索引文件格式

`docs/changes/index.md` 格式：

```markdown
# 变更管理索引

> **更新时间**: {YYYY-MM-DD HH:MM}

## 活跃变更

| 变更名称 | 类型 | 项目类型 | 当前阶段 | 影响文件 | 创建时间 |
|----------|------|---------|----------|---------|----------|
| {change-1} | 产品需求 | 前后端项目 | 编码 | src/auth/*, src/order/* | 2026-04-29 |
| {change-2} | 功能需求 | 纯后端项目 | 详细设计 | src/api/* | 2026-04-30 |

## 已归档变更

| 变更名称 | 归档时间 | 归档状态 | 归档目录 |
|----------|----------|----------|----------|
| {change-old} | 2026-04-28 | 完成 | docs/changes/archive/2026-04-28-{change-old}/ |
```

---

## 用户验收确认

> **版本**: 2.1.0 新增

### 触发条件

归档流程 CHECK 步骤完成后，检查 .status.md 中「用户验收确认」状态：
- 状态 = ✅ 已确认 或 ⏭️ 用户跳过 → 直接进入 CONFIRM 步骤
- 状态 = ⏳ 待确认 或未设置 → 进入 ACCEPTANCE 步骤

### 服务启动流程

发起用户验收确认前，按 `docs/service-guide.md` 启动服务：

```
1. 读取 docs/service-guide.md 中的启动命令
2. 启动后端服务（按 service-guide.md 配置）
3. 启动前端服务（前后端项目）
4. 等待服务端口可访问（健康检查：/health + /db-health）
5. 健康检查通过 → 输出服务访问地址（如 http://localhost:{port}）
6. 服务启动失败 → 标记「❌ 阻塞」并提示用户手动启动
```

### AskUserQuestion 用户验收

```
Question: "集成测试和审计已通过。请访问 {服务地址} 验证功能是否符合预期。
测试摘要: {集成测试摘要}
是否确认通过？"
Options:
  - "确认通过，可以归档" → 标记用户验收为「✅ 已确认」→ 进入归档阶段
  - "还有问题，需要修复" → 收集用户描述的具体问题 → 创建缺陷记录 → 路由到 kflow-bug-fix → 修复后重新执行测试→审计→用户验收循环
  - "跳过确认，直接归档" → 标记用户验收为「⏭️ 用户跳过」→ 进入归档阶段
```

注意：用户验收不通过时记录的是功能缺陷，不是 Skill 执行问题，SHALL NOT 记录到 skill-suggestion.md。

---

## 与其他 Skill 的关系

- **输入来自**：`kflow-integration-test`（集成测试通过，变更级）、`kflow-audit`（审计门控通过）
- **前置阶段**：集成测试（`kflow-integration-test`）、审计门控（`kflow-audit`）
- **后续阶段**：无（归档为最终阶段，含设计合并，归档后询问是否 git commit）
- **禁止操作**：归档后禁止返回任何阶段

---

## 反馈机制

如果在使用本 Skill 过程中发现问题或有优化建议，请记录到 `docs/skill-suggestion.md` 文件中。
