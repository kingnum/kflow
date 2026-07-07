---
name: kflow-resume
version: 0.16.0
description: Use when user needs to resume interrupted work/继续、恢复、resume {change-name}, or when kflow-guide routes to RESUME mode.
license: MIT
triggers:
  - 继续 {change-name}
  - 恢复 {change-name}
  - resume {change-name}
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Skill
---

# 角色

中断恢复执行器。通过变更标识名称精确恢复中断的变更执行。读取状态文件和 checkpoint 定位断点，输出五问题快速摘要后直接调度对应阶段 Skill 继续执行。变更名定位断点，优先级链读取状态（checkpoint 优先），断点定位（确定阶段+子变更+待执行任务+回退处理），快速门控验证，输出恢复摘要，服务恢复检测（E2E/集成测试阶段），直接调度阶段 Skill。

# 任务

变更存在性验证 -> 优先级链读取状态（checkpoint > .status.md > tasks.md）-> 定位断点（阶段+子变更+待执行任务+回退处理）-> 快速门控验证 -> 输出五问题快速摘要 -> 详细恢复信息 -> 服务恢复检测（仅 E2E/集成测试阶段）-> 直接调度阶段 Skill。

# 门控检查

此阶段为按需恢复阶段，无前置门控要求。但执行时进行以下验证：

| 检查项 | 检查方式 | 失败处理 |
|--------|---------|---------|
| 变更目录存在性 | `Bash: test -d docs/changes/{change}/` | 报错：变更不存在 |
| 归档状态 | `Glob: docs/archive/*/` 搜索变更名 | 报错：变更已归档，无法恢复 |

# 输入要求

| 产物 | 图例 | 说明 |
|------|------|------|
| 变更标识名称 | ✅ 必须 | kebab-case 格式，如 `add-user-auth` |
| 变更目录 | ✅ 必须 | `docs/changes/{change}/` 必须存在且未归档 |

# 输出产物

在对话中输出恢复摘要，不产生新文件。

| 产物 | 说明 | 图例 |
|------|------|------|
| 五问题快速摘要 | 一屏内确认恢复状态（≤15行） | ✅ 必须 |
| 详细恢复信息 | 变更描述、类型、当前阶段、进度概览、流程位置图、待执行任务列表 | ✅ 必须 |
| 阶段调度 | 直接调用对应阶段 Skill | ✅ 必须 |

# 执行流程

## 总流程

```
VERIFY(存在性验证) -> STATE(优先级链读状态) -> LOCATE(断点定位) -> GATE(门控验证)
    -> SUMMARIZE(五问题摘要) -> SERVICE(服务检测) -> DISPATCH(调度阶段Skill)
```

```
┌─────────────────────────────────────────────────────────────────┐
│                       RESUME WORKFLOW                            │
├─────────────────────────────────────────────────────────────────┤
│  1. VERIFY     变更存在性验证                                    │
│     ├── docs/changes/{change}/ 目录存在？                        │
│     ├── 不在 docs/archive/ 下？                                  │
│     ├── 不存在 -> 报错：变更不存在                               │
│     └── 已归档 -> 报错：变更已归档，无法恢复                     │
│  2. STATE      按优先级链读取状态                                 │
│     ├── 优先: subchanges/*/checkpoints/（最近时间）              │
│     ├── 其次: checkpoints/（变更级）                             │
│     ├── 再次: subchanges/*/.status.md（子变更级）                │
│     ├── 再次: .status.md（变更级）                               │
│     └── 最后: tasks.md（checkbox 状态反推）                      │
│  3. LOCATE     定位恢复断点                                      │
│     ├── 确定当前阶段                                             │
│     ├── 确定当前子变更（子变更级阶段时）                          │
│     ├── 确定待执行任务列表（未勾选 checkbox）                     │
│     └── 处理阶段回退状态（⚠️ 需修订 -> 回退目标阶段）           │
│  4. GATE       快速门控验证 + 产物完整性验证                   │
│     ├── 检查前置阶段产物是否存在                                  │
│     ├── 检查前置阶段状态是否为 ✅ 完成                            │
│     ├── 产物完整性验证（对已完成阶段二次校验）                    │
│     │   ├── 执行轮次 = N / N（N 由弹性轮次决策确定）                  │
│     │   ├── 产物文件存在性                                       │
│     │   └── traceability 覆盖率达标                              │
│     ├── 门控通过 -> 继续                                         │
│     └── 门控失败 -> 提示先完成前置阶段                            │
│  5. SUMMARIZE  输出恢复摘要                                      │
│     ├── 五问题快速摘要（≤15行）                                   │
│     └── 详细恢复信息（流程位置图+待执行任务）                    │
│  6. SERVICE    服务恢复检测（仅 E2E 测试/集成测试阶段）          │
│     ├── 检测服务状态: curl localhost:{port}                       │
│     ├── 服务不可用 -> 变更级 agent 执行编译重启                   │
│     ├── 跳过已在 migration-log.md 标记为「已执行」的迁移         │
│     └── 健康检查通过后继续                                        │
│  7. DISPATCH   直接调度阶段 Skill                                │
│     ├── 阶段 = ❌ 阻塞 -> 输出阻碍信息，不调度                   │
│     ├── 阶段 = ⚠️ 需修订 -> 按调度映射调度回退目标阶段          │
│     └── 正常 -> 按调度映射表调度对应阶段 Skill                    │
└─────────────────────────────────────────────────────────────────┘
```

## 步骤 1：VERIFY — 变更存在性验证

```
验证逻辑:

1. 构建变更目录路径: docs/changes/{change}/
2. 检查目录存在性 (Bash: test -d)
3. 检查归档状态:
   ├── Glob: docs/archive/*/{change}/.status.md 是否存在
   ├── 或 Glob: docs/archive/*-{change}/ 目录是否存在
   └── 已归档 -> 报错
4. 均通过 -> 进入 STATE 步骤
```

## 步骤 2：STATE — 优先级链读取状态

按优先级从高到低读取，一旦命中即停止，不再查更低优先级：

```
Priority 1: Subchange checkpoint（最高精度）
├── Glob: docs/changes/{change}/subchanges/*/checkpoints/*.md
├── 按 timestamp 降序排列，取最新的一个
└── 命中 -> 解析 frontmatter 获取 {status, files_modified, timestamp}

Priority 2: Change-level checkpoint
├── Glob: docs/changes/{change}/checkpoints/*.md
├── 按 timestamp 降序排列，取最新的一个
└── 命中 -> 解析 frontmatter

Priority 3: Subchange .status.md
├── Glob: docs/changes/{change}/subchanges/*/.status.md
├── 读取所有子变更状态
└── 命中 -> 从「当前阶段」和阶段状态矩阵获取

Priority 4: Change .status.md
├── Read: docs/changes/{change}/.status.md
└── 命中 -> 从「当前阶段」字段和阶段状态表获取

Priority 5: tasks.md（兜底）
├── Read: docs/changes/{change}/tasks.md
├── 从 checkbox 状态反推当前阶段
└── 未勾选的最小阶段序号 = 当前阶段
```

## 步骤 3：LOCATE — 断点定位

```
断点定位逻辑:

1. 解析状态来源确定当前阶段:
   ├── checkpoint -> checkpoint 中记录的阶段
   ├── .status.md -> 「当前阶段」字段
   └── tasks.md -> 第一个有未勾选任务的阶段

2. 确定断点层级:
   ├── 变更级阶段（设计探索、原型设计、详细设计、集成测试、归档）
   │   └── 从变更级 tasks.md 获取待执行列表
   └── 子变更级阶段（计划、编码、代码审查、接口单元测试、E2E测试）
       ├── 确定当前活跃子变更（第一个状态为 🔄 的子变更）
       └── 从子变更 tasks.md 获取未勾选的功能点任务

3. 阶段回退状态处理:
   ├── 当前阶段 = ⚠️ 需修订
   │   ├── 定位回退目标阶段
   │   ├── 回退目标 = 调度目标
   │   └── 汇总受影响子变更
   └── 当前阶段 = ❌ 阻塞
       └── 输出阻碍信息，不调度

4. 待执行任务列表:
   └── 收集目标 tasks.md 中所有 - [ ] 项
```

## 步骤 4：GATE — 快速门控验证 + 产物完整性验证

```
门控验证（按正向门控规则）:

1. 确定当前阶段的进入门控

2. 逐条检查:
   ├── 前置阶段状态 = ✅ 完成？
   ├── 前置阶段产物文件存在？
   ├── (如适用) 审查报告存在？
   └── (如适用) 用户评审已确认？

3. 产物完整性验证（对标记为 ✅ 完成的阶段执行二次校验）:
   ├── 3a. 执行轮次验证:
   │   ├── 读取 .status.md 执行轮次计数器
   │   ├── 执行类阶段（plan/code/code-review/api-test/e2e-test/integration-test/bug-fix）
   │   │   └── 要求: 执行轮次 = N / N（N 由弹性轮次决策确定）
   │   ├── 自审类阶段（explore/prototype/design）
   │   │   └── 要求: 自审轮次 = 10 / 10
   │   └── 验证类阶段（prototype VERIFY）
   │       └── 要求: 导航验证 = 5 / 5, Playwright 验证 = 5 / 5
   ├── 3b. 产物文件存在性:
   │   ├── 设计探索: functional-designs/index.md + part-NN.md + CONTEXT.md
   │   ├── 原型设计: prototype/index.md + design-prompt.md
   │   ├── 详细设计: detailed-design.md + 子变更划分结果
   │   ├── 计划: tasks.md（功能点级全展开）
   │   ├── 编码: 代码变更文件 + migration-log.md（如涉及迁移）
   │   ├── 代码审查: test-reports/review/code-review.md
   │   ├── 接口单元测试: test-reports/api-test/round-*.md + summary.md
   │   ├── E2E 测试: test-reports/e2e/round-*.md + summary.md
   │   └── 集成测试: test-reports/integration/summary.md
   ├── 3c. traceability 覆盖率:
   │   ├── 读取 traceability.md
   │   ├── 检查「编码实现」列覆盖率 = 100%
   │   ├── 检查「接口测试」列覆盖率 = 100%
   │   └── 如有缺失列 → 标记为不完整
   └── 3d. 结果记录:
       ├── 全部通过 → 记录"产物完整性验证通过"→ 继续恢复
       └── 任一项失败 → 记录"产物完整性验证未通过，缺失项: {列表}"
           └── 提示用户：当前变更可能在中断时丢失了部分产物，建议先补充缺失项再继续

4. 门控结果:
   ├── 通过 -> 进入 SUMMARIZE
   └── 失败 -> 输出缺失项，停止恢复
```

## 步骤 5：SUMMARIZE — 输出恢复摘要

### 五问题快速摘要

先输出五问题快速摘要（控制在 15 行以内），再输出详细恢复信息：

```markdown
## 恢复摘要：{change-name}

| 问题 | 回答 |
|------|------|
| 当前位置 | {当前阶段} -> {当前子变更（如适用）} -> {当前功能点（如适用）} |
| 剩余路径 | {未完成阶段按顺序用 -> 连接} |
| 变更目标 | {从 .status.md 的「变更描述」字段获取} |
| 设计依据 | {当前阶段依赖的主要设计文档路径及章节} |
| 已完成 | {已完成数}/{总任务数} 任务 |
```

### 5 个字段定义

| 字段 | 说明 | 数据来源 |
|------|------|---------|
| 当前位置 | 当前阶段 -> 当前子变更（如适用）-> 当前功能点（如适用），逐级细化到可执行的恢复点 | .status.md：当前阶段字段 + 子变更进度矩阵 |
| 剩余路径 | 按顺序列出未完成的阶段（用 -> 连接），仅显示当前变更剩余阶段 | .status.md：阶段状态表（筛选 ⏳ 待开始） |
| 变更目标 | 一句话描述变更的核心目标 | .status.md：变更描述字段 |
| 设计依据 | 指向当前阶段依赖的主要设计文档及章节号 | 按当前阶段映射（见下表） |
| 已完成 | 当前级别的任务完成统计 | 子变更级：子变更 tasks.md checkbox 统计；变更级：变更 tasks.md checkbox 统计 |

### 设计依据映射规则

| 当前阶段 | 设计依据指向 |
|---------|-------------|
| 设计探索 | `functional-designs/index.md` |
| 原型设计 | `functional-designs/index.md` + `prototype/index.md` |
| 详细设计 | `functional-designs/index.md` |
| 计划 | `detailed-design.md` 子变更划分章节 |
| 编码 | `detailed-design.md` 对应功能点的技术设计章节 |
| 代码审查 | `detailed-design.md` NFR 章节 |
| 接口单元测试 / E2E 测试 | `detailed-design.md` + `api-tests/` 或 `e2e-tests/` |
| 集成测试 | `detailed-design.md` + `integration-tests/` |
| 审计 | `detailed-design.md` NFR 章节 + 审查报告 |
| 归档 | 所有设计文档 |

### 摘要输出规则

| 规则 | 说明 |
|------|------|
| 输出位置 | 五问题摘要 SHALL 在详细恢复信息之前展示 |
| 长度控制 | 摘要 SHALL 控制在 15 行以内，使用简洁表格格式 |
| 字段完整性 | 5 个字段 SHALL 全部填写，暂无数据的字段填 `—` |
| 详细输出保留 | 五问题摘要之后 SHALL 继续输出完整的恢复流程信息 |

### 详细恢复信息

五问题摘要之后输出完整恢复信息：

```markdown
## 中断恢复：{change-name}

### 变更信息

| 字段 | 值 |
|------|-----|
| 变更描述 | {变更描述} |
| 变更类型 | {产品需求/功能需求/功能缺陷} |
| 项目类型 | {前后端项目/纯后端项目} |
| 中断时间 | {checkpoint timestamp 或 "未知"} |

### 恢复断点

| 字段 | 值 |
|------|-----|
| 当前阶段 | {阶段名称} |
| 当前子变更 | {子变更名称 或 "变更级阶段"} |
| 断点来源 | {checkpoint / .status.md / tasks.md} |

### 流程位置

{用 ✅/🔄/⏳/⏭️ 标注各阶段状态}

### 待执行任务

{从 tasks.md 提取的未勾选任务列表}

### 下一步

正在调用 `{target-skill}` 继续执行...
```

## 步骤 6：SERVICE — 服务恢复检测

仅当恢复到 **E2E 测试**或**集成测试**阶段时执行：

```
服务恢复检测流程:

1. 从 .status.md 或 toolchain.md 获取服务端口号
2. 检测服务状态:
   └── curl -s localhost:{port}/health 或 curl -s localhost:{port}
3. 服务不可用:
   ├── 启动变更级 agent
   ├── agent 执行编译构建
   ├── agent 检查 migration-log.md，跳过已执行迁移
   ├── agent 执行待执行的数据库迁移
   └── agent 启动服务
4. 健康检查通过:
   └── curl 返回成功 -> 继续 DISPATCH
5. 服务启动失败:
   └── 输出错误信息，提示用户手动排查
```

跳过规则：
- 跳过已在 `migration-log.md` 标记为「已执行」的迁移
- 跳过未变更模块的服务

## 步骤 7：DISPATCH — 直接调度阶段 Skill

### 调度映射表

| 当前阶段 | 调度 Skill | 上下文 |
|---------|-----------|--------|
| 设计探索 | `kflow-explore` | 变更级 |
| 原型设计 | `kflow-prototype-design` | 变更级 |
| 详细设计 | `kflow-design` | 变更级 |
| 计划 | `kflow-plan` | 子变更级 |
| 编码 | `kflow-code` | 子变更级 |
| 代码审查 | `kflow-code-review` | 子变更级 |
| 接口单元测试 | `kflow-e2e-test` | 子变更级 |
| E2E测试 | `kflow-e2e-test` | 子变更级 |
| 集成测试 | `kflow-integration-test` | 变更级 |
| 审计 | `kflow-audit` | 变更级 |
| 归档 | `kflow-archive` | 变更级 |

### 调度逻辑

```
DISPATCH 调度逻辑:

1. 判断当前阶段状态:
   ├── ✅ 完成 -> 自动推进到下一阶段，递归 DISPATCH
   ├── 🔄 进行中 -> 调度当前阶段 Skill
   ├── ⚠️ 需修订 -> 调度回退目标阶段 Skill
   ├── ❌ 阻塞 -> 输出阻碍信息，不调度
   └── ⏳ 待开始 -> 调度当前阶段 Skill

2. 传递上下文:
   ├── 变更名: 传递给目标 Skill
   ├── 子变更名（如适用）: 传递给目标 Skill
   └── 断点信息: 在调度消息中说明恢复位置

3. 调度方式:
   └── Skill(skill="{target-skill}", args="{change-name}")
```

# 与其他 Skill 的关系

- **由 `kflow-guide` 调用**：guide 识别 RESUME 模式后路由到 resume
- **调用阶段 Skill**：resume 定位断点后直接调度对应阶段 Skill
- **不创建文件**：resume 是纯恢复路由层，不产生持久化产物
- **与 checkpoint 机制协作**：优先使用 checkpoint 定位精确断点，回退到 .status.md 或 tasks.md

# 核心提醒

- **优先级链不可跳过**：checkpoint > .status.md > tasks.md，按顺序读取，一旦命中即停止
- **五问题摘要必须在详细恢复信息之前输出**，控制在 15 行以内
- **E2E/集成测试阶段恢复时检测服务状态**：服务不可用时自动编译重启
- **⚠️ 需修订时调度回退目标阶段**，而非当前标注需修订的阶段
- **❌ 阻塞时不调度**，仅输出阻碍信息
- **✅ 完成时自动推进到下一阶段**，递归 DISPATCH 直到遇到非完成状态
- **断点来源必须明确标注**（checkpoint / .status.md / tasks.md），让用户了解数据可信度
- **产物完整性验证**：GATE 步骤对已完成阶段执行二次校验（执行轮次/产物文件/traceability 覆盖率），防止中断时跳过未完成阶段

# 反馈机制

如果在使用本 Skill 过程中发现问题或有优化建议，请记录到 `docs/skill-suggestion.md` 文件中。
