# 阶段钩子执行规范（运行时）

> **版本**: 1.1.0
> **类型**: 运行时共享文件（被各阶段 SKILL.md 引用）
> **创建时间**: 2026-05-28
>
> **v1.2.0**: bug-fix 快车道模式的钩子支持项目级与变更级两种缺陷工作区——`CHECK_STATE` / `RELOAD` / `UPDATE_STATE` 的路径按 triage 声明的工作区解析（项目级 `docs/bugs/` / 变更级 `docs/changes/{change}/bugs/`），验证目标扩展为已有测试、新增回归测试与手工验证步骤。

> **加载层级**: 服务层
> **适用阶段**: api-test/e2e-test/integration-test

本文档是各阶段 PRE_HOOK 和 POST_HOOK 的运行时执行规范。阶段 Skill 的 SKILL.md 在执行流程中通过引用本文档接入钩子机制，不在自身 SKILL.md 中内联复制钩子逻辑。

---

## 一、12 阶段钩子配置表

| 阶段 | 需要服务 | RELOAD 清单 |
|------|:------:|------------|
| explore | ❌ | CONTEXT.md, functional-designs/index.md, module-summary.md(条件), .status.md |
| prototype-design | 🔶 浏览器 | CONTEXT.md, toolchain.md, functional-designs/, docs/designs/prototypes/manifest.md(条件), prototype-changes.md(条件), .status.md |
| design | ❌ | CONTEXT.md, functional-designs/, functional-designs/index.md, module-summary.md(条件), docs/designs/prototypes/manifest.md(条件), prototype-changes.md(条件), .status.md |
| plan | ❌ | detailed-design.md, functional-designs/index.md, functional-designs/part-NN.md, module-summary.md(条件), api-tests/index.md, docs/designs/prototypes/manifest.md(条件,前端SC), prototype-changes.md(条件,前端SC), .status.md |
| code | 🔶 编译验证 | service-guide.md, CONTEXT.md, detailed-design.md, functional-designs/index.md, docs/designs/prototypes/manifest.md(条件,前端SC), prototype-changes.md(条件,前端SC), .status.md |
| code-review | ❌ | service-guide.md, CONTEXT.md, detailed-design.md, functional-designs/index.md, docs/designs/prototypes/manifest.md(条件,前端SC), prototype-changes.md(条件,前端SC), .status.md |
| api-test | ✅ 后端 | service-guide.md, api-tests/, detailed-design.md, functional-designs/index.md, docs/designs/prototypes/manifest.md(条件), prototype-changes.md(条件), .status.md |
| e2e-test | ✅ 前后端 | service-guide.md, e2e-tests/, detailed-design.md, functional-designs/index.md, docs/designs/prototypes/manifest.md(条件,前端SC), prototype-changes.md(条件,前端SC), .status.md |
| integration-test | ✅ 前后端 | service-guide.md, integration-tests/, detailed-design.md, functional-designs/index.md, docs/designs/prototypes/manifest.md(条件), prototype-changes.md(条件), .status.md |
| audit | ❌ | 全量产物, cross-reviews/, test-reports/, .status.md |
| bug-fix | 同触发阶段 | service-guide.md, 相关文档, .status.md |
| archive | ❌ | 全量产物, .status.md |

> 上表为概览；各文件的**定位来源**（`index.md` 或章节号）见 §4.1，读取侧 SHALL 按定位来源读取目标分册或行区间。

### 图例

| 图例 | 含义 |
|------|------|
| ❌ | 不需要服务，仅执行 CHECK_STATE + RELOAD |
| 🔶 浏览器 | 需要浏览器进程（Playwright），阶段结束后清理 |
| 🔶 编译验证 | 仅编译验证（不启动持久服务） |
| ✅ 后端 | 需要后端服务持久运行 |
| ✅ 前后端 | 需要前后端服务同时运行 |
| 同触发阶段 | 继承触发阶段的钩子配置 |

### 裁剪阶段的钩子豁免

变更档位为 `轻量` 且某阶段被阶段适用性声明判定为 `⏭️ 不适用` 时，该阶段的钩子 SHALL NOT 执行：

| 阶段 | 裁减时跳过的钩子步骤 | 说明 |
|------|-------------------|------|
| api-test | PRE_HOOK 全部步骤（含 READ_SERVICE_GUIDE/COMPILE/MIGRATE/START_SERVICE/HEALTH_CHECK）与 POST_HOOK 全部步骤 | SHALL NOT 启动服务，SHALL NOT 重启或停止服务 |
| e2e-test | 同上（含 COMPILE_BE/COMPILE_FE/START_FE/HEALTH_FE） | SHALL NOT 启动浏览器进程 |
| integration-test | 同上 | SHALL NOT 执行变更级服务刷新与集成测试收尾 |

> 裁剪阶段的豁免仅适用于上述三个阶段，且 MUST 以变更级 `.status.md` 的阶段适用性声明依据为前提。无声明依据的 `⏭️` SHALL NOT 触发豁免，按门控规则阻塞。裁剪判定见 [gates.md](gates.md) §1.2，声明字段定义见 [state-values.md](state-values.md) §5。
>
> **豁免范围**: PRE_HOOK 与 POST_HOOK 整体跳过，包括 `CHECK_STATE`、`RELOAD`、服务生命周期操作与 `UPDATE_STATE`。阶段状态由 kflow-design 在写入适用性声明时一次性标记为 `⏭️ 不适用`，不由被裁剪阶段自身更新。

### bug-fix 快车道模式的钩子

`kflow-bug-fix` 的**快车道模式**（由 `kflow-bug-triage` 的 L4 结论触发、无触发测试阶段上下文）不适用「同触发阶段」的继承规则，其钩子配置独立，并支持项目级与变更级两种工作区：

| 钩子 | 服务依赖 | 步骤 |
|------|:------:|------|
| PRE_HOOK | ❌ 不需要服务 | `CHECK_STATE`（验证 triage 声明工作区的缺陷级状态文件存在且受影响项清单已填）→ `RELOAD`（重读缺陷级产物与受影响项代码） |
| POST_HOOK | ❌ 不需要服务 | `UPDATE_STATE` → 更新**缺陷级** `bugfix-status.md`（修复记录区 / 定向验证区 / 收口结论区） |

> **服务依赖说明**: 快车道模式 SHALL NOT 启动、停止或刷新任何服务，SHALL NOT 执行编译 / 迁移 / 健康检查——其验证为**定向验证**（仅执行受影响项清单覆盖的验证目标：已有测试 / 新增回归测试 / 手工验证步骤），由修复者本地执行。
>
> **状态写入边界**: 快车道模式的 POST_HOOK SHALL NOT 更新变更级 `.status.md` 的阶段状态、`执行轮次` 或 `终止结果` 字段。项目级工作区下 SHALL NOT 读写任何变更级状态文件。状态写入边界详见 `skills/kflow-plan/references/state-values.md` 与 `bugfix-fast-lane` 能力。

---

## 二、PRE_HOOK 执行步骤

### 2.1 不需要服务的阶段（❌）

```
PRE_HOOK（轻量）:
  1. CHECK_STATE → 验证前置阶段状态为 ✅ 完成
  2. RELOAD      → 按 RELOAD 清单重读基础信息文件
```

## 三、POST_HOOK 执行步骤

### 3.1 不需要服务的阶段（❌）

```
POST_HOOK（轻量）:
  1. UPDATE_STATE → 更新 .status.md（阶段状态、完成时间）
```

## 四、RELOAD 清单详情

### 4.1 各阶段 RELOAD 文件列表

清单中的每个条目 SHALL 标注定位来源——`index.md`（经索引定位目标分册）或章节号（按章节定位目标区间）。读取侧 SHALL 按标注的来源定位后读取目标分册或行区间，SHALL NOT 整体读取已拆分文档或大体量单文件。

| 阶段 | 必须重读文件（定位来源） | 条件重读文件（定位来源） |
|------|------------------------|------------------------|
| explore | `CONTEXT.md`（术语表章节）、`functional-designs/index.md`（全文，索引）、`.status.md`（全文） | `module-summary.md`（如存在，全文） |
| prototype-design | `CONTEXT.md`（术语表章节）、`toolchain.md`（全文）、`functional-designs/index.md`（全文）、`.status.md`（全文） | `docs/designs/prototypes/manifest.md`（按页面 ID 定位条目）；`prototype-changes.md`（按本变更页面 ID 定位） |
| design | `CONTEXT.md`（术语表章节）、`functional-designs/index.md`（全文）、`.status.md`（全文） | `module-summary.md`（如存在，全文）；`manifest.md`（按页面 ID）；`prototype-changes.md`（按页面 ID）；`functional-designs/part-NN.md`（经 index.md 定位目标分册） |
| plan | `detailed-design.md`（经 `detailed-design/index.md` 定位子变更相关设计域，单文件时按章节标题定位）、`functional-designs/index.md`（全文）、`api-tests/index.md`（全文）、`.status.md`（全文） | `functional-designs/part-NN.md`（经 index.md 定位）；`module-summary.md`；`manifest.md`；`prototype-changes.md` |
| code | `service-guide.md`（dev 环境章节）、`CONTEXT.md`（术语表章节）、`detailed-design.md`（按子变更相关设计域章节定位）、`functional-designs/index.md`（全文）、`.status.md`（全文） | `manifest.md`（前端 SC，按页面 ID）；`prototype-changes.md`（前端 SC） |
| code-review | `service-guide.md`（dev 环境章节）、`CONTEXT.md`（术语表章节）、`detailed-design.md`（按子变更相关设计域章节定位）、`functional-designs/index.md`（全文）、`.status.md`（全文） | `manifest.md`（前端 SC，按页面 ID）；`prototype-changes.md`（前端 SC） |
| api-test | `service-guide.md`（dev 环境章节）、`api-tests/index.md`（全文）、`api-tests/part-NN.md`（经 index.md 定位本阶段用例分册）、`detailed-design.md`（接口设计章节）、`functional-designs/index.md`（全文）、`.status.md`（全文） | `manifest.md`（如存在）；`prototype-changes.md`（如存在） |
| e2e-test | `service-guide.md`（dev 环境章节）、`e2e-tests/index.md`（全文）、`e2e-tests/part-NN.md`（经 index.md 定位）、`detailed-design.md`（页面/流程相关章节）、`functional-designs/index.md`（全文）、`.status.md`（全文） | `manifest.md`（前端 SC）；`prototype-changes.md`（前端 SC） |
| integration-test | `service-guide.md`（dev 环境章节）、`integration-tests/index.md`（全文）、`integration-tests/part-NN.md`（经 index.md 定位）、`detailed-design.md`（跨子变更接口契约章节）、`functional-designs/index.md`（全文）、`.status.md`（全文） | `manifest.md`（如存在）；`prototype-changes.md`（如存在） |
| audit | 全量产物（经各文档组 index.md 定位）、`cross-reviews/`（最新批次目录）、`test-reports/`（各阶段 `summary.md`）、`.status.md`（全文）、`status-log.md`（审计场景读取） | — |
| bug-fix | `service-guide.md`（dev 环境章节）、失败测试报告（按用例 ID 定位）、相关设计文档（经 index.md 或章节标题定位）、`.status.md`（全文）；**快车道模式**见 §2.6 / §3.5（不读 `.status.md`，按 triage 声明的工作区读取缺陷级产物） | — |
| archive | 全量产物（经各文档组 index.md 定位）、`.status.md`（全文） | — |

### 4.2 RELOAD 执行规则

1. 仅重读 RELOAD 清单中列出的文件，并按清单标注的定位来源读取目标分册/章节/行区间
2. 文件 mtime 未变化且已在当前会话中读取过，可跳过重读
3. 文件 mtime 发生变化或首次读取时 SHALL 完整重读（已拆分文档仍按定位来源读取目标分册）
4. RELOAD 清单中文件不存在时 ❌ 阻塞，不继续执行

### 4.3 RELOAD 增量模式

子代理是全新上下文，每次冷启动必须完整重读所有 RELOAD 文件。对于大型变更（detailed-design.md 多文件、functional-designs/ 多文件），RELOAD 的 Token 开销显著。增量模式允许主 Agent 为已读取且未变化的文件生成"已验证标记"，子代理收到标记后可跳过完整读取。

#### 4.3.1 已验证文件标记格式

主 Agent 在子代理 prompt 中注入以下格式的标记块：

```markdown
## RELOAD 已验证文件 (mtime 未变, 本会话已读取)
以下文件自上次读取后未发生变化，你可以信任主 Agent 提供的摘要信息：
- CONTEXT.md (术语表): {2 行摘要}
- functional-designs/index.md: {1 行摘要}
- detailed-design.md: {3 行摘要, 仅当前子变更相关域}
```

每条标记包含：
- **文件路径**：RELOAD 清单中的文件路径
- **文件角色**：括号内标注文件用途（如"术语表"）
- **摘要信息**：1-3 行关键内容摘要，足以覆盖子代理常规引用需求

#### 4.3.2 主 Agent 生成标记的时机和规则

| 规则 | 说明 |
|------|------|
| 生成时机 | 每次调度子代理前，对 RELOAD 清单中的文件逐一检查 |
| mtime 检查 | 文件 mtime 未变化且主 Agent 在当前会话中已读取过该文件时，方可生成标记 |
| 摘要生成 | 主 Agent 从已读取的文件内容中提取 1-3 行关键摘要写入标记 |
| mtime 已变 | 文件 mtime 发生变化时 SHALL 不生成标记，子代理须完整重读 |
| 首次读取 | 主 Agent 在当前会话中未读取过的文件 SHALL 不生成标记 |
| 标记有效期 | 仅在当前子代理调用内有效，下一个子代理调用时须重新检测 mtime |

#### 4.3.3 子代理收到标记后的行为规则

| 规则 | 说明 |
|------|------|
| 跳过完整读取 | 收到已验证标记的文件，子代理 SHALL NOT 重新完整读取 |
| 使用摘要 | 引用标记文件内容时，使用主 Agent 提供的摘要信息 |
| 保留自行读取权 | 执行过程中如发现摘要信息不足（超出摘要范围），子代理 SHALL 自行读取完整文件 |
| 标记不可传递 | 子代理不得将标记转发给其他子代理或假设标记在其他上下文中有效 |

---

## 五、服务生命周期操作步骤

服务生命周期具体操作指令定义在 `skills/kflow-code/references/service-lifecycle.md` 中。本文档仅列出各阶段各服务类型需要执行的操作步骤。执行时参考 `service-lifecycle.md` 获取每条指令的具体调用方式。

### 5.1 各服务类型操作映射

| 操作 | ❌ 不需要服务 | 🔶 编译验证 | ✅ 后端 | ✅ 前后端 |
|------|:---------:|:--------:|:-----:|:------:|
| CHECK_STATE | ✅ | ✅ | ✅ | ✅ |
| RELOAD | ✅ | ✅ | ✅ | ✅ |
| CHECK_PORTS | — | — | ✅ | ✅ |
| STOP_STALE | — | — | ✅ | ✅ |
| COMPILE | — | ✅（仅编译） | ✅ | ✅（前后端） |
| MIGRATE | — | — | ✅ | ✅ |
| START_SERVICE | — | — | ✅（后端） | ✅（前后端） |
| HEALTH_CHECK | — | — | ✅（/health, /db-health） | ✅（/health BE+FE, /db-health） |
| STOP_SERVICE | — | — | ✅ | ✅ |
| VERIFY_STOP | — | — | ✅ | ✅ |
| BROWSER_CLEANUP | — | 🔶（如有） | — | ✅（如有） |
| UPDATE_STATE | ✅ | ✅ | ✅ | ✅ |
