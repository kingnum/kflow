# Tasks

> **范围说明**：本任务清单仅含变更的实际交付工作。归档（`/opsx:archive`）、Git commit、版本自增、打包等元工作流任务由 CLAUDE.md 的「归档后规则」自动驱动，不列入本清单。

## 1. 机制规范层（波次 1：先确立权威定义）

- [x] 1.1 重写 `docs/designs/core-mechanisms/07-agent-model.md` §16 自审机制章节：删除见证轮四判据、不收敛判定、轮间摘要注入、累积未复核修复清单；改为「主 Agent 签署自证（零子代理）→ 单轮独立子代理验证 → 主 Agent 统一修复」；验证子代理打假契约（先独立遍历后读清单、只报告不修改产物）；验证方式：全文检索该文件不再出现「见证轮」「不收敛」「收敛驱动」等已废除术语

- [x] 1.2 更新 `docs/designs/core-mechanisms/07-agent-model.md` §15 子代理执行模型：区分单轮类阶段（测试三阶段）与重复制类阶段（编码/代码审查/缺陷修复）的执行模型；验证方式：§15 中测试三阶段不再表述为重复制循环

- [x] 1.3 更新 `docs/designs/core-mechanisms/03-status-and-tasks.md` §3.1.1 档位判定：删除「产品需求 → 完整档」硬映射，产品需求按功能点数比照功能需求分档；终止结果字段取值改为 `验证通过` / `验证发现问题({N})`；验证方式：该文件内检索「产品需求」不再出现无条件完整档表述

- [x] 1.4 在 `docs/designs/overview.md` 与 `docs/designs/index.md` 的核心设计决策表中替换自审与审计相关行：自审由「收敛驱动自审」改为「单轮验证 + 签署清单」；审计由「四维度加权评分」改为「记账员职责」；新增「阶段耗时遥测」决策行；验证方式：两个文件内检索「收敛驱动」不再出现在自审/审计相关行

- [x] 1.5 运行 `python scripts/validate-frontmatter.py` 与 `bash scripts/sync-references.sh`，确认机制规范层改动未引入 front matter 或引用一致性问题；验证方式：两条命令均以退出码 0 结束

## 2. 设计类 Skill 与 Plan Skill（波次 2）

- [x] 2.1 全量重写 `skills/kflow-explore/references/self-review.md`（v2.0.0 → v3.0.0）：单轮验证流程、签署清单 4 维度（完整性/闭环性/必要性/清晰性）与证据锚点要求、验证子代理打假契约、验证报告结构、终止结果写入；保证 skill 自包含（不引用外部重复制规范文件）；验证方式：该文件全文检索不再出现「见证轮」「不收敛」「轮数上限」

- [x] 2.2 全量重写 `skills/kflow-design/references/self-review.md`（v2.0.0 → v3.0.0）：同上，维度为一致性/完备性/可行性/可测性；保留「真正的独立验证留给交叉审查」的设计意图表述；验证方式：同上

- [x] 2.3 全量重写 `skills/kflow-prototype-design/references/self-review.md`（v2.0.0 → v3.0.0）：单轮验证 + 原型 VERIFY 三环节合并为单轮单报告、合并报告四分区结构（导航/Playwright/UX/对比度）与全量遍历证明要求；BUILD 四项静态门控保留为零子代理；验证方式：该文件内「nav-check」「playwright-check」「ux-check」「contrast-check」四个子目录路径均已替换为 `verify-report.md`

- [x] 2.4 更新 `skills/kflow-explore/SKILL.md`：SELFREV 步骤改为单轮验证、PROTO_GATE 步骤保留、TIER 步骤删除「产品需求 → 完整」映射；验证方式：SKILL.md 流程框图中 SELFREV 不再标注收敛循环

- [x] 2.5 更新 `skills/kflow-design/SKILL.md`：SELFREV 步骤改为单轮验证、TIER_RECHECK 步骤映射规则同步、REVIEW 步骤不变；验证方式：SKILL.md 内 SELFREV 章节不再出现见证轮判据

- [x] 2.6 更新 `skills/kflow-prototype-design/SKILL.md`：VERIFY 步骤由三个收敛循环改为单轮合并验证，报告路径改为 `self-reviews/prototype/verify-report.md`；验证方式：SKILL.md 内不再出现三个 check 子目录路径

- [x] 2.7 更新 `skills/kflow-plan/SKILL.md` 与 `skills/kflow-plan/references/repetition.md`：SELFREV 步骤改为单轮验证（4 个定制维度保留，签署自证零子代理）；验证方式：`repetition.md` 内 SELFREV 相关章节不再出现收敛循环表述

- [x] 2.8 更新 `skills/kflow-explore/references/self-review-dimensions.md` 与 `skills/kflow-explore/references/clarify-convergence.md`：维度说明与收敛门表述对齐单轮验证口径（注意：`clarify-convergence.md` 的需求澄清收敛门是**独立机制**，不在本次改造范围，仅需确认其术语不与自审单轮化冲突）；验证方式：`self-review-dimensions.md` 内不再出现见证轮表述

- [x] 2.9 更新 `skills/kflow-status/SKILL.md` 与 `skills/kflow-resume/SKILL.md`：读取终止结果字段时按新取值与历史归并规则处理；验证方式：两个 SKILL.md 内终止结果字段读取逻辑覆盖 `验证通过` / `验证发现问题({N})` / 历史 `收敛` 三类取值

## 3. 执行类 Skill（测试单轮化）（波次 2）

- [x] 3.1 更新 `skills/kflow-api-test/references/repetition.md` 与 `SKILL.md`：重复制循环改为单轮全面执行 + 定向重验（仅重跑失败用例），删除轮间摘要与见证轮判据；保留审查范围冻结；验证方式：该文件内不再出现「见证轮」「轮间摘要」

- [x] 3.2 更新 `skills/kflow-e2e-test/references/repetition.md` 与 `SKILL.md`：同 3.1；验证方式：同上

- [x] 3.3 更新 `skills/kflow-integration-test/references/repetition.md` 与 `SKILL.md`：同 3.1；验证方式：同上

- [x] 3.4 确认 `skills/kflow-code/references/repetition.md`、`skills/kflow-code-review/references/repetition.md`、`skills/kflow-bug-fix/references/repetition.md` 的重复制循环**保持不变**，仅同步终止结果取值与轮次验收判据口径（不再以见证轮为通过前提）；验证方式：三个文件仍保留重复制遍历指令与轮间摘要，且验收判据改为「执行报告完整 + 产物齐全 + 覆盖率达标」

## 4. 审计 Skill（波次 2）

- [x] 4.1 更新 `skills/kflow-audit/SKILL.md`：四维度加权评分改为四项记账职责（门控校验/覆盖率与产物校验/耗时汇总/阻塞兜底），删除评分表与加权总分，保留阻塞级问题拦截权与归档门控地位；验证方式：SKILL.md 内不再出现权重百分比（45%/30%/15%/10%）

- [x] 4.2 更新 `skills/kflow-audit/references/` 下全部分支文件（含 gates.md、hooks.md、state-values.md 等）与审计相关的检查项目录：删除四维度详细检查项，改为记账职责实施细则与阻塞级问题清单；验证方式：`references/` 目录内检索「四维度加权」无结果

## 5. 模板层（波次 3：签署清单与计时区的载体）

- [x] 5.1 在 `docs/designs/templates/changes/{change}/functional-designs/part-NN.md` 末尾追加「完成前签署」区：4 维度表（维度 / 自证结论 / 证据锚点），并同步更新 `functional-designs/index.md` 的产物结构说明；验证方式：模板文件中签署区含三列且证据锚点列有填写要求说明

- [x] 5.2 在 `docs/designs/templates/changes/{change}/detailed-design.md` 的每个功能点设计块末尾追加签署区；验证方式：模板中签署区出现在功能点设计块结构内

- [x] 5.3 在 `docs/designs/templates/changes/{change}/api-tests/part-NN.md` 与 `e2e-tests/part-NN.md` 追加签署区；验证方式：两个模板文件均含 4 维度签署表

- [x] 5.4 在 `docs/designs/templates/subchanges/{subchange}/subchange-tasks.md` 追加签署区（计划阶段 4 维度：任务覆盖完整性/DoD 正确性/子变更类型标注/任务粒度）；验证方式：模板含签署区且维度名与 `plan-self-review` 一致

- [x] 5.5 更新 `docs/designs/templates/changes/{change}/change-status.md`：新增「阶段耗时与轮次统计」区（阶段/开始/结束/耗时/子代理轮次/执行方式）与「阶段内事件计时」区（事件/开始/结束/耗时），并说明自动标注触发条件；验证方式：模板含两个新区，且终止结果字段取值说明更新

- [x] 5.6 更新 `docs/designs/templates/changes/{change}/audit-report.md`：删除四维度评分表与加权总分形态，改为记账记录形态（四项职责结论 + 耗时效率摘要 + 分级问题清单 + 改进建议）；验证方式：模板内不再出现评分表结构

- [x] 5.7 更新 `docs/designs/templates/skills/SKILL-template.md`：如含自审/审查轮次相关占位则同步单轮口径；验证方式：模板内不再出现轮数上限相关占位

## 6. 设计文档同步与示例（波次 4）

- [x] 6.1 更新 `docs/designs/skills/kflow-{explore,design,prototype-design,plan}.md`：同步单轮验证、签署清单、原型合并验证、档位映射四处改动；验证方式：四个文件内不再出现见证轮四判据

- [x] 6.2 更新 `docs/designs/skills/kflow-{api-test,e2e-test,integration-test}.md`：同步测试单轮化与定向重验；验证方式：三个文件内重复制循环表述已改为单轮

- [x] 6.3 更新 `docs/designs/skills/kflow-audit.md`：同步记账员职责；验证方式：该文件内不再出现四维度权重

- [x] 6.4 更新 `docs/designs/examples/change-status.md` 与 `docs/designs/examples/audit-report.md`：示例对齐新模板（耗时统计区、记账记录形态、终止结果新取值）；验证方式：两个示例文件与对应模板的章节结构一致

- [x] 6.5 更新 `README.md` 的版本更新说明条目，说明本次变更的范围与影响；验证方式：README 中本次变更条目存在且描述了单轮验证、记账员审计、档位调整三项

## 7. 集成验证

- [x] 7.1 运行 `bash scripts/sync-references.sh` 与 `python scripts/validate-frontmatter.py`，确认全部 skill 自包含且 front matter 合法；验证方式：两条命令以退出码 0 结束且无告警

- [x] 7.2 全仓检索一致性：确认 `docs/designs/`、`skills/` 中不再出现已废除机制的活跃表述（见证轮、不收敛判定、安全丝、累积未复核修复清单、四维度加权评分、产品需求强制完整档）；验证方式：检索「见证轮」在 `skills/kflow-*/SKILL.md` 与 `skills/kflow-*/references/*.md` 中零命中（历史变更记录文件除外）

- [x] 7.3 端到端流程走查：以「标准档功能需求」为样例，逐阶段核对阶段流转可跑通（设计探索单轮验证 → 原型合并验证 → 详细设计单轮验证 + 四视角交叉审查 → 计划单轮验证 → 编码 → 代码审查 → 测试三阶段单轮 → 记账员审计 → 归档）；验证方式：走查记录中每阶段的输入产物、执行方式、输出产物与门控判据均可对应到本次变更后的规范

- [x] 7.4 计时遥测验证：确认 `.status.md` 两个新区能被各阶段写入，且归档时计时摘要回流 `docs/skill-suggestion.md` 的规则可执行；验证方式：以走查样例产出一份含计时数据的状态文件与一条 skill-suggestion.md 计时摘要记录

## 8. 设计文档 → SKILL.md 同步

- [x] 8.1 逐项核对 `docs/designs/skills/kflow-*.md` 与 `skills/kflow-*/SKILL.md` 的一致性：本次变更涉及的全部阶段（explore/design/prototype-design/plan/api-test/e2e-test/integration-test/audit）的设计规格与可运行 Skill 内容对应无遗漏；验证方式：逐阶段列出检查项对照表并确认无未同步项

- [x] 8.2 检查全部改动后 skill 的自包含性：各 skill 的辅助规则（钩子、门控、自审规范）位于自身 `references/` 子目录，安装后零外部依赖；验证方式：`scripts/sync-references.sh` 无跨 skill 引用告警

- [x] 8.3 检查全部 SKILL.md 的 `version` 字段与仓库根 `VERSION` 一致（`scripts/sync-version.sh` 执行的准备条件）；验证方式：逐文件比对 version 字段值
