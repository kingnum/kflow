# Design

## Context

- `kflow-design` 的 REVIEW 步骤当前无条件执行四视角并行审查（业务/技术/安全/质量 4 个 Agent）+ review-closed-loop 分级重审闭环，是变更级最重的审查环节。
- 变更类型 `{产品需求|功能需求|功能缺陷}` 已记录在 `.status.md` 基本信息中，且 `design-level-restructure` 已确立「功能缺陷级走简化流程」的先例。
- 归档目录当前为 `docs/archive/`，但 `kflow-status` 的 SCAN/FILTER 流程文档已写成「扫描 docs/changes/ → 排除 archive/ 子目录」，与实际 Glob 路径 `docs/archive/` 存在错位。
- 动机见 proposal.md - Why。

## Goals / Non-Goals

**Goals:**
- 让功能缺陷级小变更的设计审查降本提速，同时不牺牲功能需求/产品需求级变更的审查深度。
- 统一归档目录到 `docs/changes/archive/`，消除 status/resume 检测路径的文档-实现错位。

**Non-Goals:**
- 不引入「跳过审查」——设计审查始终强制，仅深度分级。
- 不改动 `kflow-code-review`（代码审查）与 `kflow-audit`（审计）的强制性与执行流程。
- 不改动 `kflow-design` 的 SELFREV（10 轮自循环审查）——那是设计质量底线，不属于「审查分级」范围。

## Decisions

### D1: 判定依据用「变更类型」而非 FP 复杂度 / FP 数量

- **选择**：功能缺陷级 → 简化模式；功能需求级/产品需求级 → 完整模式。
- **理由**：变更类型已在 `.status.md` 记录，判定零成本；与 `design-level-restructure`「功能缺陷级走简化流程」语义一致，不引入新的评估链路。
- **备选**：FP 复杂度（无高复杂度 FP → 简化）更精确但依赖 `design-complexity-gate` 的评估结果，且与「变更整体规模」不完全等价；FP 数量（≤20 → 简化）已存在阈值但「小变更」未必 FP 少。

### D2: 简化模式 = 单视角综合审查（单 Agent 串行）

- **选择**：单个 Agent 串行过完业务/技术/安全/质量四视角的全部检查项。
- **理由**：速度最快，且不丢失检查项覆盖面（四视角的检查清单完整保留，只是合并为一个 Agent 顺序执行）。
- **备选**：4 视角合并为 2 视角并行（对齐 code-review 先例）——仍需 2 个 Agent，提速有限；4 视角保留但精简检查项——仍 4 个 Agent，调度成本不降；4 视角 + 简化闭环——并行成本不变，收益最小。

### D3: 简化模式产物 = `cross-reviews/{timestamp}/synthesis.md`（单文件）

- **选择**：简化模式只输出单一 `synthesis.md`，复用「综合报告」语义。
- **理由**：单视角综合审查的本质就是「综合报告」；门控与 audit 已有 synthesis.md 检查，无需新增产物名。
- **备选**：新建 `quick-review.md` 文件名——需额外在门控/audit 增加分支，徒增复杂度。

### D4: 简化模式不执行分级重审闭环，高严重度问题仍复检

- **选择**：简化模式单轮出报告；若发现高严重度问题，修复后仍走单视角单轮复检（不进入 review-closed-loop 的按严重度多批次验证）。
- **理由**：闭环是完整模式的最大成本之一；但高严重度问题不可放过，故保留单轮复检兜底。

### D5: 归档目录统一到 `docs/changes/archive/`，不保留 `docs/archive/` 兜底

- **选择**：归档目标与检测路径全部切到 `docs/changes/archive/{YYYY-MM-DD}-{change}/`，一次性移动，不保留旧路径兜底检测。
- **理由**：KFlow 是 skill 框架，目录结构由 skill 定义、随 skill 版本演进，无跨版本运行的历史包袱；保留兜底会在 status/resume 里长期残留双路径判断。
- **备选**：resume/status 同时检测 `docs/archive/` 与 `docs/changes/archive/`——过渡期更稳，但引入长期双路径复杂度。

### D6: 门控与审计按模式分支

- **选择**：「进入计划」门控与 kflow-audit「审查 20%」维度读取变更类型，分别接受完整模式（4 视角报告 + synthesis）或简化模式（单 synthesis）产物。
- **理由**：复用 `.status.md` 已记录的变更类型作为分支键，不新增判定。

## Risks / Trade-offs

- [简化模式单 Agent 可能漏掉多视角互补发现的交叉问题] → 缓解：单 Agent 仍覆盖四视角全部检查项清单；功能缺陷级变更影响面小；kflow-audit 七维度仍兜底审计。
- [归档路径全局替换遗漏一处 → 归档检测/移动失效] → 缓解：tasks 按文件清单逐项替换；完成后用 `grep -rn "docs/archive"` 全量扫描确认零残留。
- [审计「审查 20%」维度在简化模式下评分语义变化] → 缓解：D6 明确按模式分支给分，简化模式不缺项不误扣；spec 已固化该行为。

## Migration Plan

1. 更新 skill 定义：设计文档（`02-directory-structure.md`、`08-governance.md`、`04-gates-and-transitions.md`）与各 skill 的 SKILL.md/references 同步。
2. 已在使用 KFlow 的项目升级后：将现有 `docs/archive/` 整体移动为 `docs/changes/archive/`，并同步更新 `docs/changes/index.md` 归档列表路径。
3. 回滚策略：本变更为 skill 定义层面的纯文档/规则改动，无运行时状态；回滚即还原对应 skill 版本并移回 `docs/archive/`。
