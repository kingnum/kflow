# 设计文档：拆分 kflow-e2e-test + 修复归档条件

> **变更名称**: split-api-e2e-test-and-fix-archive
> **版本**: 1.0.0

---

## 一、kflow-api-test 设计规格

### 1.1 基本信息

```yaml
name: kflow-api-test
description: 接口单元测试阶段 - 使用 curl/HTTP 请求对 api-tests/ 中定义的接口逐条测试。适用于所有项目类型（前后端+纯后端）。强制 10 轮 Agent 迭代执行，每轮输出 round-{n}.md，最终输出 summary.md 含健康评分。覆盖 traceability.md「接口测试(ID)」列。/接口测试/API测试/接口单元测试
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

### 1.2 项目类型判断

| 项目类型 | 阶段处理 |
|---------|---------|
| 前后端项目 | 必须执行接口单元测试阶段（作为 E2E 测试前置） |
| 纯后端项目 | 必须执行接口单元测试阶段（作为最终验收标准） |

> **关键变更**：纯后端项目不再跳过接口单元测试。当前 `kflow-e2e-test` 声明纯后端项目 ⏭️ 跳过，导致 `kflow-design` 已生成的 `api-tests/` 无人执行。`kflow-api-test` 对所有项目类型必须执行。

### 1.3 门控检查

进入接口单元测试阶段前检查：
- .status.md 存在
- 编码状态 = ✅ 完成（含代码审查通过）
- 子变更代码审查报告存在 (test-reports/review/code-review.md)
- api-tests/ 测试用例文档存在
- docs/service-guide.md 存在（服务启动配置可用）

### 1.4 输出产物

| 产物 | 文件 | 图例 | 内容要求 |
|------|------|------|---------|
| API测试轮次报告 | subchanges/*/test-reports/api/round-{n}.md | ✅ 必须 | 接口测试用例执行结果 |
| API测试总结文档 | subchanges/*/test-reports/api/summary.md | ✅ 必须 | 各轮次统计、健康评分、是否通过 |
| 状态文件更新 | subchanges/*/.status.md | ✅ 必须 | 标记子变更测试阶段状态 |
| 变更状态更新 | .status.md | ✅ 必须 | 更新子变更进度矩阵 |

### 1.5 执行模式

Agent 迭代执行，强制 10 轮下限：
- 复杂度评估（接口数 × 1.5 + 场景数 × 2）
- 各轮次按节奏指引分配测试深度
- 覆盖率目标：traceability.md「接口测试(ID)」列 = 100%
- 主 Agent 验收：轮次计数器 = 10/10（硬性条件）

### 1.6 健康评分维度

| 维度 | 数据源 | 评分规则 |
|------|--------|---------|
| 功能完整性 | 测试用例执行结果 | 通过数/总数 × 100 |
| 响应时间 | curl 计时 | < 200ms 满分，每超 100ms 扣 10 分 |
| HTTP 状态码 | curl 返回码 | 非 2xx/3xx 扣分 |
| 错误处理 | 异常输入响应 | 正确错误码+消息体格式 |
| 契约一致性 | 与 api-tests/ 定义对比 | 响应结构匹配度 |

---

## 二、kflow-e2e-test 修改后设计

### 2.1 职责精简

移除所有接口单元测试职责，仅保留浏览器自动化测试：

| 职责 | 修改前 | 修改后 |
|------|--------|--------|
| 接口单元测试（curl） | ✅ 包含 | ❌ 移除（移交 kflow-api-test） |
| E2E 浏览器测试（Playwright） | ✅ 包含 | ✅ 保留 |
| API 轮次报告输出 | ✅ 包含 | ❌ 移除 |
| E2E 轮次报告输出 | ✅ 包含 | ✅ 保留 |
| generated-test.spec.ts | ✅ 包含 | ✅ 保留 |

### 2.2 门控检查更新

进入 E2E 测试阶段前检查：
- .status.md 存在
- 项目类型 = 前后端项目（纯后端项目跳过此阶段）
- **接口单元测试状态 = ✅ 完成**（新增：由 `kflow-api-test` 执行）
- 子变更代码审查报告存在 (test-reports/review/code-review.md)
- traceability.md「接口测试」列覆盖率 = 100%
- docs/service-guide.md 存在

### 2.3 输出产物精简

移除 API 测试产物，仅保留 E2E 测试产物。

---

## 三、kflow-archive 修复

### 3.1 修复位置

**位置 1**：§门控检查 第 37 行
```markdown
# 修改前
- 所有子变更各阶段完成检查（计划、编码、接口单元测试、E2E测试）
# 修改后
- 所有子变更各阶段完成检查（计划、编码、代码审查、接口单元测试、E2E测试）
```

**位置 2**：§归档条件 第 172 行
```markdown
# 修改前
- [ ] 所有子变更各阶段（计划、编码、接口单元测试、E2E测试）完成
# 修改后
- [ ] 所有子变更各阶段（计划、编码、代码审查、接口单元测试、E2E测试）完成
```

> **说明**：`core-mechanisms.md` §6.3（第 1049 行）已正确包含代码审查阶段，kflow-archive.md 为遗漏修复。

---

## 四、全局影响变更详情

### 4.1 core-mechanisms.md（7 处变更）

| 位置 | 变更 |
|------|------|
| §1.3 阶段差异表（第 40-41 行） | 接口单元测试行保持不变，但 Skill 映射需在 §12.3 更新 |
| §6.1 前后端流程图（第 867-869, 889 行） | 新增 `kflow-api-test` 节点：`计划 → 编码 → 代码审查 → 接口单元测试(kflow-api-test) → E2E测试(kflow-e2e-test)` |
| §6.1 纯后端流程图（第 906 行） | 新增 `kflow-api-test` 节点：`计划 → 编码 → 代码审查 → 接口单元测试(kflow-api-test)` |
| §3.4 门控规则（第 574-606 行） | 接口单元测试门控独立为 kflow-api-test；E2E 测试门控增加前置接口测试完成检查 |
| §12.3 调度映射表（第 1486-1487 行） | 拆分为两行：接口单元测试 → `kflow-api-test`；E2E测试 → `kflow-e2e-test` |
| §15 Agent 迭代执行（第 1680 行） | 执行类阶段列表增加 `kflow-api-test` |
| §6.3 归档条件（第 1049 行） | 已正确包含代码审查，无需修改 |

### 4.2 索引文件变更

| 文件 | 变更 |
|------|------|
| `docs/designs/index.md` §Skills 清单 | 新增 `kflow-api-test` 行；更新 `kflow-e2e-test` 描述为"E2E浏览器自动化测试" |
| `docs/designs/overview.md` §1.4, §3.1, §3.2 | 新增 Skill 行、更新实施顺序、更新依赖图（kflow-code-review → kflow-api-test → kflow-e2e-test） |
| `docs/designs/skills/index.md` | 新增 Skill 行、更新触发时机、更新依赖关系图、更新阶段流转图 |

### 4.3 关联 Skill 引用更新

| Skill | 位置 | 变更 |
|-------|------|------|
| kflow-guide.md | 第 228-229 行（流程概览表） | 拆分"接口单元测试"和"E2E测试"为两行，分别映射到 kflow-api-test 和 kflow-e2e-test |
| kflow-guide.md | 第 116 行（关键词映射） | "测试"关键词拆分为"接口测试/API测试"→kflow-api-test 和"E2E/QA/功能测试"→kflow-e2e-test |
| kflow-resume.md | 第 218-219 行（调度映射） | 拆分为两行 |
| kflow-code.md | 第 553 行（后续阶段） | 更新为 `代码审查 → 接口单元测试(kflow-api-test) → E2E测试(kflow-e2e-test)` |
| kflow-code-review.md | 第 225 行（输出给） | 更新为 `接口单元测试(kflow-api-test)` |
| kflow-bug-fix.md | 第 567 行（输入来自） | 更新为 `kflow-api-test（接口单元测试失败）、kflow-e2e-test（E2E 测试失败）` |
| kflow-integration-test.md | 第 360-361 行 | 更新输入来源引用 |
| kflow-audit.md | 第 281 行（回退路由） | 增加 `kflow-api-test` 到回退路由列表 |
| kflow-init.md | 第 88-89 行（工具推荐） | 接口单元测试行增加 Skill 名称 `kflow-api-test`；E2E 测试行增加 Skill 名称 `kflow-e2e-test` |
| templates/index.md | 第 30-34, 55-57 行 | API 测试模板（api-round-report, api-summary）产出 Skill 从 `kflow-e2e-test` 改为 `kflow-api-test`；E2E 模板保持不变 |

---

## 五、设计决策

### 决策 1：阶段顺序

**决策**：接口单元测试 → E2E 测试（串行，接口测试在前）

**理由**：
- 接口层问题应在浏览器层问题之前修复（成本更低）
- 纯后端项目仅需接口测试，无需 E2E
- 当前门控规则已定义此顺序

### 决策 2：traceability.md 列独立性

**决策**：保持「接口测试(ID)」和「E2E测试(ID)」两列独立

**理由**：
- 两阶段由不同 Skill 执行，对应列由各自 Skill 填写
- 覆盖率门控分别验证（接口测试列 = 100% → 释放 E2E 门控；E2E测试列 = 100% → 释放集成测试门控）

### 决策 3：执行模式

**决策**：两个 Skill 均采用 Agent 迭代执行模式（强制 10 轮下限）

**理由**：接口单元测试和 E2E 测试同属执行类阶段，适用现有 Agent 迭代框架。
