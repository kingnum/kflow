# Proposal

## Why

`变更档位` 在三次简化后语义已收窄为「只决定审查形态与产出深度，不决定轮数」：0.23.0 `converge-review-termination` 删除了轮数上限，0.24.0 `streamline-design-flow` 把设计类审查单轮化、把审计降为全档位同一形态的记账员、并删除了「产品需求 → 完整档」硬映射。轮次维度拆除后，三档里 `标准` 与 `完整` 的全部行为差异只剩两处——设计交叉审查的并行度（两视角 vs 四视角）与完整档专属的自审评分报告深度（评分不参与终止判定）。以两处残差维持一个贯穿全流程的并列取值，成本与收益已经倒挂：

- 枚举、两段式判定、门控分支、子代理 prompt 透传、状态文件字段、hooks 开关、repetition 规则表都带一条并行的第三分支，`skills/` 下共 **64 个文件、756 处**引用 `档位`，其中 49 个文件写着 `完整档` / `完整模式`。
- 并列分支已经产生实际不一致：10 份 `skills/kflow-*/references/state-values.md` 的第 69 行仍保留 0.24.0 已删除的「或变更类型为 `产品需求`」硬映射；`design-review-tiering` 仍保留「审计按档位给分」的要求，与 `devflow-audit` 已确立的「四项记账职责、SHALL NOT 输出评分表」直接矛盾。

同时，轻量档承载的**阶段裁剪链**（阶段适用性声明、测试三阶段条件适用、覆盖率分母口径、归档裁剪依据、跳过子变更划分）是必须保留的真实价值，它需要一个前置分级信号作为载体——因此不取消档位概念，只把三档收敛为二档。

## What Changes

### 一、档位枚举三档收敛为二档 **BREAKING**

- `变更档位` 取值由 `{轻量, 标准, 完整}` 收敛为 `{轻量, 标准}`；`完整` 取值废除
- 阈值映射由 `≤3 轻量 / 4~15 标准 / >15 完整` 改为 `≤3 轻量 / >3 标准`，影响范围分数公式（`功能点数 × 1 + 接口数 × 1.5 + 数据模型变更数 × 2`）与两段式判定时机（explore 初判 / design 复核）保持不变
- **缺省回退值变更**：字段缺失或取值非法时由「按 `完整` 档处理」改为「按 `标准` 档处理」；历史变更遗留的 `完整` 取值在读取侧一律归并为 `标准`（归并规则与 0.24.0 确立的 `收敛` → `验证通过` 同形）
- 单向升档安全阀保留，语义收窄为「轻量 → 标准」，仍仅升不降、不回退 explore

### 二、设计交叉审查形态二档化 **BREAKING**

- 设计交叉审查形态收敛为：`轻量` = 单 Agent 串行综合（覆盖业务/技术/安全/质量四视角全部检查项）；`标准` = 两视角并行（业务+技术 / 安全+质量）
- **四视角并行模式废除**：`完整` 档消失后不再存在四份独立视角报告的产出路径
- **检查项覆盖不缩减**：轻量单 Agent 与标准两视角 SHALL 覆盖原四视角的全部检查项——被移除的是并行度，不是审查内容；此约束与 0.24.0 已确立的「检查项不得缩减，仅并行度与产物形态随档位变化」一致
- 进入计划门控由三分支（四份视角报告 / 两份视角报告 / 单一综合报告）简化为两分支（两份视角报告与 synthesis.md / 单一 synthesis.md）
- 代码审查形态维持现状（`轻量` 单 Agent / `标准` 两视角），仅取值表述更新

### 三、删除完整档专属的评分报告深度

- 删除「`完整` 档下自审、代码审查与测试类阶段的执行报告 SHALL 输出各维度 0–10 评分与不达标项清单」的产出深度要求；该要求原本即不参与终止判定，档位无规模信号后若保留将变为对全部变更的无条件评分要求，与审计去除评分的既定方向相悖

### 四、同路径既有不一致的清理

- 修正 10 份 `skills/kflow-*/references/state-values.md` 中「`完整` = 影响范围分数 > 15，或变更类型为 `产品需求`」的残句（0.24.0 已删除该硬映射）
- 删除 `design-review-tiering` 的「审计审查维度适配审查模式」要求（审计已无评分维度，该要求的前提不存在）
- 修正 `integration-testing` 中「集成测试阶段 SHALL 按轻量档轮次（1 轮）执行」的残句（轮次已不由档位决定）

## Capabilities

### New Capabilities

无新增能力。

### Modified Capabilities

- `change-tier-classification`: 枚举收敛为 `{轻量, 标准}`；阈值改为 `≤3 / >3`；缺省回退值由 `完整` 改为 `标准`，新增历史 `完整` 取值归并规则
- `design-review-tiering`: 审查模式由三模式（简化 / 两视角 / 完整四视角）收敛为两模式；进入计划门控由三分支改为两分支；删除「审计审查维度适配审查模式」要求
- `convergence-driven-repetition`: 审查形态枚举由三档表述收敛为两档（轻量单 Agent / 标准两视角并行）；缺省回退值同步
- `code-review-skill`: 档位适用范围表述由「`标准` 或 `完整`」改为「`标准`」；门控与闭环验证的档位分支同步
- `review-closed-loop`: 审查关闭条件、交叉审查批次目录的视角报告数表述按两档收敛（标准档两份视角报告 / 轻量档仅 synthesis.md）
- `lightweight-flow-trimming`: 「`标准` 与 `完整` 档 SHALL NOT 应用裁剪」表述收敛为「`标准` 档 SHALL NOT 应用裁剪」；升档目标值不变
- `subchange-type-validation`: 非轻量档枚举表述由「`标准` 或 `完整`」改为「`标准`」
- `subchange-phase-unification`: 前后端项目全阶段执行的档位枚举表述同步
- `integration-testing`: 轻量档条件适用表述保留；删除「按轻量档轮次（1 轮）执行」的档位化轮次表述
- `devflow-audit`: 「无论档位为 `轻量`、`标准` 或 `完整`」等枚举表述收敛为两档
- `devflow-guide`: 流程概览的档位分支表述由「`标准` 档与 `完整` 档」收敛为「`标准` 档」

## Impact

### 规范文档（`docs/designs/`）

- `core-mechanisms/03-status-and-tasks.md`（§3.1.1 档位判定：枚举、阈值、缺省回退）
- `core-mechanisms/04-gates-and-transitions.md`（6 处档位分支）、`05-execution-services.md`、`07-agent-model.md`
- `skills/kflow-{explore,design,plan,code,code-review,prototype-design,guide,archive,bug-fix}.md`（含 `kflow-design.md` 14 处、`kflow-code-review.md` 11 处）
- `templates/index.md`、`templates/changes/{change}/review-reports/*.md`（5 份视角报告模板）、`templates/subchanges/{subchange}/code-review.md`
- `examples/audit-report.md`、`index.md`、`overview.md`

### 可运行 Skills（`skills/`）

- 10 份 `references/state-values.md`（枚举行、阈值行、行为差异表）
- 10 份 `references/gates.md`（进入计划门控与代码审查门控的三档分支表）
- 13 份 `references/hooks.md`（档位开关表述）
- 8 份 `references/repetition.md`（审查形态表、完整档评分深度章节）
- 3 份 `references/self-review.md`、`kflow-design/references/review-content.md`
- 16 份 `SKILL.md`（档位判定步骤、审查形态说明）
- `kflow-archive/references/archive-rules.md`、`kflow-init` 注入模板中的档位说明

### 用户文档

- `README.md`（档位章节 13 处、Skills 清单档位列、版本更新说明）

### 兼容性

- **BREAKING**：历史变更 `.status.md` 的 `变更档位 = 完整` 需按读取侧归并规则读作 `标准`；不再存在四视角审查产物路径，历史 `cross-reviews/` 下的四份视角报告不做迁移，读取侧不再要求其存在
- **BREAKING**：字段缺失或取值非法时按 `标准` 档处理（原为 `完整`）——该变更使缺省回退不再等价于「历史行为」，但两档均已无轮次差异，回退值只影响审查并行度

### 不在本次范围

- 阶段裁剪机制的判据不变更（仍以轻量档为前置条件，不改为无条件按客观信号生成声明）
- 编码 / 代码审查 / 缺陷修复三阶段的重复制循环模型不变
- 缺陷修复快车道不读取档位的既有约束不变
