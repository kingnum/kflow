# Tasks

## 1. 主规格结构修复（归档前置）

openspec 主规格存在三类结构缺陷，导致需求对解析器不可见、归档会被拒绝：delta 分节头残留（首行型 / 中部型）、缺少 `# <name> Specification` 一级标题、缺少 `## Purpose`。本组为纯结构修复，不改变任何需求语义。

> **本组已完成**（89 个主规格已修复，`openspec validate --all` 132 通过 / 0 失败，`requirementCount` 为 0 的规格数为 0）。

- [x] 1.1 修复 `openspec/specs/` 下 33 个「首行即 delta 分节头」的主规格：补 `# <name> Specification` 一级标题与 `## Purpose`，把首行 delta 头改为 `## Requirements`。验证：对每个文件运行 `openspec show "<name>" --type spec --json --no-scenarios`，返回非空 requirements 数组
- [x] 1.2 修复 19 个「中部混入 delta 分节头」的主规格：删除或归并 `## ADDED by` / `## MODIFIED by` / `## Modified by` 分节头，`## REMOVED Requirements` 整节删除，同名需求用后来者替换。验证：同 1.1 的命令，且 `openspec show` 返回的需求数等于文件中实际存在的 `### Requirement:` 数
- [x] 1.3 补齐 9 个 Purpose 占位符（`architecture-auto-assessment`、`code-review-skill`、`design-complexity-gate`、`design-doc-directory`、`doc-consistency`、`integration-test-skill`、`plan-self-review`、`prototype-review-artifacts`、`resume-plan-mode-bypass`）。验证：`grep -rn "^TBD" openspec/specs/` 无输出
- [x] 1.4 修复 27 个缺少 `# <name> Specification` 一级标题和/或 `## Purpose` 的主规格，使其可被解析器解析。验证：`openspec show "<name>" --type spec --json --no-scenarios` 对每个返回非空 requirements
- [x] 1.5 合并 `devflow-archive` 中被 `## MODIFIED by` 取代的旧版需求、清理 `playwright-cli-e2e-workflow` 需求标题中的 `（MODIFIED）` 残留、合并 `change-rollback` 与 `phase-file-reload` 的同名重复需求。验证：`grep -rn "^### Requirement:.*（\(ADDED\|MODIFIED\|REMOVED\)）" openspec/specs/` 无输出
- [x] 1.6 全库规格可达性与校验。验证：`openspec list --specs --json` 中 `requirementCount` 为 0 的规格数为 0；`openspec validate --all` 无失败项

## 2. 目录结构与模板定义（产品级原型）

- [x] 2.1 更新 `docs/designs/core-mechanisms/02-directory-structure.md`：把 `docs/designs/prototypes/` 补全为完整产品级原型目录（`index.html`、`manifest.md`、`design-tokens.css`、`design-system/MASTER.md`、`screens/`、`components/`、`assets/`）；变更级移除 `prototype/` 目录描述，改为 `prototype-changes.md`、`prototype-backup/`、`prototype-plan/`、`element-coverage-tree.md`；更新 2.2 命名规范表。验证：文档中不再把变更级 `prototype/` 描述为产物目录
- [x] 2.2 更新 `docs/designs/core-mechanisms/09-phase-hooks.md` 的阶段重载清单，把 `prototype/index.md` 等旧路径改为产品级 `docs/designs/prototypes/manifest.md` + 变更级 `prototype-changes.md`。验证：清单中不再出现变更级 `prototype/` 相对路径
- [x] 2.3 重定义原型模板：更新 `docs/designs/templates/changes/{change}/prototype/index.md`、`design-prompt.md`、`style-decision.md`，新增 `prototype-changes.md` 模板（含 `| 文件路径 | 类型 | 改动前哈希 | 说明 |` 表头），产物路径改指向 `prototype-plan/`。验证：模板文件存在且无 `prototype/index.md` 旧定位描述
- [x] 2.4 更新 `docs/designs/templates/index.md`、`docs/designs/index.md`、`README.md` 中的目录树与产物清单。验证：三处均出现 `docs/designs/prototypes/`，且不再出现 `docs/prototype/`

## 3. kflow-prototype-design 设计文档改写

- [x] 3.1 在 `docs/designs/skills/kflow-prototype-design.md` 改写 TOOLCHAIN 步骤：默认复用 `docs/toolchain.md`（含变更级覆盖 `docs/changes/{change}/toolchain.md`）已锁定的工具链且不询问；仅三种例外重新选择（无锁定、引用 Skill 不可用、用户显式要求更换）；SCAN 仅在需要重新选择时执行。验证：文档中 TOOLCHAIN 步骤含上述四条分支与例外条件
- [x] 3.2 在同一文档新增 BUILD 步骤定义：四项静态检查（CDN 扫描、交叉引用完整性、必检产物存在、清单与磁盘一致）、零子代理约束、不通过则修复重跑。验证：文档中 BUILD 定义含全部四项检查
- [x] 3.3 在同一文档新增审查方式选择定义：BUILD 通过后 AskUserQuestion 二选一（人工审查 / 子代理自动审查验证），并说明两条路径的后续步骤差异。验证：文档含两条路径的分支描述
- [x] 3.4 在同一文档把 VERIFY 的 15 轮子代理验证与 SELFREV 改为仅在「子代理自动审查验证」路径下执行；「人工审查」路径下完全跳过。验证：文档中 VERIFY/SELFREV 均带前置条件，且无「无条件强制」表述
- [x] 3.5 在同一文档改写 DESIGN 与 COMPLETE：产物直写产品级 `docs/designs/prototypes/`；变更级维护 `prototype-changes.md`（改动前哈希）、`prototype-backup/`；新增并发写入检测与三选项用户裁决；`element-coverage-tree.md` 落变更级。验证：文档含哈希比对流程与裁决选项
- [x] 3.6 在同一文档改写修订模式：入口 A 检测对象由 `prototype/index.html` 改为 `prototype-changes.md`，加载的已有约束路径改为 `prototype-plan/design-prompt.md`。验证：文档中不再以 `prototype/index.html` 作为修订模式判定依据
- [x] 3.7 更新同一文档的架构模型图、执行流程图、输出产物表、输入要求表、阶段边界约束，使全篇路径与产物口径一致。验证：全篇不再出现 `docs/prototype/` 与变更级 `prototype/` 产物路径

## 4. 归档与下游阶段口径统一

- [x] 4.1 改写 `docs/designs/skills/kflow-archive.md` 的设计合并流程：删除「原型设计不合并」与规格矛盾的表述，改为「原型在原型设计阶段已直写产品级，归档时仅登记改动到 `docs/designs/prototypes/manifest.md`」。验证：文档中归档流程含原型改动登记步骤，无「不合并」表述
- [x] 4.2 更新 `skills/kflow-archive/SKILL.md` 与 `skills/kflow-archive/references/archive-rules.md` 的设计合并流程，与 4.1 口径一致。验证：两文件均含登记步骤、无「原型设计（.html 文件）不合并到产品级」语句
- [x] 4.3 更新下游设计文档的原型路径引用：`docs/designs/skills/` 下 `kflow-explore.md`、`kflow-design.md`、`kflow-code.md`、`kflow-code-review.md`、`kflow-e2e-test.md`、`kflow-verify.md`、`kflow-plan.md`。验证：各文档中除负向断言外不再出现变更级 `prototype/` 作为输入路径
- [x] 4.4 更新 `docs/designs/skills/index.md` 中 `kflow-prototype-design` 一行与阶段依赖图。验证：描述与改写后的阶段行为一致

## 5. 设计文档 → SKILL.md 同步

- [x] 5.1 【设计文档 → SKILL.md 同步】重写 `skills/kflow-prototype-design/SKILL.md`：步骤流改为 BUILD → 审查方式选择 → REVIEW，TOOLCHAIN 默认复用，DESIGN 直写产品级原型。验证：SKILL.md 含 BUILD 与审查方式选择步骤，且无「SHALL 完成全部 5 轮」的无条件表述
- [x] 5.2 【设计文档 → SKILL.md 同步】更新 `skills/kflow-prototype-design/references/` 下 `gates.md`、`hooks.md`、`self-review.md`、`state-values.md`：门控与自审规则随审查方式条件化，状态值补充审查方式记录字段。验证：四个引用文件与 SKILL.md 的步骤编号、门控条件一致
- [x] 5.3 【设计文档 → SKILL.md 同步】更新下游 7 个 SKILL.md 的原型路径引用：`skills/kflow-plan/SKILL.md`、`kflow-code/SKILL.md`、`kflow-code-review/SKILL.md`、`kflow-e2e-test/SKILL.md`、`kflow-verify/SKILL.md`、`kflow-design/SKILL.md`、`kflow-explore/SKILL.md`。验证：`grep -rn "prototype/index.md" skills/` 仅命中负向断言或无命中

## 6. 集成校验

- [x] 6.1 运行 `openspec validate redesign-prototype-stage` 确认无 ERROR。验证：输出含 `is valid` 且无 `[ERROR]`
- [x] 6.2 全仓旧路径残留扫描。验证：`grep -rn "docs/prototype/" docs/ skills/ openspec/specs/ README.md` 无命中（`openspec/changes/archive/` 下的历史记录除外）
- [x] 6.3 运行 `scripts/sync-references.sh` 一致性校验。验证：脚本退出码为 0
- [x] 6.4 规格与实现双向核对：逐个比对 `openspec/specs/` 与本变更各 delta 描述的行为，与 `skills/kflow-prototype-design/SKILL.md` 实际步骤是否一致。验证：产出核对结论，列出所有不一致项并修正

> **6.4 核对结论**（核对范围：17 个 capability 主规格 ↔ `skills/kflow-prototype-design/SKILL.md` + 4 个 references + 设计文档 + 下游 8 个 SKILL.md 及其 references + 模板）
>
> **主干机制核对一致**：直写模型、BUILD 四项门控、审查方式二选一、TOOLCHAIN 默认复用、改动追踪与哈希并发检测、写权限归属、归档只登记不合并、下游通过清单动态取路径。
>
> **本次修正的不一致项（10 项）**：
> 1. 两个新建主规格末行被生成脚本截断（`prototype-build-gate`、`prototype-change-tracking`）→ 已补回缺失的 3 行 ×2
> 2. `SKILL.md` 步骤编号比设计文档与主规格多 1 格（PRE_HOOK 计为步骤 1）→ 已统一为 CHECK=1、PRE_HOOK=1.5、DESIGN=6、BUILD=7、审查方式选择=8、VERIFY=9、SELFREV=10、REVIEW=11、COMPLETE=12、POST_HOOK=13
> 3. `SKILL.md` 缺 6 处规格/设计文档已定义内容（STYLE 的「适用/不适用场景」与两个额外选项、`design-prompt.md` 的"已执行"终态、GENERATE 结果摘要、INPUT 的 `components/` 与 `MASTER.md`、首次原型"无已有设计令牌"标注、`available-skills.json`）→ 已补齐
> 4. 设计文档 INPUT 缺 `components/` 与 `design-system/MASTER.md` → 已补齐
> 5. `change-status.md` 模板缺承载审查方式的字段 → 已新增「原型设计阶段审查方式」段落
> 6. `03-status-and-tasks.md` 原型设计阶段任务清单仍为旧模型（含已废弃产物 `prototype/index.md`）→ 已按新流程重写
> 7. `html-prototype-workflow`「huashu-design 子代理委托调用」硬绑定 huashu-design，与「有效工具链」模型矛盾 → 已改写为「原型子代理委托调用」（delta 与主规格同步）
> 8. `prototype-revision-mode`「修订模式下底层 skill 可替换」要求硬检测 huashu-design → 已改写为「修订模式复用有效工具链」（delta 与主规格同步）
> 9. `prototype-manifest` 的 Purpose 与 Playwright 场景名残留旧路径 → 已更新
> 10. `design-review-tiering` 的弹性轮次规格与各 skill `references/gates.md` 硬编码「10 个 design 自审报告」冲突、`references/repetition.md` 硬编码「SELFREV（10 轮自审）」→ 已改为按自审目标轮次判定，并同步全部副本
>
> **本次裁决并修正的规格冲突（1 项）**：`prototype-design-system-output` 要求下游加载 `design-system/MASTER.md`，与 `prototype-manifest` 的「下游仅消费 entry/page/tokens/shared」冲突。裁决：以 manifest 为准，MASTER.md 不供下游消费；已同步修改 delta 与主规格的场景。
>
> **不在本次范围、需另开变更处理**：13 个 capability 的主规格仍引用变更级 `prototype/` 旧路径 —— `subchange-input-source`(14)、`phase-file-reload`(11)、`e2e-element-coverage-tree`(11)、`frontend-implementation-subchange`(7)、`prototype-design-prompt-template`(4)、`conditional-product-refs`(4)、`phase-boundary-enforcement`(3)、`design-change-record`(3)、`phase-artifact-verification`(2)、`resume-product-gate`(1)、`playwright-cli-e2e-workflow`(1)、`kflow-runtime-isolation`(1)、`bug-triage-skill`(1)（括号内为旧路径引用处数）。这些 capability 未列入本提案的 Capabilities 段。
