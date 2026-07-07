---
name: kflow-code-review
version: 0.16.0
description: Use when user needs code review/代码审查、审查代码、code review, or subchange coding is complete and ready for review. 两视角并行审查（安全+规范/质量+性能），分级重审闭环验证。独立于编码阶段，子变更级必须阶段。含 PRE_HOOK/POST_HOOK 阶段钩子引用（不需要服务，纯静态分析）。
license: MIT
triggers:
  - 代码审查
  - code review
  - 审查代码
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
---

# 角色

代码审查执行器（子变更级）。独立于编码阶段，对已完成 TDD 的子变更代码执行两视角并行审查（Agent 1: 安全+规范 / Agent 2: 质量+性能），含分级重审闭环验证机制。采用重复制模式。

> ⚠ **子代理强制规则**（参见 skills/kflow-code-review/references/repetition.md §12）:
> 1. 本阶段主工作 MUST 通过 Agent 子代理执行，主 Agent 仅负责调度和验收
> 2. 主 Agent SHALL NOT 直接执行本阶段主工作，无例外
> 3. 子代理 SHOULD 前台运行（推荐 `run_in_background=false`），后台模式仅在权限已预配置时使用
> 4. 适用场景：直接触发 + triage 路由 + 其他 Skill 调用
> 5. 后台子代理权限失败时 SHALL 创建新的前台子代理重新执行，主 Agent SHALL NOT 直接接管（参见 §12.7）

# 任务

门控检查（编码完成状态）→ 收集审查材料 → 两视角并行审查 → 门控判定 → 输出审查报告（含问题追踪矩阵）→ 分级重审闭环（高/中/低严重度差异化验证）→ 更新状态。

# 门控检查

进入代码审查阶段前检查：

| 检查项 | 要求 |
|--------|------|
| 子变更编码状态 | = ✅ 完成 |
| 子变更 `tasks.md` | 所有实现任务已完成 |
| 所有功能点 TDD 循环 | 全 Green + 已提交 |

不满足则 ❌ 阻塞，提示先完成编码阶段。

# 输入要求

| 产物 | 图例 | 说明 |
|------|------|------|
| 子变更 `tasks.md` | ✅ 必须 | 子变更任务清单（确认所有任务完成） |
| 子变更代码变更 | ✅ 必须 | TDD 编码完成的代码（diff） |
| 变更级 `detailed-design.md` | ✅ 必须 | 统一详细设计（用于对照检查） |
| `CONTEXT.md` | ✅ 必须 | 项目级领域词汇表，用于检查代码命名对齐 |
| `docs/service-guide.md` | ✅ 必须 | 服务配置（检查配置安全性） |
| `prototype/index.md` | 🔶 条件 | 原型产物清单，存在时从清单获取 tokens/coverage/spec/nav-tree 文件路径纳入对账 |
| `prototype/element-spec.md` | 🔶 条件 | 原型元素清单，存在时纳入对账 |
| `prototype/nav-tree.md` | 🔶 条件 | 原型导航树，存在时纳入对账 |

# 输出产物

| 产物 | 文件 | 图例 | 验收标准 |
|------|------|------|---------|
| 代码审查报告 | `docs/changes/{change}/subchanges/{subchange}/test-reports/review/code-review.md` | ✅ 必须 | 两视角审查通过（门控满足），含问题追踪矩阵 |

# 执行流程

```
代码审查阶段流程:

┌───────────────────────────────────────────────────────────────────────┐
│                     CODE REVIEW WORKFLOW                               │
├───────────────────────────────────────────────────────────────────────┤
│  1. PRE_HOOK  → 引用 skills/kflow-code-review/references/hooks.md code-review 阶段 PRE_HOOK │
│  2. CHECK     → 门控检查（编码完成状态）                               │
│  3. COLLECT   → 收集审查材料（代码变更 diff、详细设计、tasks.md 等）   │
│  3.3 CROSS_TIER → 跨层越界检测                                          │
│  │   ├── 后端SC: Grep .tsx/.jsx/.vue + 硬编码颜色 + prototype/ 引用  │
│  │   ├── 前端SC: Grep migrations/ + ORM注解 + 服务端路由注册         │
│  │   └── 排除 node_modules/ .next/ dist/ .git/ 测试文件等            │
│  4. PARALLEL  → 两视角并行审查                                         │
│  │   ┌───────────────────────┐  ┌───────────────────────┐             │
│  │   │ Agent 1: 安全+规范     │  │ Agent 2: 质量+性能     │             │
│  │   │ ├── SQL 注入           │  │ ├── N+1 查询           │             │
│  │   │ ├── XSS/CSRF          │  │ ├── 内存泄漏           │             │
│  │   │ ├── 敏感信息泄露       │  │ ├── 错误处理完整性      │             │
│  │   │ ├── 编码规范          │  │ ├── 代码复杂度        │             │
│  │   │ ├── 命名对齐          │  │ └── 性能瓶颈           │             │
│  │   │ └── 依赖安全漏洞       │  │                        │             │
│  │   └───────────────────────┘  └───────────────────────┘             │
│  5. GATE     → 门控判定                                               │
│  │   ├── Agent 1 高=0 且 Agent 2 高=0 且 Agent 2 中<3                 │
│  │   │   → ✅ 审查通过 → 输出报告 → 完成                               │
│  │   └── 任一不满足 → ❌ 阻塞                                          │
│  │       ├── 输出完整问题清单（含修复建议）                             │
│  │       ├── 标记子变更编码阶段为 ❌ 阻塞                               │
│  │       └── 修复完成后重新触发 kflow-code-review                     │
│  6. REPORT   → 输出 code-review.md（含问题追踪矩阵）                   │
│  7. RE-REVIEW→ 分级重审闭环（高/中/低严重度差异化验证）                │
│  8. COMPLETE → 更新子变更状态（编码+审查完成）                          │
│  9. POST_HOOK→ 引用 skills/kflow-code-review/references/hooks.md code-review 阶段 POST_HOOK │
└───────────────────────────────────────────────────────────────────────┘
```

---

## 步骤 1：PRE_HOOK — 阶段前置钩子

引用 `skills/kflow-code-review/references/hooks.md` code-review 阶段 PRE_HOOK（❌ 不需要服务：CHECK_STATE + RELOAD）。

> RELOAD: 重读 service-guide.md, CONTEXT.md, detailed-design.md, .status.md。

## 步骤 2：CHECK — 门控检查

验证编码完成状态、所有任务完结、TDD 循环全部通过。不满足条件时 ❌ 阻塞。

## 步骤 3：COLLECT — 收集审查材料

收集以下审查材料：
- 代码变更 diff（当前子变更的所有修改文件）
- `detailed-design.md`（对照设计检查实现）
- `tasks.md`（确认所有任务已完成）
- `CONTEXT.md`（检查命名对齐）
- `service-guide.md`（检查配置安全性）
- `prototype/index.md`（条件，从清单获取 tokens/coverage/spec/nav-tree 文件路径，原型一致性对账）
- `prototype/element-spec.md`（条件，原型元素对账）
- `prototype/nav-tree.md`（条件，原型导航对账）

## 步骤 3.3：跨层越界检测

> **版本**: 当前变更新增

在原型对账之前执行，验证代码产出不超越子变更类型边界。

### 后端子变更越界检测

```bash
# 检测前端源文件
grep -r --include='*.tsx' --include='*.jsx' --include='*.vue' --include='*.svelte' \
  --exclude-dir=node_modules --exclude-dir=.next --exclude-dir=dist --exclude-dir=build \
  -l .

# 检测样式文件（排除 globals.css）
grep -r --include='*.css' --include='*.scss' --include='*.less' \
  --exclude='globals.css' \
  --exclude-dir=node_modules --exclude-dir=.next --exclude-dir=dist --exclude-dir=build \
  -l .

# 检测硬编码颜色值（≥ 3 次标记）
grep -rn '#[0-9a-fA-F]\{3,6\}\|rgb(' --include='*.{ts,tsx,js,jsx,vue}' \
  --exclude='*.d.ts' --exclude='*.test.*' --exclude='*.spec.*' \
  --exclude-dir=node_modules --exclude-dir=.next --exclude-dir=dist --exclude-dir=build \
  --exclude-dir=__tests__ --exclude-dir=mocks --exclude-dir=__mocks__ \
  . | wc -l

# 检测 prototype/ 路径引用
grep -rn 'prototype/' --include='*.{ts,tsx,js,jsx}' \
  --exclude-dir=node_modules --exclude-dir=.next --exclude-dir=dist --exclude-dir=build \
  .
```

### 前端子变更越界检测

```bash
# 检测数据库迁移脚本
grep -rn 'migrations/\|schema\.sql\|\.prisma' --include='*.{ts,tsx,js,jsx}' \
  --exclude-dir=node_modules --exclude-dir=.next --exclude-dir=dist \
  --exclude='*.test.*' --exclude='*.spec.*' \
  .

# 检测 ORM 模型定义
grep -rn '@Entity\|@Table\|prisma\.model\|mongoose\.Schema' --include='*.{ts,tsx,js,jsx}' \
  --exclude-dir=node_modules --exclude-dir=.next --exclude-dir=dist \
  --exclude='*.test.*' --exclude='*.spec.*' \
  .

# 检测服务端路由注册
grep -rn 'app\.use(\|app\.post(\|router\.get(\|@PostMapping\|@GetMapping' \
  --include='*.{ts,tsx,js,jsx}' \
  --exclude-dir=node_modules --exclude-dir=.next --exclude-dir=dist \
  --exclude='*.test.*' --exclude='*.spec.*' --exclude-dir=__tests__ \
  .
```

### 越界检测输出

结果写入审查报告「跨层一致性」章节（位于原型对账章节之前）：
- 🟡 警告 → 审查建议，不阻塞
- 🔵 建议 → 审查建议，不阻塞
- 原型对账仅在前端子变更时执行

## 步骤 3.5：原型对账 Grep 验证（条件触发）

> **来源**: refine-skill-execution-rules 变更。代码审查阶段 SHALL 对 Grep 源码中的元素名/颜色值与 spec 文件对账，验证代码实现与原型的一致性。

### 触发条件

| 条件 | 处理 |
|------|------|
| `prototype/index.md` 存在且含 tokens 角色文件 | 执行设计令牌对账（从清单获取 tokens 文件路径） |
| `prototype/index.md` 存在且含 coverage 角色文件 | 执行元素对账（从清单获取 coverage 文件路径） |
| `prototype/index.md` 存在且含 entry 角色文件 | 执行导航对账（从清单获取 entry 文件路径） |
| 以上均不存在（原型设计被跳过） | 跳过本节 |

### 对账方式

使用 Grep 执行纯文本对账（非截图对比），轻量且可重复：

1. **设计令牌对账**: 从 prototype/index.md 获取 tokens 角色文件路径 → Grep 源码中的颜色值/字体值与该 tokens 文件对比
   - 验证代码中使用的颜色是否在 tokens 文件中定义
   - 验证字体大小/字重是否对齐 tokens 文件

2. **元素对账**: 从 prototype/index.md 获取 coverage 角色文件路径 → Grep 源码中的组件名/按钮名/表单名与 coverage 文件对比
   - 验证 coverage 文件中的元素是否在源码中实现
   - 允许新增元素（代码可能补充设计），标注「代码新增」

3. **导航对账**: 从 prototype/index.md 获取 entry 角色文件中的导航结构 → Grep 源码中的路由/链接对比
   - 验证 nav-tree.md 中的导航项是否在代码中实现
   - 标注缺失的导航项

### 对账结果

对账结果写入 code-review.md，标注：
- ✅ 一致：设计令牌/元素/导航在源码中正确使用
- ⚠️ 偏差：使用了未在 spec 中定义的值（列出具体偏差）
- ❌ 缺失：spec 中的元素/导航项未在源码中实现
- ➕ 新增：源码中新增了 spec 未定义的元素

## 步骤 4：PARALLEL — 两视角并行审查

使用 Agent 工具并行启动两个审查 Agent。

### Agent 1: 安全+规范

| 检查项 | 说明 | 严重度 |
|--------|------|--------|
| SQL 注入 | 是否使用参数化查询，禁止字符串拼接 SQL | 高 |
| XSS / CSRF | 输出编码、CSRF token 防护 | 高 |
| 敏感信息泄露 | 密钥/token/密码是否明文写入，日志是否脱敏 | 高 |
| 依赖安全漏洞 | 第三方依赖是否存在已知 CVE 漏洞 | 中 |
| 命名对齐 | 代码命名（模块/类/函数）是否与 CONTEXT.md 领域词汇表冲突 | 中 |
| 编码规范 | 命名规范、代码格式、注释规范 | 低 |

### Agent 2: 质量+性能

| 检查项 | 说明 | 严重度 |
|--------|------|--------|
| N+1 查询 | 循环内数据库查询、批量操作优化缺失 | 高 |
| 内存泄漏 | 未关闭的资源、循环引用、未移除的事件监听器 | 高 |
| 错误处理完整性 | 异常捕获缺失、错误返回不规范、事务回滚缺失 | 中 |
| 代码复杂度 | 圈复杂度 > 10、函数超过 50 行 | 中 |
| 性能瓶颈 | 同步阻塞、大对象加载、缺少数据库索引 | 中 |

## 步骤 5：GATE — 门控判定

### 门控规则

| 条件 | 判定 |
|------|------|
| Agent 1 高严重度 = 0 且 Agent 2 高严重度 = 0 且 Agent 2 中严重度 < 3 | ✅ 审查通过 |
| Agent 1 高严重度 ≥ 1 或 Agent 2 高严重度 ≥ 1 或 Agent 2 中严重度 ≥ 3 | ❌ 阻塞 |

### 阻塞处理

```
阻塞处理流程:

❌ 门控阻塞
  ├── 输出完整问题清单（含修复建议）
  ├── 标记子变更编码阶段为 ❌ 阻塞
  ├── 修复完成后重新触发 kflow-code-review
  └── 进入分级重审闭环（见 §步骤 7）
```

## 步骤 6：REPORT — 输出审查报告

输出 `code-review.md`，包含问题追踪矩阵。

### 审查报告格式

```markdown
# 代码审查报告：{subchange-name}

## 基本信息
- **审查时间**: {YYYY-MM-DD HH:MM}
- **子变更**: {subchange-name}
- **审查文件数**: {数量}
- **审查 Agent 数**: 2
- **执行轮次**: {N} / 10

## 审查结果汇总

| Agent | 高严重度 | 中严重度 | 低严重度 | 通过 |
|--------|---------|---------|---------|------|
| Agent 1 (安全+规范) | {n} | {m} | {k} | ✅/❌ |
| Agent 2 (质量+性能) | {n} | {m} | {k} | ✅/❌ |

## 问题追踪矩阵

| 序号 | Agent | 严重度 | 文件 | 行号 | 问题描述 | 修复建议 | 修复轮次 | 复审状态 | 最终状态 |
|------|-------|--------|------|------|---------|---------|---------|---------|---------|
| 1 | 安全+规范 | 高 | src/auth/login.ts | 45 | SQL 拼接未使用参数化查询 | 改用 PreparedStatement | R2 | 双视角已验证 | ✅ 已修复 |
| 2 | 质量+性能 | 中 | src/service.ts | 128 | 循环内逐条查询数据库 | 改用批量查询 | R3 | 原视角已验证 | ✅ 已修复 |
| 3 | 安全+规范 | 低 | src/utils.ts | 12 | 变量命名不符合规范 | 改用驼峰命名 | R4 | 抽样已验证 | ✅ 已修复 |

## 审查结论
- [ ] Agent 1 通过（高严重度 = 0）
- [ ] Agent 2 通过（高严重度 = 0 且 中严重度 < 3）
- [ ] 门控结论: ✅ 审查通过 / ❌ 审查阻塞
```

## 步骤 7：RE-REVIEW — 分级重审闭环

审查阻塞修复完成后，按严重度分级执行重审：

### 分级重审规则

| 严重度 | 验证方式 | 说明 |
|--------|---------|------|
| 高 | 原视角 + 安全视角交叉检查 | 两个视角均确认修复后才可关闭 |
| 中 | 原视角重新审查 | 确认修复不引入新问题 |
| 低 | 随机 30% Agent 验证 + 70% 开发者自查 | 抽样验证，减轻审查负担 |

### 重审闭环流程

```
修复完成 → 触发重审:

高严重度问题:
  ├── Agent 1 复查（原视角）
  ├── Agent 2 交叉检查（安全视角）
  └── 双方确认 → 关闭问题

中严重度问题:
  ├── 原视角 Agent 重新审查
  └── 通过 → 关闭问题

低严重度问题:
  ├── 随机 30% 抽样（Agent 验证）
  │   ├── 被抽样 → Agent 验证 → 关闭/重开
  │   └── 未抽样 → 开发者自查 → 标记为已验证
  └── 70% 开发者自查
```

## 步骤 8：COMPLETE — 更新子变更状态

更新子变更 `.status.md`：标记编码阶段和代码审查阶段为 ✅ 完成，记录完成时间。

## 步骤 9：POST_HOOK — 阶段后置钩子

引用 `skills/kflow-code-review/references/hooks.md` code-review 阶段 POST_HOOK（❌ 不需要服务：UPDATE_STATE）。

---

# 重复制（执行类阶段）

代码审查阶段属于执行类阶段，采用重复制模式。目标轮次由弹性轮次决策规则确定（参见 `skills/kflow-code-review/references/repetition.md` §14）：首次执行 10 轮，回退重执行按影响范围分数缩减。

## 每轮工作内容

**遍历项**：**双层遍历**——外层遍历全部已完成编码的子变更，内层遍历每个子变更的全部代码变更

> **来源**: skill-execution-reliability 变更。代码审查阶段「工作项」定义为「全部已完成编码的子变更」，每轮自动处理所有子变更的审查，而非逐个子变更审查。

**每轮流程**：
1. **外层遍历**：读取所有子变更的编码+审查状态，筛选出已完成编码但未通过审查的子变更
2. **内层遍历**：对每个待审查的子变更，遍历其全部代码变更，两视角并行审查全部检查项：
   - 安全+规范：SQL 注入、XSS/CSRF、敏感信息泄露、编码规范、命名对齐、依赖安全漏洞
   - 质量+性能：N+1 查询、内存泄漏、错误处理完整性、代码复杂度、性能瓶颈
3. 已审查通过的文件执行深化检查，未通过的文件继续标记
4. 发现问题记录到 code-review.md 问题追踪矩阵
5. 分级重审闭环：高严重度双视角交叉检查、中严重度原视角重审、低严重度 30% 抽样

**每轮产物**：code-review.md 问题追踪矩阵更新

**轮次结束后**：更新 .status.md 执行轮次计数器

## 复杂度评估

复杂度评估仅信息展示，不驱动执行行为：

```
复杂度分 = 修改文件数 × 1 + 新增代码行数(百行) × 1.5

低复杂度 (< 20 分) / 中复杂度 (20-50 分) / 高复杂度 (> 50 分)
```

分级阈值保留但仅用于信息分类，复杂度分写入 .status.md 备注列标注「仅供参考，不驱动执行行为」。无论复杂度高低，均须完成全部 10 轮迭代后方可返回。

## 执行流程

```
1. 复杂度评估 → 写入 .status.md 备注列（仅信息展示，不驱动执行行为）

1.5 INIT → 主 Agent 按弹性轮次决策确定目标轮次 N，写入 .status.md 执行轮次为 1 / N

2. 构建阶段专属提示词
   ├── kflow-shared 分层加载（基础层 + 执行层）:
   │   ├── skills/kflow-code-review/references/state-values.md（摘要）
   │   ├── skills/kflow-code-review/references/gates.md（当前阶段相关门控）
   │   ├── skills/kflow-code-review/references/repetition.md
   ├── 输入: 所有子变更代码变更 diff + detailed-design.md + tasks.md + CONTEXT.md + service-guide.md
   ├── 两视角并行审查 (安全+规范 / 质量+性能)
   ├── 双层遍历: 外层遍历全部子变更 + 内层遍历全部代码变更
   ├── 闭环验证 (高/中/低严重度分级重审)
   ├── traceability.md 待填充列: 代码审查通过状态
   ├── 重复制遍历指令:
   │   「每轮遍历全部已完成编码的子变更，每个子变更内遍历全部代码变更独立执行完整审查。
   │     更新 .status.md 中执行轮次计数器为当前轮次号。
   │     禁止按轮次分段分配工作重点——每轮均须对所有子变更的全部代码变更执行完整检查。
   │     必须完成全部 10 轮迭代后才可返回验收报告，禁止在第 10 轮前返回。
   │     若当前轮次无新发现且无可执行工作，仍须递增计数器并继续。」
   ├── 轮间摘要注入（第 2 轮起）: 主 Agent 每轮子代理返回后提取摘要（已发现问题/未解决问题/覆盖率变化/本轮建议关注），注入下一轮子代理 prompt（参见 repetition-model.md §13）
   └── 完成承诺: COMPLETED

3. 启动 Agent 迭代子代理 (Agent(description, prompt, run_in_background))
   └── 子代理内维持现有两视角并行审查 + 闭环验证机制

4. 主 Agent 验收
   ├── 轮次: .status.md 执行轮次 = N / N（N 为目标轮次，由弹性轮次决策确定）
   ├── 产物: code-review.md 存在且格式正确，含问题追踪矩阵
   ├── 门控: Agent 1 高 = 0 且 Agent 2 高 = 0 且 Agent 2 中 < 3
   ├── 闭环: 所有高/中严重度问题已修复并验证
   └── 无占位符: 无 TODO/TBD/{待填写}
```

## 验收结果处理

| 情况 | 处理方式 |
|------|---------|
| 通过 | 更新 .status.md → 释放接口单元测试阶段门控 |
| 轮次不足（< 10） | 拒收，直接重新启动 Agent 子代理继续执行，不进入 AskUserQuestion |
| 轮次达标但产物不合格 | 记录 `docs/skill-suggestion.md` → AskUserQuestion 询问重跑 |

---

# 与其他 Skill 的关系

| 关系 | Skill / 阶段 | 说明 |
|------|-------------|------|
| 输入来自 | `kflow-code` | 编码阶段（子变更级） |
| 输出给 | 接口单元测试（子变更级）或 `kflow-bug-fix`（审查阻塞时按需） | 下一阶段或缺陷修复 |
| 前置阶段 | 编码 | 门控依赖 |
| 后续阶段 | 接口单元测试（子变更级）→ E2E 测试（前后端项目） | 阶段链 |
| 关系说明 | 从 `kflow-code` 拆分出的独立 Skill | 原 `kflow-code` 不再包含代码审查子阶段 |
| 执行模式 | 重复制（内嵌两视角并行审查） | 弹性轮次决策（参见 repetition-model.md §14），复杂度评估仅信息展示，主 Agent 验收闭环 |

# 核心提醒

- 两视角使用 Agent 工具**并行**审查，非串行执行
- 代码命名必须对齐 CONTEXT.md 领域词汇表
- **双层遍历**：每轮遍历全部已完成编码的子变更，每个子变更内遍历全部代码变更
- **原型对账**：原型存在时从 prototype/index.md 清单获取 tokens/coverage/entry 文件路径，用 Grep 对账 vs 源码
- 审查阻塞时路由到 `kflow-bug-fix` 进行修复
- 高严重度问题必须双视角交叉检查后才可关闭
- 中严重度问题由原视角重审，低严重度 30% 随机抽样
- 审查报告必须包含问题追踪矩阵（序号、Agent、严重度、文件、行号、修复建议、修复轮次、复审状态）

# 反馈机制

如果在使用本 Skill 过程中发现问题或有优化建议，请记录到 `docs/skill-suggestion.md` 文件中。
