# Proposal

## Why

多轮审查机制（设计自审 SELFREV、prototype VERIFY、执行类重复制）现行的终止判据只看「轮次是否用尽」，不看「是否还有修复未经独立验证」。§4.5 的复核义务被绑定在「本轮零新发现且零修改」上，而上限那一轮恰恰因为**有修改**才成为上限轮——复核义务的触发条件与待复核修复的存在永远错开。

轻量档把这个错开变成了必然：轮次上限为 1，第 1 轮只要发现并修复任何一个问题，该轮就不是见证轮，系统立即判定 `达上限` 并滑入非收敛分支（记录 `skill-suggestion.md` + `AskUserQuestion` + 可标记 ⚠️ 阻塞）。结果是两重失真——修复质量零保障（无人复验），且「轻量档正常地发现并修复了 1 个问题」被记为「非收敛」这种异常态。

同一缺口在标准档第 2 轮、完整档第 5 轮同样存在（上限轮恰好含修复时）。交叉审查侧已有等价闭环（`review-closed-loop`：轻量档「单轮复检，复核全部已修复问题」），自审侧缺失，形成机制不对称。

## What Changes

- **新增「复检轮」（recheck round）**：多轮审查循环按现行规则到达终止点时，主 Agent SHALL 判定是否存在未经独立复核的修复；存在时 SHALL 追加 1 轮复检轮。
- **复检轮不消耗档位轮次预算**：全局最多追加 1 轮，与档位上限解耦（轻量档实际执行 1~2 轮）。复检轮只做验证、不再审；不复核则不得充当终止轮。
- **复检轮通过判据复用见证轮定义**：构成见证轮（零新发现 + 零修改 + 全量遍历 + 全部待复核修复逐项通过）即为通过；未构成则终止原因 `达上限` 并进入非收敛分支。有界，不会无限续杯。
- **复核范围覆盖全部累积修复**：复检轮 SHALL 逐项复核自审循环开始以来全部尚未通过复核的修复，而非仅最后一轮。
- **`.status.md` 终止原因扩为三值**：`收敛` / `收敛（复检轮）` / `达上限`，使审计可判读「为何停在第 N+1 轮」及是否使用了追加预算。
- **`执行轮次` 字段格式不变**：仍为 `{N} / {上限}`，只计审查轮；复检轮的存在由终止原因蕴含，不触发 BREAKING。
- **前轮修复清单改为累积维护**：`inter-round-summary` 的清单由「上轮修复」扩展为「累积未复核修复」，供终止判定与复检轮消费（不再仅限见证轮候选）。
- **门控与审计判定同步**：自审报告份数上限允许 `档位上限 + 1`（仅当存在合规复检轮时）；审计 SHALL NOT 因 `收敛（复检轮）` 或份数 = 上限 + 1 判定轮次不足、超额或缺项。
- **修正三份 `references/self-review.md` 的悬空引用**：`kflow-explore` / `kflow-design` / `kflow-prototype-design` 的 `self-review.md` 引用 `references/repetition.md` §13，但三者目录下均无该文件。复检轮须消费前轮摘要，引用不可悬空，本变更一并修正为指向有效位置。

## Capabilities

### New Capabilities

- `recheck-round`: 复检轮机制的唯一权威定义——触发条件（存在未复核修复）、预算规则（不消耗档位轮次、全局最多 1 轮）、复核范围（全部累积未复核修复）、通过判据（构成见证轮）、失败处理（进入非收敛分支）、报告与状态写入要求。其他能力引用本能力，SHALL NOT 另行定义。

### Modified Capabilities

- `tier-driven-repetition`: 收敛终止条件新增复检轮触发分支（清单非空 → 追加）；终止原因扩为三值；明确复检轮不消耗档位轮次预算。
- `subagent-self-review`: SELFREV 串行执行需求新增复检轮步骤；轻量档行为更新为「第 1 轮零发现即收敛，第 1 轮含修复则追加复检轮」，不再因发现问题直接判非收敛。
- `agent-iteration-execution`: 主 Agent 验收判据、硬性拒收条件与非收敛分支新增复检轮分支；prompt 规范补充复检轮指令。
- `plan-self-review`: plan 阶段 SELFREV 适用复检轮；计划自审的 4 维度检查后新增终止前复检环节。
- `inter-round-summary`: 前轮修复清单由「上轮修复」扩展为「累积未复核修复」；消费方由「见证轮候选」扩展到「终止判定 + 复检轮」。
- `round-counter`: 明确复检轮 SHALL NOT 计入 `执行轮次` 计数器，字段格式保持 `{N} / {上限}`。
- `execution-repetition-mode`: 重复制模型的终止与验证门控对齐复检轮；明确复检轮场景下的门控判定。
- `flexible-repetition-mode`: 回退重执行的轮次上限（`max(档位上限, 映射)`）之外，复检轮同样适用且不占该上限。
- `prototype-navigation-verification`: 导航合理性验证的轮次循环新增终止前复检轮（下限 1 / 上限 5 之外追加 1 轮）。
- `prototype-playwright-5round-verification`: Playwright 全覆盖验证的轮次循环新增终止前复检轮。

## Impact

**唯一权威定义新增**：`openspec/specs/recheck-round/spec.md`。

**实现层（`skills/`）**：

- `references/repetition.md` × 8（`kflow-code`、`kflow-code-review`、`kflow-api-test`、`kflow-e2e-test`、`kflow-integration-test`、`kflow-bug-fix`、`kflow-bug-triage`、`kflow-plan`）——§4 流程图 ACCEPT 分支、§7 Agent 完成判断、§8 验收标准表、§9 验收失败处理、§14.5 终止原因（二值 → 三值）、§14.6 非收敛分支、§15 验证门控。
- `references/self-review.md` × 3（`kflow-explore`、`kflow-design`、`kflow-prototype-design`）——§4 轮次取值、§4.5 终止条件与复核义务、§5 自审流程图、§6 自审执行方式、§7 自审记录存储、§8 自审报告内容规范；三份内容须保持一致（`phase-self-review` 要求）。
- `references/self-review-dimensions.md`（`kflow-explore`）——见证轮相关表述同步。
- `references/gates.md` × 10——份数判定（轻量 ≤1 / 标准 ≤2 / 完整 ≤5）改为允许 `+1`（仅当存在合规复检轮）。
- 各 `SKILL.md`（`kflow-explore`、`kflow-design`、`kflow-prototype-design`、`kflow-plan`、`kflow-code`、`kflow-code-review`、`kflow-api-test`、`kflow-e2e-test`、`kflow-integration-test`、`kflow-bug-fix`、`kflow-bug-triage`、`kflow-resume`、`kflow-audit`）——份数判定、终止原因、非收敛分支、验收块、SELFREV 步骤描述。

**设计层（`docs/designs/`）**：`core-mechanisms/03-status-and-tasks.md`、`04-gates-and-transitions.md`、`07-agent-model.md`、`08-governance.md`、`skills/kflow-*.md`（10 份）。

**入口**：`README.md`（档位行为差异表、FAQ 中执行类重复制说明、版本说明条目）。

**不改动**：`review-closed-loop`（交叉审查侧已具备等价闭环，事件驱动、无轮次上限制缺口）；`phase-self-review`（其规定的「三份 self-review.md 内容一致」要求自动覆盖新增的复检轮规则，无需变更）。

**兼容性**：`执行轮次` 字段格式不变，历史变更的 `.status.md` 读取路径不受影响；终止原因新增取值 `收敛（复检轮）`，读取方若未按枚举校验会将其视为未知值——本变更同步更新全部读取点。
