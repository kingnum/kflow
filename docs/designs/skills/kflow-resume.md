# kflow-resume（中断恢复）

> **版本**: 参见仓库根目录 `VERSION` 文件
> **阶段**: 中断恢复（按需阶段）

---

## 基本信息

```yaml
name: kflow-resume
description: 中断恢复 - 通过变更标识名称精确恢复中断的变更执行。读取状态文件和 checkpoint 定位断点，输出恢复摘要后直接调度对应阶段 Skill 继续执行。
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
```

---

## 门控检查

此阶段为按需恢复阶段，无前置门控要求。但执行时进行以下验证：

- 变更目录存在性检查（`docs/changes/{change}/`）
- 归档状态检查（不在 `docs/archive/` 下）

---

## 输入要求

| 产物 | 图例 | 说明 |
|------|------|------|
| 变更标识名称 | ✅ 必须 | kebab-case 格式，如 `add-user-auth` |
| 变更目录 | ✅ 必须 | `docs/changes/{change}/` 必须存在且未归档 |

---

## 输出产物

在对话中输出恢复摘要，不产生新文件。核心输出：

| 产物 | 模板 | 说明 |
|------|------|------|
| checkpoint 恢复 | [checkpoint](../../templates/changes/{change}/checkpoint.md) | checkpoint 文件格式定义（恢复时读取 checkpoint 定位断点） |
| 恢复摘要 | N/A（会话输出） | 变更描述、类型、当前阶段、进度概览、待执行任务列表、下一步操作 |
| 阶段调度 | N/A（会话输出） | 直接调用对应阶段 Skill |

---

## 执行流程

> 完整规范参见 `skills/kflow-resume/references/recovery-protocol.md` §3

```
中断恢复流程:

┌─────────────────────────────────────────────────────────────┐
│                    RESUME WORKFLOW                           │
├─────────────────────────────────────────────────────────────┤
│  1. VERIFY    → 变更存在性验证                                │
│  2. STATE     → 按优先级链读取状态                             │
│  3. LOCATE    → 定位恢复断点                                  │
│  4. GATE      → 快速门控验证 + 产物完整性验证                  │
│  5. SUMMARIZE → 输出恢复摘要                                  │
│  6. SERVICE   → 服务恢复检测（仅 E2E 测试/集成测试阶段）      │
│  │   ├── 恢复到 E2E 测试或集成测试阶段时                       │
│  │   ├── 检测服务状态: curl localhost:{port}                  │
│  │   ├── 服务不可用 → 变更级 agent 执行编译重启                │
│  │   ├── 跳过已在 migration-log.md 标记为「已执行」的迁移     │
│  │   └── 健康检查通过后继续                                    │
│  7. DISPATCH  → 直接调度阶段 Skill                            │
│      ├── 阶段 = ❌ 阻塞 → 输出阻碍信息，不调度                │
│      ├── 阶段 = ⚠️ 需修订 → 按调度映射调度回退目标阶段       │
│      ├── 产物验证不通过 → 调度回退到对应阶段重新执行          │
│      └── 正常 → 按调度映射表调度对应阶段 Skill                 │
└─────────────────────────────────────────────────────────────┘
```

> VERIFY/STATE/LOCATE/GATE/SUMMARIZE/DISPATCH 步骤的详细逻辑参见 `skills/kflow-resume/references/recovery-protocol.md`。SERVICE 步骤为本 Skill 特有（测试阶段服务恢复检测）。

---

## VERIFY 步骤详解

> 完整规范参见 `skills/kflow-resume/references/recovery-protocol.md` §3 步骤 1

验证变更目录存在且未归档。

---

## STATE 步骤：读取优先级链

> 完整规范参见 `skills/kflow-resume/references/recovery-protocol.md` §2

按 5 级优先级链查找恢复断点：子变更 checkpoint → 变更级 checkpoint → 子变更 .status.md → 变更级 .status.md → tasks.md checkbox 反推。每层命中后立即使用，不继续向下查找。

---

## LOCATE 步骤：断点定位

```
断点定位逻辑:

1. 解析状态来源确定当前阶段:
   ├── checkpoint → checkpoint 中记录的阶段
   ├── .status.md → 「当前阶段」字段
   └── tasks.md → 第一个有未勾选任务的阶段

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

---

## GATE 步骤：快速门控验证 + 产物完整性验证

> 完整规范参见 `skills/kflow-resume/references/gates.md` §2 规则 9

对 .status.md 标记为「✅ 完成」的每个阶段执行产物验证（编码轮次+覆盖率、代码审查报告、测试 summary、设计自审+交叉审查等）。验证不通过的阶段标记为「⚠️ 需修订」并调度回退重新执行。

---

## 产物验证映射表

> 完整规范参见 `skills/kflow-resume/references/gates.md` §2 规则 9

| 阶段 | 验证项 |
|------|--------|
| 编码 | 执行轮次=10/10 + traceability 编码列=100% + 无占位符 |
| 代码审查 | code-review.md 存在 + 审查通过标记 |
| 接口测试 | api/summary.md 存在 + 健康评分达标 |
| E2E 测试 | e2e/summary.md 存在 |
| 集成测试 | integration/summary.md 存在 |
| 详细设计 | detailed-design.md + self-reviews/design ≥10 文件 + cross-reviews ≥1 批次 + traceability 设计列=100% |
| 原型设计 | prototype/index.md 存在 + 清单含 entry 角色文件 + 用户评审=✅已确认 或 ⏭️跳过 |

验证不通过时输出失败项清单，将对应阶段状态回退为「⚠️ 需修订」，调度回退到该阶段重新执行。仅验证「✅ 完成」阶段，不检查「⏳ 待开始」或「🔄 进行中」阶段。

---

## 调度映射表

> 完整规范参见 `skills/kflow-resume/references/recovery-protocol.md` §4

| 当前阶段 | 调度 Skill | 上下文 |
|---------|-----------|--------|
| 设计探索 | `kflow-explore` | 变更级 |
| 原型设计 | `kflow-prototype-design` | 变更级 |
| 详细设计 | `kflow-design` | 变更级 |
| 计划 | `kflow-plan` | 子变更级 |
| 编码 | `kflow-code` | 子变更级 |
| 代码审查 | `kflow-code-review` | 子变更级 |
| 接口单元测试 | `kflow-api-test` | 子变更级 |
| E2E测试 | `kflow-e2e-test` | 子变更级 |
| 集成测试 | `kflow-integration-test` | 变更级 |
| 审计 | `kflow-audit` | 变更级 |
| 归档 | `kflow-archive` | 变更级 |

---

## 五问题快速摘要

在 SUMMARIZE 步骤中，SHALL 在详细恢复信息之前输出五问题快速摘要，使用户在一屏内确认恢复状态。

### 摘要格式

```markdown
## 恢复摘要：{change-name}

| 问题 | 回答 |
|------|------|
| 当前位置 | {当前阶段} → {当前子变更（如适用）} → {当前功能点（如适用）} |
| 剩余路径 | {未完成阶段按顺序用 → 连接} |
| 变更目标 | {从 .status.md 的「变更描述」字段获取} |
| 设计依据 | {当前阶段依赖的主要设计文档路径及章节} |
| 已完成 | {已完成数}/{总任务数} 任务 |
```

### 5 个字段定义

| 字段 | 说明 | 数据来源 |
|------|------|---------|
| 当前位置 | 当前阶段 → 当前子变更（如适用）→ 当前功能点（如适用），逐级细化到可执行的恢复点 | `.status.md`：当前阶段字段 + 子变更进度矩阵 |
| 剩余路径 | 按顺序列出未完成的阶段（用 → 连接），仅显示当前变更剩余阶段 | `.status.md`：阶段状态表（筛选 ⏳ 待开始） |
| 变更目标 | 一句话描述变更的核心目标 | `.status.md`：变更描述字段 |
| 设计依据 | 指向当前阶段依赖的主要设计文档及章节号 | 按当前阶段映射：编码/测试→detailed-design.md；设计→functional-designs/index.md；计划→detailed-design.md 子变更划分章节 |
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
| 输出位置 | 五问题摘要 SHALL 在详细恢复信息（流程位置图、待执行任务列表等）之前展示 |
| 长度控制 | 摘要 SHALL 控制在 15 行以内，使用简洁表格格式 |
| 字段完整性 | 5 个字段 SHALL 全部填写，暂无数据的字段填 `—` |
| 详细输出保留 | 五问题摘要之后 SHALL 继续输出完整的恢复流程信息 |

---

## 恢复摘要输出格式

系统 SHALL 先输出五问题快速摘要，再输出以下详细恢复信息：

```markdown
## 🔄 中断恢复：{change-name}

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

---

## 与其他 Skill 的关系

- **由 `kflow-guide` 调用**：guide 识别 RESUME 模式后路由到 resume
- **调用阶段 Skill**：resume 定位断点后直接调度对应阶段 Skill
- **不创建文件**：resume 是纯恢复路由层，不产生持久化产物
- **与 checkpoint 机制协作**：优先使用 checkpoint 定位精确断点，回退到 .status.md 或 tasks.md

---

## 反馈机制

如果在使用本 Skill 过程中发现问题或有优化建议，请记录到 `docs/skill-suggestion.md` 文件中。
