# kflow-plan（计划阶段）

> **版本**: 参见仓库根目录 `VERSION` 文件
> **阶段**: 计划（必须阶段，子变更级）

---

## 基本信息

```yaml
name: kflow-plan
description: 计划阶段 - 为各子变更创建 checkbox 任务清单（含 DoD 验收标准），细化任务到可执行粒度。必须阶段，输入来自变更级 detailed-design.md 相关章节。任务采用功能点级全展开形式，每功能点包含 4 维验收标准。阶段钩子引用 `skills/kflow-plan/references/hooks.md`（不需要服务，RELOAD：detailed-design.md, .status.md）。
license: MIT
triggers:
  - 任务计划
  - 任务清单
  - 实现计划
allowed-tools:
  - Agent
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
```

---

## 门控检查

> **机制说明**：门控规则定义在 [core-mechanisms/03-status-and-tasks.md](../core-mechanisms/03-status-and-tasks.md#34-门控规则)

进入计划阶段前检查：
- .status.md 存在
- 详细设计状态 = ✅ 完成
- 变更级 detailed-design.md 文件或 detailed-design/index.md 目录索引存在（不再检查子变更 detailed-design.md）
- 设计审查产物按变更档位分支：轻量档 → cross-reviews/{timestamp}/synthesis.md 存在且标记审查通过；标准档 → 两份视角报告（business-technical-review.md、security-quality-review.md）+ synthesis.md 存在且标记审查通过；完整档 → 四视角审查状态均 = ✅ 完成 + cross-reviews/ 四份视角报告存在 + 最新批次 synthesis.md 标记审查通过
- detailed-design.md 中 NFR 章节包含至少 1 项性能需求和 1 项安全需求
- 变更级 `.status.md` 的「阶段适用性声明」区已读取（仅轻量档；声明区缺失或非轻量档时按全部阶段适用处理），轻量档下判为 `⏭️ 不适用` 的阶段其输入产物不存在属合法跳过

---

## 输入要求

| 产物 | 文件 | 图例 | 适用SC类型 | 说明 |
|------|------|------|-----------|------|
| 变更级 detailed-design.md（或 detailed-design/index.md） | detailed-design.md | ✅ 必须 | 全部 | 统一详细设计（读取属于当前子变更的章节，适配单文件或目录两种形态） |
| 变更级 functional-designs/ | functional-designs/index.md | ✅ 必须 | 全部 | 功能设计文档（业务规则和表单项定义） |
| 变更级 api-tests/ | api-tests/index.md | ✅ 必须（轻量档：🔶 条件适用） | 全部 | 统一接口测试用例；`变更档位 = 轻量` 且适用性声明判 `接口单元测试` 为 `⏭️ 不适用` 时该产物不存在属合法跳过（无接口用例可映射） |
| CONTEXT.md | CONTEXT.md | ✅ 必须 | 全部 | 项目级领域词汇表，用于任务描述对齐 |
| traceability.md | traceability.md | ✅ 必须 | 全部 | 覆盖追溯矩阵，验证FP覆盖 |
| 变更级 e2e-tests/ | e2e-tests/index.md | 🔶 条件 | 前端子变更 | 前后端项目需要，后端子变更不适用 |
| 产品级原型清单 | docs/designs/prototypes/manifest.md | ✅ 必须 | 前端子变更 | 全产品原型清单（含页面结构、设计令牌的文件路径），前端子变更输入源 |
| 变更级原型改动清单 | prototype-changes.md | ✅ 必须 | 前端子变更 | 本变更对产品级原型目录的改动清单，界定前端子变更的转译范围 |

---

## 输出产物

| 产物 | 文件 | 模板 | 图例 | 内容要求 |
|------|------|------|------|---------|
| 子变更任务清单 | subchanges/*/tasks.md | [子变更任务清单](../../templates/subchanges/{subchange}/subchange-tasks.md) | ✅ 必须 | Checkbox 格式任务列表，含 DoD 验收标准 |
| 自审报告 | self-reviews/plan/ | — | 🔶 条件 | 收敛驱动自审报告，份数 ≥ 1（份数 = 收敛实际发生的轮次，无上限；份数为 0 判缺项），下限恒为 1 轮，见证轮收敛即终止，文件名格式：`{YYYYMMDD}-{HHMMSS}.md` |
| 状态文件更新 | .status.md | [子变更状态文件](../../templates/subchanges/{subchange}/subchange-status.md) | ✅ 必须 | 标记计划阶段完成 |

---

## 执行流程

```
计划阶段流程:

┌─────────────────────────────────────────────────────────────┐
│                     PLAN WORKFLOW                            │
├─────────────────────────────────────────────────────────────┤
│  1. PRE_HOOK  → 引用 `skills/kflow-plan/references/hooks.md` plan 阶段 PRE_HOOK (轻量) │
│  │   ├── CHECK_STATE → 验证前置阶段状态                       │
│  │   └── RELOAD → 重读 detailed-design.md, .status.md          │
│  │   └── 不需要服务                                            │
│  2. CHECK     → 门控检查                                      │
│  3. READ      → 读取变更级 detailed-design.md  + FP 类型前置校验    │
│  │   3a. 读取 functional-designs/index.md 获取本子变更 FP 类型        │
│  │   3b. 校验: 后端子变更含前端FP→🟡警告 / 前端子变更含后端FP→🟡警告  │
│  │   3c. 警告 SHALL NOT 阻塞 tasks.md 生成（向后兼容）                 │
│  │   3d. FP 类型一致性校验结果写入 tasks.md 子变更信息段               │
│  4. SPLIT     → 为每个子变更拆分任务到原子级                  │
│  5. DOD       → 为每功能点编写 DoD 验收标准                   │
│  6. ORDER     → 确定任务执行顺序（考虑依赖）                  │
│  7. OUTPUT    → 为每个子变更输出 tasks.md（含DoD）            │
│  8. VERIFY    → 验证任务覆盖所有功能点和验收标准              │
│  8.5 SELFREV  → 收敛驱动自审（重复制:每轮全4维度，子代理串行）  │
│  │   下限 1 轮 / 不设轮数上限（轮数由收敛决定，见证轮收敛即止）  │
│  │   每轮: 启动独立 Agent(subagent) 子代理                    │
│  │   子代理全四维度独立检查（任务覆盖/DoD正确性/HITL标注/任务粒度）│
│  │   报告路径: self-reviews/plan/{YYYYMMDD}-{HHMMSS}.md        │
│  9. COMPLETE  → 更新状态文件                                  │
│ 10. POST_HOOK → 引用 `skills/kflow-plan/references/hooks.md` plan 阶段 POST_HOOK (轻量) │
│  │   └── UPDATE_STATE → 更新 .status.md                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 任务细化规则

### 任务粒度标准

| 粒度 | 判断标准 | 示例 |
|------|---------|------|
| 过粗 | 包含多个独立操作 | "实现用户服务" ❌ |
| 合适 | 2-5 分钟可完成 | "编写注册接口测试" ✅ |
| 过细 | 实现细节级别 | "添加一行代码" ❌ |

### 后端 FP / 前端 FP 区分

Plan 阶段 SHALL 根据子变更类型区分后端功能点和前端功能点，使用不同的任务模板：

| FP 类型 | 子变更类型 | 任务模板 | 验证方式 |
|--------|-----------|---------|---------|
| 后端 FP | 后端子变更 | TDD 模板（Red → Green → Refactor） | 单元测试 + 接口测试 |
| 前端 FP | 前端子变更 | 原型转译模板（输入源 + 5 步实现） | 视觉对账 + Playwright 交互验证 |

**前端 FP 判定条件**：涉及页面/组件/路由/状态管理/样式/CSS 变量注入等功能点，归属到前端子变更。

**后端 FP 判定条件**：涉及 API 实现/服务逻辑/数据模型/数据库操作/业务规则等功能点，归属到后端子变更。

### FP 类型前置校验

> **版本**: 当前变更新增

进入 SPLIT 任务拆分前，SHALL 读取 functional-designs/index.md 中本子变更包含的 FP 类型进行校验：

```
1. 读取 functional-designs/index.md FP 清单「类型」列
2. 筛选本子变更包含的 FP 记录
3. 校验:
   ├── 后端子变更 含「前端」FP → 🟡 警告：「后端子变更 {name} 包含前端 FP: {fp-list}，请回退到 design 阶段重新划分」
   ├── 前端子变更 含「后端」FP → 🟡 警告：「前端子变更 {name} 包含后端 FP: {fp-list}，请回退到 design 阶段重新划分」
   └── 全部一致 → ✅ 通过
4. 警告 SHALL NOT 阻塞 tasks.md 生成（向后兼容），但 SHALL 记录在 tasks.md 子变更信息段
5. 类型列缺失（旧版文档）→ 🟡 警告，提示重新执行 kflow-explore REVISION
```

### 功能点级全展开形式（后端 FP）

每个后端功能点采用全展开形式，包含 TDD 循环步骤：

```markdown
### 功能点 {n}: {功能点描述}

#### DoD 验收标准

| 维度 | 验收标准 | 状态 |
|------|---------|------|
| Happy Path | {正常流程验收条件，至少1项} | ⏳ |
| Error Path | {异常流程验收条件，至少2项} | ⏳ |
| Edge Case | {边界条件验收条件，至少1项} | ⏳ |
| Quality | {质量验收条件，至少1项} | ⏳ |

#### 实现任务

- [ ] **Step 1: 编写测试用例代码**
  {测试代码片段或测试用例描述}

- [ ] **Step 2: 运行测试，确认失败**
  命令: {测试命令}
  预期: FAIL

- [ ] **Step 3: 实现最小代码**
  {实现描述}

- [ ] **Step 4: 运行测试，确认通过**
  命令: {测试命令}
  预期: PASS

- [ ] **Step 5: 检查代码质量**
  检查是否符合编码规范

- [ ] **Step 6: 执行必要重构（可选）**
  {重构描述，如需要}

- [ ] **Step 7: 确认重构后测试仍通过**
  命令: {测试命令}
  预期: PASS
```

### 功能点级全展开形式（前端 FP）

每个前端功能点采用「原型转译」模板，区别于后端 TDD 模板：

```markdown
### 前端功能点 {n}: {页面/组件描述}

#### 输入源
- 原型页面: 从 docs/designs/prototypes/manifest.md 获取页面清单，并以 prototype-changes.md 界定本变更涉及页面
- 设计约束: 从 docs/designs/prototypes/manifest.md 获取（设计令牌、共享资源）+ 变更级 element-coverage-tree.md
- API 契约: detailed-design.md §{api-section}

#### 实现步骤
- [ ] **Step 1: 实现组件骨架**
  搭建组件结构（HTML/JSX 结构），对齐原型 {page}.html 的布局分区和元素层级
  
- [ ] **Step 2: 注入设计令牌**
  替换硬编码样式值为 CSS 变量（var(--xxx)），对齐 design-tokens.css 中的设计令牌
  
- [ ] **Step 3: 实现交互状态**
  覆盖 element-coverage-tree.md 中该页面的所有 🎯 状态：
  hover / active / focus / disabled / loading / empty / error
  实现弹窗/抽屉的打开和关闭逻辑（对齐原型中的操作链定义）

- [ ] **Step 4: 对接 API**
  基于 API 契约使用 mock 数据开发，后端编码完成后替换为真实 API

- [ ] **Step 5: 按原型验证一致性**
  手动对照 docs/designs/prototypes/screens/{page}.html 验证视觉一致性和交互行为
```

**前端 FP 验收标准**（区别于后端 DoD）：

| 维度 | 验收标准 | 说明 |
|------|---------|------|
| 视觉一致性 | 组件视觉效果与原型一致 | 手动对照 docs/designs/prototypes/screens/{page}.html |
| 设计令牌 | 无硬编码颜色值/间距/圆角 | 全部使用 var(--xxx) |
| 交互状态 | 所有 🎯 状态已实现 | hover/active/focus/disabled/loading/empty/error |
| 路由对齐 | 路由结构与 element-coverage-tree.md 📄 节点一致 | 页面可达，导航合理 |

---

## DoD 验收标准编写规则

### 四维验收

| 维度 | 最小数量 | 说明 | 示例 |
|------|---------|------|------|
| Happy Path | ≥ 1 | 正常业务流程验收 | "用户输入有效邮箱和密码，注册成功" |
| Error Path | ≥ 2 | 异常和错误处理验收 | "输入已注册邮箱，提示已存在"、"密码长度不足8位，提示格式错误" |
| Edge Case | ≥ 1 | 边界条件验收 | "邮箱长度超过100字符，提示输入过长" |
| Quality | ≥ 1 | 质量属性验收 | "注册接口 P95 响应时间 < 500ms" |

### 验收标准格式

每条验收标准使用 WHEN/THEN 格式：

```markdown
- Happy Path: WHEN 用户输入有效用户名和密码 THEN 系统返回 JWT token 且用户状态为已激活
- Error Path: WHEN 用户输入已被注册的邮箱 THEN 系统返回 409 Conflict 且提示"邮箱已注册"
- Error Path: WHEN 用户密码长度 < 8 位 THEN 系统返回 400 Bad Request 且提示"密码长度至少8位"
- Edge Case: WHEN 用户邮箱长度 = 255 字符 THEN 系统正常处理（边界值测试）
- Quality: WHEN 并发 100 个注册请求 THEN 无数据损坏且所有请求正确处理
```

### 任务覆盖标准

| 检查项 | 要求 |
|--------|------|
| 功能点覆盖 | 所有设计文档中的功能点都有对应任务 |
| 测试先行 | 每功能点包含测试编写和测试执行步骤 |
| TDD 循环 | 包含 Red → Green → Refactor 完整流程 |
| DoD 覆盖 | 每功能点包含 Happy Path + Error Path(≥2) + Edge Case(≥1) + Quality(≥1) |

---

## HITL 子变更决策点标注

当子变更在 detailed-design.md 中被标记为 HITL 执行类型时，任务清单 SHALL 在相应位置标注决策点。

### 决策点标注格式

在子变更任务清单的「子变更信息」表格中增加执行类型行：

```markdown
## 子变更信息
- **所属变更**: {change-name}
- **功能点数**: {数量}（≤10）
- **执行类型**: AFK / HITL
- **优先级**: {高|中|低}
- **依赖子变更**: {依赖子变更列表或"无"}
- **当前阶段**: {阶段名称}
```

### HITL 决策点清单

HITL 子变更 SHALL 在任务清单中包含决策点列表：

```markdown
## HITL 决策点

| 序号 | 决策点位置 | 决策内容 | 选项 | 默认建议 |
|------|-----------|---------|------|---------|
| D1 | 编码 Step 3 前 | 缓存方案选择: Redis vs Memcached | A: Redis（持久化+丰富数据类型） / B: Memcached（更简单） | A: Redis（推荐） |
| D2 | 编码 Step 5 后 | 接口分页方式确认 | A: 偏移分页 / B: 游标分页 | A: 偏移分页（实时性要求不高） |
```

### 前端子变更依赖标注规则

前端子变更 SHALL 标注「依赖 API 契约」而非「依赖后端子变更编码完成」：

```markdown
## 子变更信息
- **依赖**: API 契约（detailed-design.md §接口设计）
- **依赖约束**: 不要求后端子变更状态为 ✅ 完成，前端子变更可与后端子变更并行启动
```

**前端子变更的依赖判定**：
- 依赖条件: detailed-design.md 中对应 API 契约章节存在且状态为 ✅ 完成
- 不依赖: 后端子变更编码状态
- 并行策略: 使用 mock 数据开发，后端子变更编码完成后替换 mock 为真实 API

### 决策点任务标识

在实现任务列表中，HITL 决策点使用 `[HITL]` 前缀标注：

```markdown
- [ ] **Step 2: 运行测试，确认失败**
- [ ] **[HITL D1] 决策点: 缓存方案选择** — 暂停等待用户确认
- [ ] **Step 3: 根据决策实现代码**
```

---

## 子变更任务清单格式

任务清单格式定义在 [core-mechanisms/03-status-and-tasks.md](../core-mechanisms/03-status-and-tasks.md#42-子变更任务清单格式)，包含：

- 子变更信息（所属变更、功能点数、执行类型、依赖等）
- 功能点清单表
- HITL 决策点清单（HITL 子变更时）
- 每功能点验收标准区块（后端 FP：4 维 DoD 验收 / 前端 FP：4 维视觉验收）
- 实现任务列表（后端 FP：TDD 流程 / 前端 FP：原型转译 5 步）
- 任务执行记录

### 前端子变更任务结构示例

```markdown
# 子变更任务清单：frontend-implementation

## 子变更信息
- **所属变更**: {change-name}
- **功能点数**: {n}（≤10）
- **执行类型**: AFK
- **子变更类型**: 前端子变更
- **依赖**: API 契约（detailed-design.md §接口设计），无后端子变更编码完成依赖
- **优先级**: 高
- **当前阶段**: 计划

## 功能点清单

| 序号 | 功能点 | 关联功能点 | 状态 |
|------|--------|-----------|------|
| 1 | 全局布局（Header/Sidebar/Footer） | — | ⏳ |
| 2 | 登录页面 | FP1 | ⏳ |
| 3 | 仪表盘页面 | FP1 | ⏳ |

---
### 前端功能点 1: 全局布局组件

#### 输入源
- 原型页面: 从 docs/designs/prototypes/manifest.md 获取
- 设计约束: 从 docs/designs/prototypes/manifest.md 与变更级 prototype-changes.md 获取

#### 实现步骤
- [ ] Step 1: 搭建布局骨架（Header/Sidebar/Footer 组件结构）
- [ ] Step 2: 注入设计令牌（var(--color-xxx), var(--spacing-xxx)）
- [ ] Step 3: 实现交互状态（Sidebar 折叠/展开、Header 导航高亮）
- [ ] Step 4: 配置路由框架（对齐 element-coverage-tree.md 📄 节点）
- [ ] Step 5: 按原型验证一致性
```

---

## 重复制执行模型

> ⚠ **子代理强制规则**（参见 skills/kflow-plan/references/repetition.md §12）：本阶段（计划）主工作 MUST 通过 Agent 子代理执行，主 Agent 仅负责调度和验收，SHALL NOT 直接执行计划主工作（任务拆分/DoD编写/任务审查等），无例外。子代理崩溃时轮次级重试（≤3 次），全部失败标记 ⚠️ 阻塞。

> **本节与「SELFREV 自审（步骤 8.5）」描述同一个循环**——计划阶段的迭代与自审不可分割，其收敛终止模型、4 个审查维度、轻量档产物门控与强制执行规则均定义在 SELFREV 一节，本节不另立第二套规则。计划阶段的循环为**产物自审**，采用与设计自审一致的收敛驱动口径：轮次下限恒为 1 轮、不设轮数上限，轮数由收敛实际发生在第几轮决定。

> 终止模型（见证轮四项判据 / 审查范围冻结 / 不收敛判定 / 终止结果二值）权威定义在 `convergence-driven-repetition` 能力；本文件 SHALL NOT 自定义轮次数值或终止条件。

> 通用规范（复杂度公式、轮次执行细节、prompt 规范、审查范围冻结、验证门控）参见 `skills/kflow-plan/references/repetition.md`

### 阶段特定参数

- **遍历项**：全部子变更 tasks.md（轻量档恒为 1 个子变更，本项即该唯一子变更；轮次下限恒为 1，每轮均须全量遍历）
- **每轮工作**：对每个子变更执行 4 维度全量检查（任务覆盖完整性 / DoD 验收标准正确性 / 子变更类型标注准确性 / 任务粒度合理性）
- **轮数**：下限恒为 1 轮、不设轮数上限（轮数由收敛实际发生在第几轮决定）；变更档位只决定每轮审查形态与产出深度。回退重执行 SHALL NOT 预置或提高轮数
- **复杂度权重**：功能点数 × 1 + 接口数 × 1.5 + 场景数 × 2
- **产物要求**：traceability.md「计划」列更新，所有子变更 tasks.md 格式正确，功能点覆盖 = 100%

---

## SELFREV 自审（收敛驱动）

> **版本**: 2.2.0 新增，2.8.0 弹性化，当前变更改为收敛驱动

### 概述

计划阶段在 VERIFY 步骤（步骤 8）之后、COMPLETE 步骤（步骤 9）之前，执行自循环审查（SELFREV）。**轮次下限恒为 1 轮（无例外）、不设轮数上限**——轮数由收敛实际发生在第几轮决定；变更档位只决定**每轮审查形态与产出深度**，SHALL NOT 决定轮数。自审由子代理（Agent subagent）串行执行，采用重复制——每轮子代理独立执行全部四个定制维度（任务覆盖完整性/DoD 验收标准正确性/子变更类型标注准确性/任务粒度合理性）。自审启动前 SHALL 读取变更级 `.status.md` 的「变更档位」字段。

**见证轮与不收敛终止**：某轮同时满足见证轮四项判据——(a) 零新发现、(b) 零修复零修改、(c) 报告证明全部 4 个维度与全部审查对象已完成全量遍历、(d) 累积未复核修复清单内全部条目逐项复核通过——时终止，终止结果 `收敛`。命中不收敛判定（无进展 / 振荡 / 安全丝）时终止，终止结果 `未收敛`，进入非收敛分支并升级用户（记录 `docs/skill-suggestion.md` + AskUserQuestion + 可标记 ⚠️ 阻塞）。**审查范围冻结**：主 Agent 每轮从阶段产物既有内容生成审查对象集合并冻结，审查维度限于四维度枚举；冻结范围之外的发现降级为「范围外观察」——不改产物、不计入本轮新发现数、不阻断收敛，越界轮 SHALL NOT 判为见证轮。机制权威定义见 `convergence-driven-repetition` 能力，落地表述见 `skills/kflow-plan/references/self-review.md`。

> 档位字段缺失时按 `完整` 档处理（审查形态与产出深度按完整档）。

> **机制说明**：终止模型（见证轮四项判据 / 审查范围冻结 / 不收敛判定 / 终止结果二值）与产物门控规则定义在 `convergence-driven-repetition` 能力；本文件 SHALL NOT 自定义轮次数值或终止条件。

> **子代理隔离规则**：自审子代理意外停止/报错/要求重做时，主代理 MUST 重新创建子代理，SHALL NOT 接管自审执行。详见 `skills/kflow-plan/references/repetition.md` §12。

### 收敛驱动的轮次与审查范围冻结

| 项 | 取值 |
|----|------|
| 轮次下限 | **1 轮**（无例外；SHALL NOT 存在 0 轮豁免路径） |
| 轮数上限 | **无**——轮数由收敛实际发生在第几轮决定 |
| 成功终止 | **见证轮**（四项判据）为唯一成功终止条件，终止结果 `收敛` |
| 失败终止 | 命中不收敛判定（无进展 / 振荡 / 安全丝）→ 终止结果 `未收敛` → 非收敛分支 |
| 评分底线 | 仅 `完整` 档适用：各维度评分均 > 8 且该轮构成见证轮方为收敛；评分 ≤ 8 时该轮须列出该维度对应的具体问题项 |

**审查范围冻结与范围外观察**：主 Agent 每轮从阶段产物既有内容生成审查对象集合并冻结，审查维度限于四维度枚举；子代理 SHALL NOT 扩大审查对象集合、SHALL NOT 新增审查维度、SHALL NOT 借审查之名新增功能点/字段/章节/分支。冻结范围之外的发现 SHALL 记为「范围外观察」——不改产物、不计入本轮新发现数、不阻断收敛，写入该轮自审报告的「范围外观察」小节；引入范围外新内容的轮次 SHALL NOT 判为见证轮，主 Agent SHALL 拒收该轮并要求在冻结范围内重审。主 Agent SHALL 在阶段终止时汇总范围外观察条目并向用户提示。

### 轻量档至少 1 轮自审与产物门控

轻量档 SHALL 至少执行 1 轮自审——SHALL NOT 跳过 SELFREV、SHALL NOT 豁免自审子代理启动、SHALL NOT 豁免自审报告产出，**不存在 0 轮豁免路径**；轮数 SHALL NOT 因档位限制为 1 轮。`self-reviews/plan/` 目录下 SHALL 产出至少 1 份自审报告（`{YYYYMMDD}-{HHMMSS}.md`，份数为 0 判缺项）。产物完整性门控 SHALL 保留为**附加硬门**：本阶段产物 SHALL 全部存在且不含 TODO、TBD 或未填充占位符；任一产物缺失或含占位符时该阶段阻塞。审计 SHALL NOT 因轻量档自审报告仅 1 份、或自审轮数少于任何数值而判定为缺项。

### 审查维度

| 维度 | 说明 | 关键检查项 |
|------|------|-----------|
| 任务覆盖完整性 | 所有 FP 是否有对应任务 | FP 覆盖 = 100%、TDD 7 步骤完整、测试用例映射正确 |
| DoD 验收标准正确性 | WHEN/THEN 格式和语义 | 四维覆盖（Happy≥1/Error≥2/Edge≥1/Quality≥1）、标准可达性 |
| HITL 标注准确性 | 决策点标注是否完整 | 决策点列表完整性、任务标识 `[HITL D{n}]`、AFK 判定验证 |
| 任务粒度合理性 | 任务是否 2-5 分钟可完成 | 粒度不过粗不过细、依赖合理性 |

### 执行流程

```
SELFREV 自审（子代理串行 + 重复制，收敛驱动）:

1. 读取变更级 .status.md 的「变更档位」字段（缺失按 完整 档处理）
2. 档位只决定每轮审查形态与产出深度，SHALL NOT 决定轮数（下限恒为 1 轮，无轮数上限）
3. 主 Agent 启动子代理 → 子代理全四维度检查 → 修复 + 报告
4. 主 Agent 读报告 + 确认 + 判定本轮是否为见证轮（四项判据：(a) 零新发现、(b) 零修复零修改、(c) 全量遍历证明、(d) 累积未复核修复清单全部条目逐项复核通过）→ 未收敛则启动下一轮（第 2 轮起注入前轮摘要）
5. 轮次控制：见证轮 → 终止（终止结果 收敛）；命中不收敛判定（无进展 / 振荡 / 安全丝）→ 终止（终止结果 未收敛）→ 非收敛分支
5.5 越界轮判定：引入范围外新内容的轮次 → 主 Agent 拒收并要求在冻结范围内重审（该轮 SHALL NOT 判为见证轮）
6. 报告路径: self-reviews/plan/{YYYYMMDD}-{HHMMSS}.md；终止后在 .status.md 写入终止结果（收敛 / 未收敛）
```

### 强制执行规则

- 全部档位 SHALL 至少执行 1 轮自审，SHALL NOT 存在 0 轮豁免路径
- 轻量档 SHALL 执行至少 1 轮；轮数 SHALL NOT 因档位限制为 1 轮，达成见证轮即终止
- 轮数 SHALL NOT 被预置或限制为任何数值；完整档各维度评分均 > 8 且该轮构成见证轮方为收敛；任一维度 ≤ 8 时该轮须列出该维度对应的具体问题项（不构成见证轮）
- 审查对象集合 SHALL 由主 Agent 每轮从阶段产物既有内容生成并冻结，审查维度限于四维度枚举；子代理 SHALL NOT 扩大审查对象集合、SHALL NOT 新增审查维度
- 冻结范围之外的发现 SHALL 记为「范围外观察」，SHALL NOT 在本轮修复、SHALL NOT 计入本轮新发现数、SHALL NOT 阻断收敛；引入范围外新内容的轮次 SHALL NOT 被判定为见证轮
- 命中不收敛判定（无进展 / 振荡 / 安全丝）时 SHALL 终止并升级用户，终止结果 `未收敛`
- SHALL NOT 为凑轮数而继续执行无增量价值的轮次
- SHALL 每轮启动独立子代理（Agent subagent），不允许主 Agent 自身执行自审，SHALL NOT 由主 Agent 接管
- SHALL NOT 并行启动多个子代理（串行执行）

---

## 与其他 Skill 的关系

- **输入来自**：`kflow-design`（详细设计阶段，变更级）
- **输出给**：`kflow-code`（编码阶段，子变更级）
- **前置阶段**：详细设计（变更级）
- **后续阶段**：编码（子变更级）
- **执行模式**：收敛驱动的重复制，轮次下限恒为 1 轮、不设轮数上限（轮数由收敛实际发生在第几轮决定），回退重执行 SHALL NOT 预置或提高轮数（参见 skills/kflow-plan/references/repetition.md §14），复杂度评估仅信息展示，主 Agent 验收闭环
- **自审轮次**：不设轮数上限（下限恒为 1 轮，见证轮四项判据收敛即终止，终止结果二值 `收敛` / `未收敛`），参见本文件 §SELFREV 自审

---

## 反馈机制

如果在使用本 Skill 过程中发现问题或有优化建议，请记录到 `docs/skill-suggestion.md` 文件中。
