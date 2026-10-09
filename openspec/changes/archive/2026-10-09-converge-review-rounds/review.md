# Review Record — converge-review-rounds

> 本文件记录实现阶段（`/opsx:apply`）的端到端走查结论与验证证据。它是本变更的非 schema 产物，
> 不参与 delta 规格应用；归档时随变更一并移动至 `openspec/changes/archive/`。

## 1. 走查方法

按更新后的实现文件逐步骤推演，不执行真实阶段。推演对象：

- 设计自审口径：`skills/kflow-explore/SKILL.md`（步骤 8e / 11）、`skills/kflow-explore/references/self-review.md`、`skills/kflow-explore/references/self-review-dimensions.md`
- 执行类口径：`skills/kflow-code/references/repetition.md`（§4 / §7 / §8 / §9 / §14 / §15）

## 2. 轻量档端到端走查（对应任务 8.3）

**样例**：某「功能缺陷级」变更，FP ≤ 3，`变更档位 = 轻量`，走 `kflow-explore` 阶段。

| 步骤 | 推演结果 | 依据 |
|------|---------|------|
| 步骤 8 — TIER | 写入 `.status.md`「变更档位 = 轻量」 | `SKILL.md` 步骤 8c |
| 步骤 10 — OUTPUT | 产出 `functional-designs/index.md` + `part-NN.md`（压缩为单页） | `SKILL.md` 步骤 8e 表（轻量档行） |
| 步骤 11 步 2 — 确定轮次上限 | 读到 `轻量` → **轮次上限 = 1**；下限恒为 1（`SKILL.md:453`） | `SKILL.md` 步骤 11「自审执行流程」第 2 步 |
| 步骤 11 步 3 — 创建目录 + 启动子代理 | **创建 `self-reviews/explore/` 目录** 并启动第 1 轮 `Agent(subagent_type="claude")` | `SKILL.md` 步骤 11「自审执行流程」第 3 步 |
| 步骤 11 步 5 — 判定见证轮 | 主 Agent 读取报告，按 (a) 零新发现 + (b) 零修改 + (c) 全量遍历证明 判定 | `references/self-review.md` §4.5 |
| 步骤 11 步 9 — 轮次控制 | 轻量档（上限 1）：第 1 轮即为见证轮 → 终止；否则因已达上限而终止 | `SKILL.md` 步骤 11「自审执行流程」第 9 步 |
| 步骤 11 步 10 — 写终止原因 | 写入 `.status.md`「终止原因」= `收敛`（第 1 轮见证轮）或 `达上限`（第 1 轮非见证轮） | `SKILL.md:471`、`SKILL.md:484` |
| 附加硬门 — 产物门控 | 校验 `functional-designs/` 产物存在性与占位符；任一缺失或含占位符 → 阻塞该阶段 | `references/self-review.md` §4.4 |

**结论 1 — 轻量档确实执行 1 轮自审**：步骤 11 的轮次上限表列出「轻量 | 下限 1 | 上限 1」，
「自审执行流程」第 2 步明确「下限恒为 1 轮，无 0 轮豁免路径」，强制执行规则首条为
「全部档位 SHALL 至少执行 1 轮自审，SHALL NOT 存在 0 轮豁免路径」。

**结论 2 — 轻量档确实保留产物门控**：门控被改写为**附加**硬门（不再「替代自审」），
`references/self-review.md` §4.4 与 `SKILL.md` 步骤 11 一致。

**结论 3 — 无「跳过自审」路径**：`grep -n "跳过自审\|跳过 SELFREV" skills/kflow-explore/SKILL.md` **无命中**。
`kflow-explore` 中唯一的自审跳过条件是 `kflow-prototype-design` 阶段的**审查方式 = 人工审查**
（与档位无关），不存在按档位跳过自审的分支。

**结论 4 — `.status.md` 记录终止原因**：终止原因字段写入点在 `SKILL.md:471`（流程第 10 步）、
`SKILL.md:484`（强制执行规则），取值域为 `收敛` / `达上限`。

## 3. 完整档端到端走查（对应任务 8.4）

**样例**：某「产品需求级」变更，`变更档位 = 完整`，走 `kflow-code`（编码阶段，执行类口径）。

| 步骤 | 推演结果 | 依据 |
|------|---------|------|
| 1.5 CHECK_HISTORY / INIT | 读到 `完整` → **轮次上限 N = 5**；写入 `.status.md`「执行轮次 = 1 / 5」 | `repetition.md` §4 流程图、§14.2 档位表、§14.3 判定流程 |
| 2. PROMPT | 注入收敛驱动遍历指令：「执行轮次 SHALL 不少于 1 轮且不超过轮次上限 N（= 5）」 | `repetition.md` §10 表 |
| 4. ITERATE | 每轮全量遍历；每轮结束后递增计数器并提取轮间摘要注入下一轮（第 2 轮起） | `repetition.md` §4、§13 |
| 分支 A — 第 3 轮达标 | 若第 3 轮零新发现 + 零修改 + 报告证明全量遍历 → 该轮为**见证轮** → 终止 | `repetition.md` §14.5 终止条件 1 |
| 分支 B — 至第 5 轮仍未收敛 | 每轮均有新发现或存在修改 → 继续；第 5 轮（= 上限）→ 终止 | `repetition.md` §14.5 终止条件 2 |
| 5. ACCEPT | 判据：`执行轮次 >= 1` 且（最近一轮为见证轮 **或** `执行轮次` = 轮次上限） | `repetition.md` §8 验收表「执行轮次达标」行 |
| 6. RESULT | 终止原因写入 `.status.md`：分支 A → `收敛`（且 `执行轮次 = 3 < 5`，触发 §15 验证门控）；分支 B → `达上限` | `repetition.md` §8「终止原因」行、§15 |

**结论 1 — 轮次上限为 5**：`repetition.md` §14.2 档位表「完整 | 5」；§14.1 明确「变更档位表示**轮次上限**，
SHALL NOT 表示必须完成的固定轮次数」；§14.4 规定 prompt 中的上限数值「SHALL NOT 硬编码为 10」。

**结论 2 — 达上限仍无见证轮触发非收敛分支**：`repetition.md` §14.6 规定该情形 SHALL：
① 记录 `docs/skill-suggestion.md`（含阶段、当前轮次 / 轮次上限、终止原因 `达上限`、覆盖缺口详情、改进建议）；
② 使用 AskUserQuestion 询问「验收不通过，是否重新启动 Agent 迭代子代理？」；
③ 用户选「否」→ 标记 `.status.md` 为 ⚠️ 需修订并**阻塞当前阶段**；系统 MAY 将该阶段标记为 ⚠️ 阻塞。

**结论 3 — 三项要素齐备**：`skill-suggestion.md` 记录、`AskUserQuestion` 询问、⚠️ 阻塞标记
三者均在 §14.6 中显式出现，并与 §9 类型 B 的验收分流保持一致（不新增范式）。

**结论 4 — 收敛提前终止合法且不放松质量**：分支 A 下 `执行轮次 = 3 < 轮次上限 5` 仍验收通过，
但 SHALL 额外满足 §15 验证门控（受影响项 100% + 全量 ≥1 轮兜底 + 产物完整性）——
即「上限 5」不会因提前收敛而放行未覆盖项。

## 4. 交付约束说明（对应任务 7.2）

任务 7.2 的验证命令 `grep -ln "5 轮子代理串行\|不允许提前终止\|目标轮次" openspec/specs/*/spec.md`
在 5 份 Purpose 段全部修正后仍命中 9 行。经核对 OpenSpec 归档实现
（`@fission-ai/openspec/dist/core/specs-apply.js`），这 9 行全部位于**标题**，且其中 2 行受
归档契约的硬约束**不得改动**：

| 命中行 | 类型 | 为何保留 |
|--------|------|---------|
| `tier-driven-repetition` L142 `### Requirement: 目标轮次写入状态文件` | MODIFIED 目标 | 本变更 delta 的 MODIFIED 块按名称匹配该 requirement；改名将导致归档时 `MODIFIED failed ... not found` 硬报错 |
| `tier-driven-repetition` L146 `#### Scenario: 轮次计数器呈现目标轮次` | MODIFIED 内的 Scenario | 归档实现校验「主规格当前块中存在但 delta 修改块中缺失的 Scenario 名」并硬报错；改名将触发 `current spec contains scenario(s) not present in the modified block` |
| `agent-iteration-execution` L9 / L13 / L35 | REMOVED 目标内 | 该 requirement 被 delta 的 REMOVED 块按名称删除，归档时随之一并消失 |
| `plan-self-review` L23 | REMOVED 目标内 | 同上 |
| `prototype-navigation-verification` L9 | REMOVED 目标内 | 同上（requirement 标题 `5 轮子代理串行导航验证` 即被删除的目标名） |
| `prototype-playwright-5round-verification` L9 | REMOVED 目标内 | 同上 |
| `subagent-self-review` L28 | REMOVED 目标内 | 同上 |

即：**7.2 的 Purpose 交付项已 100% 完成**；剩余 9 行是 delta 自身的名称契约产物，
在归档应用 delta 时由工具消除，人工预改会破坏归档。

其余所有维度均已达成零残留（任务 7.1 / 7.3 及 6.1–6.3 的验证命令全部通过）。
