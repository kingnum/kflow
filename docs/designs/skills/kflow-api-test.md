# kflow-api-test（接口单元测试阶段）

> **版本**: 参见仓库根目录 `VERSION` 文件
> **阶段**: 接口单元测试（所有项目必须阶段，子变更级）

---

## 基本信息

```yaml
name: kflow-api-test
description: 接口单元测试阶段 - 使用 curl/HTTP 请求对 api-tests/ 中定义的接口逐条测试。适用于所有项目类型（前后端+纯后端）。弹性重复制执行（首次10轮，回退按影响范围缩减），每轮输出 round-{n}.md，最终输出 summary.md 含健康评分。覆盖 traceability.md「接口测试(ID)」列。阶段钩子引用 `skills/kflow-api-test/references/hooks.md`（每轮前 STOP→编译→迁移→START→健康检查，每轮后 STOP）。/接口测试/API测试/接口单元测试
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
```

---

## 门控检查

> **机制说明**：门控规则定义在 [core-mechanisms/03-status-and-tasks.md](../core-mechanisms/03-status-and-tasks.md#34-门控规则)

进入接口单元测试阶段前检查：
- .status.md 存在
- 编码状态 = ✅ 完成（含代码审查通过）
- 代码审查状态 = ✅ 完成（kflow-code-review 通过）
- 子变更代码审查报告存在 (test-reports/review/code-review.md)
- api-tests/ 测试用例文档存在
- docs/service-guide.md 存在（服务启动配置可用）

---

## 项目类型判断

| 项目类型 | 阶段处理 |
|---------|---------|
| 前后端项目 | 必须执行接口单元测试阶段（作为 E2E 测试前置） |
| 纯后端项目 | 必须执行接口单元测试阶段（作为最终验收标准） |

> **关键变更**：纯后端项目不再跳过接口单元测试。当前 `kflow-e2e-test` 拆分后，`kflow-api-test` 对所有项目类型必须执行。

---

## 输入要求

| 产物 | 图例 | 说明 |
|------|------|------|
| 变更级 api-tests/ | ✅ 必须 | 接口测试用例文档 |
| 变更级 detailed-design.md | ✅ 必须 | 统一详细设计（接口设计章节用于契约一致性对比） |
| docs/service-guide.md | ✅ 必须 | 服务启动配置（多环境） |
| test-reports/review/code-review.md | ✅ 必须 | 代码审查通过证明 |

---

## 输出产物

| 产物 | 文件 | 模板 | 图例 | 内容要求 |
|------|------|------|------|---------|
| API测试轮次报告 | subchanges/*/test-reports/api/round-{n}.md | [API测试轮次报告](../../templates/subchanges/{subchange}/api-round-report.md) | ✅ 必须 | 接口测试用例执行结果 |
| API测试总结文档 | subchanges/*/test-reports/api/summary.md | [API测试总结](../../templates/subchanges/{subchange}/api-summary.md) | ✅ 必须 | 各轮次统计、健康评分、是否通过 |
| 状态文件更新 | subchanges/*/.status.md | [子变更状态文件](../../templates/subchanges/{subchange}/subchange-status.md) | ✅ 必须 | 标记子变更测试阶段状态 |
| 变更状态更新 | .status.md | [变更级状态文件](../../templates/changes/{change}/change-status.md) | ✅ 必须 | 更新子变更进度矩阵 |

---

## 执行流程

```
API 测试阶段流程 (curl/HTTP 驱动):

┌─────────────────────────────────────────────────────────────┐
│                   API TEST WORKFLOW                           │
├─────────────────────────────────────────────────────────────┤
│  1. PRE_HOOK  → 引用 `skills/kflow-api-test/references/hooks.md` api-test 阶段 PRE_HOOK │
│  │   ├── CHECK_STATE → 验证前置阶段状态                       │
│  │   ├── RELOAD → 重读 service-guide.md, api-tests/, detailed-design.md, .status.md │
│  │   ├── CHECK_PORTS → 检测端口占用                           │
│  │   ├── STOP_STALE → 停止残留服务                            │
│  │   ├── COMPILE → 后端编译                                   │
│  │   ├── MIGRATE → 执行未执行的迁移脚本                       │
│  │   ├── START_SERVICE → with_server.py --daemon 启动后端服务  │
│  │   └── HEALTH_CHECK → /health + /db-health 验证服务就绪     │
│  2. CHECK     → 门控检查（前置阶段完成检查）                  │
│  2. TYPECHECK → 确认项目类型（前后端/纯后端，均须执行）       │
│  3. WAIT_SYNC → 等待变更级 agent 编译重启完成                 │
│  │   └── 变更级 agent 从 docs/service-guide.md 读取启动命令和环境配置 │
│  │   └── 变更级 agent 执行: 停止→编译→迁移→启动→健康检查     │
│  │   └── 收到「服务就绪，开始 Round N」信号后继续            │
│  4. EXECUTE   → 执行 API 测试用例（curl/HTTP 请求）          │
│  │   ├── 按 api-tests/ 逐条执行接口测试                      │
│  │   ├── 记录 HTTP 状态码、响应体、响应时间                  │
│  │   ├── 验证响应结构与 api-tests/ 定义一致性                │
│  │   └── 记录执行结果                                        │
│  5. EVALUATE  → 评估测试结果 + 健康评分                       │
│  │   ├── 全部通过 → 输出 summary.md                           │
│  │   │   ├── 其他子变更未完成 → 标记 ⏸️ 等待同步             │
│  │   │   └── 所有子变更完成 → 标记完成                        │
│  │   └── 有失败 → 提示进入缺陷修复阶段                        │
│  6. FIX       → (缺陷修复阶段处理，含根因分类路由)            │
│  7. ROUND N   → 等待变更级同步 → 执行后续轮次测试             │
│  8. SUMMARY   → 输出测试总结文档 + 健康评分                   │
│  9. NEXT      → 选择下一个子变更测试（按依赖顺序）             │
│  │   └────────────────────────────────────────────────────── │
│  │   所有子变更测试完成后                                     │
│  │   └────────────────────────────────────────────────────── │
│  10. NEXT_STAGE → 前后端项目 → kflow-e2e-test                │
│  │               纯后端项目 → kflow-integration-test          │
│ 11. POST_HOOK → 引用 `skills/kflow-api-test/references/hooks.md` api-test 阶段 POST_HOOK │
│  │   ├── STOP_SERVICE → with_server.py --stop-all 停止后端服务 │
│  │   ├── VERIFY_STOP → 验证端口已释放                          │
│  │   └── UPDATE_STATE → 更新 .status.md + 清理 .service-state.json │
└─────────────────────────────────────────────────────────────┘
```

### 子变更 agent 服务使用约束

> 完整规范参见 `skills/kflow-api-test/references/service-lifecycle.md`

子变更 agent 为纯消费者，不管理服务生命周期。连接已知端口使用服务，不执行启停/编译/迁移操作。

### 服务不可用上报

> 完整规范参见 `skills/kflow-api-test/references/service-lifecycle.md`

服务不可用时上报变更级 agent，标记当前测试用例为「阻塞等待服务恢复」，等待服务恢复后继续。

---

## 健康评分数据采集

健康评分各维度通过 curl 命令采集原始数据：

| 评分维度 | 数据源 | 采集方式 | 评分规则 |
|---------|--------|---------|---------|
| 功能完整性 | 测试用例执行结果 | 统计 ✅/❌ 用例数 | 通过数/总数 × 100 |
| 响应时间 | curl 计时 | `curl -w "@curl-format.txt"` 或 `time curl` | < 200ms 满分，每超 100ms 扣 10 分 |
| HTTP 状态码 | curl 返回码 | `curl -s -o /dev/null -w "%{http_code}"` | 非 2xx/3xx 扣分 |
| 错误处理 | 异常输入响应 | 发送异常参数/缺失必填字段 | 正确错误码+消息体格式 |
| 契约一致性 | 与 api-tests/ 定义对比 | diff 响应结构与预期 schema | 响应结构匹配度 |

---

## 崩溃恢复

> 完整规范参见 `skills/kflow-api-test/references/service-lifecycle.md`

服务崩溃时子变更 agent 检测并上报，变更级 agent 执行编译重启流程（停止→编译→迁移→启动→健康检查），恢复后通知子变更 agent 从断点继续。

---

## 测试报告格式

### 测试轮次报告

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

## 重复制（执行类阶段）

> ⚠ **子代理强制规则**（参见 skills/kflow-api-test/references/repetition.md §12）：本阶段（接口单元测试）主工作 MUST 通过 Agent 子代理执行，主 Agent 仅负责调度和验收，SHALL NOT 直接执行接口测试主工作（curl测试/健康评分/报告生成等），无例外。子代理崩溃时轮次级重试（≤3 次），全部失败标记 ⚠️ 阻塞。

接口单元测试阶段属于执行类阶段，采用弹性重复制模式。目标轮次由弹性轮次决策确定（首次执行 10 轮，回退重执行按影响范围分数缩减）。子代理每轮遍历 api-tests/ 全部接口用例，逐条 curl/HTTP 执行。

> 通用规范（复杂度公式、轮次执行细节、prompt 规范、弹性轮次决策、验证门控）参见 `skills/kflow-api-test/references/repetition.md`

### 阶段特定参数

- **遍历项**：api-tests/ 全部接口用例
- **每轮工作**：逐条 curl/HTTP 执行，验证响应结构与健康评分数据采集
- **复杂度权重**：接口数 × 1.5 + 场景数 × 2
- **产物要求**：traceability.md「接口测试」列覆盖率 = 100%，round-{n}.md + summary.md，健康评分各维度已采集

---

## 常见陷阱

| 序号 | 陷阱 | 错误做法 | 正确做法 |
|------|------|---------|---------|
| 1 | 忽略服务就绪检查 | 门控检查后直接发送请求 | 每轮测试前先 curl 确认服务端口可连接 |
| 2 | 不验证响应体结构 | 仅检查 HTTP 状态码 | 同时验证响应体结构与 api-tests/ 定义一致 |
| 3 | 遗漏异常输入测试 | 仅测试 Happy Path | 按 api-tests/ 逐条覆盖 Error Path 和 Edge Case |
| 4 | 不记录响应时间 | 仅记录通过/失败 | 使用 curl -w 记录各接口响应时间用于健康评分 |
| 5 | 轮次报告不增量 | 每轮重复完整用例清单 | 增量记录本轮新增的成败变化 |

---

## 上下文管理

- **curl 优先于浏览器**：接口测试使用 curl/HTTP 请求，轻量高效，无需浏览器环境
- **增量轮次报告**：每轮报告仅记录本轮新增的成败变化，不重复完整用例清单
- **选择性读取**：读取 detailed-design.md 时仅提取当前子变更相关的接口设计章节

---

## 与其他 Skill 的关系

- **输入来自**：代码审查（`kflow-code-review`，子变更级）
- **输出给**：`kflow-e2e-test`（前后端项目，子变更级）、`kflow-bug-fix`（测试失败时）、`kflow-integration-test`（纯后端项目所有子变更通过时）
- **前置阶段**：编码 → 代码审查（`kflow-code-review`）
- **后续阶段**：E2E 测试（前后端项目）或集成测试（纯后端项目）
- **服务管理**：服务生命周期由变更级 agent 独占管理，子变更 agent 为纯消费者
- **项目类型**：所有项目类型必须执行
- **执行模式**：弹性重复制，目标轮次由弹性轮次决策确定（参见 skills/kflow-api-test/references/repetition.md §14），复杂度评估仅信息展示，主 Agent 验收闭环

---

## 反馈机制

如果在使用本 Skill 过程中发现问题或有优化建议，请记录到 `docs/skill-suggestion.md` 文件中。
