# Design

## Context

- 设计三阶段（explore/prototype/design）的 SELFREV 当前无条件固定 10 轮、不可提前终止，见 `subagent-self-review` spec 与各 skill 的 `references/self-review.md`。
- 上一轮 `design-review-tiering` 已对四视角 REVIEW 按变更类型分级，但刻意将 SELFREV 排除在外（见其归档 design.md：「SELFREV 是设计质量底线」）。
- `kflow-init` 已有「产品文档 8 项检测」及 LEGACY 触发条件（`docs/CONTEXT.md` 不存在 或 `docs/designs/functional-designs/` 为空 → 无设计基础），本变更复用并收紧该信号。
- 动机见 proposal.md - Why。

## Goals / Non-Goals

**Goals:**
- 让非首次创建（已有设计基础）的增量变更在设计三阶段自审降本提速，同时保留首次创建的 10 轮打地基。
- 用「评分底线 > 8」守住质量，确保轮次少 ≠ 评分松。

**Non-Goals:**
- 不引入「跳过自审」——自审始终强制，仅深度分级。
- 不改动四视角 REVIEW 分级（design-review-tiering 现有 REVIEW 需求保持不变）。
- 不改动 kflow-plan 的 SELFREV（plan 属执行类阶段，维持 10 轮）。
- 不改动执行类阶段的弹性重复制公式（repetition-model.md §14）。

## Decisions

### D1: 判定轴用「首次/非首次创建」而非「变更类型」

- **选择**：首次/非首次 = 项目是否已有设计基础。
- **理由**：SELFREV 的成本随「有多少全新设计需要收敛」缩放，而非随变更风险缩放；产品需求级≈首次、功能需求/缺陷级≈非首次，但两者解耦以覆盖「首个变更即功能级」或「产品扩张」等边界。
- **备选**：沿用 REVIEW 的变更类型轴（产品=首次，需求/缺陷=非首次）——与「设计基础」偶合，边界情形会误判。

### D2: 判定信号复用 kflow-init 已有检测

- **选择**：`docs/CONTEXT.md` 存在 且 `docs/designs/detailed-designs/` 非空 → 非首次。
- **理由**：`kflow-init` LEGACY 触发条件已用「CONTEXT.md 不存在 或 functional-designs 为空」判定无设计基础；本变更取「CONTEXT.md + detailed-designs」作为更严格的「详细设计基础已建立」信号，语义更贴合 SELFREV（对齐 detailed-design 的一致性/完备性检查）。
- **备选**：仅 CONTEXT.md 存在——信号过弱，词汇表不代表架构/数据模型已建立。

### D3: 弹性轮次 = 影响范围分数决定目标轮次，下限 1

- **选择**：复用执行类阶段「影响范围分数」公式结构，但按设计阶段映射规模指标（explore=功能点数、prototype=页面数+交互元素数、design=功能点数+接口数+数据模型数）；轮次映射沿用执行阶段档位，仅下限从 3 改为 1。
- **理由**：与执行类阶段弹性重复制语义一致，团队已熟悉该模型；下限 1 让功能缺陷级等微小变更降到最低成本。
- **备选**：固定降 N 轮（3/5）——无弹性；单轮——放弃规模化差异。

### D4: 评分底线 = 各维度 > 8（0–10 量纲），未达标补审

- **选择**：SELFREV 每轮输出维度得分（沿用 §7 审查维度得分表），各维度均 > 8 方通过；未达标补审至 10 轮上限。
- **理由**：轮次下限降到 1 后，靠评分底线兜住质量——「轮次少 ≠ 评分松」。
- **量纲说明**：0–10 整数计分下「> 8」即 9 或 10；spec 保留用户口径「> 8」。
- **备选**：仅轮次弹性无评分底线——trivial 变更 1 轮即过，质量无兜底。

### D5: 门控/审计现状无需改动

- **选择**：不新增门控/审计 spec 需求。调查确认：门控检查的是阶段状态与输入产物（不查自审报告份数），kflow-audit「审查质量」维度评的是四视角 REVIEW 与代码审查（不评自审轮次），故弹性轮次不破坏现有门控/审计。
- **理由**：避免为不存在的检查点凭空造需求。
- **备注**：tasks 保留一条「核对 kflow-audit 产物完整性对弹性自审报告份数的判定」任务。

## Risks / Trade-offs

- [弹性轮次单轮可能漏掉多维度互补发现的问题] → 缓解：评分底线 > 8 兜底；功能缺陷级等小变更影响面小；四视角 REVIEW（完整/简化）仍独立兜底。
- [「首次/非首次」判定信号在边界项目误判] → 缓解：信号复用 kflow-init 既有检测、语义一致；边界情形（legacy 项目有 CONTEXT 无 detailed-designs）按「首次」处理更保守（多跑几轮不损失质量）。
- [评分量纲 0–10 与「> 8」的整数语义歧义] → 缓解：design 明确 0–10 量纲，整数计分下「> 8」即 9/10；spec 写「> 8」保留用户口径。

## Migration Plan

1. 更新 spec 增量（design-review-tiering ADDED、subagent-self-review MODIFIED）。
2. 更新三设计 skill 的 SKILL.md SELFREV 步骤 + `references/self-review.md`（10 轮强制 → N 轮弹性 + 评分底线）。
3. 更新 `07-agent-model.md` §16 自审机制表述、README.md「10 轮自审」描述。
4. 回滚策略：本变更为 skill 定义层纯规则改动，无运行时状态；回滚即还原对应 skill 版本。
