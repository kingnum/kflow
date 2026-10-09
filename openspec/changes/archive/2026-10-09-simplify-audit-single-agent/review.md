# Review Record — simplify-audit-single-agent

> 本文件记录实现阶段（`/opsx:apply`）的端到端走查结论与验证证据。它是本变更的非 schema 产物，
> 不参与 delta 规格应用；归档时随变更一并移动至 `openspec/changes/archive/`。

## 1. 走查方法

按改写后的实现文件逐步骤推演，不执行真实阶段。推演对象：

- 审计口径：`skills/kflow-audit/SKILL.md`（主改）、`skills/kflow-archive/SKILL.md` 与 `skills/kflow-archive/references/archive-rules.md`（门控项）、`skills/kflow-guide/SKILL.md`（路由表）
- 设计文档与产物形态：`docs/designs/` 下的 skill 规格、索引、核心机制、模板与示例
- 规格基准确认：本变更的 delta（`openspec/changes/simplify-audit-single-agent/specs/`）

## 2. 门控链路走查：EVALUATE → SCORE → REPORT（对应任务 6.2）

**样例**：两份变更，分别取 `变更档位 = 轻量` 与 `变更档位 = 完整`，均进入审计阶段。

### 2.1 EVALUATE（`SKILL.md` 执行流程步骤 4）

| 推演步骤 | 推演结果 | 实现依据 | delta 依据 |
|---------|---------|---------|-----------|
| 读变更档位 | 读变更级 `.status.md`「变更档位」；字段缺失按 `完整` 档处理 | `SKILL.md` §审计路径分流 引导句 | `审计四维度评估` 需求（各维度判定 SHALL 以变更档位为基准） |
| 确定执行者 | **无论档位，均启动 1 个审计子代理**；主 Agent 不执行审计、不启动并行子代理 | `SKILL.md:68-71`（分流表执行者列两行均为「审计子代理（1 个）」）、`SKILL.md:24`（角色）、`SKILL.md:208`（流程图步骤 4） | ADDED `审计由单一子代理执行` → Scenario `全部档位由单一子代理执行` |
| 轻量档分支 | 走轻量自检，三项检查项（阶段完整性 / 阶段产物存在性与无占位符 / 裁剪合法性），不启动并行评分 | `SKILL.md:73`、`SKILL.md:79`、`SKILL.md:80-84` | MODIFIED `轻量档审计降级为轻量自检` → Scenario `轻量档走轻量自检`、`轻量自检检查项` |
| 标准/完整档分支 | 走四维度事实采集（含 Post-mortem 汇总），逐维度呈现判定证据 | `SKILL.md:72`、`SKILL.md:208-211`、`SKILL.md:128` | MODIFIED `审计四维度评估`；ADDED `证据先于评分` |
| 子代理异常 | 新建子代理重跑，主 Agent 不接管，上限 3 次，不适用轮次级粒度 | `SKILL.md:75` | ADDED `审计子代理异常时的处置`；`subagent-isolation-rule` MODIFIED → Scenario `审计阶段的规则适用子集` |

**结论 1 — 执行者模型已统一为单一子代理**：`grep -n "4 个 Agent\|主 Agent（SHALL NOT 启动子代理）\|并行 Agent 评估" skills/kflow-audit/SKILL.md` 无命中；
分流两行执行者均为「审计子代理（1 个）」，与 `全部档位由单一子代理执行` 场景的 AND 子句（主 Agent SHALL NOT 直接执行、SHALL NOT 启动多个并行审计子代理）逐条对应。

**结论 2 — 轻量档不再由主 Agent 自检**：`grep -n "主 Agent 轻量自检" skills/kflow-audit/SKILL.md` 无命中；
轻量路径改写为「降为轻量自检（由审计子代理执行）」（`SKILL.md:79`），对应 `轻量自检 SHALL 由审计子代理执行`。

### 2.2 SCORE（`SKILL.md` 执行流程步骤 5）

| 推演步骤 | 推演结果 | 实现依据 | delta 依据 |
|---------|---------|---------|-----------|
| 轻量档 | 跳过评分：不算加权总分、不输出评分表 | `SKILL.md:79`、`SKILL.md:212`、`SKILL.md:361` | Scenario `轻量档走轻量自检`（SHALL NOT 计算加权总评分 / SHALL NOT 输出四维度评分表） |
| 标准/完整档 — 顺序 | **先完成四维度事实采集 → 逐维度呈现证据 → 统一评分**；不在采集未完成时输出得分 | `SKILL.md:126-131`（§证据先于评分）、`SKILL.md:280`（报告 §一.1 引导句） | ADDED `证据先于评分` → Scenario `证据先于评分`（4 条 AND 子句） |
| 标准/完整档 — 维度 | 四维度加权：流程与产物合规性 45% / 审查与缺陷闭环 30% / 测试充分性 15% / 效率与改进 10% | `SKILL.md:117-122`（四维度表）、`SKILL.md:291-298`（评分表） | MODIFIED `审计四维度评估`（维度与权重、合计 100%） |
| 档位基准 | 各维度以变更档位为基准给分，五组 SHALL NOT 误扣声明全部保留 | `SKILL.md:137-142`（按档位给分表） | MODIFIED `审计四维度评估` 各 Scenario 的 SHALL NOT 子句 |

**结论 3 — 四维度与权重逐字对应**：`SKILL.md:117-122` 四行维度名与权重为「流程与产物合规性 45% / 审查与缺陷闭环 30% / 测试充分性 15% / 效率与改进 10%」，合计 45 + 30 + 15 + 10 = 100%，
与 `审计四维度评估` 需求的「维度与权重为：流程与产物合规性 45%、审查与缺陷闭环 30%、测试充分性 15%、效率与改进 10%，权重合计 100%」逐字一致。

**结论 4 — 「证据先于评分」可被执行层检查**：约束落在两处可观测结构上——`SKILL.md:128` 的 SHALL/SHALL NOT 句式，以及报告格式 §一 的「1. 维度证据（先于评分）→ 2. 四维度评分（证据呈现完成后填写）」分节顺序（`SKILL.md:278-298`），
对应 `证据先于评分` 场景的「SHALL 先完成全部四个维度的事实采集 / AND SHALL 逐维度呈现判定证据 / AND SHALL 在证据呈现完成后才统一评分 / AND SHALL NOT 在证据采集未完成时输出维度得分」四句。

### 2.3 REPORT（`SKILL.md` 执行流程步骤 8 → 步骤 9 判定）

| 推演步骤 | 推演结果 | 实现依据 | delta 依据 |
|---------|---------|---------|-----------|
| 标准/完整档产物 | 输出审计报告：维度证据 + 四维度评分表 + 问题清单 + 改进建议 + 效率统计 | `SKILL.md:262-352`（报告格式） | MODIFIED `审计报告输出` → Scenario `审计报告内容` |
| 总分定位 | 总分标为「健康度参考，SHALL NOT 参与门控判定」 | `SKILL.md:124`、`SKILL.md:270`、`SKILL.md:300` | MODIFIED `审计报告输出`（加权总分 SHALL 仅作变更健康度参考） |
| 判定链路 | 判定依据问题清单严重度分级；总分低但无阻塞/严重级问题时仍判通过 | `SKILL.md:124`、`SKILL.md:213-220`（步骤 6 CLASSIFY） | MODIFIED `审计四维度评估` → Scenario `加权总分不参与门控` |
| 轻量档产物 | 简化审计记录：检查项结论 + 问题清单；无评分表与总分 | `SKILL.md:361-384`（简化记录格式） | MODIFIED `轻量档审计降级为轻量自检` → Scenario `轻量档审计报告形态`；MODIFIED `审计报告输出` → Scenario `轻量档审计记录形态` |
| 门控地位 | 轻量档发现阻塞级问题仍阻断归档 | `SKILL.md:94-98`（归档门控地位） | Scenario `轻量自检保留归档门控地位` |

**结论 5 — 「总分为健康度参考」在两处落点一致**：`SKILL.md:124`（维度章节总则）与报告格式的 §一.2 说明（`SKILL.md:300`）均声明总分不参与门控，
与 `加权总分不参与门控` 场景的「判定 SHALL 依据问题清单的严重度分级 / 加权总分 SHALL NOT 作为判定依据 / 总分低于任一阈值但无阻塞级与严重级问题时判定为通过」三句逐条对应。

**结论 6 — 轻量档产物形态未因执行者变更而改变**：三项检查项、不评分、简化记录结构均保持原状（`SKILL.md:80-98`、`SKILL.md:361-384`），
仅执行者由主 Agent 改为审计子代理，符合本变更 Non-Goals 中「不改变轻量档的产物形态」。

## 3. 全仓残留扫描（对应任务 6.1）

命令：`grep -rn "七维度\|六维度" skills/ docs/ README.md openspec/specs/`

### 3.1 命中分类

| 归属 | 命中位置 | 判定 |
|------|---------|------|
| kflow-verify 的七维度产物诊断 | `skills/kflow-verify/SKILL.md`（4 处）、`docs/designs/skills/kflow-verify.md`（4 处）、`docs/designs/skills/kflow-bug-triage.md:44`、`README.md:170/567/575`、`openspec/specs/phase-artifact-verification/spec.md`（2 处） | 允许——术语属产物诊断体系，与本变更无关 |
| `skills/kflow-guide/SKILL.md` 的产物诊断行 | `skills/kflow-guide/SKILL.md:410` | 允许——该行为 `kflow-verify` 的路由描述 |
| 主规格中由 delta 承载的旧口径 | `openspec/specs/devflow-audit/spec.md`（6 处） | 由 delta 在归档时替换，见 3.2 |

`skills/`、`docs/`、`README.md` 三处**无一行审计域残留**；`kflow-audit/SKILL.md`、`docs/designs/skills/kflow-audit.md`、审计报告模板与示例均已零命中。

### 3.2 主规格残留的收口方式（沿用本仓库既有做法）

apply 阶段主规格仍持 delta 应用前的旧口径——这是 OpenSpec 的既定模型（delta 为权威，归档时改写主规格）；
先例见 `openspec/changes/archive/2026-09-29-sync-legacy-prototype-specs/tasks.md` 任务 6.2，其做法为
「以临时副本模拟 `openspec archive` 后复扫确认」。

本变更按同一做法验证：把 `openspec/` 复制到临时目录，运行
`openspec archive simplify-audit-single-agent --yes`，再对归档后的规格复扫：

| 复扫项 | 结果 |
|--------|------|
| `grep -rn "七维度\|六维度" <副本>/openspec/specs/` | 仅剩 `phase-artifact-verification/spec.md`（2 处，kflow-verify 体系）——**审计域命中数为 0** |
| 归档后 `devflow-audit` 口径 | 需求名 `审计四维度评估`；新增 `审计由单一子代理执行`；`轻量档审计降级为轻量自检` 正文为「由四维度加权评分降为轻量自检……SHALL 由审计子代理执行」；报告需求标注「加权总分 SHALL 仅作变更健康度参考」 |
| 归档后 `subagent-isolation-rule` 口径 | 适用范围含「审计评估与轻量自检」与 `kflow-audit`；场景 `审计阶段的规则适用子集` 含重试上限 3 次与「SHALL NOT 适用轮次级重试粒度」 |
| `openspec validate --specs`（副本） | 129 passed / 0 failed |
| 归档应用统计 | `devflow-audit`: +1 added / ~3 modified / →1 renamed；`subagent-isolation-rule`: ~1 modified |

即：任务 6.1 的验收判据在 apply 阶段拥有的编辑面上 100% 达成；主规格中剩余的审计旧口径全部为 delta 契约内容，
在归档应用 delta 时由工具消除，apply 阶段预改会与 delta 重复。

### 3.3 旧执行者模型的残留

`grep -rn "主 Agent 轻量自检\|4 个 Agent\|七维度并行\|并行 Agent 评估" skills/ docs/ README.md openspec/specs/` 的命中：

- `docs/designs/templates/changes/{change}/review-reports/review-synthesis.md:41` 的 `4 个 Agent`——该处描述**代码审查**的四视角并行（完整档），与审计执行者无关，属宽正则假阳性，按变更范围不动。
- `openspec/specs/devflow-audit/spec.md:11` 的 `主 Agent 轻量自检`——delta 承载的旧口径，同 3.2。

## 4. 校验闭环（对应任务 6.3）

| 命令 | 结果 |
|------|------|
| `python scripts/validate-frontmatter.py` | 通过 40 / 失败 0，状态「✓ 所有 front matter 与设计规格 yaml 代码块合法」，无 ERROR |
| `openspec validate simplify-audit-single-agent` | `Change 'simplify-audit-single-agent' is valid` |
| `openspec validate simplify-audit-single-agent --strict` | `Change 'simplify-audit-single-agent' is valid` |

## 5. 实施阶段的裁决记录

以下三处不在任务清单的字面范围内，为避免口径丢失或自相矛盾而作的裁决：

1. **`skills/kflow-audit/SKILL.md` 四维度表的「合并来源」列不写旧权重百分比**。任务 1.1 的验收判据要求
   `grep -n "22%\|23%\|Post-mortem5%" skills/kflow-audit/SKILL.md` 无命中，而该列与 `design.md` D1 表内容重复。
   仅保留合并来源的维度名，权重的完整溯源留在 `design.md` D1（及其镜像说明）。
2. **审计报告格式新增「维度证据」前置小节**。delta 的 `证据先于评分` 场景要求「先采集、逐维度呈现证据、再统一评分」，
   设计 D3 明确该约束的验收方式为「报告是否按『证据分节 → 评分表』组织」。为使报告结构可承载该判据，
   `SKILL.md` 报告格式与审计报告模板的形态 B 均补入证据表（列：维度 / 证据来源 / 事实采集结果），评分表列于其后。
   模板的 `version` 由 1.0.0 递增为 1.1.0 并新增修订记录区，满足 `stage-doc-templates` 的 `产物格式变更时更新模板` 场景。
3. **回退路由清单补入 `kflow-api-test`**。镜像 `docs/designs/skills/kflow-audit.md` 时发现：`HEAD` 版设计文档的
   「与其他 Skill 的关系 → 回退路由」列出 `kflow-explore / kflow-design / kflow-code / kflow-api-test / kflow-e2e-test`，
   而 `skills/kflow-audit/SKILL.md` 同一行缺 `kflow-api-test`——该分歧先于本变更存在。
   裁决：两份文件均补该 skill（不在镜像中缩小既有清单，同时使两份文件一致）。
   `kflow-integration-test` 两边原本均未列，属另一处既存缺口，不在本变更范围内，未处理。
4. **`docs/designs/core-mechanisms/04-gates-and-transitions.md` 与 `docs/designs/overview.md` 的流程节点名保留
   `审计(轻量自检，门控)`** 未改为含「单子代理 + 四维度」的长名：该节点位于「轻量档阶段流转」专属流程图内，
   节点名对轻量档是精确的，且「四维度」不适用于轻量档；ASCII 图的对齐对字符显示宽度敏感，
   加长节点名会破坏箭头对齐。新口径由紧随其后的档位分支说明段（该段已改写）与两文件的档位表、Skill 表承载。
   「单子代理」这一信息已在 `docs/designs/index.md` 的档位表「审计形态」列展开。

