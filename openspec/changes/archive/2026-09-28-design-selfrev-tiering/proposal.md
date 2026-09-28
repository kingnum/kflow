# Proposal

## Why

设计四视角审查（REVIEW）已按变更类型分级（功能缺陷级→简化模式），但设计阶段的 10 轮自审（SELFREV）仍固定 10 轮、不可提前终止。对非首次创建（项目已有设计基础）的增量变更而言，这套固定 10 轮自审成本过高、拖慢交付——上一轮「设计审查分级」变革刻意将 SELFREV 排除在分级之外（视作「设计质量底线」），本次补齐这一缺口：让非首次创建的变更用「弹性轮次 + 评分底线」降本，同时保留首次创建的 10 轮打地基。

## What Changes

- **SELFREV 分级（默认弹性）**：设计三阶段（explore / prototype-design / design）的 10 轮自审改为分级执行——**首次创建**（项目无设计基础）固定 10 轮；**非首次创建**（已有设计基础）走弹性轮次（影响范围分数决定目标轮次，下限 1 轮、上限 10 轮）+ 评分底线（各维度自审评分 > 8 方通过，未达标继续补审至上限 10 轮）。
- **首次/非首次判定信号**：以项目是否已有设计基础为准——`docs/CONTEXT.md` 存在 **且** `docs/designs/detailed-designs/` 非空 → 非首次；否则 → 首次。
- **统一分级能力**：将 SELFREV 分级并入 `design-review-tiering`，使其成为覆盖 REVIEW + SELFREV 的统一「设计审查分级」能力。
- **自审轮次去硬编码**：`subagent-self-review` 中「10 轮顺序执行」改为「N 轮（弹性，由设计审查分级决定）」。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `design-review-tiering`: 扩展为统一「设计审查分级」——新增 SELFREV 分级需求（首次/非首次判定信号、弹性轮次公式、评分底线 > 8、门控/审计适配），保留原 REVIEW 分级需求。
- `subagent-self-review`: 自审轮次由固定「10 轮顺序执行」改为「N 轮（弹性决策）顺序执行」，三设计阶段弹性、plan 阶段维持 10 轮。

## Impact

- **kflow-explore / kflow-prototype-design / kflow-design**：SELFREV 步骤新增「首次/非首次」分支 + 弹性轮次 + 评分底线判定。
- **各 skill 的 `references/self-review.md`**：10 轮强制规则改为 N 轮弹性 + 评分底线规则。
- **kflow-plan**：不受影响（plan 属执行类阶段，SELFREV 维持现状）。
- **kflow-audit**：自审维度评分需按「首次/非首次」模式适配，评分底线 > 8 与审计「审查」维度口径对齐。
- **核心机制文档**：`07-agent-model.md` §16 自审机制表述同步。
- **README.md**：`10 轮自审机制` 描述同步。
- **无 API / 外部依赖变更**。
