# kflow-bug-triage（问题分诊阶段）

> **版本**: 参见仓库根目录 `VERSION` 文件
> **类型**: 独立诊断 Skill（非流程阶段）
> **创建时间**: 2026-06-16

---

## 基本信息

```yaml
name: kflow-bug-triage
description: 问题分诊 - 四层溯源诊断（L1需求→L2原型→L3设计→L4实现）、缺陷工作区判定（项目级 docs/bugs/ / 变更级 docs/changes/{change}/bugs/）、路由决策（L1/L2/L3→创建或复用变更的 REVISION 模式，L4 满足快车道条件→缺陷修复快车道且不创建变更，L4 不满足→创建功能缺陷变更）。独立诊断 Skill（非流程阶段），可在存在或不存在活跃变更时执行。含 PRE_HOOK/POST_HOOK 阶段钩子引用（不需要服务，RELOAD：选定工作区, 诊断证据来源, 活跃变更 .status.md（条件））。
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
```

---

## 定位

kflow-bug-triage 是独立诊断 Skill，非流程阶段。接收用户反馈后执行四层溯源漏斗（L1 需求定义 → L2 原型设计 → L3 详细设计 → L4 实现执行），将问题登记到 `bugs/` 目录，并路由到问题源头阶段的 REVISION 模式（L1/L2/L3）或**缺陷修复快车道**（L4）。

### 与 kflow-verify 的关系

```
kflow-bug-triage (问题分诊)           kflow-verify (产物诊断)
├── 用户反馈驱动                          ├── 产物质量驱动
├── 四层溯源定位问题源头                   ├── 七维度检查产物完整性
├── 路由到 REVISION 或快车道               ├── 路由到 REVISION 或重新执行
├── 输出 bugs/ 登记                       ├── 输出 verify-report.md
└── L1-L3 修改 .status.md（阶段回退）      └── 不修改 .status.md
    L4 不修改 .status.md（快车道）
```

### 与 kflow-bug-fix 的关系

```
kflow-bug-triage (分诊台)               kflow-bug-fix (手术室)
├── 诊断问题源头层级                       ├── 执行实现层修复
├── L1-L3 → REVISION 模式                 ├── 二分法（实现错误/测试错误）
├── L4 → 缺陷修复快车道入口                ├── 快车道模式（状态写入 bugfix-status.md）
│   （创建缺陷级状态文件 + 受影响项清单）    │   出口为定向验证 → 快速收口
├── 不执行任何修复                         └── 既有模式入口仅限测试失败报告（B路径）
└── 用户反馈唯一入口（A路径）
```

---

## 门控检查

> **机制说明**：门控规则定义在 [core-mechanisms/03-status-and-tasks.md](../core-mechanisms/03-status-and-tasks.md#34-门控规则)

此 Skill 为独立诊断阶段，门控要求：

- 用户提供问题描述（自然语言）
- 执行诊断前 SHALL 完成缺陷工作区判定（项目级 / 变更级）与归属判定
- SHALL NOT 以「存在活跃变更」作为执行前置条件——无活跃变更时在项目级 `docs/bugs/` 工作区执行诊断

**工作区判定分支**：

| 条件 | 工作区 | 诊断证据来源 |
|------|--------|-------------|
| 不存在活跃变更 | 项目级 `docs/bugs/` | 产品级 `docs/designs/` |
| 存在活跃变更 且 缺陷由该变更引入 | 变更级 `docs/changes/{change}/bugs/` | 该变更的 `.status.md` 与变更目录产物 |
| 存在活跃变更 但 缺陷不属于该变更 | 项目级 `docs/bugs/` | 产品级 `docs/designs/` |
| 归属无法判断 | AskUserQuestion 询问用户后再判定 | 按用户确认的归属选择 |
| 测试阶段自动发现的失败 | 变更级 `docs/changes/{change}/bugs/` | 该变更的测试报告与变更目录产物 |

---

## 输入要求

| 产物 | 图例 | 说明 |
|------|------|------|
| 用户的问题描述 | ✅ 必须 | 自然语言描述，经 kflow-guide 路由传入 |
| 活跃变更的 `.status.md` 与变更目录 | 🔶 条件 | 存在活跃变更且缺陷归属于该变更时读取 |
| 产品级设计产物 `docs/designs/` | 🔶 条件 | 无活跃变更或缺陷不属于任何活跃变更时作为诊断证据 |
| 项目级 `docs/bugs/index.md` | 🔶 条件 | 存在时读取；项目级工作区已有问题登记时使用 |
| 变更级 `docs/changes/{change}/bugs/index.md` | 🔶 条件 | 变更级工作区已有问题登记时读取 |
| 选定的缺陷工作区（项目级 / 变更级） | ✅ 必须 | 在登记前由工作区判定确定 |

---

## 输出产物

| 产物 | 文件 | 模板 | 图例 | 内容要求 |
|------|------|------|------|---------|
| 问题索引 | 项目级：docs/bugs/index.md<br>变更级：docs/changes/{change}/bugs/index.md | [bugs-index.md](../../templates/bugs/bugs-index.md)（项目级）/ [bugs-index.md](../../templates/changes/{change}/bugs/bugs-index.md)（变更级） | ✅ 必须 | 统计+问题列表+分页表；按选定工作区解析路径；含「处理路径」列区分快车道缺陷 |
| 问题详情 | 项目级：docs/bugs/bug-NNN-NNN.md<br>变更级：docs/changes/{change}/bugs/bug-NNN-NNN.md | [bugs-detail.md](../../templates/bugs/bugs-detail.md)（项目级）/ [bugs-detail.md](../../templates/changes/{change}/bugs/bugs-detail.md)（变更级） | ✅ 必须 | 四层溯源诊断、影响范围评估（含分数与验证目标）、解决方案（含 EXECUTION_MODE 声明）、处理状态、修复记录占位节（由 bug-fix 或快车道回写）、快车道入口与收口状态节（L4 结论时）；记录工作区 |
| 缺陷级状态文件 | 项目级：docs/bugs/fix/{BUG-ID}/bugfix-status.md<br>变更级：docs/changes/{change}/bugs/fix/{BUG-ID}/bugfix-status.md | [bugfix-status.md](../../templates/bugs/fix/{BUG-ID}/bugfix-status.md)（项目级）/ [bugfix-status.md](../../templates/changes/{change}/bugs/fix/{BUG-ID}/bugfix-status.md)（变更级） | 🔶 L4 结论且满足快车道条件时必须 | **仅当诊断结论为 L4 且满足快车道准入条件时创建**。六区齐全：基本信息（含工作区）、分诊结论、受影响项清单、修复记录、定向验证、收口结论。创建时 SHALL 一并写入分诊结论与受影响项清单（受影响功能点 / 接口 / **验证目标**）；其余区由 `kflow-bug-fix` 快车道模式回写。SHALL NOT 修改变更级 `.status.md` 的阶段状态矩阵字段 |
| 新建 `功能缺陷` 变更 | docs/changes/{change}/ | — | 🔶 L1/L2/L3 无归属变更或 L4 不满足快车道条件时必须 | 创建变更并关联缺陷，再路由到对应设计阶段；SHALL NOT 在项目级工作区内直接修改设计产物 |

---

> **状态双写**：仅当路由涉及变更级状态变更（L1/L2/L3 路由到变更 REVISION 或创建 `功能缺陷` 变更）时，主 Agent SHALL 向 `docs/changes/{change}/status-log.md` 追加事件记录，并刷新 `.status.md` 的当前状态字段；`.status.md` SHALL 保持在 100 行以内。项目级工作区与 L4 快车道路由 SHALL NOT 写入变更级状态文件。常规阶段推进与门控判定 SHALL 仅读取 `.status.md`，`status-log.md` 仅在中断恢复与审计场景读取。权威定义见 `status-file-layering` 能力。

## 执行流程

```
问题分诊流程:

┌─────────────────────────────────────────────────────────────┐
│                    TRIAGE WORKFLOW                            │
├─────────────────────────────────────────────────────────────┤
│  1. PRE_HOOK  → 引用 `skills/kflow-bug-triage/references/hooks.md` bug-triage 阶段 PRE_HOOK │
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
│  8. POST_HOOK → 引用 `skills/kflow-bug-triage/references/hooks.md` bug-triage 阶段 POST_HOOK │
│  │   └── UPDATE_STATE → 变更级路由更新 .status.md；项目级与 L4 快车道不修改阶段矩阵 │
└─────────────────────────────────────────────────────────────┘
```

---

## 缺陷工作区判定与归属判定

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
   ├── 明确由既有功能或历史代码导致 → 项目级 docs/bugs/
   └── 无法判断 → AskUserQuestion 询问归属，确认前 SHALL NOT 创建变更
3. TEST_FAILURE → 测试阶段自动发现的失败直接使用变更级（B 路径），无需归属询问
4. RECORD → 在问题详情记录「工作区」与「关联变更」
```

**规则**：

- 项目级与变更级工作区 SHALL 各自独立维护 BUG-ID 递增序号
- 存在活跃变更但缺陷与它无关时，SHALL 登记到项目级，SHALL NOT 因存在活跃变更而新建变更
- 归属无法判断时 SHALL 先询问用户，SHALL NOT 自行假定归属或先行创建变更

---

## 四层溯源诊断

### 诊断顺序

从最上游到下游逐层排查，某层判定为 ❌ 时停止向下排查。诊断证据来源按工作区解析：

| 工作区 | 证据根 |
|--------|--------|
| 变更级 | 变更目录 `docs/changes/{change}/` 下的阶段产物 |
| 项目级 | 产品级设计产物 `docs/designs/` |

> 产品级设计产物缺失时 SHALL 在诊断报告中标注「该层无法评估」，SHALL NOT 直接判定为通过。

### L1 需求定义

**证据来源**：
- 变更级工作区：变更级 `functional-designs/index.md` + `functional-designs/part-NN.md` + `CONTEXT.md`
- 项目级工作区：`docs/designs/functional-designs/` + `CONTEXT.md`

**检查项**：
- 用户反馈的功能是否在 functional-designs/ 中有对应功能点？
- 功能点描述是否覆盖用户期望的行为？
- 是否存在歧义表述或遗漏边界条件？
- CONTEXT.md 中的领域术语是否与用户反馈中的概念一致？

**快速排除条件**：用户反馈涉及的功能点在 functional-designs/ 中有完整覆盖且无歧义 → ✅ 通过

### L2 原型设计

**证据来源**：
- 变更级工作区：`docs/designs/prototypes/index.html`（产品级原型入口）+ 变更级 `prototype-changes.md` + 变更级 `element-coverage-tree.md` + 变更级 `functional-designs/`
- 项目级工作区：`docs/designs/prototypes/index.html` + `docs/designs/prototypes/manifest.md` + `docs/designs/functional-designs/`

**检查项**：
- 原型是否正确实现了 L1 确认的功能点？
- 交互流程是否与用户预期一致？
- 视觉呈现是否传达了正确的功能语义？
- element-coverage-tree.md 中对应节点是否标记为已覆盖？

**快速排除条件**：纯后端项目（无 `docs/designs/prototypes/` 目录）或用户反馈不涉及 UI/交互 → ✅ 通过（跳过）

### L3 详细设计

**证据来源**：
- 变更级工作区：变更级 `detailed-design.md` + `api-tests/index.md` + 变更级 `functional-designs/`
- 项目级工作区：`docs/designs/detailed-designs/` + `docs/designs/functional-designs/`

**检查项**：
- 接口定义是否与 functional-designs/ 的功能描述一致？
- 数据模型是否支持用户反馈中涉及的数据操作？
- 状态流转定义是否完整覆盖用户描述的场景？
- NFR（非功能需求）定义是否与用户期望匹配？

**快速排除条件**：detailed-design.md 中相关接口/数据模型/状态流转与上游一致且完整 → ✅ 通过

### L4 实现执行

**证据来源**：
- 变更级工作区：代码实现（src/、app/ 等项目源码目录）+ 变更级 `detailed-design.md`
- 项目级工作区：代码实现 + `docs/designs/detailed-designs/`

**检查项**：
- 代码是否正确实现了 detailed-design.md 的定义？
- 边界条件是否按设计处理？
- 错误处理是否按设计实现？

**判定规则**：L4 是唯一代码层面检查——如果 L1-L3 均通过，问题默认归因于 L4。

---

## 严重度分级

| 严重度 | 判定标准 | 路由影响 |
|--------|---------|---------|
| 🔴 阻塞 | 功能无法正常使用或核心流程中断 | 路由立即执行；未关闭时分别阻断归档（项目级 `docs/bugs/index.md` / 变更级 `bugs/index.md`） |
| 🟡 警告 | 功能可用但存在明显异常或体验问题 | 正常路由流程 |
| 🔵 建议 | 非功能性问题（性能优化、代码风格等） | 正常路由流程 |

> **说明**：严重度作为独立字段记录（`🔴 阻塞`/`🟡 警告`/`🔵 建议`），不编码到 BUG-ID 中。BUG-ID 使用纯序号 `BUG-{NNN}` 格式。

---

## 影响范围评估

四层诊断完成后，SHALL 一并执行影响范围评估，为回退后的档位驱动弹性重复制轮次决策提供依据（推荐轮次引用统一映射，见「推荐轮次」节）。

### 评估步骤

| 步骤 | 证据来源 | 输出 |
|------|---------|------|
| 识别受影响功能点 | 诊断结论 × functional-designs/（按工作区解析为变更级或 `docs/designs/functional-designs/`） | 受影响功能点清单（如 FP-003, FP-007） |
| 识别受影响接口 | 诊断结论 × 详细设计的 API 定义（变更级 `detailed-design.md` 或 `docs/designs/detailed-designs/`） | 受影响接口清单（如 /api/orders/export） |
| 识别验证目标 | 诊断结论 × 已有测试、`api-tests/`、`e2e-tests/` 或项目测试代码 | 验证目标清单：已有自动化测试用例 / 新增回归测试 / 手工验证步骤 |
| 识别数据模型变更 | 诊断证据中的 schema/存储修改 | 数据模型变更描述（none / 描述） |
| 计算影响范围分数 | 公式计算 | 数值 |

### 影响范围分数计算公式

```
影响范围分数 = 功能点数 × 1 + 接口数 × 1.5 + 数据模型变更 × 2
```

### 影响范围分数的用途

影响范围分数 SHALL NOT 映射为重复制轮次——审查轮数由收敛实际发生在第几轮决定（下限 1 轮，无轮数上限）。分数仅用于下游阶段的**受影响项清单**与**回退判定**：

- **受影响项清单**（`Affected Functional Points` + `Affected Interfaces`）SHALL 经 `.status.md`「Recent Revision Info」节传递给目标阶段，供其验证门控的「受影响项 100% 覆盖」使用。
- **L4 快车道的受影响项清单**（受影响功能点 + 受影响接口 + **验证目标**）SHALL 写入选定工作区缺陷级状态文件 `bugfix-status.md` 的「受影响项清单」区，作为**定向验证的唯一验证范围**。L4 结论下该清单 SHALL NOT 写入变更级 `.status.md`；清单 SHALL NOT 由修复者自行圈定，修复中发现实际影响面超出清单时判定为**分诊失效**并退回本 Skill 重新评估。
- **L4 快车道不使用影响范围分数**——快车道不进入变更级阶段集合，其验证轮次由定向验证的实际重试次数决定（复用三次修复尝试上限，有界）。
- **影响范围分数本身**作为回退影响范围的记录性信息一并传递，SHALL NOT 用于推算轮次数值。
- 本 Skill 仅诊断与路由，不执行修复，SHALL NOT 自行追加审查轮次；目标阶段轮数 SHALL NOT 因路由而被预置或提高。

### 执行模式声明

路由输出 SHALL 包含 `EXECUTION_MODE = SUBAGENT_REQUIRED` 声明，指定目标 Skill MUST 使用 Agent 子代理执行主工作，子代理 SHOULD 前台运行。

---

## 路由决策

### 快车道准入判定（L4）

| 条件 | 判定 |
|------|------|
| 诊断结论为 L4 实现执行 | 必须满足 |
| 修复不需要修改 L1/L2/L3 产物 | 必须满足 |
| 修复不需要数据迁移或破坏性接口契约变更 | 必须满足 |
| 受影响项可枚举为验证目标（已有测试 / 新增回归测试 / 手工步骤） | 必须满足 |
| 用户确认（展示受影响项与影响范围分数作为提示信号） | 必须满足 |

全部满足 → 进入缺陷修复快车道，SHALL NOT 创建变更；任一不满足 → 创建 `功能缺陷` 变更并路由到对应设计阶段。

### L1 需求问题路由

```
诊断确定 L1 → 回退到 explore REVISION:
1. .status.md 中 explore 阶段: ✅ → ⚠️ 需修订
2. prototype-design、design、plan、code、test 等后续阶段: 重置为 ⏳ 待开始
3. 受影响产物标记为「待修订」（不删除）
4. 将问题登记信息作为修订需求传递给 explore
5. 进入 explore REVISION 模式
```

### L2 原型问题路由

```
诊断确定 L2 → 回退到 prototype-design REVISION:
1. .status.md 中 prototype-design 阶段: ✅ → ⚠️ 需修订
2. design、plan、code、test 等后续阶段: 重置为 ⏳ 待开始
3. 受影响产物标记为「待修订」（不删除）
4. 将问题登记信息作为修订需求传递给 prototype-design
5. 进入 prototype-design REVISION 模式
```

### L3 设计问题路由

```
诊断确定 L3 → 回退到 design REVISION:
1. .status.md 中 design 阶段: ✅ → ⚠️ 需修订
2. plan、code、test 等后续阶段: 重置为 ⏳ 待开始
3. 受影响产物标记为「待修订」（不删除）
4. 将问题登记信息作为修订需求传递给 design
5. 进入 design REVISION 模式
```

### L4 实现问题路由

```
诊断确定 L4 → 判定快车道准入:
├── 满足快车道条件 → 进入缺陷修复快车道（不新建变更）:
│   1. 在 triage 选定的缺陷工作区创建 fix/{BUG-ID}/bugfix-status.md
│      （项目级 docs/bugs/ / 变更级 docs/changes/{change}/bugs/）
│   2. 写入「基本信息」（含工作区）、「分诊结论」与「受影响项清单」
│      （受影响功能点 / 受影响接口 / 验证目标）
│   3. 在问题详情文件中标记快车道入口与入口时间
│   4. 路由输出声明快车道入口、工作区与受影响项清单
│   5. SHALL NOT 修改变更级 .status.md 的阶段状态矩阵字段
│   6. 快车道出口为定向验证（仅执行受影响项清单覆盖的验证目标）→ 快速收口
│   7. 快速收口后更新选定工作区 index.md 对应行状态为「已解决」
│   8. EXECUTION_MODE = SUBAGENT_REQUIRED
└── 不满足快车道条件 → 创建「功能缺陷」变更并关联缺陷，路由到 explore 或设计 REVISION
    （SHALL NOT 以快车道身份修改设计产物）
```

> **L1/L2/L3 与 L4 的路由差异**: L1/L2/L3 在归属的活跃变更存在时路由到该变更的 REVISION，不新建变更；无归属变更时创建 `功能缺陷` 变更后再路由。L4 满足快车道条件时**不含任何变更级状态文件修改，也不创建变更**；L4 不满足时创建变更。三条 L1/L2/L3 路由的动作与既有行为一致，仅补充无归属变更时的创建分支。

---

## 问题登记机制

### bugs/ 目录结构

项目级与变更级工作区结构同构，由工作区判定选用：

```
docs/bugs/                              # 项目级：用户反馈 / 不属于任何活跃变更的缺陷
docs/changes/{change}/bugs/             # 变更级：测试阶段自动发现 / 由该变更引入的缺陷
├── index.md              # 问题索引（统计+列表+分页表）
├── bug-001-020.md        # 第 1 分页（BUG-001 ~ BUG-020）
├── bug-021-040.md        # 第 2 分页（BUG-021 ~ BUG-040）
├── fix/                  # 仅 L4 快车道缺陷存在此目录
│   └── {BUG-ID}/
│       ├── bugfix-status.md      # 缺陷级状态文件（快车道生命周期载体）
│       └── verify-report.md      # 定向验证报告（由快车道产出）
└── ...
```

> **工作区规则**: 项目级与变更级各自独立维护 BUG-ID 递增序号；项目级 `docs/bugs/` SHALL NOT 随任何变更归档移动或删除；变更级 `docs/changes/{change}/bugs/` 随变更整体归档。跨工作区引用 SHALL 使用「工作区路径 + BUG-ID」形式。
>
> **`fix/` 目录的创建条件**: 仅当诊断结论为 L4、缺陷进入快车道时由本 Skill 在选定工作区创建 `fix/{BUG-ID}/bugfix-status.md`。L1/L2/L3 或 L4 不满足快车道条件时 SHALL NOT 创建该目录与文件。快速收口后 `bugfix-status.md` SHALL 保留为历史记录，SHALL NOT 删除。

### 分页规则

- 每个分页文件最多 20 个问题
- **追加优先、满额新建**：登记新 BUG 时 SHALL 追加到选定工作区的当前分页文件末尾，SHALL NOT 每次登记创建新文件；仅当当前分页文件已满 20 条时才创建新分页
- 文件命名：`bug-{start}-{end}.md`（起止 ID 范围，如 `bug-001-020.md`、`bug-021-040.md`）
- 首个文件：`bug-001-020.md`
- BUG-ID 使用纯序号 `BUG-{NNN}` 格式（工作区内递增编号，不含严重度前缀；项目级与变更级各自独立维护序号）

### 问题状态流转

```
待处理 → 处理中 → 已解决 → 已关闭
  └──→ 已挂起（用户选择暂缓）
```

| 状态 | 触发时机 |
|------|---------|
| 待处理 | 问题登记时 |
| 处理中 | 路由到对应阶段并开始修复 |
| 已解决 | 修复验证通过 |
| 已关闭 | 用户确认关闭 |
| 已挂起 | 用户选择暂缓处理 |

---

## 约束

- SHALL NOT 修改任何代码、测试、设计文档（所有修复委托给下游 Skill）
- SHALL 在诊断完成后获取用户确认才执行路由
- SHALL 使用四层溯源从上到下逐层排查
- SHALL 在某层判定 ❌ 时停止向下排查
- SHALL 在登记前完成缺陷工作区判定与归属判定；归属无法判断时 SHALL 先用 AskUserQuestion 询问
- SHALL 为每个问题分配唯一 BUG-ID（工作区内递增）
- **L4 结论且满足快车道条件时 SHALL 在选定工作区创建缺陷级状态文件 `fix/{BUG-ID}/bugfix-status.md` 并写入受影响项清单**；SHALL NOT 修改变更级 `.status.md` 的阶段状态矩阵字段；SHALL NOT 表述为直接调用 `kflow-bug-fix`
- **L1/L2/L3 无归属变更或 L4 不满足快车道条件时 SHALL 创建 `功能缺陷` 变更**并关联缺陷，再路由到对应阶段
- 🔴 阻塞级未关闭问题 SHALL 阻断 kflow-archive 归档——项目级读取 `docs/bugs/index.md`，变更级读取 `docs/changes/{change}/bugs/index.md`
- 项目级缺陷 SHALL NOT 创建 `docs/changes/{change}/` 目录，SHALL NOT 进入变更级阶段状态矩阵、审计或归档

---

## 与其他 Skill 的关系

- **输入来自**：用户反馈（经 `kflow-guide` 路由）
- **输出给**：`kflow-explore REVISION`（L1 路由，归属的活跃变更存在时）
- **输出给**：`kflow-prototype-design REVISION`（L2 路由，归属的活跃变更存在时）
- **输出给**：`kflow-design REVISION`（L3 路由，归属的活跃变更存在时）
- **输出给**：新建 `功能缺陷` 变更 → 对应设计阶段 REVISION（L1/L2/L3 无归属变更，或 L4 不满足快车道条件时）
- **输出给**：**缺陷修复快车道**（L4 满足快车道条件时）——本 Skill 在选定工作区创建缺陷级状态文件 `{工作区}/fix/{BUG-ID}/bugfix-status.md` 并写入受影响项清单，快车道修复由 `kflow-bug-fix` 的**快车道模式**承载；SHALL NOT 表述为直接调用 `kflow-bug-fix`
- **与 kflow-verify 互补**：verify 检查「产物质量」，triage 诊断「问题源头」
- **与 kflow-bug-fix 互补**：triage 负责「诊断+登记+路由」，bug-fix 负责「复现+修复+验证」；L4 路由下 bug-fix 以快车道模式执行（状态写入缺陷级状态文件、出口为定向验证）

---

## 反馈机制

如果在使用本 Skill 过程中发现问题或有优化建议，请记录到 `docs/skill-suggestion.md` 文件中。
