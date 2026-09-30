# Tasks

## 1. 核心机制文档

- [x] 1.1 更新 `docs/designs/core-mechanisms/03-status-and-tasks.md`：在变更级 `.status.md` 基本信息中加入「变更档位」字段（`{轻量|标准|完整}`），并说明其由 explore 写入、design 复核后更新、缺失时按完整档处理。验证：该文件的基本信息表中含「变更档位」行，且缺省规则有明确表述。
- [x] 1.2 更新 `docs/designs/core-mechanisms/04-gates-and-transitions.md` §6.1：将「设计审查分级与进入计划门控分支」表由变更类型（功能缺陷级/功能需求级/产品需求级）改为变更档位（轻量/标准/完整），并补上标准档两视角一行；Gate 2 门控分支改为三档。验证：grep 该文件确认审查分级表的行标签为轻量/标准/完整，且不再以「功能缺陷级」作为分级依据。
- [x] 1.3 更新 `docs/designs/core-mechanisms/07-agent-model.md` §15：将「首次执行 10 轮，回退重执行按影响范围分数缩减」改为「档位基线（轻量 1 / 标准 3 / 完整 10），回退重执行取 `max(档位基线, 影响范围分数映射)`」。验证：该章节含档位基线表与 `max` 叠加规则，且不再出现「首次执行 10 轮」表述。
- [x] 1.4 更新 `docs/designs/core-mechanisms/07-agent-model.md` §16：将自审分级由「首次创建固定 10 轮 / 非首次弹性」改为档位驱动（轻量 0 轮 / 标准 2 轮 / 完整 10 轮），并删除「首次/非首次判定信号」表述。验证：该章节含档位自审轮次表，且 grep 确认「首次创建」「非首次创建」在自审语境下无残留。
- [x] 1.5 更新 `docs/designs/core-mechanisms/08-governance.md`：将其中涉及阶段轮次与自审的分级口径改为引用变更档位。验证：该文件中所有轮次表述均标注档位来源，无「固定 10 轮」表述。
- [x] 1.6 更新 `docs/designs/index.md` 与 `docs/designs/overview.md`：将「设计自审分级」「执行类阶段重复制」两条决策项改为档位驱动表述，并新增「变更档位判定」决策项。验证：两文件的决策表中含档位机制条目，且原有「首次创建固定 10 轮」「10 轮自然收敛」条目已改写。

## 2. 设计文档 → Skill 规格同步

- [x] 2.1 更新 `docs/designs/skills/kflow-explore.md`：新增档位初判步骤（SPLIT 之后，按变更类型 + 功能点数映射）、用户覆盖档位确认、轻量档单页产出、轻量档跳过原型设计主动询问；SELFREV 章节改为按档位轮次。验证：文件含初判映射表与档位写法，且 SELFREV 章节不再出现「首次创建固定 10 轮」。
- [x] 2.2 更新 `docs/designs/skills/kflow-design.md`：DIVIDE 之后新增档位复核步骤（完整公式 + 单向升档安全阀）；REVIEW 步骤改为三档（轻量单 Agent 综合 / 标准两视角 / 完整四视角）；SELFREV 章节改为按档位轮次。验证：文件含复核步骤与三档审查表，且审查分级不再以变更类型为依据。
- [x] 2.3 更新 `docs/designs/skills/kflow-prototype-design.md`：SELFREV 章节改为按档位轮次，并保留「人工审查时跳过自审」的例外。验证：文件的自审轮次来源标注为变更档位，且例外规则保留。
- [x] 2.4 更新 `docs/designs/skills/kflow-plan.md`：自审轮次由固定 10 轮改为档位驱动（轻量 0 / 标准 2 / 完整 10）。验证：文件含档位自审轮次表，且不再出现「必须完成全部 10 轮」表述。
- [x] 2.5 更新 `docs/designs/skills/kflow-code.md` 与 `docs/designs/skills/kflow-code-review.md`：编码阶段轮次改为档位基线；代码审查新增轻量档单 Agent 单轮形态与按档位的门控条件。验证：两文件含档位轮次与门控分支，且代码审查章节含轻量档单 Agent 形态。
- [x] 2.6 更新 `docs/designs/skills/kflow-api-test.md`、`kflow-e2e-test.md`、`kflow-integration-test.md`、`kflow-bug-fix.md`：执行轮次改为档位基线。验证：四个文件的轮次章节均引用档位基线，grep 确认无「首次执行 10 轮」残留。
- [x] 2.7 更新 `docs/designs/skills/kflow-bug-triage.md`：影响范围分数 → 推荐轮次表改为引用统一映射（分数 <= 3 映射 1 轮 / 4-15 映射 3 轮 / > 15 映射 10 轮），并按 `max(档位基线, 映射值)` 表述。验证：文件不再自定义数值区间表，改为引用统一映射。
- [x] 2.8 更新 `docs/designs/skills/kflow-audit.md`：审查维度按档位给分；流程合规性与产物完整性维度显式声明不因轻量档零轮自审、缺 self-reviews/ 目录、单 Agent 审查而判为缺项；效率指标以档位基线为达标基准。验证：三个维度的表述中含按档位给分与不误扣的明确说明。
- [x] 2.9 更新 `docs/designs/skills/kflow-guide.md` 与 `docs/designs/skills/kflow-archive.md`：指引输出中展示变更档位；归档门控与设计合并按档位适配（含轻量档自审记录缺失的合法状态）。验证：kflow-guide 的 NEW CHANGE 输出含档位字段；kflow-archive 的归档条件不因轻量档零轮自审阻塞。

## 3. Skill 实现同步（设计文档 → SKILL.md 同步）

- [x] 3.1 同步 8 份执行类 `references/repetition.md`（`skills/kflow-plan`、`kflow-code`、`kflow-code-review`、`kflow-api-test`、`kflow-e2e-test`、`kflow-integration-test`、`kflow-bug-fix`、`kflow-bug-triage`）：将 §14 弹性轮次决策的「首次执行 10 轮」改为「档位基线（轻量 1 / 标准 3 / 完整 10）」，回退重执行改为 `max(档位基线, 统一映射)`。验证：`scripts/sync-references.sh` 报告 8 份文件一致，且 grep 确认其中无「首次执行」正文轮次表述。
- [x] 3.2 同步 3 份 `references/self-review.md`（`skills/kflow-explore`、`kflow-prototype-design`、`kflow-design`）：将「首次创建固定 10 轮 / 非首次弹性 + 评分底线」改为档位驱动（轻量 0 / 标准 2 / 完整 10，评分底线仅完整档适用），删除首次/非首次判定信号。验证：三份文件内容一致，`scripts/sync-references.sh` 通过，grep 确认无「首次创建」判定信号残留。
- [x] 3.3 同步 `skills/kflow-explore/references/self-review-dimensions.md` 与 `skills/kflow-explore/SKILL.md`：SKILL.md 新增档位初判步骤（SPLIT 之后）与用户覆盖确认，SELFREV 步骤改为读取档位轮次，轻量档跳过自审并改为产物门控。验证：SKILL.md 的执行流程含档位判定步骤，且 SELFREV 步骤对轻量档有明确跳过分支。
- [x] 3.4 同步 `skills/kflow-design/SKILL.md` 与 `references/gates.md`：新增 DIVIDE 后档位复核步骤与单向升档安全阀；REVIEW 步骤实现三档分支；Gate 2 门控按三档检查产物。验证：SKILL.md 含复核步骤，gates.md 的进入计划门控对三档分别给出检查项。
- [x] 3.5 同步 `skills/kflow-code-review/SKILL.md` 与 `references/gates.md`：新增轻量档单 Agent 单轮审查分支（覆盖两视角全部检查项），门控对轻量档按「高严重度 = 0 且中严重度 < 3」判定且不要求多份视角报告。验证：SKILL.md 含档位分支，gates.md 含轻量档门控条件。
- [x] 3.6 同步 `skills/kflow-prototype-design/SKILL.md`：SELFREV 步骤改为按档位轮次，保留人工审查时完全跳过自审的例外。验证：SKILL.md 的自审轮次来源为变更档位，例外规则保留。
- [x] 3.7 同步 `skills/kflow-plan/SKILL.md`：SELFREV 步骤改为按档位轮次，轻量档跳过并改为产物门控。验证：SKILL.md 含档位自审轮次表与轻量档跳过分支。
- [x] 3.8 同步 `skills/kflow-code/SKILL.md`、`kflow-api-test`、`kflow-e2e-test`、`kflow-integration-test`、`kflow-bug-fix`、`kflow-bug-triage` 的 `SKILL.md`：重复制章节的目标轮次改为读取变更档位，prompt 模板中的轮次表述改为按目标轮次取值。验证：六个 SKILL.md 均引用变更档位，grep 确认无「必须完成全部 10 轮」硬编码表述。
- [x] 3.9 同步 `skills/kflow-audit/SKILL.md`：审查维度按档位给分，轻量档零轮自审与单 Agent 审查不判缺项，效率指标以档位基线为基准。验证：SKILL.md 的审计维度描述含按档位给分与不误扣说明。
- [x] 3.10 同步各 skill 的 `references/state-values.md`（共 9 份：`kflow-explore`、`kflow-prototype-design`、`kflow-design`、`kflow-plan`、`kflow-code`、`kflow-code-review`、`kflow-api-test`、`kflow-e2e-test`、`kflow-integration-test`）与相关 `references/gates.md`：透传并校验「变更档位」字段，门控按档位分支。验证：9 份 state-values.md 均含变更档位字段定义，涉及的门控文件含档位分支；`scripts/sync-references.sh` 通过。

## 4. 模板与项目文档

- [x] 4.1 更新 `docs/designs/templates/changes/{change}/change-status.md`：基本信息新增「变更档位」字段（含缺省说明）。验证：模板含该字段行。
- [x] 4.2 更新审查与审计相关模板（`docs/designs/templates/changes/{change}/review-reports/` 下的审查报告模板、`audit-report.md`）：审查报告模板支持单视角综合、两视角、四视角三种产物形态；审计报告模板的审查维度与效率指标标注按档位给分。验证：审查模板的字段说明覆盖三种形态，审计模板含档位基准说明。
- [x] 4.3 更新 `docs/designs/templates/changes/{change}/self-reviews/review-round.md`：标注轻量档不产生自审报告轮次文件。验证：模板头部含适用档位说明。
- [x] 4.4 更新 `README.md`：将「三阶段强制 10 轮自审」「执行类阶段 10 轮」等表述改为档位驱动，并补充变更档位机制说明。验证：README 不再出现无条件的「10 轮」表述，含档位判定说明。

## 5. 全链路一致性校验

- [x] 5.1 全局残留检查：grep 全仓库（`docs/`、`skills/`、`README.md`）确认「首次执行 10 轮」「首次创建固定 10 轮」「必须完成全部 10 轮」「功能缺陷级」「功能需求级」「产品需求级」在轮次与审查分级语境下无残留。验证：grep 输出为空，或剩余命中均为合理保留（如变更类型的定义本身、历史变更归档内容）。
- [x] 5.2 运行 `scripts/sync-references.sh`，确认 8 份 `repetition.md`、3 份 `self-review.md` 及其他同名 references 文件一致，修复脚本报告的偏差。验证：脚本执行通过且无新增不一致报告。
- [x] 5.3 档位链路端到端走查：以一份虚构的轻量档变更（1 个功能点、0 接口、0 数据模型变更）与一份完整档变更（FP > 15）为输入，沿 explore 初判 → design 复核 → plan/code/code-review 轮次 → 审计给分的路径逐一核对各 skill 的档位读取与分支落点。验证：轻量档路径下自审为 0 轮、执行类阶段为 1 轮、代码审查为单 Agent 单轮、审计不判缺项；完整档路径下全部维持 10 轮与四视角审查。
- [x] 5.4 运行 `openspec validate add-change-tier` 确认规格增量仍通过校验。验证：命令输出「Change 'add-change-tier' is valid」。
