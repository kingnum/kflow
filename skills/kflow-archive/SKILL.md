---
name: kflow-archive
version: 0.16.0
description: Use when user needs to archive a change/归档、完成、变更结束, or all stages and integration tests are complete with audit passed. 变更归档——集成测试门控、审计门控、设计合并（functional-designs + technical-designs/6文件体系）、索引更新、询问是否 git commit。必须阶段，变更级。含 PRE_HOOK/POST_HOOK 阶段钩子引用（不需要服务，RELOAD: 全量产物, .status.md）。
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
---

# 角色

变更归档执行器。在所有阶段完成后将变更整体归档，执行设计知识沉淀（合并到产品级文档），更新索引文件，询问用户是否 git commit。归档后变更进入只读保护状态，禁止任何修改操作。

# 任务

门控检查（集成测试 + 审计门控 + 所有子变更阶段完成）→ 用户确认归档 → 设计合并到产品级（EXTRACT → MATCH → MERGE → ANNOTATE → CONFLICT → CHANGELOG → SUMMARY）→ 功能模块摘要更新 → ADR 索引更新检查 → 移动变更目录到 archive/ → 更新状态文件和索引 → 输出归档完成信息 → 分析归档内容 → 询问是否 git commit。

# 门控检查

进入归档阶段前检查：
- 主变更 `.status.md` 存在
- 主变更 `.status.md` 中所有阶段标记完成（✅ 完成 或 ⏭️ 跳过）
- 所有子变更各阶段完成检查（计划、编码、接口单元测试、E2E测试）
- 集成测试通过检查（`test-reports/integration/summary.md` 存在且标记"集成测试通过"）
- **审计门控通过**（kflow-audit 七维度评估通过，无阻塞/严重问题）
- **用户验收确认通过**（`.status.md` 中「用户验收确认」状态 = ✅ 已确认 或 ⏭️ 用户跳过）

# 输入要求

| 产物 | 图例 | 说明 |
|------|------|------|
| 变更名称 | ✅ 必须 | 要归档的变更 |
| 用户确认 | ✅ 必须 | 确认归档操作 |
| test-reports/integration/summary.md | ✅ 必须 | 集成测试通过证明 |
| 审计报告 | ✅ 必须 | kflow-audit 审计通过证明 |
| functional-designs/ | ✅ 必须 | 功能设计（用于设计合并） |
| detailed-design.md | ✅ 必须 | 详细设计（用于设计合并） |

# 输出产物

| 产物 | 文件 | 图例 | 内容要求 |
|------|------|------|---------|
| 归档变更目录 | `docs/archive/{YYYY-MM-DD}-{change}/` | ✅ 必须 | 变更整体移动 |
| 状态文件更新 | `docs/archive/{change}/.status.md` | ✅ 必须 | 添加归档记录 |
| 索引文件更新 | `docs/changes/index.md` | ✅ 必须 | 活跃列表移除，归档列表添加 |
| 产品级功能设计文档（合并） | `docs/designs/functional-designs/{menu}/index.md` + `{menu}/part-NN.md`（前后端）或 `{domain}.md`（纯后端） | ✅ 必须 | 设计合并后的产品级功能设计，按 FP-ID 追加/替换，更新 index.md 分册总览 |
| 技术设计全景文档更新 | `docs/designs/technical-designs/{architecture,data-model,api-catalog,nfr-baseline,config-items,error-handling}.md` | 🔶 条件 | 涉及跨模块变更时按类型分散更新至 6 文件 |
| 变更日志更新 | `docs/designs/changelog.md` | 🔶 条件 | 新增功能模块或结构变更时更新 |
| 功能模块摘要更新 | `docs/designs/functional-designs/module-summary.md` | ✅ 必须 | 设计合并后更新模块摘要（模块名+核心功能+FP-ID范围+文档位置） |

# 执行流程

```
归档阶段流程:

┌─────────────────────────────────────────────────────────────┐
│                    ARCHIVE WORKFLOW                          │
├─────────────────────────────────────────────────────────────┤
│  1. PRE_HOOK  → 引用 skills/kflow-archive/references/hooks.md archive 阶段 PRE_HOOK │
│  2. CHECK     → 门控检查（含集成测试+审计门控+所有子变更阶段） │
│  3. ACCEPTANCE→ 用户验收确认（如未确认）                      │
│  │   ├── 检查 .status.md 用户验收确认状态                     │
│  │   ├── 已确认/已跳过 → 进入 CONFIRM                          │
│  │   └── 未确认 → 启动服务 + AskUserQuestion 用户验收        │
│  4. CONFIRM   → 用户确认归档                                 │
│  │   ├── 已完成变更 → 确认归档                               │
│  │   └── 未完成变更 → 询问归档原因，记录                     │
│  5. MERGE     → 执行设计合并到产品级                          │
│  │   ├── EXTRACT: 提取 functional-designs/ 功能设计            │
│  │   ├── EXTRACT: 提取 detailed-design.md 技术设计            │
│  │   ├── MATCH: 匹配合并目标 functional-designs/{module}.md   │
│  │   │   ├── 检测目标文档是否含「由 AI 逆向分析生成」草稿标记  │
│  │   │   └── 含草稿标记 → 首次合并，替换为正式来源标注         │
│  │   ├── MERGE: 按功能模块合并功能设计（按 FP-ID 追加/替换）   │
│  │   ├── MERGE: 按类型更新 technical-designs/*.md             │
│  │   ├── ANNOTATE: 标注来源变更和归档时间                     │
│  │   ├── CONFLICT: 检测冲突，默认替换更新，结构性冲突人工裁决  │
│  │   └── CHANGELOG: 更新 docs/designs/changelog.md           │
│  5.5 ADR     → ADR 索引更新检查（如有新增 ADR）               │
│  │   ├── 检查 docs/adr/ 目录是否有新创建的 ADR                  │
│  │   └── 有新增 → 更新 docs/adr/index.md（如有遗漏）            │
│  5.6 SUMMARY → 更新功能模块摘要                                │
│  │   ├── 扫描合并后的 functional-designs/ 目录                  │
│  │   ├── 按模块生成 2-3 行摘要（模块名+核心功能+FP-ID范围+位置）│
│  │   └── 更新 docs/designs/functional-designs/module-summary.md │
│  6. MOVE      → 移动变更目录到 archive/                      │
│  │   └── docs/changes/{change}/ →                            │
│  │       docs/archive/{YYYY-MM-DD}-{change}/                 │
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
│ 12. POST_HOOK → 引用 skills/kflow-archive/references/hooks.md archive 阶段 POST_HOOK │
└─────────────────────────────────────────────────────────────┘
```

## 步骤 1：PRE_HOOK — 阶段前置钩子

引用 `skills/kflow-archive/references/hooks.md` archive 阶段 PRE_HOOK（❌ 不需要服务：CHECK_STATE + RELOAD）。

> RELOAD: 重读全量产物, .status.md。

---

# 用户验收确认

> **来源**: skill-execution-reliability 变更。集成测试+审计通过后，归档前增加用户最终验收确认环节。这是变更交付前的最后一道人工验证门控。

## 触发时机

归档流程 CHECK 步骤完成后，检查 `.status.md` 中「用户验收确认」状态：

| 状态 | 处理 |
|------|------|
| ✅ 已确认 | 跳过验收，进入 CONFIRM 步骤 |
| ⏭️ 用户跳过 | 跳过验收，进入 CONFIRM 步骤 |
| 无记录/未确认 | 执行用户验收流程 |

## 服务启动

发起用户验收确认前，按 `docs/service-guide.md` 启动服务：

```
1. 读取 docs/service-guide.md 获取服务启动命令和端口
2. 执行服务启动命令（后端 + 前端，如适用）
3. 健康检查: curl localhost:{port}/health 或 curl localhost:{port}
4. 服务就绪 → 进入 AskUserQuestion
5. 服务启动失败 → 提示用户手动排查
```

### AskUserQuestion 用户验收

```
Question: "变更已完成集成测试和审计，请验收确认：
  - 变更名称: {change-name}
  - 功能点: {数量} 个
  - 集成测试: ✅ 通过
  - 审计: ✅ 通过
  请在实际环境中访问并验证功能是否符合预期。"

Options:
  - "确认通过，可以归档" → 标记用户验收为「✅ 已确认」→ 进入归档阶段
  - "还有问题，需要修复" → 收集用户描述的具体问题 → 创建缺陷记录 → 路由到 kflow-bug-fix → 修复后重新执行测试→审计→用户验收循环
  - "跳过确认，直接归档" → 标记用户验收为「⏭️ 用户跳过」→ 进入归档阶段
```

> **注意**：用户验收不通过时记录的是功能缺陷，不是 Skill 执行问题，SHALL NOT 记录到 skill-suggestion.md。

## 状态写入

验收完成后在 `.status.md` 中写入：
```markdown
| 用户验收确认 | ✅ 已确认 / ⏭️ 用户跳过 | {YYYY-MM-DD HH:MM} | 验收备注 |
```

---

# 设计合并流程

> **核心机制**：归档时不仅移动文件，还将设计知识沉淀到产品级文档。

```
设计合并详细流程:

1. EXTRACT（提取）:
   ├── 从 functional-designs/ 提取功能描述、需求分析、功能点清单
   └── 从 detailed-design.md 提取技术设计、数据模型、接口设计、NFR、配置项、错误处理

2. MATCH（匹配）:
   ├── 按功能点的「所属页面与菜单」信息定位目标模块
   ├── 前后端项目: 按一级菜单匹配 docs/designs/functional-designs/{menu}/
   │   ├── 目录已存在 → 按 FP-ID 匹配 part-NN.md（已存在则替换，不存在则追加）
   │   └── 目录不存在 → 新建 index.md + part-01.md
   ├── 纯后端项目: 按设计域匹配 docs/designs/functional-designs/{domain}.md
   │   ├── 文件已存在 → 按 FP-ID 合并更新
   │   └── 文件不存在 → 新建（使用 backend-domain.md 模板）
   ├── 检测目标文件/目录是否含「由 AI 逆向分析生成」草稿标记 → 首次合并去草稿
   └── 模块归属模糊 → AskUserQuestion 确认模块归属

3. MERGE（合并）:
   ├── 功能设计 → functional-designs/{menu}/part-NN.md 或 {domain}.md 对应章节（按 FP-ID 匹配）
   ├── 更新目标目录的 index.md 分册总览
   ├── 技术设计 → technical-designs/*.md（按类型分散更新，含 config-items.md、error-handling.md）
   ├── NFR 变更 → 更新 docs/designs/technical-designs/nfr-baseline.md（如有变化）
   ├── 数据模型变更 → 更新 docs/designs/technical-designs/data-model.md（如有新增实体）
   ├── API 变更 → 更新 docs/designs/technical-designs/api-catalog.md（如有新增/修改接口）
   ├── 架构变更 → 更新 docs/designs/technical-designs/architecture.md（如有架构调整）
   ├── 配置项变更 → 更新 docs/designs/technical-designs/config-items.md
   ├── 错误处理变更 → 更新 docs/designs/technical-designs/error-handling.md
   └── 首次合并 → 替换草稿标记为正式来源标注

4. ANNOTATE（溯源标注）:
   └── 每合并章节标注:
       > 来源变更: {change-name} | 归档时间: {YYYY-MM-DD}
       > 原始文件: docs/archive/{YYYY-MM-DD}-{change}/

5. CONFLICT（冲突处理）:
   ├── 默认策略: 替换更新（新设计覆盖旧设计）
   ├── 保留旧版本链接: docs/archive/{YYYY-MM-DD}-{change}/
   └── 结构性冲突: AskUserQuestion 提示人工裁决

6. CHANGELOG（更新变更日志）:
   └── docs/designs/changelog.md 追加本次合并记录

7. SUMMARY（更新功能模块摘要）:
   ├── 文件不存在 → 首次创建，全量扫描 functional-designs/ 生成摘要
   ├── 文件已存在 → 增量更新本次涉及的模块摘要
   ├── 格式: 模块名 | 核心功能（2-3 项）| FP-ID 范围 | 文档位置
   └── 更新 docs/designs/functional-designs/module-summary.md

注意: 原型设计 (.html 文件) 不合并到产品级，保留在变更级归档目录中。
```

---

# 归档条件

```markdown
归档前检查:
- [ ] 主变更 .status.md 中所有阶段标记完成（✅ 完成 或 ⏭️ 跳过）
- [ ] 所有子变更各阶段（计划、编码、接口单元测试、E2E测试）完成
- [ ] 前后端项目：所有子变更 E2E测试和接口单元测试通过
- [ ] 纯后端项目：所有子变更接口单元测试通过
- [ ] 集成测试通过（test-reports/integration/summary.md 存在且标记"集成测试通过"）
- [ ] 审计门控通过（kflow-audit 七维度评估，无阻塞/严重问题）
- [ ] ADR 索引已更新（如有新增 ADR，docs/adr/index.md 已包含本次变更的 ADR）
- [ ] 无遗留的阻碍记录
- [ ] **用户验收确认通过**（.status.md 中「用户验收确认」状态 = ✅ 已确认 或 ⏭️ 用户跳过）
```

---

# 归档后禁止操作

已归档的变更禁止任何修改操作：

| 禁止操作 | 说明 |
|---------|------|
| 继续已归档变更 | 系统拒绝并提示创建新变更 |
| 修改归档变更文件 | 系统拒绝任何编辑操作 |
| 重新测试归档变更 | 系统拒绝执行测试阶段 |

如需继续相关工作：
- 创建新变更，引用已归档变更的文档
- 在新变更中实现补充功能或修复

---

# 未完成变更归档

允许归档未完成的变更，但需记录原因：

```markdown
## 归档记录

- **归档时间**: {YYYY-MM-DD HH:MM}
- **归档状态**: 未完成
- **归档原因**: {用户提供的归档原因}
- **完成进度**: {完成的阶段和进度}
```

---

# 归档后 git commit

## 触发时机

在归档流程的 COMPLETE 步骤之后（第 10-11 步 ANALYZE → COMMIT）。

## 执行流程

```
归档后 commit 流程:

1. ANALYZE   → 分析归档内容
   ├── 从归档目录 docs/archive/{YYYY-MM-DD}-{change}/ 读取变更摘要
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

## 失败处理

| 场景 | 处理方式 |
|------|---------|
| git commit 失败（无变更内容） | 提示"无内容需要提交"，不阻塞归档 |
| git commit 失败（git 配置问题） | 提示失败原因，建议手动提交，不影响已完成的归档操作 |
| 用户明确要求不提交 | 跳过 COMMIT 步骤，输出提醒"归档内容尚未提交" |

## 提交信息示例

```
归档变更 add-2fa: 新增双因素认证，更新认证域文档
归档变更 fix-payment-callback: 修复支付回调签名验证异常
归档变更 refactor-user-module(未完成): 用户模块重构中途归档，已完成60%
```

---

## 步骤 12：POST_HOOK — 阶段后置钩子

引用 `skills/kflow-archive/references/hooks.md` archive 阶段 POST_HOOK（❌ 不需要服务：UPDATE_STATE）。

---

# 索引文件格式

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
| {change-old} | 2026-04-28 | 完成 | docs/archive/2026-04-28-{change-old}/ |
```

---

# 与其他 Skill 的关系

- **输入来自**：`kflow-integration-test`（集成测试通过，变更级）、`kflow-audit`（审计门控通过）
- **前置阶段**：集成测试（`kflow-integration-test`）、审计门控（`kflow-audit`）
- **后续阶段**：无（归档为最终阶段，含设计合并，归档后询问是否 git commit）
- **禁止操作**：归档后禁止返回任何阶段

---

# 自动流转禁止规则

**Archive 是 KFlow 体系中唯一禁止自动流转的阶段。** 审计通过后 MUST 通过 AskUserQuestion 获取用户显式确认后方可进入归档阶段。其他阶段的流转可在门控通过后自动或半自动调度，但归档阶段不得被任何前置阶段自动调度进入。

## 进入归档的唯一方式

```
kflow-audit 完成且审计通过
    │
    ├── 输出审计摘要: 变更名称、子变更完成状态、测试结果摘要、E2E覆盖率、审计结论
    │
    ├── AskUserQuestion: "审计已通过，是否进入归档阶段？"
    │   ├── "确认归档" → 进入 kflow-archive
    │   ├── "暂时不归档" → 保持在 audit 完成状态，等待用户手动调用
    │   └── "需要进一步验证" → 用户手动验证后自行调用 kflow-archive
    │
    └── 禁止:
        ❌ audit 自动调度 archive
        ❌ 任何阶段以"流程完成"为由自动进入 archive
        ❌ 系统根据状态文件自动判定进入 archive
```

# 核心提醒

- **禁止自动进入**：归档阶段 SHALL NOT 被任何前置阶段自动调度进入，MUST 用户显式确认
- **用户验收确认**：集成测试+审计通过后、归档前必须执行用户验收（AskUserQuestion），通过/跳过/不通过三种结果
- **验收不通过时**：路由到 kflow-bug-fix 修复，修复后重新测试→审计→验收循环
- 归档后禁止对变更进行任何修改操作（进入只读保护状态）
- 归档后询问是否 git commit（AskUserQuestion：确认提交/修改提交信息/跳过），提交信息含变更名称和归档日期
- 未完成变更可归档但需记录原因
- 设计合并按项目类型区分：前后端按菜单 → `functional-designs/{menu}/`；纯后端按设计域 → `functional-designs/{domain}.md`
- 原型设计（.html）不合并到产品级文档
- 首次合并时检测并去除「由 AI 逆向分析生成」草稿标记
- 结构性冲突需 AskUserQuestion 人工裁决
- 设计合并后自动更新 `module-summary.md`（模块名+核心功能+FP-ID范围+文档位置），首次全量扫描，后续增量更新
- 提交失败不阻塞归档流程

# 反馈机制

如果在使用本 Skill 过程中发现问题或有优化建议，请记录到 `docs/skill-suggestion.md` 文件中。
