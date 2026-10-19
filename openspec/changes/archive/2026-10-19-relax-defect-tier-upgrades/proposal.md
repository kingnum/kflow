# Proposal

## Why

变更档位本应衡量“设计变更量”，但当前影响范围分数把“受影响接口数”与“修改接口数”混为一谈，且轻量档以单一子变更为前提：任何全栈缺陷都会因 FP 类型混合被强制升为标准档。结果是简单缺陷频繁触发升档，标准档又把三个测试阶段与更重的审查全部拉回流程。

本变更修正档位公式的计量单位，放宽轻量档的子变更数量，并把升档从“机械提示”改为“必要性判定 + 用户可保留轻量”。

## What Changes

- 影响范围分数（设计面分数）的计量单位明确为：接口数 = 新增/修改的接口契约数；数据模型变更数 = schema/migration 数。受影响但未改契约的接口不计入档位分数。
- 受影响项清单（爆炸半径）仍由 triage 产出，仅用于定向验证范围与回退判定，不参与档位计算。
- 轻量档由“单一子变更”放宽为“最多 2 个子变更（后端 1 + 前端 1）”，使用最小划分表；标准档仍拒绝同一子变更内混合 FP。
- 功能点类型混合不再强制升档；按 2 子变更处理。
- 升档分为硬升档（数据迁移、破坏性契约变更、跨变更契约影响；不可拒绝）与软升档（仅审查强度提升；默认保持轻量，可主动升档，拒绝后记录理由且不再重复提示）。
- 升档必要性判定：仅当升档会实际新增下游测试阶段或属于硬升档时才提示；否则维持轻量并记录“未升档理由”。
- 清理三档时代残留：`docs/designs/skills/kflow-design.md` 与 `change-tier-classification` spec 中的 `4~15 / >15 / 完整` 表述。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `change-tier-classification`: 明确分数计量单位（新增/修改契约、schema）；新增硬/软升档分类、升档必要性判定与用户拒绝规则；清理三档残留场景。
- `lightweight-flow-trimming`: 轻量档由单一子变更放宽为最多 2 个子变更（前后端各一）；移除“FP 类型混合强制升档”，改为最小划分表；阶段适用性声明按两子变更口径调整。
- `subchange-type-validation`: 轻量档 FP 类型混合不再升档，改为拆分为后端子变更 + 前端子变更；标准档的混合阻塞规则不变。

## Impact

- 运行时 Skills: `kflow-design`（DIVIDE / TIER_RECHECK）、`kflow-explore`（初判提示）；`kflow-code-review` 与 `kflow-design` 的档位分支说明在表述受影响时同步。
- references: `references-src/state-values.md`、`references-src/gates.md`、`references-src/phase-transition.md`，以及由 `scripts/sync-references.sh` 生成的各 skill 副本。
- 设计文档: `docs/designs/core-mechanisms/03-status-and-tasks.md` §3.1.1、`04-gates-and-transitions.md`、`07-agent-model.md`；`docs/designs/skills/kflow-design.md`、`kflow-explore.md`；`docs/designs/index.md`、`overview.md`。
- OpenSpec: `change-tier-classification` spec 的三档残留场景清理。
- 兼容性: 历史 `完整` 取值仍按 `标准` 读取；已升档的变更不回退降档（单向规则保留）。
