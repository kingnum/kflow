# Proposal

## Why

`redesign-prototype-stage` 变更把原型产物改为**变更直写产品级** `docs/designs/prototypes/`（变更级只保留 `prototype-changes.md`、`prototype-backup/`、`prototype-plan/`、`element-coverage-tree.md`），但该变更的 Capabilities 段只覆盖了 17 个 capability。全库扫描发现**另有 20 个主规格仍描述旧的"变更级 `prototype/` 副本"模型或已移除的 Pencil 产物**——它们会要求 `prototype/index.html`、`prototype/index.md`、`prototype/design-tokens.css`、`prototype/element-coverage-tree.md`、`prototype/design-prompt.md`、`prototype.pen` 这类已不存在的产物。

这 20 个 capability 的**实现侧已在 `redesign-prototype-stage` 中被顺带清扫**（`skills/` 全量已无旧路径），因此当前状态是**规格落后于实现**：规格要求的行为与技能实际行为不一致，违反 CLAUDE.md「验证闭环」与 openspec 的规格权威原则。下游阶段（plan / code / code-review / e2e-test / integration-test / resume / verify / triage）的门控与输入限定会按旧模型判定，属于会实际误报的缺陷。

现在处理是因为：`redesign-prototype-stage` 尚未归档，两个变更合并考虑可避免中间态被归档为"权威规格"。

## What Changes

统一 17 个 capability 的原型路径口径，使规格与已更新的实现一致。逐条：

### 原型产物入口改为"产品级清单 + 变更级改动清单"

- 变更级 `prototype/index.md` 的引用统一改为产品级 `docs/designs/prototypes/manifest.md` 与变更级 `prototype-changes.md` 两者（前者为全产品清单、后者界定本变更涉及页面）。
- 角色集合由 `entry/page/tokens/coverage/shared` 收敛为 `entry/page/tokens/shared`——`coverage`（元素覆盖树）与 `process`（`prototype-plan/`）归变更级，不计入产品级清单。
- 涉及 capability：`conditional-product-refs`、`subchange-input-source`、`phase-file-reload`、`phase-boundary-enforcement`、`phase-artifact-verification`、`frontend-implementation-subchange`、`resume-product-gate`、`design-level-restructure`。

### 原型文件路径改为产品级目录

- 变更级 `prototype/` 目录下的原型文件引用统一改为 `docs/designs/prototypes/`（屏幕在 `screens/`、共享组件在 `components/`、静态资源在 `assets/`）。
- 涉及 capability：`kflow-runtime-isolation`、`prototype-offline-constraint`、`e2e-element-coverage-tree`、`playwright-cli-e2e-workflow`、`bug-triage-skill`、`cross-tier-violation-detection`。

### 元素覆盖树落点固定为变更根目录

- 有原型时元素覆盖树落 `docs/changes/{change}/element-coverage-tree.md`（原为 `prototype/` 目录下），使 TC-ID 追溯保持在变更级、不被后续变更覆盖。
- 涉及 capability：`e2e-element-coverage-tree`、`playwright-cli-e2e-workflow`。

### 提示词与过程产物路径改为变更级 `prototype-plan/`

- `prototype/design-prompt.md` → `prototype-plan/design-prompt.md`；`prototype/style-decision.md` → `prototype-plan/style-decision.md`。
- 涉及 capability：`prototype-prompt-optimization`。

### 设计产物记录载体调整

- "三个设计目录均含 `index.md`"改为：变更级 `functional-designs/index.md` 与 `detailed-design.md`（或 `detailed-design/index.md`）+ 产品级 `docs/designs/prototypes/manifest.md`；修订记录表格式统一到这三者。
- 该 capability 的 `kflow-guide 集中检测设计修订意图` 需求同步改写：修订目标解析由 `prototype` 别名改为产品级 `docs/designs/prototypes/`，修订完成后更新目标设计产物载体的修订记录（含产品级 `manifest.md`），与 `change-rollback` 的修订目标枚举口径一致。
- 涉及 capability：`design-change-record`。

### 命名口径修正

- 修订目标枚举与类似表述中的 `prototype` 指向改为产品级 `docs/designs/prototypes/`，并明确 UI 修订须经 `kflow-prototype-design` REVISION 模式。
- 涉及 capability：`change-rollback`、`design-level-restructure`。

### 已移除的 Pencil 产物口径修正

- `prototype.pen`（Pencil 工具生成物）的引用改为 HTML 原型产物口径——Pencil 依赖已在 `html-prototype-workflow` 的「移除 Pencil 依赖」中被移除，但以下 capability 仍以 `.pen` 描述原型产物。
- 涉及 capability：`phase-boundary-enforcement`、`stage-doc-templates`、`user-review-gate`。

### 要求标题重命名（RENAMED）

- `kflow-runtime-isolation`：`prototype/ 目录纯净性保证` → `docs/designs/prototypes/ 目录纯净性保证`。
- `design-change-record`：`三个设计目录均含 index.md` → `设计产物记录载体均含修订记录表`。

### 机制限制（需在实施阶段直接编辑主规格收口）

openspec 的 delta 机制**按名称匹配** requirement 与 scenario，因此有两类文本无法通过 delta 表达，需在实施阶段直接编辑主规格：

- **scenario 标题**中内嵌的旧路径（6 处：`phase-file-reload`、`phase-boundary-enforcement`、`e2e-element-coverage-tree`、`kflow-runtime-isolation`×2、`design-change-record`）——重命名会被 `openspec validate` 判为"丢失 scenario"而拒绝。delta 正文已修正，标题保留旧措辞，并附非规范性说明。
- **`## Purpose`** 中内嵌的旧路径（3 处：`conditional-product-refs`、`kflow-runtime-isolation`、`prototype-design-prompt-template`）——openspec 对既有 capability 的 Purpose 只告警并忽略。

这两类共 9 处，作为一个独立任务在实施阶段处理（主规格与 delta 需配对修改以保持校验通过）。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `conditional-product-refs`: 原型产物统一入口由变更级 `prototype/index.md` 改为产品级 `manifest.md` + 变更级 `prototype-changes.md`。
- `subchange-input-source`: 前端子变更输入源的入口与角色集合改写（去 `coverage`，`coverage` 归变更级元素覆盖树）。
- `phase-file-reload`: RELOAD 清单中的变更级 `prototype/index.md` 改为产品级 `manifest.md` + 变更级 `prototype-changes.md`。
- `phase-boundary-enforcement`: Plan / Code 入口门控的原型产物检查对象改写。
- `phase-artifact-verification`: D3 输入源正确性检查中的原型产物清单改写。
- `frontend-implementation-subchange`: 前端编码输入限定、工程骨架搭建、逐页转译的原型路径与角色口径改写。
- `e2e-element-coverage-tree`: 有原型时树的生成来源与落点（变更根目录）改写。
- `kflow-runtime-isolation`: 原型 HTML 引用路径与"目录纯净性"约束的对象由变更级 `prototype/` 改为 `docs/designs/prototypes/`。
- `prototype-offline-constraint`: 离线自包含约束中图片与扫描范围的目标目录改写。
- `prototype-prompt-optimization`: OPTIMIZE 的输出路径与提示词文件位置改写为 `prototype-plan/`。
- `design-change-record`: 设计产物记录载体由"三个变更级 index.md"改为"两个变更级 + 产品级 manifest.md"。
- `design-level-restructure`: 越界约束中"禁止修改 prototype/"的口径改写。
- `bug-triage-skill`: L2 原型设计层诊断的证据来源改写。
- `resume-product-gate`: 原型阶段产物完整性验证项改写（加入 BUILD 报告与审查方式记录）。
- `playwright-cli-e2e-workflow`: 无原型判定依据与元素覆盖树生成触发条件改写。
- `cross-tier-violation-detection`: code-review 原型路径引用检测的路径口径改写。
- `change-rollback`: 修订目标枚举中 `prototype` 的指向改写。
- `prototype-design-prompt-template`: 提示词文件位置改为变更级 `prototype-plan/design-prompt.md`；第六章硬约束改为直写产品级原型目录 + 改动记录与备份。
- `stage-doc-templates`: 模板覆盖范围的例外项由 `prototype.pen` 改为 HTML 原型产物。
- `user-review-gate`: 原型设计用户评审门控的产物描述由 `prototype.pen` 改为产品级原型产物与 `manifest.md`。

## Impact

### 规格层（主要影响）

`openspec/specs/` 下 20 个 capability 的 `spec.md`。逐个 capability 一个 delta（共 39 个需求块），归档时应用。

### 实现层（预期无实质改动）

`redesign-prototype-stage` 已把 `skills/` 全量清扫到新口径（含各技能的 `references/gates.md`、`hooks.md`、`repetition.md`、`self-review.md`、`state-values.md` 副本）。本变更 SHALL 逐条核对实现是否已满足改写后的规格；**如发现实现缺口则补齐**，否则仅确认一致。已预判一处待核对项：`phase-artifact-verification` 的 D3.1 要求检查变更级 `element-coverage-tree.md`，而 `skills/kflow-verify/SKILL.md` 当前只列出 `manifest.md` 与 `prototype-changes.md`。

### 设计文档层

`docs/designs/` 下与这 20 个 capability 对应的设计文档若含有旧口径（例：`conditional-product-refs` 的图例约定、`design-change-record` 的修订记录载体说明、`e2e-element-coverage-tree` 的落点表、`kflow-runtime-isolation` 的目录纯净性表述），需同步。

### 兼容性影响

- 不改变任何运行时行为——实现已先行，本变更使规格追上实现。
- 已归档变更不受影响（其 `prototype/` 目录原地保留在 `docs/changes/archive/` 下）。
- 不使用原型设计的变更（纯后端项目、跳过原型）不受影响。

### 与 `redesign-prototype-stage` 的关系

两者是同一重构的两次交付：前者的 Capabilities 段遗漏了这 20 个 capability。本变更**依赖前者已落地的实现**，但不依赖其归档状态；若前者先归档，本变更的 delta 仍可正常应用（目标规格文件互不重叠，已核对无交集）。
