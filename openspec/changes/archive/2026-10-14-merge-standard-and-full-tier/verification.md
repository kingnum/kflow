# 集成验证记录

> 本文件承载 `tasks.md` 第 6 组（集成验证与一致性收口）的检索记录与走查证据。范围说明：本文件是变更的验证证据，不属于归档、版本自增、打包等元工作流范畴。

## 1. 一致性收口检索（任务 6.1）

**检索口径**：在 `skills/`、`docs/designs/`、`README.md` 三个范围内检索 `完整档`、`完整模式`、`或变更类型为`、`轻量档轮次` 四个字符串；`openspec/changes/archive/` 与历史变更记录文件不在范围内。

```
$ grep -rn "完整档\|完整模式\|或变更类型为\|轻量档轮次" skills/ docs/designs/ README.md
（无输出）

$ grep -rn '完整档\|完整模式\|或变更类型为\|轻量档轮次' skills/ docs/designs/ README.md | wc -l
0
```

**结论**：四个字符串零命中，收口判据成立。

> `README.md` 的 `### v0.27.0` 版本更新条目在描述本次收敛时以反引号包裹历史取值（`完整`），不含无包裹的 `完整档` 字符串。

## 2. 档位读取点核对（任务 6.2）

`变更档位` 的全部读取位置及其在本次变更后的口径：

| # | 读取点 | 文件 | 枚举校验 | 缺省回退 | 历史 `完整` 归并 |
|---|--------|------|---------|---------|----------------|
| 1 | 字段定义 | 10 份 `skills/kflow-*/references/state-values.md` §4 | `{轻量, 标准}` | `标准` 档 | 有（显式条目：归并为 `标准` 后判读） |
| 2 | 阶段入口门控 | 10 份 `skills/kflow-*/references/gates.md` §1.1 | `{轻量, 标准}` | `标准` 档 | 有（显式条目「历史取值归并」） |
| 3 | 进入计划门控（Gate 2） | 10 份 `gates.md` §门控检查表第 2 项 | 按 `{轻量, 标准}` 两分支 | `标准` 档分支 | 有（标准档分支注明「历史 `完整` 取值按本分支判读」且不要求四份视角报告） |
| 4 | 代码审查门控 | 10 份 `gates.md` §4 | 两档行（轻量 / 标准） | `标准` 档 | 有（§4 说明行注明缺失或历史 `完整` 取值按 `标准` 档处理） |
| 5 | 设计审查形态 | `skills/kflow-design/SKILL.md` §11、`references/review-content.md` | 两档表 | `标准` 档 | 有 |
| 6 | 自审形态 | `skills/kflow-{explore,design,prototype-design}/references/self-review.md` §7 与各 `SKILL.md` 自审步骤 | 两档表 | `标准` 档 | 有 |
| 7 | 子代理 prompt 透传 | 8 份 `skills/kflow-*/references/repetition.md` §14 档位语义 | 两档枚举 | `标准` 档 | 有 |
| 8 | 审计档位判读 | `skills/kflow-audit/SKILL.md`（全档位同一形态，不因档位改变职责集合） | `{轻量, 标准}` | 不适用（形态与档位无关） | 有（审计形态不因历史取值变化） |
| 9 | 流程概览 | `skills/kflow-guide/SKILL.md` 步骤 7 | 两档表 | 历史 `完整` 或字段缺失时按 `标准` 档展示 | 有 |
| 10 | 阶段适用性声明前提 | `state-values.md` §5、各 `gates.md` §1.2 | 仅 `轻量` 档生成 | 声明区缺失按全阶段适用 | 不适用（与档位取值无关） |
| 11 | 归档裁剪判定 | `skills/kflow-archive/references/archive-rules.md`、`gates.md` 归档门控 | 仅 `轻量` 档 | 无 | 有（归档条件按 `标准` 档判读） |

**核对结论**：11 类读取点全部按 `{轻量, 标准}` 二值校验；字段定义、门控校验、自审、重复制、流程概览、归档六类读取点均含历史 `完整` 取值的归并规则；不存在按 `完整` 档分支的残留（检索 `按完整档处理`、`展示完整（缺省）`、`档位 = 标准/完整` 均零命中）。

## 3. 端到端流程走查（任务 6.3）

### 3.1 样例 A：`标准` 档功能需求

**样例构造**：变更类型 `功能需求`，功能点数 8，接口数 3，数据模型变更数 2，前后端项目。

**档位判定**：explore 初判按「功能需求 FP > 2 → `标准`」得 `标准`；design 复核按完整公式 `8×1 + 3×1.5 + 2×2 = 16.5 > 3` → `标准`（维持，不升档）。

| # | 阶段 | 本次变更后的判据 | 对应规范 |
|---|------|----------------|---------|
| 1 | 设计探索 | TIER 初判 `标准`（FP > 2）；SELFREV 单轮验证，不输出各维度评分 | `skills/kflow-explore/SKILL.md` 步骤 8a / 步骤 11 |
| 2 | 详细设计 | DIVIDE 后 TIER_RECHECK 复核为 `标准`，维持；**不生成阶段适用性声明**；设计审查走**两视角并行**，产出 `business-technical-review.md` + `security-quality-review.md` + `synthesis.md`；修复后走**分级重审闭环**（高 → 原视角+安全视角交叉检查；中 → 原视角重审；低 → 随机 30% 抽查），新批次目录追加至 synthesis.md 的「审查批次索引」 | `review-content.md`、`gates.md` §4、`review-synthesis.md` 批次表 |
| 3 | 进入计划门控（Gate 2） | `标准` 档分支：`cross-reviews/{timestamp}/` 存在两份视角报告且最新批次 `synthesis.md` 标记审查通过；SHALL NOT 检查四份独立视角报告 | `gates.md` 门控检查表第 2 项 |
| 4 | 计划 | 子变更 `tasks.md` + SELFREV 单轮验证 | `kflow-plan/SKILL.md` |
| 5 | 编码 | 重复制循环，轮次由实际循环决定，终止结果 `执行完成` | `repetition.md` §14 |
| 6 | 代码审查 | 两视角并行（Agent 1 安全+规范 / Agent 2 质量+性能）；门控 = Agent 1 高 = 0 且 Agent 2 高 = 0 且 Agent 2 中 < 3；修复后分级重审闭环 | `kflow-code-review/SKILL.md` 步骤 4/5/7 |
| 7-9 | 接口单元测试 / E2E测试 / 集成测试 | 全部执行（`标准` 档无裁剪），单轮全面执行 + 定向重验 | `integration-testing`、`subchange-phase-unification` |
| 10 | 审计 | 单一子代理执行四项记账职责，报告为记账记录形态（无评分表） | `devflow-audit` |
| 11 | 归档 | 全部阶段 ✅；无裁剪阶段 | `archive-rules.md` |

**走查结论**：样例 A 的阶段流转、审查形态（两视角）、门控判据（两分支中的标准分支）、产物清单（两份视角报告 + synthesis.md）均可对应到本次变更后的规范；分级重审闭环的触发档位为 `标准`，与 `review-closed-loop` 与 `review-synthesis.md` 一致。

### 3.2 样例 B：`轻量` 档功能缺陷

**样例构造**：变更类型 `功能缺陷`，功能点数 2，接口数 0，数据模型变更数 0，纯后端项目。

**档位判定**：explore 初判按「功能缺陷 FP ≤ 3 → `轻量`」得 `轻量`；design 复核 `2×1 = 2 ≤ 3` → `轻量`（维持）。

| # | 阶段 | 本次变更后的判据 | 对应规范 |
|---|------|----------------|---------|
| 1 | 设计探索 | TIER 初判 `轻量`；阶段集合提示为「计划→编码→代码审查 恒执行；三测试阶段条件适用」；SELFREV 单轮验证 + 产物完整性门控 | `kflow-explore/SKILL.md` 步骤 8d/8e |
| 2 | 详细设计 | DIVIDE 跳过划分表，产出单一子变更；DIVIDE 之后生成**阶段适用性声明**——本样例 `detailed-design.md` 接口设计章节无本变更条目且跨子变更契约章节无条目 → 三测试阶段全部判 `⏭️ 不适用`；设计审查走**简化模式**（单 Agent 串行覆盖四视角全部检查项），仅产出 `cross-reviews/{ts}/synthesis.md`；修复后走单轮复检 | `state-values.md` §5、`review-content.md` 简化模式、`kflow-design/SKILL.md` §13 |
| 3 | 进入计划门控（Gate 2） | `轻量` 档分支：仅检查 `cross-reviews/{timestamp}/synthesis.md` 存在且标记审查通过；SHALL NOT 检查视角报告 | `gates.md` 门控检查表第 2 项 |
| 4 | 计划 → 编码 → 代码审查 | 三阶段恒执行；代码审查为单 Agent 串行覆盖两视角全部检查项，门控 = 高 = 0 且 中 < 3；修复后单轮复检 | `kflow-code-review/SKILL.md` 步骤 4/5/7 |
| 5 | 接口单元测试 / E2E测试 | 均 `⏭️ 不适用`（有声明依据）→ 子变更在代码审查完成后**直接进入变更级同步点**，SHALL NOT 进入 `⏸️ 等待同步` | `03-status-and-tasks.md`、`gates.md` §1.2 |
| 6 | 集成测试 | `⏭️ 不适用`（有声明依据）→ 不启动 `kflow-integration-test`，直接进入审计 | `integration-testing` |
| 7 | 审计 | 单一子代理四项记账职责，**与 `标准` 档同一形态**，不因轻量档走简化路径 | `devflow-audit` |
| 8 | 归档 | 有声明依据的 `⏭️` 视为门控满足；`traceability.md` 对应列整列 `⏭️` 且不计入覆盖率分母；不因产物缺失判缺项 | `archive-rules.md`、`gates.md` 归档门控 |

**走查结论**：样例 B 的裁剪链（阶段适用性声明 → 三测试阶段条件适用 → 归档裁剪判定）完整可用；审查形态为单 Agent 综合（仅 `synthesis.md`）；门控判据为两分支中的轻量分支；产物清单与本次变更后的规范一致。

### 3.3 两样例对照

| 维度 | 样例 A（`标准`） | 样例 B（`轻量`） |
|------|-----------------|-----------------|
| 设计审查形态 | 两视角并行 → 两份视角报告 + synthesis.md | 单 Agent 综合 → 仅 synthesis.md |
| 设计审查修复后 | 分级重审闭环（多批次） | 单轮复检 |
| 代码审查形态 | 两视角并行 | 单 Agent 串行覆盖两视角全部检查项 |
| 阶段适用性声明 | 不生成 | 生成，三测试阶段条件适用 |
| 子变更划分 | 按依赖关系划分 | 跳过，单一子变更 |
| Gate 2 判据 | 两份视角报告 + synthesis.md | 仅 synthesis.md |
| 审计形态 | 同一形态（四项记账职责） | 同一形态（四项记账职责） |

**结论**：两个样例的审查形态、门控判据与产物清单互不重叠、各自自洽，且均可对应到本次变更后的规范，无引用已废除机制的判据。

## 4. 历史兼容走查（任务 6.4）

**构造样例**：一份历史变更 `.status.md`，其基本信息含 `- **变更档位**: 完整`，且 `cross-reviews/` 下留有历史四份独立视角报告（`business-review.md`、`technical-review.md`、`security-review.md`、`quality-review.md`）与 `synthesis.md`。

```
docs/changes/legacy-change/.status.md
  - **变更档位**: 完整          ← 三档枚举时代的取值，未迁移
docs/changes/legacy-change/cross-reviews/2026xxxx-xxxxxx/
  business-review.md  technical-review.md  security-review.md  quality-review.md  synthesis.md
```

| # | 核对点 | 本次变更后的判读 | 对应规范 |
|---|--------|----------------|---------|
| 1 | 设计审查门控（Gate 2） | 读取侧将 `完整` 归并为 `标准` → 走**标准档分支**：检查两份视角报告与 `synthesis.md` 是否存在且最新批次标记通过。历史四份独立视角报告**不被要求存在**，其存在亦**不导致门控阻塞**（无「产物超出档位要求」的一致性判定） | `gates.md` §1.1 历史取值归并条目 + 门控检查表第 2 项标准档分支；`opsx` delta `design-review-tiering` 的 Migration 段 |
| 2 | 审计报告形态 | 审计不因档位改变执行方式与职责集合；该变更按**统一记账记录形态**输出（四项记账职责结论 + 耗时效率摘要 + 分级问题清单 + 改进建议），SHALL NOT 因历史 `完整` 取值要求四视角审查产物，SHALL NOT 输出评分表 | `skills/kflow-audit/SKILL.md`、`devflow-audit` delta |
| 3 | 流程概览 | `kflow-guide` 步骤 7 的档位分支按 `标准` 判读：按项目类型显示完整阶段集合，SHALL NOT 标注档位裁剪；`变更档位` 展示为 `标准`（归并），不展示第三档专属标注 | `skills/kflow-guide/SKILL.md` 步骤 7 |
| 4 | 状态字段读取 | `state-values.md` §4 的历史取值归并条目生效：归并为 `标准` 后判读；SHALL NOT 要求用户手工修改历史状态文件 | `state-values.md` §4 |
| 5 | 重复制阶段的档位语义 | 子代理 prompt 透传的档位按 `标准` 判读 → 审查形态为两视角并行，轮次不受档位影响 | `repetition.md` §14 档位语义 |
| 6 | 归档门控 | 按 `标准` 档的归档条件判读；无裁剪阶段，`traceability.md` 全部列要求 100% | `archive-rules.md` |

**走查结论**：含 `变更档位 = 完整` 的历史变更在**设计审查门控**（按标准档两视角路径通过）、**审计报告形态**（统一记账记录形态通过）、**流程概览**（按标准档展示、不标注第三档专属标注）三处均按 `标准` 档路径通过，且不因历史 `cross-reviews/` 下四份视角报告的存在或缺失而阻塞；无需用户手工迁移状态文件。

## 5. 校验脚本与规格校验（任务 6.5、6.6）

```
$ bash scripts/sync-references.sh
=== References 一致性校验 ===
  repetition.md / hooks.md / gates.md / state-values.md / service-lifecycle.md
  self-review.md / phase-transition.md
=== 结果 ===
检查项: 7
状态: ✓ 所有多 skill 共享的 references 文件一致

$ python scripts/validate-frontmatter.py
=== 结果 ===
通过: 40, 失败: 0
状态: ✓ 所有 front matter 与设计规格 yaml 代码块合法
```

两条命令均以退出码 0 结束、无告警。`openspec validate merge-standard-and-full-tier --strict` 的结果见任务 6.6 执行记录。

## 6. 设计规格 → SKILL.md 同步核对（任务 7.1）

核对口径：本次变更涉及的每个阶段，其设计规格（`docs/designs/skills/kflow-*.md`）与可运行 Skill（`skills/kflow-*/SKILL.md`）中的档位相关检查项须逐项对应，无未同步项。

| 阶段 | 档位相关检查项 | 设计规格 | SKILL.md | 一致 |
|------|--------------|---------|---------|------|
| explore | 初判映射表（功能缺陷 FP≤3/>3；功能需求 FP≤2/>2；产品需求比照功能需求） | `kflow-explore.md` §初判映射规则 | `SKILL.md` 步骤 8a | ✓ |
| explore | 阶段集合提示表（轻量 / 标准 两行） | §阶段集合提示 | 步骤 8d | ✓ |
| explore | 档位对 explore 自身的产出深度影响（两行，无评分行） | §档位影响 | 步骤 8e | ✓ |
| explore | 档位读取与缺省回退 + 历史 `完整` 归并 | §档位影响 | 步骤 11 档位语义 | ✓ |
| design | 设计审查形态表（轻量简化模式 / 标准两视角模式） | §设计审查分级 | 步骤 11 档位表 | ✓ |
| design | Gate 2 产物清单（两份视角报告 + synthesis.md） | §设计审查产物 | 步骤 11 + `references/gates.md`（共享） | ✓ |
| design | 分级重审闭环的档位分支（轻量单轮复检 / 标准分级重审闭环） | §分级重审闭环的档位分支 | 步骤 13 | ✓ |
| design | 阶段适用性声明生成条件（仅 `轻量`）+ 档位隔离 | §阶段适用性声明 | 步骤 9.6 | ✓ |
| design | 变更档位复核阈值（≤3 轻量 / >3 标准）与单向升档 | §TIER_RECHECK | 步骤 9.5 | ✓ |
| design | 缺省回退 + 历史 `完整` 归并（DIVIDE / 9.5 / 9.6 / 10 / 11 五处读取点） | 各节 | 步骤 9 / 9.5 / 9.6 / 10 / 11 | ✓ |
| prototype-design | 自审档位表（两行，评分底线行已删） | §SELFREV 档位表 | 步骤 10 | ✓ |
| prototype-design | 档位读取与缺省回退 + 历史归并 | §SELFREV | 步骤 10 档位语义 + 强制执行规则 | ✓ |
| plan | 档位语义（只决定形态与产出深度、不决定轮数） | §档位语义 | 步骤 8.5 | ✓ |
| plan | Gate 2 设计审查产物按两分支判读 + 历史 `完整` 归并 | §门控检查 | 门控检查表 | ✓ |
| plan | 自审评分底线行已删 | §强制执行规则 | 强制执行规则 | ✓ |
| code | 档位读取与历史归并 | §重复制类阶段 | 档位读取 | ✓ |
| code | 阶段适用性声明仅轻量档；`标准` 档及声明区缺失按全部适用 | §阶段适用性声明 | 输入产物表 | ✓ |
| code-review | 审查形态表（两档行） | §审查形态 | 步骤 4 档位表 | ✓ |
| code-review | 门控表（轻量 / 标准两行） | §门控规则 | 步骤 5 门控表 | ✓ |
| code-review | 闭环验证分支（轻量单轮复检 / 标准分级重审闭环） | §修复后验证 | 步骤 7 | ✓ |
| code-review | 档位读取与历史归并 | §重复制类阶段 | 1.5 INIT | ✓ |
| api-test | 适用范围（仅 `轻量`；`标准` 档 SHALL NOT 应用） | §适用范围 | 适用范围声明 | ✓ |
| api-test | 档位来源与历史归并 | §档位语义 | 档位来源 | ✓ |
| e2e-test | 适用范围 + 档位来源 + 历史归并 | §适用范围 / §档位语义 | 同名两处 | ✓ |
| integration-test | 适用范围 + 档位来源 + 历史归并 + 阶段裁剪 | §适用范围 / §档位语义 / §阶段裁剪 | 同名三处 | ✓ |
| audit | 全档位同一形态（枚举两值） | §适用范围 | §全档位同一形态 / 强制执行规则 | ✓ |
| archive | 裁剪适用范围（仅 `轻量`）+ 归档条件按 `标准` 档判读 | §档位适配 | 裁剪处理 | ✓ |
| guide | 流程概览档位分支表（两行）+ 归属枚举 + 缺省/归并展示 | §GUIDE | 步骤 7 | ✓ |
| resume | 衔接决策表不含档位分支（档位仅由调度目标的 SKILL 读取） | — | 仅引用共享 `references/phase-transition.md` | ✓（无档位分支，无需同步） |
| status | 未归档变更汇总不展示档位取值 | — | — | ✓（无档位分支，无需同步） |
| verify | 裁剪判定仅适用于 `轻量` 档 | §产物诊断 | 裁剪判定条目 | ✓ |

**核对结论**：12 个含档位分支的阶段中，档位相关检查项在设计规格与可运行 Skill 间逐项对应，无未同步项；`resume` / `status` 两个阶段不含档位分支（档位由被调度的阶段 Skill 自行读取），无需同步。全阶段检索 `完整档`、`完整模式`、`四视角并行`、`{轻量|标准|完整}` 均零命中。

## 7. 自包含性与版本一致性核对（任务 7.2、7.3）

**自包含性（任务 7.2）**：`scripts/sync-references.sh` 校验 7 类多 skill 共享的 `references/` 文件（`repetition.md` 8 份、`hooks.md` 13 份、`gates.md` 10 份、`state-values.md` 10 份、`service-lifecycle.md` 4 份、`self-review.md` 3 份、`phase-transition.md` 11 份）在全部持有 skill 间内容一致，结果「✓ 所有多 skill 共享的 references 文件一致」，无跨 skill 引用告警。各 skill 的辅助规则（钩子 / 门控 / 重复制规范 / 状态字段定义）均位于自身 `references/` 子目录，安装后零外部依赖。

**版本一致性（任务 7.3）**：仓库根 `VERSION` = `0.26.0`；18 个 `skills/kflow-*/SKILL.md` 的 `version` 字段逐文件比对结果全部为 `0.26.0`，无失配项（版本自增由归档后规则驱动，不在本次交付范围内）。
