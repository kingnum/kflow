---
name: kflow-bug-triage
version: 0.31.0
description: Use when user needs bug triage/问题分诊、反馈、报告问题、报bug、提bug、问题诊断, or user reports an issue through kflow-guide. Independent diagnostic Skill (not a workflow phase). 四层溯源诊断（L1需求→L2原型→L3设计→L4实现）、缺陷工作区判定（项目级 `docs/bugs/` / 变更级 `docs/changes/{change}/bugs/`）、路由决策（L1/L2/L3→创建或复用变更的 REVISION 模式，L4 满足快车道条件→缺陷修复快车道且不创建变更，L4 不满足→创建功能缺陷变更）。可在存在或不存在活跃变更时执行；用户反馈默认登记到项目级工作区，测试阶段自动发现登记到变更级工作区。含 PRE_HOOK/POST_HOOK 阶段钩子引用（不需要服务，RELOAD：选定工作区, 诊断证据来源, 活跃变更 .status.md（条件））。
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

问题分诊台。接收用户反馈后执行四层溯源漏斗（L1 需求定义 → L2 原型设计 → L3 详细设计 → L4 实现执行），先判定缺陷工作区（项目级 `docs/bugs/` 或变更级 `docs/changes/{change}/bugs/`）并登记问题，精确定位问题源头阶段后路由到对应 REVISION 模式（L1/L2/L3）或**缺陷修复快车道**（L4）。独立诊断 Skill，非流程阶段。不执行任何修复。

# 任务

接收用户反馈 -> 工作区判定与归属判定 -> 问题登记（选定工作区）-> 四层溯源诊断（L1→L2→L3→L4，证据来源按工作区解析）-> 影响范围评估 -> 输出诊断报告 -> 用户确认路由 -> 执行路由（L1/L2/L3→对应 REVISION 或创建功能缺陷变更；L4 满足快车道条件→缺陷修复快车道且创建缺陷级状态文件；L4 不满足→创建功能缺陷变更）-> 更新问题状态。

# 门控检查

此 Skill 为独立诊断阶段，门控要求：

- 用户提供问题描述（自然语言）
- 执行诊断前 SHALL 完成缺陷工作区判定（项目级 / 变更级）与归属判定（见 `# 缺陷工作区判定与归属判定`）
- SHALL NOT 以「存在活跃变更」作为执行前置条件——无活跃变更时在项目级 `docs/bugs/` 工作区执行诊断

**工作区判定分支**：

| 条件 | 工作区 | 诊断证据来源 |
|------|--------|-------------|
| 不存在活跃变更 | 项目级 `docs/bugs/` | 产品级 `docs/designs/` |
| 存在活跃变更 且 缺陷由该变更引入 | 变更级 `docs/changes/{change}/bugs/` | 该变更的 `.status.md` 与变更目录产物 |
| 存在活跃变更 但 缺陷不属于该变更 | 项目级 `docs/bugs/` | 产品级 `docs/designs/` |
| 归属无法判断 | AskUserQuestion 询问用户后再判定 | 按用户确认的归属选择 |
| 测试阶段自动发现的失败 | 变更级 `docs/changes/{change}/bugs/` | 该变更的测试报告与变更目录产物 |

# 输入要求

| 产物 | 图例 | 说明 |
|------|------|------|
| 用户的问题描述 | ✅ 必须 | 自然语言描述，经 kflow-guide 路由传入 |
| 活跃变更的 `.status.md` 与变更目录 | 🔶 条件 | 存在活跃变更且缺陷归属于该变更时读取 |
| 产品级设计产物 `docs/designs/` | 🔶 条件 | 无活跃变更或缺陷不属于任何活跃变更时作为诊断证据 |
| 项目级 `docs/bugs/index.md` | 🔶 条件 | 存在时读取；项目级工作区已有问题登记时使用 |
| 变更级 `docs/changes/{change}/bugs/index.md` | 🔶 条件 | 变更级工作区已有问题登记时读取 |
| 选定的缺陷工作区（项目级 / 变更级） | ✅ 必须 | 由 `# 缺陷工作区判定与归属判定` 在登记前确定 |

# 输出产物

| 产物 | 文件 | 图例 | 内容要求 |
|------|------|------|---------|
| 问题索引 | 项目级：`docs/bugs/index.md`<br>变更级：`docs/changes/{change}/bugs/index.md` | ✅ 必须 | 统计+问题列表+分页表；按选定工作区解析路径 |
| 问题详情 | 项目级：`docs/bugs/bug-NNN-NNN.md`<br>变更级：`docs/changes/{change}/bugs/bug-NNN-NNN.md` | ✅ 必须 | 四层溯源诊断、影响范围评估（含分数与验证目标）、解决方案（含 EXECUTION_MODE 声明）、处理状态、修复记录占位节（由 bug-fix 或快车道回写）、快车道入口标记位（L4 结论时）；记录工作区与关联变更（可选） |
| 缺陷级状态文件 | 项目级：`docs/bugs/fix/{BUG-ID}/bugfix-status.md`<br>变更级：`docs/changes/{change}/bugs/fix/{BUG-ID}/bugfix-status.md` | 🔶 L4 结论且进入快车道时必须 | **仅当诊断结论为 L4 且满足快车道条件时创建**。含六个必填区：基本信息（含工作区）、分诊结论、受影响项清单（受影响功能点/接口/验证目标）、修复记录、定向验证、收口结论。创建时 SHALL 一并写入分诊结论与**受影响项清单**，后续由快车道修复与定向验证回写其余区；SHALL NOT 修改变更级 `.status.md` 的阶段状态矩阵字段 |
| 新建 `功能缺陷` 变更 | `docs/changes/{change}/` | 🔶 L1/L2/L3 或 L4 不满足快车道条件时必须 | 创建变更并将缺陷与之关联，再路由到对应阶段；SHALL NOT 在项目级工作区内直接修改设计产物 |

> **L4 结论的额外输出**: 诊断结论为 L4 且满足快车道准入条件时，本 Skill 除问题索引与问题详情外，SHALL 额外在选定工作区创建缺陷级状态文件 `bugfix-status.md` 并写入受影响项清单——该清单是快车道定向验证的唯一验证范围依据，SHALL NOT 由修复者自行圈定。文件结构与隔离规则参见 `docs/designs/core-mechanisms/03-status-and-tasks.md` §3.5，机制定义参见 `bugfix-fast-lane` 能力。

## 状态双写规则

> **适用范围**: 仅当路由涉及变更级状态变更时适用——即 L1/L2/L3 路由到变更 REVISION、或创建 `功能缺陷` 变更时。**项目级工作区**、**L4 快车道路由**与**仅登记项目级缺陷**时 SHALL NOT 写入变更级 `.status.md` 或 `status-log.md`。

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
│  │   ├── CHECK_STATE → 校验问题描述存在，扫描活跃变更（不要求存在） │
│  │   └── RELOAD → 重读选定的缺陷工作区与诊断证据来源             │
│  1.5 WORKSPACE → 缺陷工作区判定与归属判定                        │
│  │   ├── 无活跃变更 → 项目级 docs/bugs/                          │
│  │   ├── 缺陷由活跃变更引入 → 变更级 docs/changes/{change}/bugs/ │
│  │   ├── 活跃变更无关 → 项目级 docs/bugs/                        │
│  │   └── 归属无法判断 → AskUserQuestion 询问用户（确认前不建变更）│
│  2. REGISTER  → 问题登记（选定工作区）                           │
│  │   ├── 分配 BUG-ID（工作区内独立递增编号）                      │
│  │   ├── 评估严重度（🔴阻塞/🟡警告/🔵建议）                      │
│  │   ├── 创建/更新工作区 index.md                                │
│  │   └── 创建/更新工作区 bug-NNN-NNN.md 基本信息节               │
│  3. DIAGNOSE  → 四层溯源诊断（证据来源按工作区解析）             │
│  │   ├── L1 需求定义 → 检查 functional-designs/（变更级或产品级）│
│  │   ├── L2 原型设计 → 检查 prototypes/                          │
│  │   ├── L3 详细设计 → 检查 detailed-design（变更级或产品级）    │
│  │   └── L4 实现执行 → 检查代码实现                              │
│  │   └── 某层判定 ❌ → 停止向下排查，确定为源头                   │
│  3.5 IMPACT   → 影响范围评估                                      │
│  │   ├── 识别受影响功能点（交叉引用 functional-designs/）         │
│  │   ├── 识别受影响接口（检查详细设计）                           │
│  │   ├── 识别验证目标（已有自动化测试 / 新增回归测试 / 手工步骤）│
│  │   ├── 识别数据模型变更                                         │
│  │   └── 计算影响范围分数（FP×1 + 接口×1.5 + 数据模型×2）        │
│  4. REPORT    → 填写诊断结果到问题详情                            │
│  │   ├── 四层路径表（每层结论+证据）                              │
│  │   ├── 问题源头层级和判断依据                                   │
│  │   └── 建议路由目标和解决方案                                   │
│  5. CONFIRM   → 用户确认路由                                      │
│  │   ├── AskUserQuestion 展示诊断结论                             │
│  │   │   ├── 选项 1: 确认执行路由                                 │
│  │   │   ├── 选项 2: 覆盖诊断结论（指定源头层级）                 │
│  │   │   └── 选项 3: 暂不处理                                     │
│  │   └── 用户覆盖时记录覆盖原因到问题详情                         │
│  6. ROUTE     → 执行路由                                          │
│  │   ├── L1/L2/L3（归属的活跃变更存在）→ 该变更的 REVISION       │
│  │   ├── L1/L2/L3（无归属变更）→ 创建 功能缺陷 变更 → REVISION   │
│  │   ├── L4 满足快车道条件 → 进入缺陷修复快车道（不新建变更）     │
│  │   └── L4 不满足快车道条件 → 创建 功能缺陷 变更 → 设计阶段     │
│  │       ├── 创建缺陷级状态文件（仅 L4 快车道）                   │
│  │       │   {工作区}/fix/{BUG-ID}/bugfix-status.md               │
│  │       ├── 写入受影响项清单（功能点 / 接口 / 验证目标）         │
│  │       ├── 在问题详情文件中标记快车道入口                       │
│  │       └── 路由输出声明快车道入口与工作区 → bug-fix 快车道模式  │
│  │           （SHALL NOT 修改变更级 .status.md 阶段矩阵字段）      │
│  7. UPDATE    → 更新问题状态为「处理中」                          │
│  8. POST_HOOK → 引用 skills/kflow-bug-triage/references/hooks.md bug-triage 阶段 POST_HOOK │
│  │   └── UPDATE_STATE → 变更级路由更新 .status.md；项目级与 L4 快车道不修改阶段矩阵 │
└─────────────────────────────────────────────────────────────┘
```

## 步骤 1：PRE_HOOK — 阶段前置钩子

引用 `skills/kflow-bug-triage/references/hooks.md` bug-triage 阶段 PRE_HOOK（不需要服务，RELOAD：选定的缺陷工作区、诊断证据来源、活跃变更的 `.status.md`（存在且缺陷归属于该变更时））。

---

## 步骤 1.5：WORKSPACE — 缺陷工作区判定与归属判定

工作区 SHALL 在登记前确定，判定结果 SHALL 写入问题详情「基本信息」的工作区字段；后续所有路径按该结果解析。

```
工作区判定与归属判定:

1. SCAN → 扫描 docs/changes/，排除 docs/changes/archive/
   ├── 0 个活跃变更 → 项目级 docs/bugs/
   └── ≥1 个活跃变更 → 进入 2. ATTRIBUTE
2. ATTRIBUTE → 判断缺陷是否由某个活跃变更引入:
   ├── 证据来源: 该变更的代码/产物改动范围、变更的测试报告、
   │            git 变更集、缺陷涉及的 FP/接口是否属于该变更
   ├── 明确由该变更引入 → 变更级 docs/changes/{change}/bugs/
   │                       （记录关联变更名）
   ├── 明确由既有功能或历史代码导致 → 项目级 docs/bugs/
   │                       （关联变更仅作追溯，不新建变更）
   └── 无法判断 → AskUserQuestion:
        Question: "该缺陷是否由活跃变更 {change} 引入？"
        Options:
          - "由 {change} 引入（变更级）"
          - "与活跃变更无关（项目级）"
          - "暂不判定，先登记到项目级"
        ├── 用户确认前 SHALL NOT 创建新的变更
        └── 判定依据与用户回答 SHALL 记录到问题详情「关联」节
3. TEST_FAILURE → 测试阶段自动发现的失败直接使用变更级（B 路径），无需归属询问
4. RECORD → 在问题详情记录「工作区: 项目级 / 变更级」与「关联变更」
```

**规则**：

- 项目级与变更级工作区 SHALL 各自独立维护 BUG-ID 递增序号
- 存在活跃变更但缺陷与它无关时，SHALL 登记到项目级，SHALL NOT 因存在活跃变更而新建变更
- 归属无法判断时 SHALL 先询问用户，SHALL NOT 自行假定归属或先行创建变更
- 测试阶段自动发现的缺陷（触发测试阶段上下文）不属于用户反馈路径，仍按变更级 B 路径登记

---

## 步骤 2：REGISTER — 问题登记硬约束

REGISTER 步骤 SHALL 按以下规则执行：

**必填节清单**（按顺序输出，SHALL NOT 省略任何节）：
1. 基本信息（ID、工作区、关联变更（可选）、登记时间、严重度、问题来源）
2. 问题描述（用户原始反馈、问题现象、复现步骤）
3. 诊断结果（四层溯源路径表、问题源头层级、判断依据）
4. 影响范围评估（受影响功能点、受影响接口、验证目标、数据模型变更、影响范围分数）
5. 解决方案（建议方案、处理路径、影响范围、下游影响、**EXECUTION_MODE = SUBAGENT_REQUIRED**）
6. 处理状态（checkbox 列表；L4 结论时 SHALL 含快车道入口标记位与收口状态字段）
7. 修复记录（占位节，由 bug-fix 或快车道回写）
8. 关联（关联变更、关联功能点）

**分页与编号规则**：
- SHALL 追加到选定工作区的当前分页文件末尾，SHALL NOT 每次登记创建新文件
- 仅当当前分页文件已满 20 条时，SHALL 在选定工作区创建新分页文件
- BUG-ID 使用纯序号 `BUG-{NNN}`（在工作区内递增，不含严重度前缀）；项目级与变更级各自独立维护序号

---

# 四层溯源诊断

## 诊断顺序

从最上游到下游逐层排查，某层判定为 ❌ 时停止向下排查。诊断证据来源按工作区解析（见 `# 步骤 1.5`）：

| 工作区 | 证据根 |
|--------|--------|
| 变更级 | 变更目录 `docs/changes/{change}/` 下的阶段产物 |
| 项目级 | 产品级设计产物 `docs/designs/` |

> 产品级设计产物缺失时 SHALL 在诊断报告中标注「该层无法评估」，SHALL NOT 直接判定为通过。

## L1 需求定义

**证据来源**：
- 变更级工作区：变更级 `functional-designs/index.md` + `functional-designs/part-NN.md` + `CONTEXT.md`
- 项目级工作区：`docs/designs/functional-designs/` + `CONTEXT.md`

**检查项**：
- 用户反馈的功能是否在 functional-designs/ 中有对应功能点？
- 功能点描述是否覆盖用户期望的行为？
- 是否存在歧义表述或遗漏边界条件？

**快速排除**：功能点完整覆盖且无歧义 → ✅ 通过

## L2 原型设计

**证据来源**：
- 变更级工作区：`docs/designs/prototypes/index.html` + 变更级 `prototype-changes.md` + 变更级 `element-coverage-tree.md` + 变更级 `functional-designs/`
- 项目级工作区：`docs/designs/prototypes/index.html` + `docs/designs/prototypes/manifest.md` + `docs/designs/functional-designs/`

**检查项**：
- 原型是否正确实现了 L1 确认的功能点？（变更级工作区以 `prototype-changes.md` 界定的本变更涉及页面为准；项目级工作区以 `manifest.md` 登记的页面为准）
- 交互流程是否与用户预期一致？

**快速排除**：纯后端项目（无 `docs/designs/prototypes/`）或用户反馈不涉及 UI/交互 → ✅ 通过（跳过）

## L3 详细设计

**证据来源**：
- 变更级工作区：变更级 `detailed-design.md` + `api-tests/index.md` + 变更级 `functional-designs/`
- 项目级工作区：`docs/designs/detailed-designs/` + `docs/designs/functional-designs/`

**检查项**：
- 接口定义是否与 functional-designs/ 一致？
- 数据模型是否支持用户描述的数据操作？
- 状态流转是否完整？

**快速排除**：相关接口/数据模型/状态流转与上游一致且完整 → ✅ 通过

## L4 实现执行

**证据来源**：
- 变更级工作区：代码实现 + 变更级 `detailed-design.md`
- 项目级工作区：代码实现 + `docs/designs/detailed-designs/`

**检查项**：
- 代码是否正确实现了详细设计的定义？
- 边界条件和错误处理是否按设计实现？

**判定**：L1-L3 均通过时，问题默认归因于 L4。

---

# 严重度分级

| 严重度 | 判定标准 | 路由影响 |
|--------|---------|---------|
| 🔴 阻塞 | 功能无法使用或核心流程中断 | 路由立即执行；未关闭时分别阻断归档（项目级 `docs/bugs/index.md` / 变更级 `bugs/index.md`） |
| 🟡 警告 | 功能可用但存在明显异常 | 正常路由 |
| 🔵 建议 | 非功能性问题 | 正常路由 |

> **说明**：严重度作为独立字段（`🔴 阻塞`/`🟡 警告`/`🔵 建议`），BUG-ID 使用纯序号 `BUG-{NNN}`，不含严重度前缀。

---

# 影响范围评估

四层诊断完成后，SHALL 一并执行影响范围评估，为回退后的受影响项清单与回退判定提供依据。**影响范围分数 SHALL NOT 用于推算轮次**——执行类阶段的轮次由实际执行的重复制循环决定。

## 评估步骤

| 步骤 | 证据来源 | 输出 |
|------|---------|------|
| 识别受影响功能点 | 诊断结论 × functional-designs/（按工作区解析为变更级或 `docs/designs/functional-designs/`） | 受影响功能点清单（如 FP-003, FP-007） |
| 识别受影响接口 | 诊断结论 × 详细设计的 API 定义（变更级 `detailed-design.md` 或 `docs/designs/detailed-designs/`） | 受影响接口清单（如 /api/orders/export） |
| 识别验证目标 | 诊断结论 × 已有测试、`api-tests/`、`e2e-tests/` 或项目测试代码 | 验证目标清单：已有自动化测试用例 / 新增回归测试 / 手工验证步骤 |
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
- **L4 快车道的受影响项清单**（受影响功能点 + 受影响接口 + **验证目标**）SHALL 写入选定工作区缺陷级状态文件 `bugfix-status.md` 的「受影响项清单」区，作为定向验证的**唯一验证范围**。L4 结论下该清单 SHALL NOT 写入变更级 `.status.md`；清单 SHALL NOT 由修复者自行扩大或缩小，修复中发现实际影响面超出清单时判定为**分诊失效**并退回本 Skill 重新评估。
- **影响范围分数本身**作为回退影响范围的记录性信息一并传递，SHALL NOT 用于推算轮次数值。该分数 SHALL NOT 用于 L4 快车道——快车道不进入变更级阶段集合，其验证轮次由定向验证的实际重试次数决定（复用三次修复尝试上限，有界）。
- 本 Skill 仅诊断与路由，不执行修复，SHALL NOT 自行追加审查轮次。

> 执行类阶段的终止模型（自然终止 / 停滞升级、审查范围冻结）的权威定义见 `agent-iteration-execution` 能力；落地表述见被路由 Skill 的 `references/repetition.md` §13（轮间摘要）、§14.3（重复制类阶段循环终止）与 §14.4（终止结果写入）。kflow-bug-triage 亦随附该规范（`skills/kflow-bug-triage/references/repetition.md`）。

---

# 路由决策

## 快车道准入判定（L4）

| 条件 | 判定 |
|------|------|
| 诊断结论为 L4 实现执行 | 必须满足 |
| 修复不需要修改 L1/L2/L3 产物（功能设计、原型、详细设计/测试用例） | 必须满足 |
| 修复不需要数据迁移或破坏性接口契约变更 | 必须满足 |
| 受影响项可枚举为验证目标（已有测试 / 新增回归测试 / 手工步骤） | 必须满足 |
| 用户确认（确认时展示受影响项与影响范围分数作为提示信号） | 必须满足 |

全部满足 → 进入缺陷修复快车道，SHALL NOT 创建变更；任一不满足 → 创建 `功能缺陷` 变更并路由到对应设计阶段。

> 影响范围分数仅作为提示信号展示给用户，SHALL NOT 作为快车道准入的硬阈值。

## 路由表

| 源头层级 | 前提 | 路由目标 | 变更创建 | 执行动作 | 执行模式 |
|---------|------|---------|---------|---------|---------|
| L1 需求 | 存在归属的活跃变更 | explore REVISION | 不新建 | `.status.md` explore → ⚠️，后续阶段重置为 ⏳ | EXECUTION_MODE = SUBAGENT_REQUIRED |
| L2 原型 | 存在归属的活跃变更 | prototype-design REVISION | 不新建 | `.status.md` prototype-design → ⚠️，后续阶段重置为 ⏳ | EXECUTION_MODE = SUBAGENT_REQUIRED |
| L3 设计 | 存在归属的活跃变更 | design REVISION | 不新建 | `.status.md` design → ⚠️，后续阶段重置为 ⏳ | EXECUTION_MODE = SUBAGENT_REQUIRED |
| L1/L2/L3 | 无归属的活跃变更 | 新建 `功能缺陷` 变更 → explore / prototype-design / design REVISION | **创建** | 创建变更并关联缺陷，再执行对应 REVISION | EXECUTION_MODE = SUBAGENT_REQUIRED |
| L4 实现 | 满足快车道准入条件 | **缺陷修复快车道** | **不新建** | 在选定工作区创建 `fix/{BUG-ID}/bugfix-status.md` 并写入受影响项清单，在问题详情中标记快车道入口；**SHALL NOT 修改变更级 `.status.md` 阶段状态矩阵字段**；出口为定向验证 | EXECUTION_MODE = SUBAGENT_REQUIRED |
| L4 实现 | 不满足快车道准入条件 | 新建 `功能缺陷` 变更 → explore 或设计 REVISION | **创建** | 创建变更并关联缺陷，路由到需要修改的设计阶段；SHALL NOT 以快车道身份修改设计产物 | EXECUTION_MODE = SUBAGENT_REQUIRED |

> **L4 快车道与 L1/L2/L3 的差异**: L1/L2/L3 的路由动作包含「修改变更级 `.status.md`」（标记源头阶段 ⚠️ 需修订、后续阶段重置 ⏳ 待开始）；L4 快车道的路由动作**不含任何变更级状态文件修改**——快车道不进入变更级阶段状态矩阵与门控（参见 `docs/designs/core-mechanisms/03-status-and-tasks.md` §3.5.1）。
>
> **不新建变更的分支**: L4 满足快车道条件时 SHALL NOT 创建变更；缺陷归属的活跃变更存在时，L1/L2/L3 路由 SHALL NOT 新建变更。**创建变更的分支**: L1/L2/L3 无归属变更，或 L4 不满足快车道条件时，SHALL 创建 `功能缺陷` 变更并将缺陷与之关联。
>
> **用户选择变更路径**: 缺陷满足快车道条件但用户选择创建变更时，SHALL 创建 `功能缺陷` 变更，并将用户选择原因记录到问题详情。

---

# 问题登记机制

## bugs/ 目录结构

项目级与变更级工作区结构同构，由 `# 步骤 1.5` 判定选用：

```
docs/bugs/                              # 项目级：用户反馈 / 不属于任何活跃变更的缺陷
docs/changes/{change}/bugs/             # 变更级：测试阶段自动发现 / 由该变更引入的缺陷
├── index.md              # 问题索引
├── bug-001-020.md        # 第 1 分页（≤20 条）
├── bug-021-040.md        # 第 2 分页
├── fix/                  # 仅 L4 快车道缺陷存在此目录
│   └── {BUG-ID}/
│       ├── bugfix-status.md      # 缺陷级状态文件（快车道生命周期载体）
│       └── verify-report.md      # 定向验证报告（由快车道产出）
└── ...
```

> **工作区规则**: 项目级与变更级各自独立维护 BUG-ID 递增序号；项目级 `docs/bugs/` SHALL NOT 随任何变更归档移动或删除；变更级 `docs/changes/{change}/bugs/` 随变更整体归档。跨工作区引用 SHALL 使用「工作区路径 + BUG-ID」形式。
>
> **`fix/` 目录的创建条件**: 仅当诊断结论为 L4 实现执行、缺陷进入快车道时，由本 Skill 在选定工作区创建 `fix/{BUG-ID}/bugfix-status.md`。L1/L2/L3 路由或 L4 不满足快车道条件时 SHALL NOT 创建该目录与文件。快速收口后 `bugfix-status.md` SHALL 保留为历史记录，SHALL NOT 随收口删除。

## 问题状态流转

```
待处理 → 处理中 → 已解决 → 已关闭
  └──→ 已挂起（用户选择暂缓）
```

---

# 约束

- SHALL NOT 修改任何代码、测试、设计文档
- SHALL 在诊断完成后获取用户确认才执行路由
- SHALL 在登记前完成缺陷工作区判定与归属判定；归属无法判断时 SHALL 先用 AskUserQuestion 询问
- 🔴 阻塞级未关闭问题 SHALL 阻断 kflow-archive 归档——项目级读取 `docs/bugs/index.md`，变更级读取 `docs/changes/{change}/bugs/index.md`
- 项目级缺陷 SHALL NOT 创建 `docs/changes/{change}/` 目录，SHALL NOT 进入变更级阶段状态矩阵、审计或归档

# 步骤 8：POST_HOOK — 阶段后置钩子

引用 `skills/kflow-bug-triage/references/hooks.md` bug-triage 阶段 POST_HOOK（不需要服务，含 UPDATE_STATE）。UPDATE_STATE 仅在路由涉及变更级状态变更时更新 `.status.md`；项目级与 L4 快车道路由 SHALL NOT 修改变更级阶段矩阵字段。

---

# 与其他 Skill 的关系

- **输入来自**：用户反馈（经 `kflow-guide` 路由）
- **输出给**：`kflow-explore REVISION`（L1 路由，归属的活跃变更存在时）
- **输出给**：`kflow-prototype-design REVISION`（L2 路由，归属的活跃变更存在时）
- **输出给**：`kflow-design REVISION`（L3 路由，归属的活跃变更存在时）
- **输出给**：新建 `功能缺陷` 变更 → 对应设计阶段 REVISION（L1/L2/L3 无归属变更，或 L4 不满足快车道条件时）
- **输出给**：**缺陷修复快车道**（L4 满足快车道条件时）——本 Skill 在选定工作区创建缺陷级状态文件 `{工作区}/fix/{BUG-ID}/bugfix-status.md` 并写入受影响项清单，快车道修复由 `kflow-bug-fix` 的快车道模式承载；SHALL NOT 表述为直接调用 `kflow-bug-fix`
- **与 kflow-verify 互补**：verify 检查「产物质量」，triage 诊断「问题源头」
- **与 kflow-bug-fix 互补**：triage 负责「诊断+登记+路由」，bug-fix 负责「复现+修复+验证」；L4 路由下 bug-fix 以**快车道模式**执行（状态写入缺陷级状态文件、出口为定向验证）

---

# 核心提醒

- 四层诊断从上到下逐层排查，某层 ❌ 即停止
- 不执行任何修复，所有修复委托给下游 Skill
- 路由前必须获得用户确认
- **先判定工作区再登记**：项目级 `docs/bugs/`（用户反馈 / 无归属变更）或变更级 `docs/changes/{change}/bugs/`（测试阶段发现 / 由变更引入）；归属无法判断时先用 AskUserQuestion 询问，确认前 SHALL NOT 创建变更
- 问题登记到选定工作区，使用对应模板格式；两个工作区各自独立维护 BUG-ID 序号
- 🔴 阻塞级问题未关闭时阻断归档（项目级与变更级分别读取各自索引）
- **L4 满足快车道条件时进入缺陷修复快车道且不创建变更**：在选定工作区创建 `fix/{BUG-ID}/bugfix-status.md` 并写入受影响项清单，SHALL NOT 修改变更级 `.status.md` 阶段状态矩阵字段，SHALL NOT 表述为直接调用 `kflow-bug-fix`；**L4 不满足快车道条件或 L1/L2/L3 无归属变更时应创建 `功能缺陷` 变更**
- **执行轮次**：被路由的执行类 Skill 的轮数由实际执行的重复制循环决定（下限恒为 1 轮，SHALL NOT 预置或受限于任何数值）；某轮无新发现且无可执行工作即自然终止，终止结果 `执行完成`；连续 3 轮无实质进展时终止结果 `停滞` 并升级用户。本 Skill 不执行修复，SHALL NOT 自行追加轮次。**执行轮次与影响范围分数无关**——分数只供下游的受影响项清单与回退判定使用

# 反馈机制

如果在使用本 Skill 过程中发现问题或有优化建议，请记录到 `docs/skill-suggestion.md` 文件中。
