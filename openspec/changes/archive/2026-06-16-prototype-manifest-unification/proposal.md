## Why

当前体系中，下游阶段（kflow-plan、kflow-code、kflow-code-review、kflow-e2e-test 等）的输入表硬编码了三个原型产物文件（`prototype/index.html`、`prototype/design-tokens.css`、`prototype/element-coverage-tree.md`），假设原型产物的文件结构是固定的。但实际上，不同原型设计 Skill（如 `huashu-design`、`frontend-design`）的产物结构可能不同（单文件 vs 多页面），这种硬编码导致下游阶段无法感知原型产物的真实结构，缺乏灵活性。

已有 `prototype/index.md`（原型索引），本可在原型设计结束时描述实际产物全貌，但下游阶段未将其作为输入源，形成了"索引文件存在却不被消费"的断裂。

## What Changes

- **强化 `prototype/index.md` 为「原型产物清单」（Prototype Manifest）**：在原型设计阶段结束时（用户确认通过后），自动更新 `index.md` 使其完整描述原型产物的实际结构——产物组织方式、所有 HTML 文件清单（含角色标注）、页面与文件映射关系、设计令牌文件位置、元素覆盖树位置、共享资源清单。
- **下游阶段输入表统一入口**：将 kflow-plan、kflow-code、kflow-code-review、kflow-e2e-test 输入表中的三个硬编码原型产物引用替换为 `prototype/index.md`（✅ 必须，前端SC），下游阶段通过读取 `index.md` 动态获取原型文件列表。
- **门控规则和阶段钩子同步调整**：`gate-rules.md` 和 `phase-hooks.md` 中的前端子变更门控检查，从"三个文件各自检查"改为"检查 `prototype/index.md` 存在且内容完整"。
- **执行流程动态化**：编码阶段的"原型转译"四阶段子流程、计划阶段的"前端功能点全展开模板"，从直接引用 `prototype/index.html` 改为引用 `prototype/index.md` 中声明的对应文件。
- **输入限定规则调整**：`前端SC 输入限定`规则从"限定三个核心产物文件"改为"限定 `prototype/index.md` 声明的产物文件"，保留过程产物排除规则（design-prompt.md、design-system/MASTER.md）。

## Capabilities

### New Capabilities
- `prototype-manifest`: 原型产物清单（Prototype Manifest）机制——定义 `prototype/index.md` 的完整清单结构（产物组织方式、HTML 文件清单与角色标注、页面-文件映射、设计令牌引用、元素覆盖树引用、共享资源清单），以及原型设计阶段结束时自动生成/更新清单的时机。

### Modified Capabilities
- `prototype-design-index`: 扩展 `prototype/index.md` 的内容规格，新增「产物组织方式描述」和「共享资源清单」段落，强化其作为下游消费入口的定位。
- `subchange-input-source`: 前端子变更输入源从硬编码三个原型产物文件改为 `prototype/index.md`（✅ 必须，前端SC），输入限定规则同步调整。
- `prototype-to-code-consistency`: 编码阶段前端转译流程从直接引用 `prototype/index.html` 改为读取 `prototype/index.md` 声明的产物文件，设计令牌和元素覆盖树的引用路径改为从清单获取。
- `conditional-product-refs`: 门控检查逻辑从逐一检查三个原型文件改为检查 `prototype/index.md` 的完整性和存在性。
- `html-prototype-workflow`: 原型设计阶段结束时的产物总结步骤强化——用户确认通过后自动更新 `index.md` 反映最终产物全貌。

## Impact

**SKILL.md 文件**（运行时 Skill）:
- `kflow-plan/SKILL.md` — 输入表（行 57）+ 前端功能点模板（行 189）+ 质量检查表（行 369）
- `kflow-code/SKILL.md` — 输入表（行 53、56）+ 原型转译四阶段流程（行 418-445）+ 降级表（行 451-453）+ 验收标准（行 730）
- `kflow-code-review/SKILL.md` — 输入表（行 48）+ 执行流程（行 117、192）
- `kflow-e2e-test/SKILL.md` — 输入表（行 54）+ 视觉一致性评分（行 215、223-224）+ 报告模板（行 399）
- `kflow-verify/SKILL.md` — 验收标准（行 45、76）
- `kflow-resume/SKILL.md` — 产物存在性检查（行 201）+ 恢复上下文（行 257）
- `kflow-prototype-design/SKILL.md` — 输出产物（行 108）+ 修订模式检测（行 146）+ 修订逻辑（行 796）
- `kflow-shared/gate-rules.md` — 前端子变更门控检查（行 71-73）+ 集成测试门控（行 123）+ 恢复验证（行 149）
- `kflow-shared/phase-hooks.md` — PRE_HOOK 产物加载表（行 21-25）+ RELOAD 产物加载表（行 204-208）

**设计文档**:
- `docs/designs/skills/kflow-plan.md`、`kflow-code.md`、`kflow-code-review.md`、`kflow-e2e-test.md`、`kflow-verify.md`、`kflow-resume.md`、`kflow-prototype-design.md` — 同步修改输入表、执行流程、验收标准中的原型产物引用
- `docs/designs/core-mechanisms/03-status-and-tasks.md`、`04-gates-and-transitions.md`、`08-governance.md` — 同步修改模板和治理规则

**模板文件**:
- `docs/designs/templates/changes/{change}/prototype/index.md` — 扩展模板结构
- `docs/designs/templates/changes/{change}/change-status.md`、`change-tasks.md` — 同步更新引用
- `docs/designs/templates/subchanges/{subchange}/e2e-round-report.md` — 同步更新引用

**规格文件**:
- `openspec/specs/prototype-design-index/`、`subchange-input-source/`、`prototype-to-code-consistency/`、`conditional-product-refs/`、`html-prototype-workflow/` — 同步更新规格
