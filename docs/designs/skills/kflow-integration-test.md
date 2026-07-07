# kflow-integration-test（集成测试阶段）

> **版本**: 参见仓库根目录 `VERSION` 文件
> **阶段**: 集成测试（必须阶段，变更级，内聚缺陷修复循环）

---

## 基本信息

```yaml
name: kflow-integration-test
description: 集成测试阶段 - 变更级集成测试执行，内聚四分法缺陷修复循环，架构评估自动触发。必须阶段，变更级。适用于前后端和纯后端项目。阶段钩子引用 `skills/kflow-integration-test/references/hooks.md`（每轮前 STOP→编译→迁移→START→健康检查，每轮后 STOP+浏览器清理）。
license: MIT
triggers:
  - 集成测试
  - 跨子变更测试
  - integration test
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

## 门控检查

> **机制说明**：门控规则定义在 [core-mechanisms/03-status-and-tasks.md](../core-mechanisms/03-status-and-tasks.md#34-门控规则)

进入集成测试阶段前检查：
- 所有子变更编码+审查状态 = ✅ 完成
- 所有子变更接口单元测试状态 = ✅ 完成
- 前后端项目：所有子变更 E2E 测试状态 = ✅ 完成
- 变更级服务刷新已完成并通过（服务编译、迁移执行、重启、健康检查）
- integration-tests/index.md 文件存在
- 任一不满足则提示先完成前置条件

---

## 输入要求

| 产物 | 图例 | 说明 |
|------|------|------|
| integration-tests/ | ✅ 必须 | 变更级集成测试用例 |
| 变更级 detailed-design.md | ✅ 必须 | 统一详细设计（接口契约定义） |
| 变更级 api-tests/ | ✅ 必须 | 接口测试用例（参考） |
| 变更级 e2e-tests/ | 🔶 条件 | 前后端项目参考 |
| docs/service-guide.md | ✅ 必须 | 服务配置（确认服务运行中） |
| 所有子变更 .status.md | ✅ 必须 | 确认子变更全部完成 |

---

## 输出产物

| 产物 | 文件 | 模板 | 图例 | 验收标准 |
|------|------|------|------|---------|
| 测试轮次报告 | test-reports/integration/round-{n}.md | [集成测试轮次报告](../../templates/changes/{change}/integration/integration-round-report.md) | ✅ 必须 | 每轮测试结果记录 |
| 测试总结文档 | test-reports/integration/summary.md | [集成测试总结](../../templates/changes/{change}/integration/integration-summary.md) | ✅ 必须 | 全部通过后输出"集成测试通过" |
| 修复报告 | test-reports/integration/fix-reports/{type}-{timestamp}.md | [缺陷修复报告](../../templates/subchanges/{subchange}/fix-report.md) / [契约错误报告](../../templates/changes/{change}/integration/contract-error-report.md) | 🔶 条件 | 失败修复时输出 |
| 架构评估报告 | test-reports/integration/fix-reports/arch-assessment-{timestamp}.md | [架构评估报告](../../templates/changes/{change}/integration/arch-assessment.md) | 🔶 条件 | 连续3轮同用例失败时 |
| 状态文件更新 | .status.md | [变更级状态文件](../../templates/changes/{change}/change-status.md) | ✅ 必须 | 标记集成测试阶段完成 |

---

## 执行流程

```
集成测试阶段流程:

┌─────────────────────────────────────────────────────────────┐
│                INTEGRATION TEST WORKFLOW                     │
├─────────────────────────────────────────────────────────────┤
│  1. PRE_HOOK  → 引用 `skills/kflow-integration-test/references/hooks.md` integration-test 阶段 PRE_HOOK │
│  │   ├── CHECK_STATE → 验证前置阶段状态                       │
│  │   ├── RELOAD → 重读 service-guide.md, integration-tests/, detailed-design.md, .status.md │
│  │   ├── CHECK_PORTS → 检测前后端端口占用                     │
│  │   ├── STOP_STALE → 停止残留服务                            │
│  │   ├── COMPILE → 前后端编译                                 │
│  │   ├── MIGRATE → 执行未执行的迁移脚本                       │
│  │   ├── START_SERVICE → with_server.py --daemon 启动前后端服务 │
│  │   └── HEALTH_CHECK → /health + /db-health + 前端 /health   │
│  2. CHECK     → 门控检查（子变更全部完成 + 服务刷新）        │
│  2. WAIT_SYNC → 等待变更级 agent 编译重启完成（每轮开始前）    │
│  │   └── 变更级 agent 执行: 停止→编译→迁移→启动→健康检查     │
│  │   └── 收到「服务就绪，开始 Round N」信号后继续            │
│  3. READ      → 读取 integration-tests/ 全部用例          │
│  4. EXECUTE   → 执行集成测试（按用例顺序）                   │
│  │   ├── 前后端: 浏览器 或 API 调用                         │
│  │   └── 纯后端: API 调用                                   │
│  │   ├── 服务崩溃时走崩溃恢复流程（见下方）                  │
│  5. REPORT    → 输出 test-reports/integration/round-{n}.md  │
│  6. EVALUATE  → 评估测试结果                                │
│  │   ├── 全部通过 → summary.md → 完成 ✅                    │
│  │   └── 有失败 → 四分法根因分类 ─────────────┐             │
│  │                                            │             │
│  ┌────────────────────────────────────────────┘             │
│  │                                                          │
│  ▼                                                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              四分法缺陷修复循环（内聚）                │    │
│  │                                                       │    │
│  │  根因分类:                                            │    │
│  │  ├── 接口实现错误(60%) → 定位子变更 → 修复代码        │    │
│  │  │   └── 子变更级重测通过 → 重新集成测试 ────┐        │    │
│  │  ├── 接口契约错误(20%) → 更新契约 → 联动修复  │        │    │
│  │  │   └── 输出 contract-error-{ts}.md ────────┤        │    │
│  │  ├── 测试用例错误(15%) → 修正测试用例         │        │    │
│  │  │   └── 重新集成测试 ───────────────────────┤        │    │
│  │  └── 架构设计错误(5%) → arch-assessment      │        │    │
│  │      ├── 标记集成测试 ❌ 阻塞                  │        │    │
│  │      ├── 标记详细设计 ⚠️ 需修订                │        │    │
│  │      ├── 重置子变更状态 ⏳ 待开始               │        │    │
│  │      └── 输出 arch-assessment-{ts}.md         │        │    │
│  │                                                │        │    │
│  └────────────────────────────────────────────────┘        │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              架构评估自动触发                         │    │
│  │                                                       │    │
│  │  条件: 同一测试用例 ID 连续 3 轮失败                  │    │
│  │  │                                                    │    │
│  │  ├── 自动收集证据 (失败详情+契约+子变更依赖+修复历史) │    │
│  │  ├── 根因深挖 (架构缺陷/契约矛盾/技术选型不当/其他)   │    │
│  │  ├── 输出多方案 (方案A推荐+方案B最小改动)             │    │
│  │  ├── AskUserQuestion → 用户选择方案                  │    │
│  │  └── 用户确认后执行 / 拒绝则按替代方向               │    │
│  │                                                       │    │
│  │  失败计数重置条件:                                    │    │
│  │  ├── 该用例在某轮通过                                │    │
│  │  ├── 相关接口契约被修订                              │    │
│  │  └── 用户手动重置                                    │    │
│  └────────────────────────────────────────────────────┘    │
│                                                             │
│  7. LOOP      → 等待变更级同步 → 重复步骤2-6，直到全部通过 │
│  8. COMPLETE  → 输出 summary.md，更新 .status.md          │
│  9. POST_HOOK → 引用 `skills/kflow-integration-test/references/hooks.md` integration-test 阶段 POST_HOOK │
│  │   ├── STOP_SERVICE → with_server.py --stop-all 停止前后端服务 │
│  │   ├── VERIFY_STOP → 验证端口已释放                          │
│  │   ├── BROWSER_CLEANUP → playwright-cli kill-all（前后端项目） │
│  │   └── UPDATE_STATE → 更新 .status.md + 清理 .service-state.json │
└─────────────────────────────────────────────────────────────┘
```

---

## 四分法根因分类

### 分类标准

| 分类 | 占比 | 判定条件 | 处理方式 |
|------|------|---------|---------|
| 接口实现错误 | ~60% | 代码实现不满足接口契约，但契约本身正确 | 定位子变更 → 修复代码 → 子变更重测 → 重新集成 |
| 接口契约错误 | ~20% | 接口契约定义本身有缺陷或不一致 | 更新 detailed-design.md → 评估联动范围 → 修复受影响子变更 → 重新集成 |
| 测试用例错误 | ~15% | 集成测试用例预期与设计不符 | 修正 integration-tests/ → 验证正确性 → 重新集成 |
| 架构设计错误 | ~5% | 架构层面结构性问题 | 标记阻塞 → 触发架构评估 → 用户决策 |

### 修复报告输出路径

| 错误类型 | 报告路径 | 内容要求 |
|---------|---------|---------|
| 接口契约错误 | `test-reports/integration/fix-reports/contract-error-{timestamp}.md` | 契约矛盾点、受影响子变更、修订建议 |
| 架构设计错误 | `test-reports/integration/fix-reports/arch-assessment-{timestamp}.md` | 架构缺陷分析、影响范围、回退建议 |

---

## 架构评估自动触发

### 触发条件

同一测试用例 ID 在连续 3 轮集成测试中均标记为 **失败** 时自动触发。

### 失败计数追踪

| 规则 | 说明 |
|------|------|
| 计数粒度 | 按测试用例 ID 独立追踪 |
| 记录位置 | 每轮测试轮次报告中记录各用例连续失败次数 |
| 跨轮保留 | 计数器跨测试轮次保留，不受其他用例通过/失败影响 |

### 失败计数重置

| 条件 | 说明 |
|------|------|
| 用例通过 | 该用例 ID 在某轮测试中通过 |
| 契约修订 | detailed-design.md 中相关接口契约被修订 |
| 用户手动重置 | 用户判断为误报或其他原因手动重置 |

### 证据收集

架构评估启动后自动收集：
- 3 轮失败用例的完整详情（预期 vs 实际、错误日志、堆栈追踪）
- 关联的接口契约定义（从 detailed-design.md 中提取）
- 受影响的子变更列表及其依赖关系
- 已尝试的修复方案及每次修复的结果

### 多方案输出

| 方案 | 内容 | 输出 |
|------|------|------|
| 方案 A（推荐方案） | 完整改造方案 + 改动量估算 + 风险评估 | 改动涉及的设计域、受影响子变更、预期工作量、建议实施顺序 |
| 方案 B（最小改动方案） | 局部修复方案 + 局限性说明 + 风险 | 最小改动范围、不改动范围、长期维护影响 |

### 用户决策

- 使用 AskUserQuestion 展示方案选项（方案 A / 方案 B / 自定义 / 拒绝改造）
- 用户确认后执行选定方案
- 用户拒绝时记录决策，按用户提供的替代方向继续
- 用户判断为误报时重置计数器，返回正常修复循环

---

## 测试报告格式

### 集成测试轮次报告

```markdown
# 集成测试轮次报告：Round {n}

## 基本信息
- **测试时间**: {YYYY-MM-DD HH:MM}
- **测试轮次**: {n}
- **变更**: {change-name}
- **项目类型**: {前后端 / 纯后端}
- **测试用例数**: {总数}
- **通过**: {通过数}
- **失败**: {失败数}

## 测试环境

| 环境项 | 值 |
|--------|---|
| 服务地址 | http://localhost:{port} |
| 数据库 | {连接信息} |

## 测试用例执行结果

| 序号 | 用例ID | 用例描述 | 执行结果 | 连续失败次数 | 备注 |
|------|--------|----------|----------|-------------|------|
| 1 | ITC-001 | {描述} | ✅ 通过 | 0 | - |
| 2 | ITC-002 | {描述} | ❌ 失败 | 3 | ⚠️ 触发架构评估 |

## 失败用例详情

### ITC-002: {用例描述}

- **预期结果**: {预期}
- **实际结果**: {实际}
- **根因分类**: {接口实现/接口契约/测试用例/架构设计}
- **修复方案**: {简述}
```

### 集成测试总结

```markdown
# 集成测试总结

## 基本信息
- **测试完成时间**: {YYYY-MM-DD HH:MM}
- **总轮次**: {n}
- **总测试用例数**: {总数}
- **最终通过**: {通过数}
- **最终失败**: 0

## 各轮次统计

| 轮次 | 通过 | 失败 | 修复类型 | 耗时 |
|------|------|------|---------|------|
| 1 | 8 | 3 | - | 15min |
| 2 | 10 | 1 | 接口实现修复 | 10min |
| 3 | 11 | 0 | 测试用例修正 | 8min |

## 结论
- [x] 集成测试全部通过
- [x] 变更可进入审计和归档阶段
```

---

## 项目类型适配

| 项目类型 | 测试方式 | 说明 |
|---------|---------|------|
| 前后端项目 | 浏览器 或 API 调用 | 跨子变更 API 调用链验证 + 数据一致性验证 |
| 纯后端项目 | API 调用 | API 间调用链验证 + 数据一致性验证，不涉及浏览器 |

---

## 服务管理约束

> 完整规范参见 `skills/kflow-integration-test/references/service-lifecycle.md`

集成测试阶段由变更级 agent 独占服务管理，子变更 agent 为纯消费者。每轮测试前执行编译重启，服务不可用时走崩溃恢复流程。

---

## 崩溃恢复

> 完整规范参见 `skills/kflow-integration-test/references/service-lifecycle.md`

服务崩溃时变更级 agent 执行 playwright-cli kill-all + 完整编译重启流程，恢复后从断点继续集成测试。

---

## 重复制（执行类阶段）

> ⚠ **子代理强制规则**（参见 skills/kflow-integration-test/references/repetition.md §12）：本阶段（集成测试）主工作 MUST 通过 Agent 子代理执行，主 Agent 仅负责调度和验收，SHALL NOT 直接执行集成测试主工作（跨子变更测试/四分法修复/架构评估等），无例外。子代理崩溃时轮次级重试（≤3 次），全部失败标记 ⚠️ 阻塞。

集成测试阶段属于执行类阶段，采用弹性重复制模式。目标轮次由弹性轮次决策确定（首次执行 10 轮，回退重执行按影响范围分数缩减）。子代理每轮遍历全部集成场景，逐条多服务协作验证。

> 通用规范（复杂度公式、轮次执行细节、prompt 规范、弹性轮次决策、验证门控）参见 `skills/kflow-integration-test/references/repetition.md`

### 阶段特定参数

- **遍历项**：integration-tests/ 全部集成场景
- **每轮工作**：逐条多服务协作验证 + 四分法根因分类处理失败 + 架构评估自动触发
- **复杂度权重**：集成场景数 × 2 + 子变更数 × 1.5
- **产物要求**：traceability.md「集成测试」列覆盖率 = 100%，round-{n}.md + summary.md 标记「集成测试通过」

---

## 与其他 Skill 的关系

- **输入来自**：
  - 前后端项目：`kflow-e2e-test`（所有子变更 E2E 测试通过后）
  - 纯后端项目：`kflow-api-test`（所有子变更接口单元测试通过后）
- **输出给**：`kflow-audit`（审计门控） → `kflow-archive`（归档）
- **前置阶段**：所有子变更编码+审查+测试通过 + 服务刷新
- **后续阶段**：审计 → 归档
- **内聚功能**：变更级缺陷修复（四分法），不跳转到 `kflow-bug-fix`
- **服务管理**：变更级 agent 独占服务生命周期管理，每轮集成测试前编译重启
- **关系说明**：`kflow-bug-fix` 仅处理子变更级缺陷修复（二分法），变更级修复由本 Skill 内聚处理
- **执行模式**：弹性重复制，目标轮次由弹性轮次决策确定（参见 skills/kflow-integration-test/references/repetition.md §14），复杂度评估仅信息展示，主 Agent 验收闭环

---

## 反馈机制

如果在使用本 Skill 过程中发现问题或有优化建议，请记录到 `docs/skill-suggestion.md` 文件中。
