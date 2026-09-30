# Tasks

> **本变更的 delta 已在提案阶段写入** `openspec/changes/sync-legacy-prototype-specs/specs/`（20 个 capability、37 个 MODIFIED 需求块 + 2 个 RENAMED 条目）。因此实施阶段的工作是**核验 delta 的覆盖度与正确性**、收口 delta 机制无法表达的残留、并核对实现与设计文档。
>
> **核验基线**：`openspec validate sync-legacy-prototype-specs` 通过；delta 与主规格逐条比对确认覆盖度；归档后的目标状态以临时副本模拟 `openspec archive` 验证（37 modified、2 renamed、`openspec validate --specs` 133/133 通过）。

## 1. 清单入口口径类 delta 核验（8 个 capability）

- [x] 1.1 核验 `conditional-product-refs` 的 delta：主规格中"原型产物统一入口"相关表述已全部改写为产品级 `docs/designs/prototypes/manifest.md` + 变更级 `prototype-changes.md`，且图例约定（✅ 必须 / 🔶 条件 / ⏭️ 跳过）未被改动。验证：`openspec validate sync-legacy-prototype-specs` 无 ERROR，且该 delta 的需求块与主规格逐条比对后无遗漏的旧口径
- [x] 1.2 核验 `subchange-input-source` 的 delta：前端子变更输入源的入口、角色集合（去 `coverage`）、过程产物排除项均已改写；后端子变更的"SHALL NOT 包含原型产物"表述已改写。验证：同上
- [x] 1.3 核验 `phase-file-reload` 的 delta：RELOAD 清单中 7 个阶段的原型条目均已由旧路径改为 `docs/designs/prototypes/manifest.md` + `prototype-changes.md`，且三处分散引用已收敛。验证：同上，并与 `skills/kflow-plan/references/hooks.md` 的 12 阶段钩子表逐条比对一致
- [x] 1.4 核验 `phase-boundary-enforcement` 的 delta：Code 入口门控、E2E 入口门控、集成测试回溯验证、阶段内容禁止越界（`prototype.pen` → HTML 原型产物）四处的限定条件均已改写。验证：同上，并与 `skills/kflow-code/references/gates.md` 比对一致
- [x] 1.5 核验 `phase-artifact-verification` 的 delta：D3 输入源正确性检查内 8 个 scenario 的前端子变更产物清单与后端越界模式均已改写。验证：同上
- [x] 1.6 核验 `frontend-implementation-subchange` 的 delta：任务模板的设计约束来源、编码子流程的骨架/逐页转译、输入限定白名单三处均已改写。验证：同上
- [x] 1.7 核验 `resume-product-gate` 的 delta：验证项映射表的原型设计行已改为 manifest + prototype-changes + BUILD 报告 + 用户评审。验证：同上
- [x] 1.8 核验 `design-level-restructure` 的 delta：design 阶段域外约束中的原型目录表述已改写；确认其余需求确实不含旧路径口径（未列入 delta 者不得遗漏真实旧口径）。验证：同上

## 2. 路径与落点类 delta 核验（6 个 capability）

- [x] 2.1 核验 `kflow-runtime-isolation` 的 delta：`## RENAMED Requirements` 生效（requirement 标题改名），playwright 运行时隔离、`/playwright-cli` 工作目录约束、目录纯净性三处正文与 WHEN/THEN 均已改为全库统一的 `docs/designs/prototypes/` 口径。验证：`openspec validate sync-legacy-prototype-specs` 无 ERROR；`grep -n "docs/designs/prototypes/" openspec/changes/sync-legacy-prototype-specs/specs/kflow-runtime-isolation/spec.md` 命中三处且无裸 `prototype/` 正文
- [x] 2.2 核验 `prototype-offline-constraint` 的 delta：图片本地文件与 CDN 扫描范围两处目标目录已改写，离线自包含约束实质（内联/base64/系统字体栈/禁 CDN）逐字未变。验证：同上（该需求 6 个 scenario 全部保留）
- [x] 2.3 核验 `e2e-element-coverage-tree` 的 delta：有原型时的生成来源改为产品级原型目录、树落点固定为变更根目录；无原型路径与 TC-ID 100% 门控语义未变。验证：同上
- [x] 2.4 核验 `playwright-cli-e2e-workflow` 的 delta："无原型"判定依据改为 `manifest.md` 不存在。验证：同上
- [x] 2.5 核验 `bug-triage-skill` 的 delta：L2 层的诊断证据来源与检查对象已改写。验证：同上，并与 `skills/kflow-bug-triage/SKILL.md` 的 L2 节比对一致
- [x] 2.6 核验 `cross-tier-violation-detection` 的 delta：越界检测的原型路径模式已改为 `docs/designs/prototypes/`（确认改在 verify D3.2 而非 code-review 需求）。验证：同上，并与 `skills/kflow-verify/SKILL.md` 比对一致

## 3. 过程产物、记录载体与命名类 delta 核验（6 个 capability）

- [x] 3.1 核验 `prototype-prompt-optimization` 的 delta：硬约束中的输出目录已改为直写产品级，且提示词输出位置补为 `prototype-plan/design-prompt.md`；7 章节与用户确认机制未变。验证：`openspec validate sync-legacy-prototype-specs` 无 ERROR
- [x] 3.2 核验 `design-change-record` 的 delta：`## RENAMED Requirements` 生效（`三个设计目录均含 index.md` → `设计产物记录载体均含修订记录表`）；载体枚举、修订记录表格式、`.status.md` 设计修订同步追踪三处均已改为"两个变更级载体 + 产品级 `manifest.md`"；核验中发现 `kflow-guide 集中检测设计修订意图` 需求块未被 delta 覆盖且含旧口径，已补入 delta（需求块数 38 → 39）并同步 `proposal.md`，使修订目标枚举与 `change-rollback` 的改写口径一致。验证：同上
- [x] 3.3 核验 `change-rollback` 的 delta：修订目标枚举已改为产品级路径，并明确原型修订须经 REVISION 模式。验证：同上
- [x] 3.4 核验 `prototype-design-prompt-template` 的 delta：文件输出与 7 章节模板结构两个需求的文件路径改为 `prototype-plan/`，第六章硬约束改为直写产品级 + 改动记录与备份，第一/三/七章的 OPTIMIZE 步骤号对齐为 5.x。验证：同上
- [x] 3.5 核验 `stage-doc-templates` 的 delta：模板覆盖范围的例外项已由 `prototype.pen` 改为 HTML 原型产物枚举。验证：同上
- [x] 3.6 核验 `user-review-gate` 的 delta：原型设计用户评审门控的产物描述已改为产品级原型产物与 `manifest.md`，4 个 scenario 全部保留。验证：同上

## 4. delta 机制外残留收口

- [x] 4.1 收口 scenario 标题中内嵌旧路径的 6 处：`phase-file-reload`（重读 prototype/index.md → 重读产品级原型清单与变更级原型改动清单）、`phase-boundary-enforcement`（前端子变更 prototype/* 强制检查 → 前端子变更原型核心产物强制检查）、`e2e-element-coverage-tree`（有原型时树落在 prototype/ 目录 → 有原型时树落在变更根目录）、`kflow-runtime-isolation`（prototype/ 目录不包含运行时文件 → 产品级原型目录不包含运行时文件、BROWSER_CLEANUP 不依赖 prototype/ 目录 → BROWSER_CLEANUP 不依赖产品级原型目录）、`design-change-record`（prototype/index.md 由原型设计阶段创建 → 产品级原型清单由原型设计阶段创建）。做法：主规格与对应 delta 的 scenario 标题**配对**改为新措辞，并移除 delta 中的非规范性说明。验证：`openspec validate sync-legacy-prototype-specs` 无 ERROR，且 `grep -rn "^#### Scenario:.*prototype/" openspec/specs/` 无命中（阶段名用法除外）
- [x] 4.2 收口 `## Purpose` 中内嵌旧路径的 4 处：`conditional-product-refs`（`prototype/index.md`）、`kflow-runtime-isolation`（`prototype/`）、`prototype-design-prompt-template`（`prototype/design-prompt.md`）、`design-change-record`（`三个设计目录 index.md`，核验中补入）。做法：直接编辑主规格的 Purpose（delta 不承载 Purpose）。验证：`openspec validate --specs` 无 ERROR，且 `grep -rn "^定义.*prototype/" openspec/specs/` 仅余阶段名用法、负向断言与本变更范围外的 capability

## 5. 实现与设计文档核对

- [x] 5.1 【设计文档 → SKILL.md 同步】逐条核对 `skills/` 实现是否满足改写后的 20 个 capability 规格的 SHALL 断言，产出核对结论。重点预判项：`phase-artifact-verification` 的 D3.1 要求检查变更级 `element-coverage-tree.md`，而 `skills/kflow-verify/SKILL.md` 当前只列出 `manifest.md` 与 `prototype-changes.md`。验证：产出核对结论清单（一致项摘要 + 不一致项逐条 `文件:行号`）——结论见下方"5.1 核对结论"
- [x] 5.2 【设计文档 → SKILL.md 同步】按 5.1 的结论补齐实现缺口——仅在与规格一致的方向上修改，且仅限"设计文档 → SKILL.md 同步"性质的措辞/清单对齐。验证：改动后 `skills/` 无旧原型路径残留，且每处改动可对应到某条规格的 SHALL 断言
- [x] 5.3 同步 `docs/designs/` 下与这 20 个 capability 对应的设计文档中残留的旧口径（含 `conditional-product-refs` 的入口表述、`design-change-record` 的修订记录载体说明、`e2e-element-coverage-tree` 的落点表、`kflow-runtime-isolation` 的目录纯净性表述）。验证：`grep -rn "prototype/index\.\|prototype\.pen\|变更级 prototype/" docs/designs/` 无命中（负向断言与历史记录除外）

### 5.1 核对结论

一致（15 项）：`conditional-product-refs`、`subchange-input-source`、`phase-file-reload`、`phase-boundary-enforcement`、`resume-product-gate`、`design-level-restructure`、`kflow-runtime-isolation`、`prototype-offline-constraint`、`e2e-element-coverage-tree`、`playwright-cli-e2e-workflow`、`prototype-prompt-optimization`、`prototype-design-prompt-template`、`stage-doc-templates`、`user-review-gate`、`design-change-record`/`change-rollback` 的原型路径与修订目标口径。

不一致并由 5.2 补齐（5 处，均为措辞/清单对齐）：

| # | 落点 | 差异 | 补齐内容 |
|---|------|------|---------|
| 1 | `skills/kflow-verify/SKILL.md:77` | D3.1 前端子变更检查项缺 `element-coverage-tree.md` | 补为 `docs/designs/prototypes/manifest.md、变更级 prototype-changes.md、变更级 element-coverage-tree.md、detailed-design.md` |
| 2 | `skills/kflow-bug-triage/SKILL.md:148` | `element-coverage-tree.md` 未标注「变更级」 | 补「变更级」限定 |
| 3 | `skills/kflow-bug-triage/SKILL.md:151` | L2 检查项未体现以变更级 `prototype-changes.md` 界定本变更涉及页面 | 补范围界定句 |
| 4 | `skills/kflow-code/SKILL.md:64`、`skills/kflow-plan/SKILL.md:376` | 前端输入白名单缺变更级 `element-coverage-tree.md` | 补入白名单 |
| 5 | `skills/kflow-guide/SKILL.md:135,140,435,441` | 修订目标仍写作 `prototype` 别名与「目标设计目录 index.md」，且缺修订目标枚举 | 改为产品级 `docs/designs/prototypes/`、设计产物载体修订记录、并补修订目标枚举与 REVISION 模式约束 |

范围外残留（未修改，另行决策）：`skills/kflow-verify/SKILL.md` 缺 D3.2 输出越界检测（规格要求 verify D3 新增 D3.2，实现仅在 `kflow-code-review` 存在）；无阶段 Skill 在 POST_HOOK 回填「设计修订同步追踪」本阶段列；`skills/kflow-code-review/SKILL.md:147` 硬编码颜色阈值 `≥ 3 次` 与规格 `≥ 5 次` 不一致。三者均超出 5.2「措辞/清单对齐」的授权边界。

## 6. 集成校验

- [x] 6.1 运行 `openspec validate sync-legacy-prototype-specs` 确认无 ERROR。验证：输出含 `is valid` 且无 `[ERROR]`
- [x] 6.2 全库旧口径残留扫描：以本变更 20 个 capability 为范围，确认 `openspec/specs/` 中不再有已废弃的变更级 `prototype/` 路径、`prototype.pen`。验证：`grep -rn "prototype/index\.\|prototype\.pen\|prototype/design-prompt\|prototype/style-decision" openspec/specs/` 无命中（负向断言与阶段名用法除外）——delta 应用前主规格中仍存旧口径（由 delta 归档时替换），故以临时副本模拟 `openspec archive` 后复扫确认：残留仅为 4 处负向断言（`prototype-change-tracking:30`、`prototype-design-index:5,16`、`prototype-manifest:52`）
- [x] 6.3 核对本变更与 `redesign-prototype-stage` 的目标规格文件集合无交集，避免两变更归档时相互覆盖。验证：两变更 `specs/` 目录名列表取交集为空（`redesign-prototype-stage` 17 个、本变更 20 个，交集 0；前者已归档于 `openspec/changes/archive/2026-09-29-redesign-prototype-stage`）
