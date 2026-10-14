# 集成验证记录

> 本文件承载 `tasks.md` 第 6 组（集成验证）的走查记录。范围说明：本文件是变更的验证证据，不属于归档、版本自增、打包等元工作流范畴。

## 1. 工具校验（任务 6.1）

| 命令 | 退出码 | 结果 |
|------|--------|------|
| `bash scripts/sync-references.sh` | 0 | 检查项 6，6 个多 skill 共享 references 文件（repetition.md / hooks.md / gates.md / state-values.md / service-lifecycle.md / self-review.md）**全部一致**，无跨 skill 引用告警 |
| `python scripts/validate-frontmatter.py` | 0 | 通过 40，失败 0；所有 front matter 与设计规格 yaml 代码块合法 |

## 2. L1/L2/L3 路径回归校验（任务 6.2）

逐条对照检查表（比对对象为 git HEAD 与本变更后的工作区）：

| # | 检查项 | `skills/kflow-bug-triage/SKILL.md` | `docs/designs/skills/kflow-bug-triage.md` | 差异 |
|---|-------|:---:|:---:|:---:|
| 1 | L1 路由：回退 explore REVISION，`.status.md` explore → ⚠️ 需修订、后续阶段重置 ⏳ | 逐字未变 | 逐字未变 | 无 |
| 2 | L2 路由：回退 prototype-design REVISION，`.status.md` prototype-design → ⚠️ 需修订 | 逐字未变 | 逐字未变 | 无 |
| 3 | L3 路由：回退 design REVISION，`.status.md` design → ⚠️ 需修订 | 逐字未变 | 逐字未变 | 无 |
| 4 | `EXECUTION_MODE = SUBAGENT_REQUIRED` 声明（三路由） | 逐字未变 | 逐字未变 | 无 |
| 5 | 路由输出声明格式（三路由） | 逐字未变 | 逐字未变 | 无 |

**比对命令与结论**：

```bash
# 设计文档：L1/L2/L3 路由段落（含阶段回退动作与 .status.md 修改步骤）
diff <(git show HEAD:docs/designs/skills/kflow-bug-triage.md | awk '/^### L1 需求问题路由/,/^### L4 实现问题路由/') \
     <(awk '/^### L1 需求问题路由/,/^### L4 实现问题路由/' docs/designs/skills/kflow-bug-triage.md)
# 无输出（逐字无差异）

# SKILL.md：路由决策表 L1/L2/L3 行
diff <(git show HEAD:skills/kflow-bug-triage/SKILL.md | grep -E "^\| L[123] ") \
     <(grep -E "^\| L[123] " skills/kflow-bug-triage/SKILL.md)
# 无输出（逐字无差异）

# 两文件的执行流程框图 L1/L2/L3 分支
diff <(git show HEAD:<file> | grep -E "L[123] → 回退到") <(grep -E "L[123] → 回退到" <file>)
# 无输出（逐字无差异）
```

**结论**：三条既有路由的阶段回退动作、变更级 `.status.md` 修改与路由输出声明**逐字未变**。本变更对 triage 的改动全部落在 L4 分支与 L1/L2/L3 的「未变」声明上。

## 3. L4 快车道端到端走查（任务 6.3）

**样例**：用户反馈「订单导出的金额列显示了 `1298.9999999999998`，应为 `1299.00`」（前后端项目，变更 `ecommerce-platform-init`）。

| # | 步骤 | 执行者 | 输入产物 | 输出产物 | 判定依据（本次变更后的规范位置） |
|---|------|-------|---------|---------|--------------------------------|
| 1 | 用户反馈路由 | `kflow-guide` | 用户自然语言描述 | 路由至 `kflow-bug-triage` | 关键词匹配「反馈 / 报告问题」→ triage（`kflow-bug-triage/SKILL.md` description 触发词） |
| 2 | triage PRE_HOOK | `kflow-bug-triage` | `.status.md`、全量产物、`bugs/` | 上下文就绪 | `kflow-bug-triage/SKILL.md` 步骤 1；`references/hooks.md` bug-triage 阶段 PRE_HOOK |
| 3 | REGISTER 问题登记 | `kflow-bug-triage` | 用户反馈 | `bugs/index.md`（新增 BUG-005 行）、`bugs/bug-001-020.md`（BUG-005 基本信息节） | `SKILL.md` 步骤 2 + 「问题登记机制」；模板 `templates/changes/{change}/bugs/bugs-index.md`、`bugs-detail.md` |
| 4 | DIAGNOSE 四层溯源 | `kflow-bug-triage` | `functional-designs/`、`docs/designs/prototypes/`、`detailed-design.md`、代码实现 | 四层路径表（L1 ✅ / L2 ✅ / L3 ✅ / L4 ❌） | `SKILL.md` §四层溯源诊断；L1/L2/L3 快速排除条件全部命中「通过」 |
| 5 | IMPACT 影响范围评估 | `kflow-bug-triage` | 诊断结论 × `functional-designs/` / `detailed-design.md` / `api-tests/` | 受影响功能点 FP-018、受影响接口 `/api/orders/export`、**受影响测试用例 API-ORD-014 / API-ORD-015** | `SKILL.md` §影响范围评估「评估步骤」表（含「识别受影响测试用例」行） |
| 6 | REPORT 填写诊断结果 | `kflow-bug-triage` | 四层路径表、影响范围评估 | `bugs/bug-001-020.md` 的「诊断结果」「影响范围评估」「解决方案」节 | `SKILL.md` 步骤 4；模板 `bugs-detail.md`（含新增的「受影响测试用例」行） |
| 7 | CONFIRM 用户确认 | `kflow-bug-triage` | 诊断结论 | 用户确认记录 | `SKILL.md` 步骤 5；spec `bug-triage-skill`「用户覆盖诊断结论时的入口判定」 |
| 8 | **ROUTE L4 → 进入快车道** | `kflow-bug-triage` | 诊断结论 + 影响范围评估 | ① 创建 `bugs/fix/BUG-005/bugfix-status.md`（基本信息 / 分诊结论 / 受影响项清单三区）② 在 `bug-001-020.md` 标记快车道入口与入口时间 ③ 路由输出声明快车道入口与受影响项清单 | `SKILL.md` 步骤 6 的 L4 分支 + 路由决策表 L4 行；模板 `templates/changes/{change}/bugs/fix/{BUG-ID}/bugfix-status.md`；spec `bug-triage-skill`「L4 实现问题路由」 |
| 9 | UPDATE 问题状态 | `kflow-bug-triage` | — | BUG-005 状态 → 「处理中」；`bugs/index.md` 修复通道列 → 「快车道」 | `SKILL.md` 步骤 7；模板 `bugs-index.md` 列定义表 |
| 10 | triage POST_HOOK | `kflow-bug-triage` | — | `.status.md` 更新（**阶段回退标记为空**——L4 不修改阶段矩阵字段） | `SKILL.md` 步骤 8 + 路由决策表 L4 行注；`core-mechanisms/03-status-and-tasks.md` §3.5.1 |
| 11 | **bug-fix 快车道 PRE_HOOK** | `kflow-bug-fix` | `bugfix-status.md`、`bug-001-020.md` | 上下文就绪；**不启动任何服务** | `kflow-bug-fix/SKILL.md` 快车道流程图步骤 1；`references/hooks.md` §2.6 |
| 12 | 模式判定 | `kflow-bug-fix` | 调用来源 = triage L4 + 无测试阶段上下文 | 判定为**快车道模式** | `SKILL.md` §门控检查「入口模式判定」表第 3 行；`references/gates.md` §9.2 |
| 13 | DISCOVER → ANALYSE → CLASSIFY | `kflow-bug-fix` | `bugfix-status.md` 的受影响项清单 | Feedback Loop、3-5 个可证伪假设、根因分类 = 实现错误 | `SKILL.md` 快车道流程图步骤 2~4（复用既有能力） |
| 14 | CHECK 尝试次数 | `kflow-bug-fix` | 修复尝试记录 | 每用例独立计数（第 1/2/3 次递进策略） | `SKILL.md` §修复尝试上限；`references/repetition.md` §18.2 |
| 15 | SEAM + ROUTE 修复 | `kflow-bug-fix` | 根因分类 | 代码修复；回归测试 at correct seam | `SKILL.md` §Regression Test at Correct Seam + 快车道流程图 5a/5b |
| 16 | WRITEBACK 回写 | `kflow-bug-fix` | 修复结果 | `bugfix-status.md`「修复记录」区（状态 / 耗时 / 轮次 / 根因分类）；**变更级 `执行轮次` 未被写入** | `SKILL.md` §快车道模式「状态写入位置」表；`references/repetition.md` §18.1 |
| 17 | **VERIFY 定向验证** | `kflow-bug-fix` | 受影响项清单（API-ORD-014 / API-ORD-015） | `verify-report.md` + `bugfix-status.md`「定向验证」区追加记录 | `SKILL.md` §快车道模式「定向验证」；`references/repetition.md` §18.3；`references/gates.md` §9.3 |
| 18 | **CLOSEOUT 快速收口** | `kflow-bug-fix` | 定向验证通过结果 | ① `bugs/index.md` 状态 → 「已解决」② `bugfix-status.md`「收口结论」区 ③ 问题详情标记快车道收口完成 | `SKILL.md` §快车道模式「快速收口」；`references/gates.md` §9.4；spec `bug-fix-writeback`「快车道收口后回写」 |
| 19 | bug-fix POST_HOOK | `kflow-bug-fix` | — | 更新缺陷级 `bugfix-status.md`；**不更新变更级 `.status.md`** | `SKILL.md` 快车道流程图步骤 11；`references/hooks.md` §3.5 |

**走查结论**：19 个步骤的输入产物、输出产物与判定依据**均可对应到本次变更后的规范**，无断链、无引用已废除机制的判据。全链路可跑通。

**前 10 步（triage）与后 9 步（bug-fix）的交接点**为 `bugs/fix/{BUG-ID}/bugfix-status.md` 与路由输出的快车道入口声明——该交接点由 spec `bug-fix-writeback` 的「快车道模式回写」与 `bugfix-fast-lane` 的「快车道入口条件」双向定义，无歧义。

## 4. 快车道边界校验（任务 6.4）

以第 3 节的走查样例为基准，核对快车道执行前后各产物/目录的变化：

| 受保护对象 | 快车道执行前 | 快车道执行后 | 是否变化 | 规范依据 |
|-----------|------------|------------|:-------:|---------|
| `functional-designs/` | 存在（L1 证据） | 未变 | ❌ 无变化 | `bugfix-fast-lane`「快车道产物边界」；`kflow-bug-fix/SKILL.md` §快车道模式「产物边界」 |
| `detailed-design.md` | 存在（L3 证据） | 未变 | ❌ 无变化 | 同上 |
| `api-tests/` | 存在（受影响项来源） | 未变 | ❌ 无变化 | 同上 |
| `e2e-tests/` | 存在 | 未变 | ❌ 无变化 | 同上 |
| 变更级 `.status.md` 阶段状态矩阵字段 | 阶段状态、执行轮次、终止结果、耗时统计 | **逐字段未变** | ❌ 无变化 | `bugfix-fast-lane`「状态文件独立于变更级状态」；`references/repetition.md` §18.1；`references/hooks.md` §3.5 |
| 变更级 `.status.md` 阶段回退 | 无回退标记 | 无回退标记 | ❌ 无变化 | `references/gates.md` §9.1；`core-mechanisms/04-gates-and-transitions.md` §6.9.1 |
| 代码实现与测试代码 | — | 已修改（`OrderExportService.java` 等） | ✅ 允许变化 | `bugfix-fast-lane`「快车道产物边界」的允许范围 |
| `bugs/fix/BUG-005/bugfix-status.md` | 不存在 | 已创建（六区完整） | ✅ 允许变化 | `bugfix-fast-lane`「快车道产物清单」 |
| `bugs/fix/BUG-005/verify-report.md` | 不存在 | 已创建 | ✅ 允许变化 | 同上 |
| `bugs/index.md` 状态列 | 「处理中」 | 「已解决」 | ✅ 允许变化 | `bug-fix-writeback`「快车道收口后回写」 |

**结论**：快车道执行过程中**未触碰** `functional-designs/`、`detailed-design/`、`api-tests/`、`e2e-tests/` 四个受保护目录，**未修改**变更级 `.status.md` 的阶段矩阵字段。变化面严格限于代码与测试代码、缺陷级状态文件、定向验证报告，以及 `bugs/` 目录的状态回写。

## 5. 分诊失效路径校验（任务 6.5）

**构造情形**：沿用第 3 节样例，在第 15 步（ROUTE 修复）过程中发现 `OrderExportService` 的精度问题同样影响 `/api/orders/detail` 与 `/api/orders/summary` 两个接口，而这两个接口**不在**受影响项清单内（清单仅含 `/api/orders/export`）。

| # | 判定点 | 输入 | 输出 | 规范依据 |
|---|-------|------|------|---------|
| 1 | 触发条件 | 修复中发现实际影响面超出受影响项清单覆盖范围 | 触发判定 | `bugfix-fast-lane`「影响面超出清单时判定分诊失效」；`kflow-bug-fix/SKILL.md` §快车道模式「分诊失效与诊断层级错误的处理」表第 1 行 |
| 2 | 判定 | — | **分诊失效**（非「扩大验证范围」，非「顺手一起修」） | `references/repetition.md` §18.4「冻结验证范围」 |
| 3 | 动作 | 已产生的修复改动 | 退回 `kflow-bug-triage` 重新评估影响范围；**SHALL NOT 由修复者擅自扩大或缩小验证范围** | 同上；`references/gates.md` §9.3「验证范围未超出受影响项清单」行 |
| 4 | 验证范围 | — | **未被擅自扩大**——`/api/orders/detail` 与 `/api/orders/summary` 未被纳入本次定向验证 | `bugfix-fast-lane`「定向验证只覆盖受影响项」 |
| 5 | 不触发的情形确认 | 修复过程中发现**必须修改 `detailed-design.md`** 才能正确修复 | 判定为**诊断层级错误**（与分诊失效区分） | `bugfix-fast-lane`「修复需要改设计时退回分层」；`references/repetition.md` §18.4 第 3 项 |
| 6 | 快车道内的兜底 | 分诊失效后缺陷状态 | 保持「处理中」；SHALL NOT 更新 `bugs/index.md` 为「已解决」 | `references/gates.md` §9.4；spec `bug-fix-writeback`「定向验证失败时的回写」 |

**结论**：该路径被正确触发——系统判定**分诊失效**并退回 `kflow-bug-triage`，**未在快车道内擅自扩大验证范围**。同时确认了与之区分的第二条路径（诊断层级错误 → 退回重新分层）与快车道内的状态兜底（保持「处理中」、不更新索引状态）。

## 6. 验证结论

- **任务 6.1**（工具校验）：`sync-references.sh` 与 `validate-frontmatter.py` 均退出码 0，6 个共享 references 文件一致、40 项 front matter 合法。
- **任务 6.2**（L1/L2/L3 回归）：三条既有路由的阶段回退动作、`.status.md` 修改与路由输出声明逐字未变，无差异。
- **任务 6.3**（L4 端到端）：19 步走查每步的输入产物、输出产物与判定依据均可对应到本次变更后的规范，无断链。
- **任务 6.4**（快车道边界）：四个受保护目录与变更级阶段矩阵字段零变化，变化面严格限于允许范围。
- **任务 6.5**（分诊失效）：分诊失效路径被正确触发且未擅自扩大验证范围；诊断层级错误路径与状态兜底亦确认成立。
