# Proposal

## Why

KFlow 的轮次决策存在两个「首次一律最大」的保守下限，且都与变更规模无关：

1. **执行类阶段**（plan/code/code-review/api-test/e2e-test/integration-test/bug-fix）首次执行固定 10 轮；
2. **设计自审**（explore/prototype-design/design）首次创建固定 10 轮。

两者叠加，使一个「修正校验逻辑」级别的单功能缺陷在现有项目上也要消耗约 78 次子代理调度。更严重的是，自审的「首次创建」判定信号是**项目级**的（`docs/CONTEXT.md` 存在且 `docs/designs/detailed-designs/` 非空），因此新项目的第一个小变更比同等工作量的后续变更贵约 30 倍——成本取决于项目历史而非变更本身。

现有体系中唯一的规模分级只覆盖「设计四视角审查」一个点（按变更类型走简化/完整模式），而最大的成本项（阶段轮次）完全没有分级入口，无法承载整体减负。

此外，影响范围分数到轮次的映射表在三个能力中各自定义且数值互不一致（`flexible-repetition-mode`、`triage-impact-assessment`、`design-review-tiering` 自审章节），形成三套并行口径。

## What Changes

**新增「变更档位」一等机制**

- 新增 `变更档位` 字段（`轻量` / `标准` / `完整`），写入变更级 `.status.md` 基本信息。
- 档位由影响范围分数派生：`功能点数 x 1 + 接口数 x 1.5 + 数据模型变更数 x 2`；分数 <= 3 为轻量，4~15 为标准，> 15 为完整；变更类型为产品需求时下限抬升为完整。
- 采用两段式判定：kflow-explore 的 SPLIT 之后用「变更类型 + 功能点数」初判（此时接口数与数据模型数尚不可知，explore 域外内容禁止接口定义与数据模型设计）；kflow-design 的 DIVIDE 之后用完整公式复核。
- 用户在 explore 确认环节可上调或下调档位；design 复核阶段仅允许单向升档（发现实际影响超出预估时经用户确认后升档，不回退 explore），禁止降档。

**废除两个「首次一律最大」的保守下限**

- 执行类阶段目标轮次由档位决定：轻量 1 轮 / 标准 3 轮 / 完整 10 轮。
- 设计自审目标轮次由档位决定：轻量 0 轮（完全不自审）/ 标准 2 轮 / 完整 10 轮（保留各维度评分 > 8 的评分底线）。
- **BREAKING**：`首次执行 10 轮` 与 `首次创建固定 10 轮` 两条规则被废除，替换为档位基线。
- 回退重执行保留弹性逻辑，但改为在档位基线上取 `max(档位基线, 按影响范围分数映射)`，且映射表统一为一份。

**审查分级从「变更类型」改为「档位」驱动**

- **BREAKING**：标准档设计审查由四视角并行降为两视角（业务+技术 / 安全+质量）；完整档保留四视角并行；轻量档沿用单 Agent 综合审查。
- 代码审查：轻量档单 Agent 单轮覆盖两视角检查项且不执行分级重审闭环；标准档两视角 x 3 轮；完整档两视角 x 10 轮。
- 代码审查门控按档位分支：轻量档高严重度 = 0 且中严重度 < 3，且不要求四份独立视角报告。

**轻量档的探索侧精简**

- kflow-explore 产出在轻量档压缩为单页（功能点清单 + 影响分析 + 修复/实现范围），仍写入既有产物路径，不新增或合并产物文件。
- 轻量档不再主动询问是否进入原型设计阶段（跳过 PROTO_GATE 询问）；用户显式要求原型设计时仍可执行。

**统一轮次映射口径**

- `triage-impact-assessment` 的「影响范围分数 → 推荐轮次」表、`flexible-repetition-mode` 的弹性轮次映射表、`design-review-tiering` 的自审轮次映射表，统一为同一份档位表。

## Capabilities

### New Capabilities

- `change-tier-classification`: 定义变更档位的判定公式、两段式判定时机（explore 初判 / design 复核）、`.status.md` 持久化字段、用户覆盖规则与单向升档安全阀。
- `tier-driven-repetition`: 定义档位驱动的轮次决策表（执行类阶段与设计自审）、回退重执行的 `max` 叠加规则、以及废除「首次一律最大」两个下限后的验证门控。

### Modified Capabilities

- `design-review-tiering`: 审查模式由「变更类型」改为「档位」驱动，新增标准档两视角档位；原「设计自审按首次/非首次分级」「首次/非首次判定信号」「非首次弹性轮次」「自审评分底线」四项要求迁出至 `tier-driven-repetition` 与 `change-tier-classification`。
- `flexible-repetition-mode`: 废除「First execution uses full 10 rounds」；目标轮次改为以档位基线为下限并叠加影响范围分数映射。
- `agent-iteration-execution`: 「执行类阶段强制10轮迭代」改为「按档位目标轮次迭代」，第 10 轮不再是固定返回条件。
- `execution-repetition-mode`: per-skill `references/repetition.md` 的轮次规则来源由「标准重复（首次 10 轮）+ 灵活重复（回退）」改为「档位基线 + 回退叠加」。
- `subagent-self-review`: 自审轮次的决定者由 `design-review-tiering` 改为变更档位；kflow-plan 不再固定 10 轮。
- `plan-self-review`: 计划阶段自审由固定 10 轮改为档位驱动（轻量 0 / 标准 2 / 完整 10）。
- `code-review-skill`: 新增轻量档单 Agent 单轮审查形态；两视角并行改为标准档与完整档形态。
- `review-closed-loop`: 轻量档不执行分级重审闭环，改为单轮复检。
- `devflow-audit`: 「审查」维度按档位给分；轻量档 0 轮自审与单 Agent 审查不算缺项、不因产物少而扣分。
- `auto-subchange-traversal`: 重复制提示词中的「必须完成全部 10 轮迭代」改为「必须完成全部目标轮次迭代」。
- `triage-impact-assessment`: 「Impact score to round mapping」的推荐轮次表统一为档位表，不再单独定义数值区间。

## Impact

**规格层**：新增 2 个能力，修改 11 个既有能力。

**实现层**：`skills/` 下 8 份 `references/repetition.md`（每份 455 行，内容需保持一致）、3 份 `references/self-review.md`（每份 277 行，另含 explore 的 `self-review-dimensions.md`）、约 15 份 `SKILL.md`（新增档位开关分支）、约 12 份 `references/gates.md`（代码审查门控与进入计划门控按档位分支）、约 15 份 `references/state-values.md`（透传档位字段）。

**设计文档层**：`docs/designs/core-mechanisms/` 的 `01-project-types.md`、`03-status-and-tasks.md`、`04-gates-and-transitions.md`、`07-agent-model.md`、`08-governance.md`；`docs/designs/skills/` 全部相关 Skill 规格；`docs/designs/templates/changes/{change}/change-status.md`（新增「变更档位」字段）与审查报告相关模板；`README.md`。

**依赖与兼容性**：`变更档位` 为新增字段，历史变更的 `.status.md` 不含该字段——需定义缺省回退（按完整档处理，保持保守）。本变更不裁剪任何阶段，阶段集合维持现状。

**非目标**：轻量档的阶段裁剪（api-test / e2e-test / 集成测试 / 审计的条件跳过）与 `traceability.md` 的 `不适用` 列处理，留待后续变更 `add-lightweight-change-flow`，因其改动门控与覆盖率分母结构，风险高于本轮参数化替换。

**已识别的遗留问题（本变更不处理）**：`shared-repetition-model` 与 `shared-self-review` 两个能力描述的是 `.claude/skills/kflow-shared/` 集中式文件，该目录在 `2026-07-04-skill-self-contained-refactor` 后已不存在，且与 `phase-self-review`、`execution-repetition-mode` 中「不得存在集中文件」的要求直接矛盾。二者为过期残留规格，需单独清理，不在本变更范围内。
