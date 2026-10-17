---
name: kflow-bug-triage
version: 0.28.0
description: Use when user needs bug triage/问题分诊、反馈、报告问题、报bug、提bug、问题诊断, or user reports an issue through kflow-guide. Independent diagnostic Skill (not a workflow phase). 四层溯源诊断（L1需求→L2原型→L3设计→L4实现）、问题登记（bugs/目录）、路由决策（L1/L2/L3→REVISION模式，L4→缺陷修复快车道）。含 PRE_HOOK/POST_HOOK 阶段钩子引用（不需要服务，RELOAD：全量产物, .status.md, bugs/）。
license: MIT
triggers:
  - 反馈
  - 报告问题
  - 报bug
  - 提bug
  - 问题分诊
  - bug triage
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
---

# 角色

问题分诊台。接收用户反馈后执行四层溯源漏斗（L1 需求定义 → L2 原型设计 → L3 详细设计 → L4 实现执行），将问题登记到 `bugs/` 目录，精确定位问题源头阶段后路由到对应 REVISION 模式（L1/L2/L3）或**缺陷修复快车道**（L4）。独立诊断 Skill，非流程阶段。不执行任何修复。

# 任务

接收用户反馈 -> 问题登记（bugs/ 目录）-> 四层溯源诊断（L1→L2→L3→L4）-> 影响范围评估 -> 输出诊断报告 -> 用户确认路由 -> 执行路由（L1→explore REVISION / L2→prototype-design REVISION / L3→design REVISION / L4→缺陷修复快车道：创建缺陷级状态文件）-> 更新问题状态。

# 门控检查

此 Skill 为独立诊断阶段，门控要求：
- 存在活跃变更（`docs/changes/{change}/` 目录存在且 `.status.md` 可读）
- 用户提供问题描述（自然语言）

# 输入要求

| 产物 | 图例 | 说明 |
|------|------|------|
| .status.md | ✅ 必须 | 变更级状态文件，获取当前变更阶段状态 |
| 变更目录 docs/changes/{change}/ | ✅ 必须 | 获取所有阶段产物用于四层溯源 |
| 用户的问题描述 | ✅ 必须 | 自然语言描述，经 kflow-guide 路由传入 |
| bugs/index.md | 🔶 条件 | 已有问题登记时读取（首次登记时创建） |

# 输出产物

| 产物 | 文件 | 图例 | 内容要求 |
|------|------|------|---------|
| 问题索引 | `docs/changes/{change}/bugs/index.md` | ✅ 必须 | 统计+问题列表+分页表 |
| 问题详情 | `docs/changes/{change}/bugs/bug-NNN-NNN.md` | ✅ 必须 | 四层溯源诊断、影响范围评估（含分数）、解决方案（含 EXECUTION_MODE 声明）、处理状态、修复记录占位节（由 bug-fix 或快车道回写）、快车道入口标记位（L4 结论时） |
| 缺陷级状态文件 | `docs/changes/{change}/bugs/fix/{BUG-ID}/bugfix-status.md` | 🔶 L4 结论时必须 | **仅当诊断结论为 L4 实现执行时创建**。含六个必填区：基本信息、分诊结论、受影响项清单（受影响功能点/接口/测试用例）、修复记录、定向验证、收口结论。创建时 SHALL 一并写入分诊结论与**受影响项清单**，后续由快车道修复与定向验证回写其余区；SHALL NOT 修改变更级 `.status.md` 的阶段状态矩阵字段 |

> **L4 结论的额外输出**: 诊断结论为 L4 时，本 Skill 除问题索引与问题详情外，SHALL 额外创建缺陷级状态文件 `bugfix-status.md` 并写入受影响项清单——该清单是快车道定向验证的唯一验证范围依据，SHALL NOT 由修复者自行圈定。文件结构与隔离规则参见 `docs/designs/core-mechanisms/03-status-and-tasks.md` §3.5，机制定义参见 `bugfix-fast-lane` 能力。

## 状态双写规则

阶段完成、回退与重执行时，主 Agent SHALL 同时执行两处写入：

1. **追加历史**：向 `docs/changes/{change}/status-log.md` 追加本次事件——阶段名、轮次、完成时间、耗时、终止结果；回退时另记回退原因与目标阶段
2. **刷新当前**：刷新变更级 `.status.md` 的当前状态字段——当前阶段、阶段状态表对应行、执行轮次、终止结果、未决事项

`.status.md` SHALL 保持在 100 行以内，超出部分改为写入 `status-log.md`。变更目录中不存在 `status-log.md`（历史变更未分层）时按既有单文件口径处理，SHALL NOT 强制回填。

> 读取边界：常规阶段推进与门控判定 SHALL 仅读取 `.status.md`；`status-log.md` 仅在中断恢复与审计场景读取。权威定义见 `status-file-layering` 能力。

# 执行流程

```
问题分诊流程:

┌─────────────────────────────────────────────────────────────┐
│                    TRIAGE WORKFLOW                            │
├─────────────────────────────────────────────────────────────┤
│  1. PRE_HOOK  → 引用 skills/kflow-bug-triage/references/hooks.md bug-triage 阶段 PRE_HOOK │
│  │   ├── CHECK_STATE → 验证活跃变更存在                       │
│  │   └── RELOAD → 重读 .status.md, 全量产物, bugs/            │
│  2. REGISTER  → 问题登记                                     │
│  │   ├── 分配 BUG-ID（递增编号）                              │
│  │   ├── 评估严重度（🔴阻塞/🟡警告/🔵建议）                  │
│  │   ├── 创建/更新 bugs/index.md                             │
│  │   └── 创建/更新 bugs/bug-NNN-NNN.md 基本信息节             │
│  3. DIAGNOSE  → 四层溯源诊断                                  │
│  │   ├── L1 需求定义 → 检查 functional-designs/              │
│  │   ├── L2 原型设计 → 检查 docs/designs/prototypes/         │
│  │   ├── L3 详细设计 → 检查 detailed-design.md               │
│  │   └── L4 实现执行 → 检查代码实现                           │
│  │   └── 某层判定 ❌ → 停止向下排查，确定为源头               │
│  3.5 IMPACT   → 影响范围评估                                  │
│  │   ├── 识别受影响功能点（交叉引用 functional-designs/）     │
│  │   ├── 识别受影响接口（检查 detailed-design.md）            │
│  │   ├── 识别受影响测试用例（交叉引用 api-tests/、e2e-tests/）│
│  │   ├── 识别数据模型变更                                     │
│  │   └── 计算影响范围分数（FP×1 + 接口×1.5 + 数据模型×2）    │
│  4. REPORT    → 填写诊断结果到问题详情                        │
│  │   ├── 四层路径表（每层结论+证据）                          │
│  │   ├── 问题源头层级和判断依据                               │
│  │   └── 建议路由目标和解决方案                               │
│  5. CONFIRM   → 用户确认路由                                  │
│  │   ├── AskUserQuestion 展示诊断结论                         │
│  │   │   ├── 选项 1: 确认执行路由                             │
│  │   │   ├── 选项 2: 覆盖诊断结论（指定源头层级）             │
│  │   │   └── 选项 3: 暂不处理                                 │
│  │   └── 用户覆盖时记录覆盖原因到问题详情                     │
│  6. ROUTE     → 执行路由                                      │
│  │   ├── L1 → 回退到 explore REVISION                        │
│  │   ├── L2 → 回退到 prototype-design REVISION               │
│  │   ├── L3 → 回退到 design REVISION                         │
│  │   └── L4 → 进入缺陷修复快车道                              │
│  │       ├── 创建缺陷级状态文件                                │
│  │       │   bugs/fix/{BUG-ID}/bugfix-status.md               │
│  │       ├── 写入受影响项清单（功能点 / 接口 / 测试用例）      │
│  │       ├── 在问题详情文件中标记快车道入口                    │
│  │       └── 路由输出声明快车道入口 → kflow-bug-fix 快车道模式 │
│  │           （SHALL NOT 修改变更级 .status.md 阶段矩阵字段）  │
│  7. UPDATE    → 更新问题状态为「处理中」                      │
│  8. POST_HOOK → 引用 skills/kflow-bug-triage/references/hooks.md bug-triage 阶段 POST_HOOK │
│  │   └── UPDATE_STATE → 更新 .status.md（阶段回退标记）       │
└─────────────────────────────────────────────────────────────┘
```

## 步骤 1：PRE_HOOK — 阶段前置钩子

引用 `skills/kflow-bug-triage/references/hooks.md` bug-triage 阶段 PRE_HOOK（不需要服务，RELOAD：全量产物, .status.md, bugs/）。

---

## 步骤 2：REGISTER — 问题登记硬约束

REGISTER 步骤 SHALL 按以下规则执行：

**必填节清单**（按顺序输出，SHALL NOT 省略任何节）：
1. 基本信息（ID、登记时间、严重度、问题来源）
2. 问题描述（用户原始反馈、问题现象、复现步骤）
3. 诊断结果（四层溯源路径表、问题源头层级、判断依据）
4. 影响范围评估（受影响功能点、受影响接口、数据模型变更、影响范围分数）
5. 解决方案（建议方案、路由目标、影响范围、下游影响、**EXECUTION_MODE = SUBAGENT_REQUIRED**）
6. 处理状态（checkbox 列表；L4 结论时 SHALL 含快车道入口标记位与收口状态字段）
7. 修复记录（占位节，由 bug-fix 或快车道回写）
8. 关联（关联子变更、关联功能点）

**分页规则**：
- SHALL 追加到当前分页文件末尾，SHALL NOT 每次登记创建新文件
- 仅当当前分页文件已满 20 条时，SHALL 创建新分页文件
- BUG-ID 使用纯序号 `BUG-{NNN}`（递增，不含严重度前缀）

---

# 四层溯源诊断

## 诊断顺序

从最上游到下游逐层排查，某层判定为 ❌ 时停止向下排查。

## L1 需求定义

**证据来源**：`functional-designs/index.md` + `functional-designs/part-NN.md` + `CONTEXT.md`

**检查项**：
- 用户反馈的功能是否在 functional-designs/ 中有对应功能点？
- 功能点描述是否覆盖用户期望的行为？
- 是否存在歧义表述或遗漏边界条件？

**快速排除**：功能点完整覆盖且无歧义 → ✅ 通过

## L2 原型设计

**证据来源**：`docs/designs/prototypes/index.html` + 变更级 `prototype-changes.md` + 变更级 `element-coverage-tree.md` + `functional-designs/`

**检查项**：
- 原型是否正确实现了 L1 确认的功能点？（检查范围以变更级 `prototype-changes.md` 界定的本变更涉及页面为准）
- 交互流程是否与用户预期一致？

**快速排除**：纯后端项目（无 `docs/designs/prototypes/`）或用户反馈不涉及 UI/交互 → ✅ 通过（跳过）

## L3 详细设计

**证据来源**：`detailed-design.md` + `api-tests/index.md` + `functional-designs/`

**检查项**：
- 接口定义是否与 functional-designs/ 一致？
- 数据模型是否支持用户描述的数据操作？
- 状态流转是否完整？

**快速排除**：相关接口/数据模型/状态流转与上游一致且完整 → ✅ 通过

## L4 实现执行

**证据来源**：代码实现 + `detailed-design.md`

**检查项**：
- 代码是否正确实现了 detailed-design.md 的定义？
- 边界条件和错误处理是否按设计实现？

**判定**：L1-L3 均通过时，问题默认归因于 L4。

---

# 严重度分级

| 严重度 | 判定标准 | 路由影响 |
|--------|---------|---------|
| 🔴 阻塞 | 功能无法使用或核心流程中断 | 路由立即执行，未关闭阻断归档 |
| 🟡 警告 | 功能可用但存在明显异常 | 正常路由 |
| 🔵 建议 | 非功能性问题 | 正常路由 |

> **说明**：严重度作为独立字段（`🔴 阻塞`/`🟡 警告`/`🔵 建议`），BUG-ID 使用纯序号 `BUG-{NNN}`，不含严重度前缀。

---

# 影响范围评估

四层诊断完成后，SHALL 一并执行影响范围评估，为回退后的受影响项清单与回退判定提供依据。**影响范围分数 SHALL NOT 用于推算轮次**——执行类阶段的轮次由实际执行的重复制循环决定。

## 评估步骤

| 步骤 | 证据来源 | 输出 |
|------|---------|------|
| 识别受影响功能点 | 诊断结论 × functional-designs/ | 受影响功能点清单（如 FP-003, FP-007） |
| 识别受影响接口 | 诊断结论 × detailed-design.md API 定义 | 受影响接口清单（如 /api/orders/export） |
| 识别受影响测试用例 | 诊断结论 × api-tests/、e2e-tests/ 用例定义 | 受影响测试用例标识清单（L4 快车道定向验证的验证范围） |
| 识别数据模型变更 | 诊断证据中的 schema/存储修改 | 数据模型变更描述（none / 描述） |
| 计算影响范围分数 | 公式计算 | 数值 |

## 影响范围分数计算公式

```
影响范围分数 = 功能点数 × 1 + 接口数 × 1.5 + 数据模型变更 × 2
```

- 功能点数：受影响的功能点数量
- 接口数：受影响的 API 端点数量
- 数据模型变更：存在数据模型修改时为 1，否则为 0

## 影响范围分数的用途

影响范围分数 SHALL NOT 映射为重复制轮次——执行类阶段的轮次由实际执行的重复制循环决定（下限 1 轮，无上限）。分数仅用于下游阶段的**受影响项清单**与**回退判定**：

- **受影响项清单**（`Affected Functional Points` + `Affected Interfaces`）SHALL 经 `.status.md`「Recent Revision Info」节传递给目标阶段，供其验证门控的「受影响项 100% 覆盖」使用。
- **L4 快车道的受影响项清单**（受影响功能点 + 受影响接口 + **受影响测试用例**）SHALL 写入缺陷级状态文件 `bugfix-status.md` 的「受影响项清单」区，作为定向验证的**唯一验证范围**。L4 结论下该清单 SHALL NOT 写入变更级 `.status.md`；清单 SHALL NOT 由修复者自行扩大或缩小，修复中发现实际影响面超出清单时判定为**分诊失效**并退回本 Skill 重新评估。
- **影响范围分数本身**作为回退影响范围的记录性信息一并传递，SHALL NOT 用于推算轮次数值。该分数 SHALL NOT 用于 L4 快车道——快车道不进入变更级阶段集合，其验证轮次由定向验证的实际重试次数决定（复用三次修复尝试上限，有界）。
- 本 Skill 仅诊断与路由，不执行修复，SHALL NOT 自行追加审查轮次。

> 执行类阶段的终止模型（自然终止 / 停滞升级、审查范围冻结）的权威定义见 `agent-iteration-execution` 能力；落地表述见被路由 Skill 的 `references/repetition.md` §13（轮间摘要）、§14.3（重复制类阶段循环终止）与 §14.4（终止结果写入）。kflow-bug-triage 亦随附该规范（`skills/kflow-bug-triage/references/repetition.md`）。

---

# 路由决策

| 源头层级 | 路由目标 | 执行动作 | 执行模式 |
|---------|---------|---------|---------|
| L1 需求 | explore REVISION | .status.md explore → ⚠️，后续阶段重置为 ⏳ | EXECUTION_MODE = SUBAGENT_REQUIRED |
| L2 原型 | prototype-design REVISION | .status.md prototype-design → ⚠️，后续阶段重置为 ⏳ | EXECUTION_MODE = SUBAGENT_REQUIRED |
| L3 设计 | design REVISION | .status.md design → ⚠️，后续阶段重置为 ⏳ | EXECUTION_MODE = SUBAGENT_REQUIRED |
| L4 实现 | **缺陷修复快车道** | 创建缺陷级状态文件 `bugs/fix/{BUG-ID}/bugfix-status.md` 并写入受影响项清单，在问题详情中标记快车道入口；**SHALL NOT 修改变更级 `.status.md` 阶段状态矩阵字段**；修复由 `kflow-bug-fix` 的快车道模式承载，出口为定向验证 | EXECUTION_MODE = SUBAGENT_REQUIRED |

> **L4 路由与 L1/L2/L3 的差异**: L1/L2/L3 的路由动作包含「修改变更级 `.status.md`」（标记源头阶段 ⚠️ 需修订、后续阶段重置 ⏳ 待开始）；L4 的路由动作**不含任何变更级状态文件修改**——快车道不进入变更级阶段状态矩阵与门控（参见 `docs/designs/core-mechanisms/03-status-and-tasks.md` §3.5.1）。L1/L2/L3 三条路由的表述与动作均未因本次调整而变化。

---

# 问题登记机制

## bugs/ 目录结构

```
docs/changes/{change}/bugs/
├── index.md              # 问题索引
├── bug-001-020.md        # 第 1 分页（≤20 条）
├── bug-021-040.md        # 第 2 分页
├── fix/                  # 仅 L4 快车道缺陷存在此目录
│   └── {BUG-ID}/
│       ├── bugfix-status.md      # 缺陷级状态文件（快车道生命周期载体）
│       └── verify-report.md      # 定向验证报告（由快车道产出）
└── ...
```

> **`fix/` 目录的创建条件**: 仅当诊断结论为 L4 实现执行、缺陷进入快车道时，由本 Skill 创建 `fix/{BUG-ID}/bugfix-status.md`。L1/L2/L3 路由 SHALL NOT 创建该目录与文件。快速收口后 `bugfix-status.md` SHALL 保留为历史记录，SHALL NOT 随收口删除。

## 问题状态流转

```
待处理 → 处理中 → 已解决 → 已关闭
  └──→ 已挂起（用户选择暂缓）
```

---

# 约束

- SHALL NOT 修改任何代码、测试、设计文档
- SHALL 在诊断完成后获取用户确认才执行路由
- 🔴 阻塞级未关闭问题 SHALL 阻断 kflow-archive 归档

# 步骤 8：POST_HOOK — 阶段后置钩子

引用 `skills/kflow-bug-triage/references/hooks.md` bug-triage 阶段 POST_HOOK（不需要服务，含 UPDATE_STATE）。

---

# 与其他 Skill 的关系

- **输入来自**：用户反馈（经 `kflow-guide` 路由）
- **输出给**：`kflow-explore REVISION`（L1 路由）
- **输出给**：`kflow-prototype-design REVISION`（L2 路由）
- **输出给**：`kflow-design REVISION`（L3 路由）
- **输出给**：**缺陷修复快车道**（L4 路由）——本 Skill 创建缺陷级状态文件 `bugs/fix/{BUG-ID}/bugfix-status.md` 并写入受影响项清单，快车道修复由 `kflow-bug-fix` 的快车道模式承载；SHALL NOT 表述为直接调用 `kflow-bug-fix`
- **与 kflow-verify 互补**：verify 检查「产物质量」，triage 诊断「问题源头」
- **与 kflow-bug-fix 互补**：triage 负责「诊断+登记+路由」，bug-fix 负责「复现+修复+验证」；L4 路由下 bug-fix 以**快车道模式**执行（状态写入缺陷级状态文件、出口为定向验证）

---

# 核心提醒

- 四层诊断从上到下逐层排查，某层 ❌ 即停止
- 不执行任何修复，所有修复委托给下游 Skill
- 路由前必须获得用户确认
- 问题登记到 bugs/ 目录，使用模板格式
- 🔴 阻塞级问题未关闭时阻断归档
- **L4 路由目标为缺陷修复快车道**：创建 `bugs/fix/{BUG-ID}/bugfix-status.md` 并写入受影响项清单，SHALL NOT 修改变更级 `.status.md` 阶段状态矩阵字段，SHALL NOT 表述为直接调用 `kflow-bug-fix`；L1/L2/L3 三条路由的表述与动作不变
- **执行轮次**：被路由的执行类 Skill 的轮数由实际执行的重复制循环决定（下限恒为 1 轮，SHALL NOT 预置或受限于任何数值）；某轮无新发现且无可执行工作即自然终止，终止结果 `执行完成`；连续 3 轮无实质进展时终止结果 `停滞` 并升级用户。本 Skill 不执行修复，SHALL NOT 自行追加轮次。**执行轮次与影响范围分数无关**——分数只供下游的受影响项清单与回退判定使用

# 反馈机制

如果在使用本 Skill 过程中发现问题或有优化建议，请记录到 `docs/skill-suggestion.md` 文件中。
