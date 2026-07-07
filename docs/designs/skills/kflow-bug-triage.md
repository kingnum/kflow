# kflow-bug-triage（问题分诊阶段）

> **版本**: 参见仓库根目录 `VERSION` 文件
> **类型**: 独立诊断 Skill（非流程阶段）
> **创建时间**: 2026-06-16

---

## 基本信息

```yaml
name: kflow-bug-triage
description: 问题分诊 - 四层溯源诊断（L1需求→L2原型→L3设计→L4实现）、问题登记（bugs/目录）、路由决策（REVISION模式或kflow-bug-fix）。独立诊断 Skill（非流程阶段），接收用户反馈后精确定位问题源头阶段再路由修复。含 PRE_HOOK/POST_HOOK 阶段钩子引用（不需要服务，RELOAD: 全量产物, .status.md, bugs/）。
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

kflow-bug-triage 是独立诊断 Skill，非流程阶段。接收用户反馈后执行四层溯源漏斗（L1 需求定义 → L2 原型设计 → L3 详细设计 → L4 实现执行），将问题登记到 `bugs/` 目录，并路由到问题源头阶段的 REVISION 模式或调用 `kflow-bug-fix` 执行实现层修复。

### 与 kflow-verify 的关系

```
kflow-bug-triage (问题分诊)           kflow-verify (产物诊断)
├── 用户反馈驱动                          ├── 产物质量驱动
├── 四层溯源定位问题源头                   ├── 七维度检查产物完整性
├── 路由到 REVISION 或 bug-fix            ├── 路由到 REVISION 或重新执行
├── 输出 bugs/ 登记                       ├── 输出 verify-report.md
└── 修改 .status.md（阶段回退）            └── 不修改 .status.md
```

### 与 kflow-bug-fix 的关系

```
kflow-bug-triage (分诊台)               kflow-bug-fix (手术室)
├── 诊断问题源头层级                       ├── 执行实现层修复
├── L1-L3 → REVISION 模式                 ├── 二分法（实现错误/测试错误）
├── L4 → 调用 bug-fix                     ├── 入口仅限测试失败报告（B路径）
├── 不执行任何修复                         └── 不判定设计错误
└── 用户反馈唯一入口（A路径）
```

---

## 门控检查

> **机制说明**：门控规则定义在 [core-mechanisms/03-status-and-tasks.md](../core-mechanisms/03-status-and-tasks.md#34-门控规则)

此 Skill 为独立诊断阶段，门控要求：

- 存在活跃变更（`docs/changes/{change}/` 目录存在且 `.status.md` 可读）
- 用户提供问题描述（自然语言）

---

## 输入要求

| 产物 | 图例 | 说明 |
|------|------|------|
| .status.md | ✅ 必须 | 变更级状态文件，获取当前变更阶段状态 |
| 变更目录 docs/changes/{change}/ | ✅ 必须 | 获取所有阶段产物用于四层溯源 |
| 用户的问题描述 | ✅ 必须 | 自然语言描述，经 kflow-guide 路由传入 |
| bugs/index.md | 🔶 条件 | 已有问题登记时读取（首次登记时创建） |

---

## 输出产物

| 产物 | 文件 | 模板 | 图例 | 内容要求 |
|------|------|------|------|---------|
| 问题索引 | docs/changes/{change}/bugs/index.md | [bugs-index.md](../../templates/changes/{change}/bugs/bugs-index.md) | ✅ 必须 | 统计+问题列表+分页表 |
| 问题详情 | docs/changes/{change}/bugs/bug-NNN-NNN.md | [bugs-detail.md](../../templates/changes/{change}/bugs/bugs-detail.md) | ✅ 必须 | 四层溯源诊断、影响范围评估（含分数）、解决方案（含 EXECUTION_MODE 声明）、处理状态、修复记录占位节（由 bug-fix 回写） |

---

## 执行流程

```
问题分诊流程:

┌─────────────────────────────────────────────────────────────┐
│                    TRIAGE WORKFLOW                            │
├─────────────────────────────────────────────────────────────┤
│  1. PRE_HOOK  → 引用 `skills/kflow-bug-triage/references/hooks.md` bug-triage 阶段 PRE_HOOK │
│  │   ├── CHECK_STATE → 验证活跃变更存在                       │
│  │   └── RELOAD → 重读 .status.md, 全量产物, bugs/            │
│  2. REGISTER  → 问题登记                                     │
│  │   ├── 分配 BUG-ID（递增编号）                              │
│  │   ├── 评估严重度（🔴阻塞/🟡警告/🔵建议）                  │
│  │   ├── 创建/更新 bugs/index.md                             │
│  │   └── 创建/更新 bugs/bug-NNN-NNN.md 基本信息节             │
│  3. DIAGNOSE  → 四层溯源诊断                                  │
│  │   ├── L1 需求定义 → 检查 functional-designs/              │
│  │   ├── L2 原型设计 → 检查 prototype/                       │
│  │   ├── L3 详细设计 → 检查 detailed-design.md               │
│  │   └── L4 实现执行 → 检查代码实现                           │
│  │   └── 某层判定 ❌ → 停止向下排查，确定为源头               │
│  3.5 IMPACT   → 影响范围评估                                  │
│  │   ├── 识别受影响功能点（交叉引用 functional-designs/）     │
│  │   ├── 识别受影响接口（检查 detailed-design.md）            │
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
│  │   └── L4 → 调用 kflow-bug-fix                            │
│  7. UPDATE    → 更新问题状态为「处理中」                      │
│  8. POST_HOOK → 引用 `skills/kflow-bug-triage/references/hooks.md` bug-triage 阶段 POST_HOOK │
│  │   └── UPDATE_STATE → 更新 .status.md（阶段回退标记）       │
└─────────────────────────────────────────────────────────────┘
```

---

## 四层溯源诊断

### 诊断顺序

从最上游到下游逐层排查，某层判定为 ❌ 时停止向下排查。

### L1 需求定义

**证据来源**：
- `functional-designs/index.md` + `functional-designs/part-NN.md`
- `CONTEXT.md`

**检查项**：
- 用户反馈的功能是否在 functional-designs/ 中有对应功能点？
- 功能点描述是否覆盖用户期望的行为？
- 是否存在歧义表述或遗漏边界条件？
- CONTEXT.md 中的领域术语是否与用户反馈中的概念一致？

**快速排除条件**：用户反馈涉及的功能点在 functional-designs/ 中有完整覆盖且无歧义 → ✅ 通过

### L2 原型设计

**证据来源**：
- `prototype/index.html`（或 prototype/index.md）
- `element-coverage-tree.md`
- `functional-designs/`（用于比对一致性）

**检查项**：
- 原型是否正确实现了 L1 确认的功能点？
- 交互流程是否与用户预期一致？
- 视觉呈现是否传达了正确的功能语义？
- element-coverage-tree.md 中对应节点是否标记为已覆盖？

**快速排除条件**：纯后端项目（无 prototype/ 目录）或用户反馈不涉及 UI/交互 → ✅ 通过（跳过）

### L3 详细设计

**证据来源**：
- `detailed-design.md`
- `api-tests/index.md`（用于接口一致性比对）
- `functional-designs/`（用于需求追溯）

**检查项**：
- 接口定义是否与 functional-designs/ 的功能描述一致？
- 数据模型是否支持用户反馈中涉及的数据操作？
- 状态流转定义是否完整覆盖用户描述的场景？
- NFR（非功能需求）定义是否与用户期望匹配？

**快速排除条件**：detailed-design.md 中相关接口/数据模型/状态流转与上游一致且完整 → ✅ 通过

### L4 实现执行

**证据来源**：
- 代码实现（src/、app/ 等项目源码目录）
- `detailed-design.md`（用于实现一致性比对）

**检查项**：
- 代码是否正确实现了 detailed-design.md 的定义？
- 边界条件是否按设计处理？
- 错误处理是否按设计实现？

**判定规则**：L4 是唯一代码层面检查——如果 L1-L3 均通过，问题默认归因于 L4。

---

## 严重度分级

| 严重度 | 判定标准 | 路由影响 |
|--------|---------|---------|
| 🔴 阻塞 | 功能无法正常使用或核心流程中断 | 路由立即执行，未关闭阻断归档 |
| 🟡 警告 | 功能可用但存在明显异常或体验问题 | 正常路由流程 |
| 🔵 建议 | 非功能性问题（性能优化、代码风格等） | 正常路由流程 |

> **说明**：严重度作为独立字段记录（`🔴 阻塞`/`🟡 警告`/`🔵 建议`），不编码到 BUG-ID 中。BUG-ID 使用纯序号 `BUG-{NNN}` 格式。

---

## 影响范围评估

四层诊断完成后，SHALL 一并执行影响范围评估，为回退后的弹性重复制轮次决策提供依据。

### 评估步骤

| 步骤 | 证据来源 | 输出 |
|------|---------|------|
| 识别受影响功能点 | 诊断结论 × functional-designs/ | 受影响功能点清单（如 FP-003, FP-007） |
| 识别受影响接口 | 诊断结论 × detailed-design.md API 定义 | 受影响接口清单（如 /api/orders/export） |
| 识别数据模型变更 | 诊断证据中的 schema/存储修改 | 数据模型变更描述（none / 描述） |
| 计算影响范围分数 | 公式计算 | 数值 |

### 影响范围分数计算公式

```
影响范围分数 = 功能点数 × 1 + 接口数 × 1.5 + 数据模型变更 × 2
```

### 执行模式声明

路由输出 SHALL 包含 `EXECUTION_MODE = SUBAGENT_REQUIRED` 声明，指定目标 Skill MUST 使用 Agent 子代理执行主工作，子代理 SHOULD 前台运行。

---

## 路由决策

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
诊断确定 L4 → 调用 kflow-bug-fix:
1. 将诊断报告中的问题描述、证据和影响范围评估传递给 bug-fix
2. bug-fix 使用二分法（实现错误/测试错误）进行分类和修复
3. bug-fix 完成后回写 bugs/ 对应 BUG 的修复记录节，并更新 bugs/index.md 状态
4. 问题状态更新为「已解决」
5. EXECUTION_MODE = SUBAGENT_REQUIRED
```

---

## 问题登记机制

### bugs/ 目录结构

```
docs/changes/{change}/bugs/
├── index.md              # 问题索引（统计+列表+分页表）
├── bug-001-020.md        # 第 1 分页（BUG-001 ~ BUG-020）
├── bug-021-040.md        # 第 2 分页（BUG-021 ~ BUG-040）
└── ...
```

### 分页规则

- 每个分页文件最多 20 个问题
- **追加优先、满额新建**：登记新 BUG 时 SHALL 追加到当前分页文件末尾，SHALL NOT 每次登记创建新文件；仅当当前分页文件已满 20 条时才创建新分页
- 文件命名：`bug-{start}-{end}.md`（起止 ID 范围，如 `bug-001-020.md`、`bug-021-040.md`）
- 首个文件：`bug-001-020.md`
- BUG-ID 使用纯序号 `BUG-{NNN}` 格式（递增编号，不含严重度前缀）

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
- SHALL 为每个问题分配唯一 BUG-ID
- 🔴 阻塞级未关闭问题 SHALL 阻断 kflow-archive 归档

---

## 与其他 Skill 的关系

- **输入来自**：用户反馈（经 `kflow-guide` 路由）
- **输出给**：`kflow-explore REVISION`（L1 路由）
- **输出给**：`kflow-prototype-design REVISION`（L2 路由）
- **输出给**：`kflow-design REVISION`（L3 路由）
- **输出给**：`kflow-bug-fix`（L4 路由）
- **与 kflow-verify 互补**：verify 检查「产物质量」，triage 诊断「问题源头」
- **与 kflow-bug-fix 互补**：triage 负责「诊断+登记+路由」，bug-fix 负责「复现+修复+验证」

---

## 反馈机制

如果在使用本 Skill 过程中发现问题或有优化建议，请记录到 `docs/skill-suggestion.md` 文件中。
