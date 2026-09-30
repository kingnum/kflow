# Design

## Context

动机见 `proposal.md`。本设计只记录影响改写口径的技术决策与交付边界。

约束：

- **新模型已由 `redesign-prototype-stage` 定稿并落地实现**。本变更不改写模型本身，只让 20 个落后 capability 的规格与已落地的实现一致。因此本变更的"正确性判据"是**与既有权威规格的一致性**，不是新的设计取向。
- **`skills/` 已在新口径上**。`redesign-prototype-stage` 执行期间已把 `skills/` 全量（含各技能 `references/gates.md`、`hooks.md`、`repetition.md`、`self-review.md`、`state-values.md` 副本）清扫到新口径，旧路径仅剩负向断言。
- **主规格是 delta 的合并目标**。本变更的 20 个 delta 与 `redesign-prototype-stage` 的 17 个 delta **目标文件不重叠**，两者可独立归档。
- **`design-change-record` 的载体模型需要重新表述**。其主规格以"三个设计产物目录各含 `index.md`"为骨架，而产品级原型目录在新模型下用 `manifest.md`，不再有 `index.md`。

## Goals / Non-Goals

**Goals:**

- 让 20 个 capability 的规格不再要求任何已废弃的变更级 `prototype/` 路径、`prototype.pen` 或旧位置的过程产物。
- 让规格描述的"下游输入限定 / 门控检查 / 落点规则"与已落地的实现逐条一致。
- 用 `openspec validate` 的"MODIFIED 不得丢失 scenario"检查，防止改写过程静默丢场景。

**Non-Goals:**

- 不改变任何运行时行为。若核对发现实现缺口，只补齐到与规格一致，不借机调整新模型。
- 不重写 `redesign-prototype-stage` 已覆盖的 17 个 capability。
- 不迁移已归档变更的 `prototype/` 目录（原地保留在 `docs/changes/archive/` 下）。
- 不引入新的产品级目录、新的角色枚举或新机制。
- 不为 `conditional-product-refs` 之外的其他 capability 调整图例/评分维度等与本变更无关的规则。

## Decisions

### D1 规格对齐，而非实现重写

**选择**：本变更的交付物以 `openspec/specs/` 下的 20 个 delta 为主。实现侧只做**核对**；仅在核对发现缺口时补齐。

**理由**：旧口径的实现已被清扫，规格落后是当前唯一缺陷。反向（改写规格去迁就旧实现）会把刚建立的直写模型推翻。若把实现重写也列入范围，会与 `redesign-prototype-stage` 的工作重复并制造冲突面。

**备选**：把落后 capability 合并回 `redesign-prototype-stage` —— 该变更已进入收尾（28/28 任务完成），追加会破坏其评审与归档边界。

### D2 记录载体由"三个变更级 index.md"改为"两个变更级 + 一个产品级清单"

**选择**：`design-change-record` 的骨架改为——变更级 `functional-designs/index.md`、变更级 `detailed-design.md`（或 `detailed-design/index.md`）、产品级 `docs/designs/prototypes/manifest.md` 三者含统一格式修订记录表。

**理由**：产品级原型目录是所有变更共用的**产品级**资产，其清单归属产品级，与 `functional-designs/`、`detailed-designs/` 由归档阶段写入不同——原型清单由原型设计阶段直写、归档时只登记。若强行保留"变更级 `prototype/index.md`"以维持"三个目录"的对称性，会与直写模型直接冲突。对称性让位于模型正确性。

**备选**：把 `manifest.md` 排除在修订记录统一步伐之外——会使产品级原型清单成为唯一不遵循统一修订记录格式的设计产物，破坏该 capability 的原意。

### D3 角色集合收敛：`coverage` 与 `process` 归变更级

**选择**：产品级清单的角色枚举为 `entry` / `page` / `tokens` / `shared` / `process`，且下游仅消费前四类。`subchange-input-source` 等规格中"角色为 entry/page/tokens/coverage/shared"的表述改为"entry/page/tokens/shared"，并把元素覆盖树显式指向变更级 `element-coverage-tree.md`。

**理由**：元素覆盖树承载 TC-ID 映射，是变更级追溯产物（design 阶段在其上追加填充），留在变更级可避免后续变更覆盖前序映射。把它列进产品级清单会诱导下游从产品级读取，与 `prototype-manifest` 的既有约定冲突。

**备选**：保留 `coverage` 在产品级清单中并标注"位于变更级"——角色枚举与实际位置矛盾，且下游需要额外分支处理。

### D4 分散原型引用收敛为"产品级清单 + 变更级改动清单"两项

**选择**：`phase-file-reload`、`phase-boundary-enforcement`、`phase-artifact-verification` 中同时出现 `prototype/index.html`、`prototype/design-tokens.css`、`prototype/element-coverage-tree.md` 三处分散引用的位置，统一收敛为 `docs/designs/prototypes/manifest.md` + `prototype-changes.md` 两项。

**理由**：`prototype-manifest` 已确立"下游通过清单动态取路径，不硬编码具体文件"与"阶段钩子使用原型产物清单加载，SHALL NOT 单独列出 design-tokens.css 和 element-coverage-tree.md"。本变更只是把这条既有决策补齐到遗漏的 capability。

**备选**：逐条把三个旧路径映射为对应的三个新路径——保留硬编码，违反既有决策。

### D5 修订目标命名改为产品级路径 + REVISION 模式

**选择**：`change-rollback`、`design-level-restructure` 中把原型修订目标表述为产品级 `docs/designs/prototypes/`，并明确须经 `kflow-prototype-design` 的 REVISION 模式（该模式复用有效工具链、跳过 INPUT/OPTIMIZE、不重复工具链选择）。

**理由**：写权限归属规定只有原型设计阶段可写产品级原型目录，其他阶段必须回退。命名上指向目录而非"prototype 阶段"可避免下游误以为可以就地改写。

**备选**：保留"prototype"作为阶段别名——与 `kflow-prototype-design` 的实际技能名不一致，且未表达"须走 REVISION"这一关键约束。

### D6 交付边界锁定在"规格 + 核对"

**选择**：`tasks.md` 中实现侧只列"核对"任务；核对发现缺口的处理作为独立的、需要停下报告的任务，而不是默认授权修改。

**理由**：核对结果未知，预先授权改实现会把范围从"规格对齐"扩大为"实现重写"，可能覆盖 `redesign-prototype-stage` 的既定结论。发现缺口时应当先报告再动手。

### D7 scenario 标题保留旧措辞，requirement 标题用 RENAMED 改名

**选择**：
- **requirement 标题**中内嵌旧路径的两处（`prototype/ 目录纯净性保证`、`三个设计目录均含 index.md`）使用 `## RENAMED Requirements` 改名，MODIFIED 块改用新标题。
- **scenario 标题**中内嵌旧路径的 6 处**不改名**，只在 delta 正文修正 WHEN/THEN 并附非规范性说明。

**理由**：`openspec validate` 按**名称**匹配 scenario 集合——实测把 scenario 改名会被判为"omits scenario(s) the current spec still has"并拒绝（与 requirement 的 RENAMED 机制不同，scenario 无对应机制）。因此 scenario 改名无法在 delta 中表达；强行改名会让变更不可校验。requirement 改名则有 `## RENAMED Requirements` 支持（本项目已有先例：`prototype-design-index`）。

**备选**：为 scenario 也走"直接编辑主规格"——需求评审（propose）阶段不应写主规格；该动作属于实施阶段，且必须与 delta 配对修改才能保持校验通过，故列入实施任务而非本次变更的 delta。

### D8 无法由 delta 表达的残留作为实施阶段的独立任务收口

**选择**：把 scenario 标题（6 处）与 `## Purpose`（3 处）中的旧路径残留，收拢为实施阶段的一个独立任务；该任务同时修改主规格与 delta，以保持 `openspec validate` 通过。

**理由**：`## Purpose` 对既有 capability 只能直接编辑主规格（openspec 忽略 delta 的 Purpose 并告警）。把这类"机制外"修改集中到一处，便于评审时一眼看清本变更**不能在规格 delta 内表达**的部分，避免它们被夹带在正文改写中而不被注意。

## Risks / Trade-offs

- **[改写过程中静默丢失 scenario]** → MODIFIED 是整块替换，`openspec validate` 会拦截"omits scenario(s) the current spec still has"；每条改写任务以 `openspec validate sync-legacy-prototype-specs` 无 ERROR 为完成判据。
- **[与 `redesign-prototype-stage` 的 delta 冲突]** → 两者的目标规格文件集合不重叠（前者 17 个、本变更 20 个，已核对无交集）。若前者先归档，本变更的 delta 仍可正常应用。
- **[核对发现实现缺口，范围外溢]** → 按 D6 停下报告，由用户决定是否扩大范围；本变更的规格改写本身不受影响。
- **[规格改写引入新的口径分歧]** → 每条改写只做路径与角色层面的等价替换，不改变行为语义；核对任务逐条比对规格与实现的 SHALL 断言。
- **[`conditional-product-refs` 的图例约定被误改]** → 该 capability 只改"原型产物统一入口"这一句，图例（✅ 必须 / 🔶 条件 / ⏭️ 跳过）与其适用性标签规则不在改动范围。

## Migration Plan

1. **规格先行**：本变更的 20 个 delta 写入 `openspec/changes/sync-legacy-prototype-specs/specs/`，`openspec validate sync-legacy-prototype-specs` 通过。
2. **归档应用**：归档时把 delta 应用到 `openspec/specs/`，主规格成为新权威。
3. **实现核对**：逐条比对改写后的规格与 `skills/` 实现，产出核对结论；发现缺口则报告。
4. **设计文档同步**：`docs/designs/` 下与这 20 个 capability 对应的文档若含旧口径，同步更新。
5. **回滚策略**：本变更为文档与规格变更，回滚即 `git revert`；不涉及运行时数据迁移。

## Open Questions

无。改写取向见 `design.md` 的 Decisions 与各 delta 的正文；不确定处按"保留原意、不臆造新行为"处理并在核对阶段暴露。
