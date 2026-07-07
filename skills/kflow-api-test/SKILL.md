---
name: kflow-api-test
version: 0.16.0
description: Use when user needs API testing/接口测试、API测试、接口单元测试, or subchange code review passes and ready for interface testing. curl/HTTP 方式对 api-tests/ 逐条测试，弹性重复制模式，健康评分（功能完整性/响应时间/HTTP状态码/错误处理/契约一致性）。适用于所有项目类型（前后端+纯后端）。含 PRE_HOOK/POST_HOOK 阶段钩子。/接口测试/API测试/接口单元测试
license: MIT
triggers:
  - 接口测试
  - API测试
  - 接口单元测试
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

子变更级接口单元测试执行器。使用 curl/HTTP 请求对 api-tests/ 中定义的接口逐条测试。所有项目类型必须阶段。服务生命周期由变更级 agent 独占管理，本 agent 为纯消费者。

> ⚠ **子代理强制规则**（参见 skills/kflow-api-test/references/repetition.md §12）:
> 1. 本阶段主工作 MUST 通过 Agent 子代理执行，主 Agent 仅负责调度和验收
> 2. 主 Agent SHALL NOT 直接执行本阶段主工作，无例外
> 3. 子代理 SHOULD 前台运行（推荐 `run_in_background=false`），后台模式仅在权限已预配置时使用
> 4. 适用场景：直接触发 + triage 路由 + 其他 Skill 调用
> 5. 后台子代理权限失败时 SHALL 创建新的前台子代理重新执行，主 Agent SHALL NOT 直接接管（参见 §12.7）

# 任务

门控检查 → 确认项目类型 → 等待变更级服务就绪 → 执行 API 测试用例 → 健康评分数据采集 → 缺陷修复路由 → 输出测试报告 → 更新状态 → 下一子变更 → 前后端项目进入 E2E 测试 / 纯后端项目进入集成测试。

# 门控检查

进入接口单元测试阶段前检查：
- `.status.md` 存在
- 编码状态 = ✅ 完成（含代码审查通过）
- 代码审查状态 = ✅ 完成（kflow-code-review 通过）
- 子变更代码审查报告存在 (`test-reports/review/code-review.md`)
- `api-tests/` 测试用例文档存在
- `docs/service-guide.md` 存在（服务启动配置可用）

# 项目类型判断

| 项目类型 | 阶段处理 |
|---------|---------|
| 前后端项目 | 必须执行接口单元测试阶段（作为 E2E 测试前置） |
| 纯后端项目 | 必须执行接口单元测试阶段（作为最终验收标准） |

纯后端项目不再跳过接口单元测试。`kflow-api-test` 对所有项目类型必须执行。

# 输入要求

| 产物 | 图例 | 说明 |
|------|------|------|
| 变更级 api-tests/ | ✅ 必须 | 接口测试用例文档 |
| 变更级 detailed-design.md | ✅ 必须 | 统一详细设计（接口设计章节用于契约一致性对比） |
| docs/service-guide.md | ✅ 必须 | 服务启动配置（多环境） |
| test-reports/review/code-review.md | ✅ 必须 | 代码审查通过证明 |

# 输出产物

| 产物 | 文件 | 图例 | 内容要求 |
|------|------|------|---------|
| API 测试轮次报告 | `subchanges/{subchange}/test-reports/api/round-{n}.md` | ✅ 必须 | 接口测试用例执行结果 |
| API 测试总结文档 | `subchanges/{subchange}/test-reports/api/summary.md` | ✅ 必须 | 各轮次统计、健康评分、是否通过 |
| 状态文件更新 | `subchanges/{subchange}/.status.md` | ✅ 必须 | 标记子变更测试阶段状态 |
| 变更状态更新 | `.status.md` | ✅ 必须 | 更新子变更进度矩阵 |

# 执行流程

```
API 测试阶段流程 (curl/HTTP 驱动):

┌─────────────────────────────────────────────────────────────┐
│                   API TEST WORKFLOW                           │
├─────────────────────────────────────────────────────────────┤
│  1. PRE_HOOK  → CHECK_STATE → RELOAD → 引用                     │
│  │              skills/kflow-api-test/references/hooks.md api-test PRE_HOOK   │
│  2. CHECK     → 门控检查（前置阶段完成检查）                  │
│  3. TYPECHECK → 确认项目类型（前后端/纯后端，均须执行）       │
│  4. WAIT_SYNC → 等待变更级 agent 编译重启完成                 │
│  │   └── 变更级 agent 执行: 停止→编译→迁移→启动→健康检查     │
│  │   └── 收到「服务就绪，开始 Round N」信号后继续            │
│  5. EXECUTE   → 执行 API 测试用例（curl/HTTP 请求）          │
│  │   ├── 按 api-tests/ 逐条执行接口测试                      │
│  │   ├── 记录 HTTP 状态码、响应体、响应时间                  │
│  │   ├── 验证响应结构与 api-tests/ 定义一致性                │
│  │   └── 记录执行结果                                        │
│  6. EVALUATE  → 评估测试结果 + 健康评分                       │
│  │   ├── 全部通过 → 输出 summary.md                           │
│  │   │   ├── 其他子变更未完成 → 标记 ⏸️ 等待同步             │
│  │   │   └── 所有子变更完成 → 标记完成                        │
│  │   └── 有失败 → 提示进入缺陷修复阶段                        │
│  7. FIX       → (缺陷修复阶段处理，含根因分类路由)            │
│  8. ROUND N   → 等待变更级同步 → 执行后续轮次测试             │
│  9. SUMMARY   → 输出测试总结文档 + 健康评分                   │
│  10. NEXT     → 选择下一个子变更测试（按依赖顺序）             │
│  │   └────────────────────────────────────────────────────── │
│  │   所有子变更测试完成后                                     │
│  │   └────────────────────────────────────────────────────── │
│  11. NEXT_STAGE → 前后端项目 → kflow-e2e-test                │
│  │               纯后端项目 → kflow-integration-test          │
│  12. POST_HOOK → 引用 skills/kflow-api-test/references/hooks.md                  │
│                  api-test 阶段 POST_HOOK                             │
└─────────────────────────────────────────────────────────────┘
```

## 子变更 agent 服务使用约束

> **核心原则**：子变更 agent 为纯消费者，不管理服务生命周期。

- ✅ 子变更 agent 连接已知端口使用服务
- ✅ 子变更 agent 通过 curl 检测服务是否就绪
- ❌ 子变更 agent 不启动、停止或重启服务
- ❌ 子变更 agent 不执行编译或迁移操作

## 服务不可用上报

当子变更 agent 检测到服务端口无响应时：

1. 执行 `curl localhost:{port}` 确认端口状态
2. 如返回 Connection Refused → 立即上报变更级 agent
3. 标记当前测试用例为「阻塞等待服务恢复」
4. 等待变更级 agent 恢复服务后继续

---

# 健康评分数据采集

健康评分各维度通过 curl 命令采集原始数据：

| 评分维度 | 数据源 | 采集方式 | 评分规则 |
|---------|--------|---------|---------|
| 功能完整性 | 测试用例执行结果 | 统计 ✅/❌ 用例数 | 通过数/总数 × 100 |
| 响应时间 | curl 计时 | `curl -w "@curl-format.txt"` 或 `time curl` | < 200ms 满分，每超 100ms 扣 10 分 |
| HTTP 状态码 | curl 返回码 | `curl -s -o /dev/null -w "%{http_code}"` | 非 2xx/3xx 扣分 |
| 错误处理 | 异常输入响应 | 发送异常参数/缺失必填字段 | 正确错误码+消息体格式 |
| 契约一致性 | 与 api-tests/ 定义对比 | diff 响应结构与预期 schema | 响应结构匹配度 |

---

# 崩溃恢复

当 API 测试过程中服务崩溃时：

```
崩溃恢复流程:

1. DETECT    → 子变更 agent 检测到 curl localhost:{port} 返回 Connection Refused
2. REPORT    → 立即上报变更级 agent
3. MARK      → 标记当前测试用例为「阻塞等待服务恢复」
4. RESTART   → 变更级 agent 执行编译重启流程
              (停止→编译后端→编译前端→迁移→启动后端→启动前端→健康检查)
5. RESUME    → 健康检查通过后变更级 agent 通知子变更 agent 继续
6. CONTINUE  → 子变更 agent 从断点测试用例继续执行
```

---

# 测试报告格式

## 测试轮次报告

```markdown
# API 测试轮次报告：Round {n}

## 基本信息
- **测试时间**: {YYYY-MM-DD HH:MM}
- **测试轮次**: {n}
- **子变更**: {subchange-name}
- **项目类型**: {前后端项目/纯后端项目}
- **测试接口数**: {总数}
- **通过**: {通过数}
- **失败**: {失败数}
- **跳过**: {跳过数}

## 测试环境

| 环境项 | 值 | 说明 |
|--------|---|------|
| 服务地址 | http://localhost:{port} | 测试服务地址 |
| 测试工具 | curl | HTTP 客户端 |

## 测试用例执行结果

| 序号 | 用例ID | 接口路径 | HTTP方法 | 预期状态码 | 实际状态码 | 响应时间 | 执行结果 | 备注 |
|------|--------|---------|---------|-----------|-----------|---------|----------|------|
| 1 | TC-001 | /api/users | GET | 200 | 200 | 45ms | ✅ 通过 | - |
| 2 | TC-002 | /api/users | POST | 201 | 400 | 120ms | ❌ 失败 | {失败原因} |

## 失败用例详情

### TC-002: {用例描述}

- **请求**: `curl -X POST ...`
- **预期结果**: 201 Created, {预期响应体}
- **实际结果**: 400 Bad Request, {实际响应体}
- **失败原因**: {原因分析}

## 健康评分

| 维度 | 分数 | 说明 |
|------|------|------|
| 功能完整性 | {score}/100 | 接口通过率 |
| 响应时间 | {score}/100 | 平均响应时间 |
| HTTP 状态码 | {score}/100 | 异常状态码数量 |
| 错误处理 | {score}/100 | 异常输入处理正确性 |
| 契约一致性 | {score}/100 | 响应结构与定义匹配度 |
```

---

# 重复制（执行类阶段）

接口单元测试阶段属于执行类阶段，采用重复制模式。目标轮次由弹性轮次决策规则确定（参见 `skills/kflow-api-test/references/repetition.md` §14）：首次执行 10 轮，回退重执行按影响范围分数缩减。

## 每轮工作内容

**遍历项**：api-tests/ 全部接口用例

**每轮流程**：
1. 遍历全部接口用例，逐条 curl/HTTP 执行：
   - 发送 HTTP 请求
   - 记录 HTTP 状态码、响应体、响应时间
   - 验证响应结构与 api-tests/ 定义一致性
2. 已通过的用例仍需重跑验证无回归
3. 失败的用例记录后进入修复流程
4. 采集健康评分数据（功能完整性/响应时间/HTTP状态码/错误处理/契约一致性）

**每轮产物**：round-{n}.md 轮次报告

**轮次结束后**：更新 .status.md 执行轮次计数器

## 复杂度评估

复杂度评估仅信息展示，不驱动执行行为：

```
复杂度分 = 接口数 × 1.5 + 场景数 × 2

低复杂度 (< 20 分) / 中复杂度 (20-50 分) / 高复杂度 (> 50 分)
```

分级阈值保留但仅用于信息分类，复杂度分写入 .status.md 备注列标注「仅供参考，不驱动执行行为」。无论复杂度高低，均须完成全部 10 轮迭代后方可返回。

## 执行流程

```
1. 复杂度评估 → 写入 .status.md 备注列（仅信息展示，不驱动执行行为）

1.5 INIT → 主 Agent 按弹性轮次决策确定目标轮次 N，写入 .status.md 执行轮次为 1 / N

2. 构建阶段专属提示词
   ├── kflow-shared 分层加载（基础层 + 执行层 + 服务层）:
   │   ├── skills/kflow-api-test/references/state-values.md（摘要）
   │   ├── skills/kflow-api-test/references/gates.md（当前阶段相关门控）
   │   ├── skills/kflow-api-test/references/repetition.md
   │   ├── skills/kflow-api-test/references/service-lifecycle.md
   │   └── skills/kflow-api-test/references/hooks.md（服务相关章节）
   ├── 输入: api-tests/ + detailed-design.md + service-guide.md
   ├── 测试执行要求 (curl/HTTP 驱动)
   ├── traceability.md 待填充列: 接口测试(ID)
   ├── 覆盖率目标: 100%
   ├── 重复制遍历指令: 「每轮遍历全部接口用例逐条独立执行。更新 .status.md 中执行轮次计数器为当前轮次号。禁止按轮次分段分配工作重点——每轮均须运行全部测试用例。必须完成全部 10 轮迭代后才可返回验收报告，禁止在第 10 轮前返回。若当前轮次无新发现且无可执行工作，仍须递增计数器并继续。」
   ├── 轮间摘要注入（第 2 轮起）: 主 Agent 每轮子代理返回后提取摘要（已发现问题/未解决问题/覆盖率变化/本轮建议关注），注入下一轮子代理 prompt（参见 repetition-model.md §13）
   └── 完成承诺: COMPLETED

3. 启动 Agent 迭代子代理 (Agent(description, prompt, run_in_background))
   └── 子代理内维持现有 curl/HTTP 驱动测试流程

4. 主 Agent 验收
   ├── 轮次: .status.md 执行轮次 = N / N（N 为目标轮次，由弹性轮次决策确定）
   ├── 产物: round-{n}.md + summary.md
   ├── 覆盖率: traceability.md「接口测试」列覆盖率 = 100%
   ├── 健康评分: 各维度评分已采集
   └── 无占位符: 无 TODO/TBD/{待填写}
```

## 验收结果处理

- **通过** → 更新 .status.md + 填写 traceability.md「接口测试」列 → 释放下一阶段门控
- **轮次不足** → 拒收，直接重新启动 Agent 子代理继续执行，不进入 AskUserQuestion
- **轮次达标但产物不合格** → 记录 skill-suggestion.md → AskUserQuestion 询问重跑

---

# 常见陷阱

| 序号 | 陷阱 | 错误做法 | 正确做法 |
|------|------|---------|---------|
| 1 | 忽略服务就绪检查 | 门控检查后直接发送请求 | 每轮测试前先 curl 确认服务端口可连接 |
| 2 | 不验证响应体结构 | 仅检查 HTTP 状态码 | 同时验证响应体结构与 api-tests/ 定义一致 |
| 3 | 遗漏异常输入测试 | 仅测试 Happy Path | 按 api-tests/ 逐条覆盖 Error Path 和 Edge Case |
| 4 | 不记录响应时间 | 仅记录通过/失败 | 使用 curl -w 记录各接口响应时间用于健康评分 |
| 5 | 轮次报告不增量 | 每轮重复完整用例清单 | 增量记录本轮新增的成败变化 |

---

# 上下文管理

- **curl 优先于浏览器**：接口测试使用 curl/HTTP 请求，轻量高效，无需浏览器环境
- **增量轮次报告**：每轮报告仅记录本轮新增的成败变化，不重复完整用例清单
- **选择性读取**：读取 detailed-design.md 时仅提取当前子变更相关的接口设计章节

---

# 与其他 Skill 的关系

- **输入来自**：代码审查（`kflow-code-review`，子变更级）
- **输出给**：`kflow-e2e-test`（前后端项目，子变更级）、`kflow-bug-fix`（测试失败时）、`kflow-integration-test`（纯后端项目所有子变更通过时）
- **前置阶段**：编码 → 代码审查（`kflow-code-review`）
- **后续阶段**：E2E 测试（前后端项目）或集成测试（纯后端项目）
- **服务管理**：服务生命周期由变更级 agent 独占管理，子变更 agent 为纯消费者
- **项目类型**：所有项目类型必须执行
- **执行模式**：重复制，弹性轮次决策（参见 repetition-model.md §14），复杂度评估仅信息展示，主 Agent 验收闭环

---

# 核心提醒

- 所有项目类型必须执行本阶段（前后端+纯后端），纯后端项目不再跳过
- 子变更 agent 为纯消费者，不管理服务生命周期
- 使用 curl/HTTP 请求进行接口测试，轻量高效
- 强制完成全部 10 轮迭代后才可返回验收报告，禁止在第 10 轮前返回
- 轮次不足时拒收并直接重新启动 Agent 子代理，不进入 AskUserQuestion
- 覆盖率目标：traceability.md「接口测试(ID)」列 = 100%

# 反馈机制

如果在使用本 Skill 过程中发现问题或有优化建议，请记录到 `docs/skill-suggestion.md` 文件中。
