# Proposal

## Why

多轮审查机制的终止条件是「收敛 **或** 轮次上限」的二元结构。上限的引入并未带来节奏控制，而是制造了一组自我循环的复杂度：

1. **上限在正常路径上惰性**——达成见证轮即提前终止，所以上限只在循环**不收敛**时生效。它承担的不是「审几轮」而是「不收敛时怎么办」。
2. **但现行参数让「预算内收敛」成为少数派**——第 1 轮审查的对象是刚产出、刚修改的产物，结构上不可能同时满足「零新发现 + 零修改」。轻量档（上限 1）的正常路径因此是「达上限 → 复检轮 → 收敛（复检轮）」，标准档设计自审（上限 2）同理偏紧。**一个为兜底而生的机制变成了常规路径。**
3. **兜底机制随之膨胀**——为覆盖「上限轮带着未复核修复终止」这一缝隙，v0.22.0 引入复检轮，连带三值终止原因、`份数 = 档位上限 + 1` 判读链、审计例外条款。机制复杂度被用于处理上限自己制造的问题。
4. **上限掩盖的真正风险是「收敛不可达」**——冷启动子代理每轮都能"发现"问题，其中相当部分在审查对象之外（范围外文件、顺手重构、借审查之名新增功能点/字段/章节、新增审查维度）。**只要审查者可以自行扩大审查范围，「零新发现」就永远不可达。**

本变更把终止模型从「收敛或上限」翻转为「收敛为唯一成功终止条件」，并补上让收敛**可达**的前提——审查范围冻结。

## What Changes

- **删除档位轮次上限**（**BREAKING**）：执行类 1/3/5、设计自审 1/2/5 全部移除。轮数不再由档位决定，而由收敛实际发生在第几轮决定。
- **删除回退叠加上限**（**BREAKING**）：`max(档位上限, 影响范围分数映射)` 与统一分数→轮次映射表移除；`Recommended Rounds` 字段移除。影响范围分数本身保留（供验证门控的受影响项清单与回退判定）。
- **收敛成为唯一成功终止条件**：见证轮定义收敛为 4 项——(a) 零新发现、(b) 零修复/零修改、(c) 报告证明全维全量遍历、(d) 累积未复核修复清单内全部条目逐项复核通过。
- **复检轮上提为见证轮第 (d) 项**（**BREAKING**）：`recheck-round` 能力删除。复检轮的通过判据本就是「构成见证轮」，其复核义务并入收敛判据后不再需要独立机制与其配套的份数判读链。
- **新增不收敛判定与升级**：无进展（连续 2 轮「新发现数」与「清单长度」双双无改善）/ 振荡（同一问题项「修复→重新发现」≥ 2 次）/ 保险丝（全局 10 轮，与档位脱钩、不参与门控判读）。命中即升级用户，复用既有非收敛分支（`skill-suggestion.md` + AskUserQuestion + 可标 ⚠️ 阻塞）。
- **新增审查范围冻结**：审查对象集合（阶段产物既有内容）冻结 + 审查维度集合封闭，**全部审查适用**（SELFREV + 执行类重复制 + prototype 三验证）。范围外发现降级为「范围外观察」——不改产物、不计入发现数、不阻断收敛；引入范围外新内容的轮次 SHALL NOT 判为见证轮。冻结按**轮**生效：清单由主 Agent 在每轮开始时生成，轮内不得扩大，跨轮可因阶段输入变化（如回退）由主 Agent 更新。
- **档位语义收敛**：只决定每轮审查强度（单 Agent / 两视角 / 四视角）与产出深度，与轮数解耦。
- **完整档评分底线内化**：评分 ≤8 时须列出具体问题项，于是「评分 ≤8」等价于「存在新发现」⇒ 不构成见证轮。取消「或达上限 5」的兜底。
- **轻量档代码审查去单轮限制**：`code-review-skill` 的「轮次上限为 1 轮、SHALL NOT 启动多轮重复制迭代」移除，与其余阶段同口径。
- **验证门控退化**：「全量至少 1 轮兜底」被见证轮定义吞并删除；「受影响项 100% 覆盖」挂到回退重执行场景；产物完整性保留为硬门。
- **字段与判读简化**：`执行轮次` 由 `{N} / {上限}` 改为 `{N} 轮`；`gates.md` 份数判定四条规则塌为「份数 ≥ 1」；审计的轮次超标判据、复检轮合法分支与「测试轮次 vs 上限」对比行删除。
- **终止原因由三值改二值**（**BREAKING**）：`收敛` / `未收敛`；具体缘由（停滞/振荡/保险丝）写入 `skill-suggestion.md`。
- **能力重命名**（**BREAKING**）：`tier-driven-repetition` → `convergence-driven-repetition`。
- **保留不动**：单用例 3 次修复上限（`defect-strike-limit`）、轮次级子代理重试 3 次上限、全局轮次下限 1 轮。

## Capabilities

### New Capabilities

- `convergence-driven-repetition`: 终止模型的唯一权威定义——收敛判据（见证轮 4 项）、不收敛判定与升级（无进展 / 振荡 / 保险丝）、审查范围冻结（对象集合冻结 + 维度集合封闭 + 范围外观察降级）、档位语义（每轮审查强度与产出深度）、全局轮次下限。取代 `tier-driven-repetition`，并吸收 `recheck-round` 的全部实质内容。

### Modified Capabilities

- `tier-driven-repetition`: 全部 Requirement 移除，能力废弃，职责迁移至 `convergence-driven-repetition`。
- `recheck-round`: 全部 Requirement 移除，能力废弃，复核义务上提为见证轮第 (d) 项。
- `agent-iteration-execution`: 「按档位轮次上限迭代」改为「迭代至收敛」；验收判据、硬性拒收条件、非收敛分支触发条件、prompt 规范同步。
- `round-counter`: `执行轮次` 格式 `{N} / {上限}` → `{N} 轮`；验收条件去掉「= 轮次上限」分支。
- `subagent-self-review`: 去掉档位轮次上限与复检轮段落；新增审查范围冻结与不收敛升级。
- `plan-self-review`: 同上（plan 取设计自审口径的例外条款一并移除）。
- `code-review-skill`: 移除轻量档「单轮、不启动多轮迭代」；轻量档保留单 Agent 审查形态，轮数由收敛决定。
- `execution-repetition-mode`: 重复制模型的终止与验证门控对齐收敛；移除档位上限与复检轮表述。
- `flexible-repetition-mode`: 移除回退叠加上限、分数→轮次映射与 `Recommended Rounds`。
- `inter-round-summary`: 摘要格式新增「范围外观察」字段，供后续轮次避免重复发现范围外内容。
- `triage-impact-assessment`: 移除「影响评分 → 重复制轮次」的映射要求；影响评分本身保留。
- `defect-strike-limit`: 删除与轮次上限的层级对照表述，改为与收敛终止的关系（3 次修复上限维度不变）。
- `auto-subchange-traversal`: 子代理 prompt 模板中的「不超过轮次上限」改为收敛驱动表述。
- `resume-product-gate`: 完成判定中的「或 = 轮次上限」分支移除。
- `review-closed-loop`: 删除「SHALL NOT 因自审轮次少于档位轮次上限判定缺项」（前提消失）。
- `devflow-audit`: 轮次达标基准改为收敛判定；删除复检轮合法分支、份数 = 上限 + 1 例外条款与「测试轮次 vs 上限」对比行。
- `prototype-navigation-verification`: 「不少于 1 轮、不超过 5 轮」→ 纯收敛驱动。
- `prototype-playwright-5round-verification`: 「不少于 1 轮、不超过 5 轮」→ 纯收敛驱动。
- `prototype-review-artifacts`: `round-{N}.md`（N 为 1-5）去掉固定 5 轮束缚；「按分级轮次上限产出的自审报告」改为按收敛实际轮次。
- `prototype-build-gate`: 「达成见证轮或达到轮次上限后方可进入 REVIEW」→ 只留收敛。
- `html-prototype-workflow`: 原型验证轮次的统一引用条款去掉「上限 5」。
- `lightweight-flow-trimming`: 档位升级场景中的「按标准档的轮次与审查形态执行」改为「审查形态」。
- `change-tier-classification`: 「按 `完整` 档确定轮次与审查形态」改为「审查形态与产出深度」。

## Impact

**唯一权威定义**：新增 `openspec/specs/convergence-driven-repetition/spec.md`；移除 `openspec/specs/tier-driven-repetition/` 与 `openspec/specs/recheck-round/`；另有 23 份既有能力 delta。

**实现层（`skills/`）**：

- `references/repetition.md` × 8（`kflow-code`、`kflow-code-review`、`kflow-api-test`、`kflow-e2e-test`、`kflow-integration-test`、`kflow-bug-fix`、`kflow-bug-triage`、`kflow-plan`）——§2 核心特征、§4 流程图、§7 完成判断、§8 验收标准、§9 验收失败分流、§10 prompt 规范、§11 触发条件、§13 轮间摘要、§14 轮次决策（重写为终止模型）、§15 验证门控（退化）、§16 执行历史、§17 分数读取（去映射）。八份须保持一致。
- `references/gates.md` × 10——§1.3 份数判定四条规则塌为「份数 ≥ 1」；归档门控与恢复完整性门控同步。
- `references/self-review.md` × 3（`kflow-explore`、`kflow-design`、`kflow-prototype-design`）——§4 轮次取值、§4.5 终止条件与复核义务、§5 流程图、§8 报告内容规范、范围冻结条款；三份须一致（`phase-self-review` 要求）。
- `references/self-review-dimensions.md`（`kflow-explore`）——见证轮与范围冻结相关表述。
- 各 `SKILL.md` × 14（`kflow-explore`、`kflow-design`、`kflow-prototype-design`、`kflow-plan`、`kflow-code`、`kflow-code-review`、`kflow-api-test`、`kflow-e2e-test`、`kflow-integration-test`、`kflow-bug-fix`、`kflow-bug-triage`、`kflow-audit`、`kflow-resume`、`kflow-archive`）——验收块、SELFREV 步骤、门控描述、审计判据。
- `.claude/skills/`（`grilling`、`skill-creator`、`to-spec`）为通用运行时技能，与本变更无关，不涉及。

**设计层（`docs/designs/`）**：`core-mechanisms/04-gates-and-transitions.md`、`07-agent-model.md`、`03-status-and-tasks.md`、`index.md`、`skills/kflow-*.md`（涉及 10 份）。

**入口**：`README.md`（档位行为差异表、执行类重复制说明、复检轮 FAQ、版本说明条目）。

**兼容性**：

- `执行轮次` 字段分母消失，历史 `.status.md` 的 `1 / 3` 形式由读取侧忽略分母处理，不要求迁移。
- 终止原因取值由三值改二值，历史 `.status.md` 中的 `收敛（复检轮）` / `达上限` 需在读取侧归并为 `收敛` / `未收敛`。
- 能力 id 变更（`tier-driven-repetition` → `convergence-driven-repetition`）影响全部交叉引用点。

**假设（可在评审时否决）**：能力 `prototype-playwright-5round-verification` 的名称含已删除的固定 5 轮语义，本变更**不重命名**（沿用 `converge-review-rounds` 变更既有的容忍先例，避免额外 churn）。如需一并改名请在评审时提出。
