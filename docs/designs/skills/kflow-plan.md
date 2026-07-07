# kflow-plan（计划阶段）

> **版本**: 参见仓库根目录 `VERSION` 文件
> **阶段**: 计划（必须阶段，子变更级）

---

## 基本信息

```yaml
name: kflow-plan
description: 计划阶段 - 为各子变更创建 checkbox 任务清单（含 DoD 验收标准），细化任务到可执行粒度。必须阶段，输入来自变更级 detailed-design.md 相关章节。任务采用功能点级全展开形式，每功能点包含 4 维验收标准。阶段钩子引用 `skills/kflow-plan/references/hooks.md`（不需要服务，RELOAD: detailed-design.md, .status.md）。
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
- 四视角审查状态均 = ✅ 完成
- cross-reviews/ 最新批次 synthesis.md 存在且标记审查通过
- detailed-design.md 中 NFR 章节包含至少 1 项性能需求和 1 项安全需求

---

## 输入要求

| 产物 | 文件 | 图例 | 适用SC类型 | 说明 |
|------|------|------|-----------|------|
| 变更级 detailed-design.md（或 detailed-design/index.md） | detailed-design.md | ✅ 必须 | 全部 | 统一详细设计（读取属于当前子变更的章节，适配单文件或目录两种形态） |
| 变更级 functional-designs/ | functional-designs/index.md | ✅ 必须 | 全部 | 功能设计文档（业务规则和表单项定义） |
| 变更级 api-tests/ | api-tests/index.md | ✅ 必须 | 全部 | 统一接口测试用例 |
| CONTEXT.md | CONTEXT.md | ✅ 必须 | 全部 | 项目级领域词汇表，用于任务描述对齐 |
| traceability.md | traceability.md | ✅ 必须 | 全部 | 覆盖追溯矩阵，验证FP覆盖 |
| 变更级 e2e-tests/ | e2e-tests/index.md | 🔶 条件 | 前端子变更 | 前后端项目需要，后端子变更不适用 |
| 原型清单 | prototype/index.md | ✅ 必须 | 前端子变更 | 原型清单入口（含页面结构、设计令牌、元素覆盖树的文件路径），前端子变更输入源 |

---

## 输出产物

| 产物 | 文件 | 模板 | 图例 | 内容要求 |
|------|------|------|------|---------|
| 子变更任务清单 | subchanges/*/tasks.md | [子变更任务清单](../../templates/subchanges/{subchange}/subchange-tasks.md) | ✅ 必须 | Checkbox 格式任务列表，含 DoD 验收标准 |
| 自审报告 | self-reviews/plan/ | — | ✅ 必须 | N/N 自审报告（N 由弹性轮次决策确定），文件名格式：`{YYYYMMDD}-{HHMMSS}.md` |
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
│  9. SELFREV   → N/N 自审（子代理串行 + 弹性重复制）            │
│  │   每轮: 启动独立 Agent(subagent) 子代理                    │
│  │   子代理全四维度独立检查（任务覆盖/DoD正确性/HITL标注/任务粒度）│
│  │   报告路径: self-reviews/plan/{YYYYMMDD}-{HHMMSS}.md        │
│ 10. POST_HOOK → 引用 `skills/kflow-plan/references/hooks.md` plan 阶段 POST_HOOK (轻量) │
│  │   └── UPDATE_STATE → 更新 .status.md                       │
│ 11. COMPLETE  → 更新状态文件                                  │
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
- 原型页面: 从 prototype/index.md 获取
- 设计约束: 从 prototype/index.md 获取（设计令牌、元素覆盖树）
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
  手动对照 prototype/{page}.html 验证视觉一致性和交互行为
```

**前端 FP 验收标准**（区别于后端 DoD）：

| 维度 | 验收标准 | 说明 |
|------|---------|------|
| 视觉一致性 | 组件视觉效果与原型一致 | 手动对照 prototype/{page}.html |
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
- 原型页面: 从 prototype/index.md 获取
- 设计约束: 从 prototype/index.md 获取

#### 实现步骤
- [ ] Step 1: 搭建布局骨架（Header/Sidebar/Footer 组件结构）
- [ ] Step 2: 注入设计令牌（var(--color-xxx), var(--spacing-xxx)）
- [ ] Step 3: 实现交互状态（Sidebar 折叠/展开、Header 导航高亮）
- [ ] Step 4: 配置路由框架（对齐 element-coverage-tree.md 📄 节点）
- [ ] Step 5: 按原型验证一致性
```

---

## 重复制（执行类阶段）

> ⚠ **子代理强制规则**（参见 skills/kflow-plan/references/repetition.md §12）：本阶段（计划）主工作 MUST 通过 Agent 子代理执行，主 Agent 仅负责调度和验收，SHALL NOT 直接执行计划主工作（任务拆分/DoD编写/任务审查等），无例外。子代理崩溃时轮次级重试（≤3 次），全部失败标记 ⚠️ 阻塞。

计划阶段属于执行类阶段，采用弹性重复制模式。目标轮次由弹性轮次决策确定（首次执行 10 轮，回退重执行按影响范围分数缩减）。子代理每轮遍历全部子变更 tasks.md，对每个子变更独立执行全部 4 维度检查。

> 通用规范（复杂度公式、轮次执行细节、prompt 规范、弹性轮次决策、验证门控）参见 `skills/kflow-plan/references/repetition.md`

### 阶段特定参数

- **遍历项**：全部子变更 tasks.md
- **每轮工作**：对每个子变更执行 4 维度全量检查（任务覆盖完整性 / DoD 验收标准正确性 / HITL 标注准确性 / 任务粒度合理性）
- **复杂度权重**：功能点数 × 1 + 接口数 × 1.5 + 场景数 × 2
- **产物要求**：traceability.md「计划」列更新，所有子变更 tasks.md 格式正确，功能点覆盖 = 100%

---

## N/N 自审 (SELFREV)

> **版本**: 2.2.0 新增，2.8.0 弹性化

### 概述

计划阶段在 VERIFY 步骤之后、COMPLETE 步骤之前，强制执行 N/N 自循环审查（N 由弹性轮次决策确定，首次执行 N=10，回退重执行按影响范围分数缩减）。自审由子代理（Agent subagent）串行执行，采用重复制——每轮子代理独立执行全部四个定制维度（任务覆盖完整性/DoD 验收标准正确性/HITL 标注准确性/任务粒度合理性）。

> **子代理隔离规则**：自审子代理意外停止/报错/要求重做时，主代理 MUST 重新创建子代理，SHALL NOT 接管自审执行。详见 `skills/kflow-plan/references/repetition.md` §12。

### 审查维度

| 维度 | 说明 | 关键检查项 |
|------|------|-----------|
| 任务覆盖完整性 | 所有 FP 是否有对应任务 | FP 覆盖 = 100%、TDD 7 步骤完整、测试用例映射正确 |
| DoD 验收标准正确性 | WHEN/THEN 格式和语义 | 四维覆盖（Happy≥1/Error≥2/Edge≥1/Quality≥1）、标准可达性 |
| HITL 标注准确性 | 决策点标注是否完整 | 决策点列表完整性、任务标识 `[HITL D{n}]`、AFK 判定验证 |
| 任务粒度合理性 | 任务是否 2-5 分钟可完成 | 粒度不过粗不过细、依赖合理性 |

### 执行流程

```
N/N 自审（子代理串行 + 弹性重复制）:

1. 主 Agent 启动子代理 → 子代理全四维度检查 → 修复 + 报告
2. 主 Agent 读报告 + 确认 → 启动下一轮子代理
3. 串行执行 N 轮（N 由弹性轮次决策确定，首次执行 N=10），不可提前终止
4. 报告路径: self-reviews/plan/{YYYYMMDD}-{HHMMSS}.md
```

### 强制执行规则

- SHALL 完成全部 N 轮自审（N 由弹性轮次决策确定），不允许提前终止
- SHALL 每轮启动独立子代理（Agent subagent），不允许主 Agent 自身执行自审
- SHALL NOT 并行启动多个子代理（串行执行）
- 即使连续多轮无新问题也必须完成全部 N 轮

---

## 与其他 Skill 的关系

- **输入来自**：`kflow-design`（详细设计阶段，变更级）
- **输出给**：`kflow-code`（编码阶段，子变更级）
- **前置阶段**：详细设计（变更级）
- **后续阶段**：编码（子变更级）
- **执行模式**：弹性重复制，目标轮次由弹性轮次决策确定（参见 skills/kflow-plan/references/repetition.md §14），复杂度评估仅信息展示，主 Agent 验收闭环

---

## 反馈机制

如果在使用本 Skill 过程中发现问题或有优化建议，请记录到 `docs/skill-suggestion.md` 文件中。
