# Tasks

> **范围说明**：本任务清单仅含变更的实际交付工作。归档（`/opsx:archive`）、Git commit、版本自增、打包等元工作流任务由 CLAUDE.md 的「归档后规则」自动驱动，不列入本清单。

## 1. 机制规范层（波次 1：先确立权威定义）

- [x] 1.1 改写 `docs/designs/core-mechanisms/03-status-and-tasks.md` §3.1.1 档位判定：枚举改为 `{轻量, 标准}`、阈值改为 `<=3 / >3`、缺省回退改为 `标准`、新增历史 `完整` 取值的读取侧归并规则；验证方式：该文件内检索「完整」不再出现在档位枚举、阈值或缺省回退表述中

- [x] 1.2 改写 `docs/designs/core-mechanisms/04-gates-and-transitions.md` 的档位分支（6 处）：进入计划门控由三分支降为两分支、代码审查门控表的三档行合并为两档、门控对历史 `完整` 取值的判读按 `标准` 处理；验证方式：该文件内检索「完整档」「完整模式」零命中

- [x] 1.3 同步 `docs/designs/core-mechanisms/05-execution-services.md` 与 `07-agent-model.md` 中残留的档位表述；验证方式：两个文件内检索「完整档」「完整模式」零命中

- [x] 1.4 更新 `docs/designs/overview.md` 与 `docs/designs/index.md` 的核心设计决策表：档位行改为二档（轻量 / 标准）并注明「完整档已合并入标准档」；验证方式：两个文件内检索「完整档」「完整模式」零命中，且档位决策行描述与 `03-status-and-tasks.md` §3.1.1 一致

- [x] 1.5 直接改写 main spec 的 `## Purpose` 段：`openspec/specs/change-tier-classification/spec.md`、`design-review-tiering/spec.md`、`lightweight-flow-trimming/spec.md` 三处 Purpose 含三档表述（delta 不承载 Purpose）；验证方式：三份 main spec 的 Purpose 段仅出现 `轻量` 与 `标准` 两个档位取值

- [x] 1.6 运行 `python scripts/validate-frontmatter.py` 与 `bash scripts/sync-references.sh`，确认机制规范层改动未引入 front matter 或引用一致性问题；验证方式：两条命令均以退出码 0 结束

## 2. 状态字段层（波次 2：字段定义先于消费点）

- [x] 2.1 更新 10 份 `skills/kflow-*/references/state-values.md` 的 §4 变更档位字段：枚举行改为 `{轻量, 标准}`、阈值行改为 `<=3 / >3`、缺省回退改为 `标准`、新增历史 `完整` 归并规则；同步修正第 69 行残留的「或变更类型为 `产品需求`」（0.24.0 已删除该硬映射）；验证方式：10 个文件内检索「或变更类型为 `产品需求`」零命中，且 §4 表格仅含两行档位取值

- [x] 2.2 更新 10 份 `state-values.md` 的「档位驱动的行为差异」表：删除完整档列，代码审查形态与产出深度行按两档收敛（删除 `完整` 档的评分报告深度行）；验证方式：10 个文件的行为差异表恰含 `轻量` 与 `标准` 两列，且不再出现评分深度要求

- [x] 2.3 更新 10 份 `state-values.md` §5 阶段适用性声明的档位前提表述：非轻量档表述由「`标准` 与 `完整` 档 SHALL NOT 生成」改为「`标准` 档 SHALL NOT 生成」；验证方式：10 个文件内检索「标准与完整」零命中

- [x] 2.4 更新 `skills/kflow-archive/references/archive-rules.md` 的裁剪适用范围表述（仅轻量档）与其版本记录条目；验证方式：该文件内检索「完整档」零命中，且归档条件表述与 `lightweight-flow-trimming` delta 一致

## 3. 门控层（波次 2）

- [x] 3.1 更新 10 份 `skills/kflow-*/references/gates.md` 的「变更档位字段的透传与校验」：枚举校验改为 `{轻量, 标准}`、缺省回退改为 `标准`、新增历史 `完整` 取值归并后判读；验证方式：10 个文件内检索 `{轻量, 标准, 完整}` 与「按 `完整` 档处理」零命中

- [x] 3.2 更新 10 份 `gates.md` 的进入计划门控分支：由「轻量 / 标准 / 完整」三分支改为「轻量 / 标准」两分支，标准分支检查两份视角报告与 synthesis.md；验证方式：10 个文件内检索「完整档（完整模式）」零命中，且门控条目恰含两个档位分支

- [x] 3.3 更新 10 份 `gates.md` 的代码审查门控表：删除 `完整` 行，`标准` 行沿用两视角判定条件；验证方式：10 个门控表的档位行数为 2，且轻量档判定条件（高严重度 = 0 且中严重度 < 3）不变

- [x] 3.4 更新 10 份 `gates.md` 中归档门控与覆盖率检查的档位分支（裁剪判定仅轻量档）；验证方式：10 个文件内检索「因轻量档裁剪」的表述仍存在且未被误改为无条件裁剪

- [x] 3.5 核查 13 份 `skills/kflow-*/references/hooks.md` 的档位开关分支，凡枚举三档者收敛为两档；验证方式：13 个文件内检索「完整」在档位上下文中零命中

## 4. 审查与执行层（波次 3）

- [x] 4.1 更新 8 份 `skills/kflow-*/references/repetition.md`：审查形态表按两档收敛（删除四视角行）、`state-values` 引用同步、删除完整档评分报告深度章节（`### 14.5 完整档评分的报告深度`）；验证方式：8 个文件内检索「完整档」零命中，且轻量 / 标准两档的审查形态与终止模型表述未变

- [x] 4.2 更新 `skills/kflow-design/SKILL.md` 与 `skills/kflow-design/references/review-content.md`：档位判定表、审查形态表（删除完整模式四视角）、审查门控产物清单按两档收敛；验证方式：两个文件内检索「四视角并行」在档位上下文中零命中，且检查项清单未被删减

- [x] 4.3 更新 3 份 `skills/kflow-{explore,design,prototype-design}/references/self-review.md` 的档位表：删除完整档的评分要求行，保留轻量 / 标准的报告深度差异；验证方式：3 个文件内检索「完整」在档位上下文中零命中

- [x] 4.4 更新 `skills/kflow-explore/SKILL.md` 的 TIER 步骤与 `skills/kflow-explore/references/self-review-dimensions.md`：初判映射规则改为「功能点 > 2 即 `标准`」、枚举与缺省回退同步；验证方式：两个文件内检索「完整」在档位上下文中零命中，且初判规则表仅产出 `轻量` / `标准` 两值

- [x] 4.5 更新 `skills/kflow-plan/SKILL.md`、`skills/kflow-plan/references/gates.md` 的档位表述；验证方式：两个文件内检索「完整档」「完整模式」零命中

- [x] 4.6 更新 `skills/kflow-code-review/SKILL.md` 与 `skills/kflow-code-review/references/gates.md`：审查适用档位由「`标准` 或 `完整`」改为「`标准`」；验证方式：两个文件内检索「或 `完整`」零命中，且轻量档单 Agent 路径不变

- [x] 4.7 核查其余阶段 SKILL.md（`kflow-{code,api-test,e2e-test,integration-test,audit,archive,resume,status,guide}`）中的档位表述并收敛为两档；验证方式：各文件内检索「完整」在档位上下文中零命中

## 5. 设计规格与文档层（波次 4）

- [x] 5.1 更新 `docs/designs/skills/kflow-{explore,design,plan,code,code-review,prototype-design,guide,archive,bug-fix}.md` 的档位相关章节（含 `kflow-design.md` 14 处、`kflow-code-review.md` 11 处）；验证方式：9 个文件内检索「完整档」「完整模式」零命中

- [x] 5.2 更新 `docs/designs/templates/index.md`、`templates/changes/{change}/review-reports/*.md`（5 份视角报告模板）、`templates/subchanges/{subchange}/code-review.md`：四视角产物模板的档位说明收敛为两档；验证方式：模板目录内检索「完整档」「完整模式」零命中，且 `review-synthesis.md` 的批次表仍支持两视角与单一综合报告两种形态

- [x] 5.3 更新 `docs/designs/examples/audit-report.md` 的档位示例取值；验证方式：该文件内检索「完整」在档位上下文中零命中

- [x] 5.4 更新 `README.md`：档位章节（枚举表、判定规则、行为差异表、缺省回退）、Skills 清单中的档位列、FAQ 条目收敛为两档；验证方式：`README.md` 内检索「完整档」「完整模式」零命中

- [x] 5.5 在 `README.md` 补充本次变更的版本更新说明条目，说明三档收敛为二档、四视角审查废除、历史 `完整` 取值归并三项；验证方式：README 中该条目存在且含上述三项要点

## 6. 集成验证与一致性收口

- [x] 6.1 全仓检索一致性收口：`skills/`、`docs/designs/`、`README.md` 中检索「完整档」「完整模式」「或变更类型为 `产品需求`」「轻量档轮次」零命中（`openspec/changes/archive/` 与历史变更记录文件除外）；验证方式：上述检索命令返回零命中并留档检索输出

- [x] 6.2 档位读取点核对：检索「变更档位」的全部读取位置（各 `gates.md` 的入口门控、`state-values.md` 字段定义、子代理 prompt 透传、审计的档位判读），确认每处均按 `{轻量, 标准}` 校验并含历史 `完整` 归并；验证方式：读取点清单逐条对照，无遗漏且无按 `完整` 档分支的残留

- [x] 6.3 端到端流程走查：以「标准档功能需求」与「轻量档功能缺陷」两个样例，逐阶段核对阶段流转与门控可跑通（含轻量档裁剪的适用性声明与标准档的两视角设计审查）；验证方式：走查记录中两个样例的审查形态、门控判据、产物清单均可对应到本次变更后的规范

- [x] 6.4 历史兼容走查：构造含 `变更档位 = 完整` 的历史 `.status.md` 样例，核对门控、审计与流程概览均按 `标准` 档判读且不阻塞；验证方式：走查记录中该样例在设计审查门控、审计报告形态、流程概览三处均按两视角路径通过

- [x] 6.5 运行 `bash scripts/sync-references.sh` 与 `python scripts/validate-frontmatter.py`，确认全部 skill 自包含且 front matter 合法；验证方式：两条命令以退出码 0 结束且无告警

- [x] 6.6 运行 `openspec validate merge-standard-and-full-tier --strict`，确认 delta specs 与实现后的规范层一致；验证方式：命令以退出码 0 结束

## 7. 设计文档 → SKILL.md 同步

- [x] 7.1 逐项核对 `docs/designs/skills/kflow-*.md` 与 `skills/kflow-*/SKILL.md` 的一致性：本次变更涉及的全部阶段（explore / design / prototype-design / plan / code / code-review / api-test / e2e-test / integration-test / audit / archive / guide）的设计规格与可运行 Skill 内容对应无遗漏；验证方式：逐阶段列出档位相关检查项对照表并确认无未同步项

- [x] 7.2 检查全部改动后 skill 的自包含性：各 skill 的辅助规则（钩子、门控、重复制规范）位于自身 `references/` 子目录，安装后零外部依赖；验证方式：`scripts/sync-references.sh` 无跨 skill 引用告警

- [x] 7.3 检查全部 SKILL.md 的 `version` 字段与仓库根 `VERSION` 一致（`scripts/sync-version.sh` 执行的准备条件）；验证方式：逐文件比对 version 字段值
