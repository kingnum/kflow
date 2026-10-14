# Tasks

## 1. 共享阶段衔接规则

- [x] 1.1 修正 `skills/kflow-resume/SKILL.md` 调度映射表中「接口单元测试」的目标 Skill，由 `kflow-e2e-test` 改为 `kflow-api-test`，使其与 `skills/kflow-resume/references/recovery-protocol.md` 的映射表一致；验证方式：两处映射表中「接口单元测试」行指向同一 Skill
- [x] 1.2 新建 `skills/kflow-explore/references/phase-transition.md`，内容包含：阶段衔接决策表（✅完成递归推进 / 🔄进行中调度当前 / ⚠️需修订调度回退目标 / ❌阻塞不调度 / ⏳待开始调度）、阶段→Skill 调度映射表（与 `recovery-protocol.md` 对齐）、归档闸口规则、人工门控边界说明；验证方式：文件存在且五分支状态与四类停止条件均可逐条对照 design.md D1/D5/D6
- [x] 1.3 将 `phase-transition.md` 复制到其余阶段 Skill 与 `kflow-resume` 的 `references/` 目录（`kflow-prototype-design`、`kflow-design`、`kflow-plan`、`kflow-code`、`kflow-code-review`、`kflow-api-test`、`kflow-e2e-test`、`kflow-integration-test`、`kflow-audit`、`kflow-resume`）；验证方式：`ls skills/kflow-*/references/phase-transition.md` 返回 11 个路径
- [x] 1.4 把 `phase-transition.md` 加入 `scripts/sync-references.sh` 的 `REF_FILES` 数组；验证方式：运行 `./scripts/sync-references.sh`，输出中 `phase-transition.md` 显示为「11 个 skill 持有，比对通过」且脚本退出码为 0

## 2. 阶段 Skill 接入自动衔接（设计文档 → SKILL.md 同步）

- [x] 2.1 更新变更级阶段 Skill 的 COMPLETE 步骤，接入阶段衔接决策（`kflow-explore` 步骤 13、`kflow-prototype-design` 步骤 12、`kflow-design` 步骤 15、`kflow-integration-test` 步骤 9），各步骤以引用 `references/phase-transition.md` 的方式表达行为并保留各自既有的人工门控；验证方式：四个 SKILL.md 的 COMPLETE 步骤均含指向 `phase-transition.md` 的引用且不再以「提示用户输入推进指令」结尾
- [x] 2.2 更新子变更级阶段 Skill 的 COMPLETE 步骤，接入阶段衔接决策（`kflow-plan` 步骤 9、`kflow-code`、`kflow-code-review` 步骤 8、`kflow-api-test`、`kflow-e2e-test`），含子变更内推进与跨子变更遍历推进两种情况；验证方式：五个 SKILL.md 的 COMPLETE 步骤均含指向 `phase-transition.md` 的引用，且子变更遍历顺序与 `auto-subchange-traversal` 既有规则一致
- [x] 2.3 更新 `kflow-audit` 的 COMPLETE 步骤（步骤 8），在衔接决策中应用归档闸口，完成后停止自动衔接并提示可发起归档，SHALL NOT 自动调度 `kflow-archive`；验证方式：该步骤文本明确写出归档闸口且不含对 `kflow-archive` 的自动调度
- [x] 2.4 同步上述改动到对应设计文档（`docs/designs/skills/kflow-explore.md`、`kflow-prototype-design.md`、`kflow-design.md`、`kflow-integration-test.md`、`kflow-plan.md`、`kflow-code.md`、`kflow-code-review.md`、`kflow-api-test.md`、`kflow-e2e-test.md`、`kflow-audit.md` 的 COMPLETE 步骤描述）再回写 SKILL.md 核对一致（**设计文档 → SKILL.md 同步**）；验证方式：逐份比对设计文档与 SKILL.md 的 COMPLETE 步骤描述，无行为差异

## 3. kflow-guide 收敛

- [x] 3.1 更新 `skills/kflow-guide/SKILL.md` 的 description：移除「做、添加、实现、搭建」等新工作意图触发词，保留「修复、Bug、缺陷」及其上下文判断所需表述；验证方式：description 中不再出现「做/添加/实现/搭建」作为新工作意图的触发词，且修复类表述保留
- [x] 3.2 拆分 `skills/kflow-guide/SKILL.md` 的 PARSE 正则分支：「恢复/resume + 变更名」路由到 `kflow-resume`，「继续 + 变更名」路由到轻量推进（读 `.status.md` 后按 `phase-transition.md` 决策表直接调度），并同步更新步骤 2 的正则表和 Plan Mode 绕过说明；验证方式：正则表存在两条独立分支且各自的路由目标明确
- [x] 3.3 更新 `skills/kflow-guide/SKILL.md` 的 INTENT 关键词映射表中「继续、下一步、接着」行与意图识别优先级规则，使其与轻量推进行为一致，并补充正则优先于关键词映射的说明；验证方式：该行推荐的后续动作不含 `kflow-resume`
- [x] 3.4 删除 `skills/kflow-guide/SKILL.md` 的步骤 6「NEW CHANGE 创建前指引」（含其输出格式模板）、步骤 3 中的新变更意图分支与「变更类型分类关键词（NEW CHANGE 分支专用）」表，以及步骤 4 中指向步骤 6 的分支；验证方式：SKILL.md 中不再出现 `NEW CHANGE` 章节，且流程图中步骤编号连续无悬空引用
- [x] 3.5 更新 `skills/kflow-guide/SKILL.md` 的角色、任务、输出产物、与其他 Skill 的关系、核心提醒各章节，移除与创建前指引、变更类型分类、变更名称建议相关的表述；验证方式：全文中不再描述 guide 承担新变更创建前指引职责

## 4. kflow-init 注入模板改写

- [x] 4.1 改写 `skills/kflow-init/SKILL.md` 的 Marker 2「变更流程强制规则」注入模板：移除「所有用户变更必须首先通过 kflow-guide 进行流程指引」与「禁止直接调用阶段 Skill」两条，将新变更入口改写为 `kflow-explore` 承接，将恢复入口改写为「恢复 {change-name}」，新增阶段自动衔接规则条目；验证方式：模板规则条目与 `specs/init-claude-md-injection/spec.md` 的 Scenario「注入扩展的流程规则」逐条对应
- [x] 4.2 运行 `./scripts/validate-injection-scope.sh` 验证注入模板未引入开发态词汇；验证方式：脚本退出码为 0
- [x] 4.3 对照改写后的模板更新 `docs/designs/skills/kflow-init.md` 的 Marker 2 章节与其「CLAUDE.md 注入」说明段（**设计文档 → SKILL.md 同步**）；验证方式：两份文件的 Marker 2 模板文本一致

## 5. kflow-resume 定位调整

- [x] 5.1 将 `skills/kflow-resume/SKILL.md` 的 DISPATCH 步骤改为引用 `references/phase-transition.md` 的共享决策表，移除私有副本；验证方式：`kflow-resume/SKILL.md` 中不再内联五分支决策表，改为引用
- [x] 5.2 更新 `skills/kflow-resume/SKILL.md` 的 triggers 与 description，将 `继续 {change-name}` 移出恢复触发词；验证方式：triggers 中不再含「继续 {change-name}」
- [x] 5.3 更新 `skills/kflow-resume/references/recovery-protocol.md` 的「5. 触发方式」章节，按推进/恢复分工改写三条入口描述；验证方式：该章节中「继续 {change-name}」不再指向 RESUME 路由，且明确指向轻量推进
- [x] 5.4 对照上述改动更新 `docs/designs/skills/kflow-resume.md`（**设计文档 → SKILL.md 同步**）；验证方式：设计文档的触发方式与调度描述与 SKILL.md、`recovery-protocol.md` 一致

## 6. 设计文档与用户文档同步

- [x] 6.1 在 `docs/designs/core-mechanisms/04-gates-and-transitions.md` §6.1「正向流程」新增阶段自动衔接规则，并与 §6.7「Archive 禁止自动流转」的表述协调；验证方式：§6.1 含衔接决策表与归档闸口，且与 §6.7 无冲突表述
- [x] 6.2 更新 `docs/designs/skills/kflow-guide.md` 的 description、步骤 3、步骤 6、触发词及各章节，与收敛后的 SKILL.md 对齐（**设计文档 → SKILL.md 同步**）；验证方式：比对设计文档与 SKILL.md 的步骤结构，编号与职责一致
- [x] 6.3 更新 `docs/designs/skills/index.md` 的路由表（第 39 行）与说明段（第 190 行）中的触发词与路由目标；验证方式：两处「继续 {change}」已改为轻量推进或移除
- [x] 6.4 更新 `skills/kflow-status/SKILL.md` 结尾的用户引导措辞（第 286 行附近），移除「使用『做/添加/实现/搭建 + 功能描述』创建新变更」与「使用 `/kflow-guide` 获取流程指引」的旧指引；验证方式：该处引导改为指向 `kflow-explore`，且同步 `docs/designs/skills/kflow-status.md` 对应段（**设计文档 → SKILL.md 同步**）
- [x] 6.5 更新 `README.md` 的流程链路图（第 46、55、66 行）、Skill 职责表（第 168 行）、使用示例（第 208、236 行）、触发词表（第 249 行）、中断恢复说明（第 386 行）与版本更新记录新增条目；验证方式：README 全文不再出现「所有变更须先经 kflow-guide」，且新增条目写明「本次升级需重跑 `/kflow-init`」

## 7. 集成验证

- [x] 7.1 运行 `openspec validate streamline-guide-routing --strict`；验证方式：输出 `is valid`
- [x] 7.2 端到端验证触发词路由：构造四类用户输入（「继续 {change}」、「恢复 {change}」、裸「继续」、裸「恢复」）逐条走查 guide 的路由分支与最终调度目标；验证方式：四类输入均命中预期分支，且两条「继续」路径均未调用 `kflow-resume`
- [x] 7.3 运行仓库级校验脚本 `./scripts/sync-references.sh`、`./scripts/validate-injection-scope.sh`、`python scripts/validate-frontmatter.py`；验证方式：三者均以退出码 0 结束
- [x] 7.4 逐份核对改写后的 SKILL.md 与 `skills/` 实现的一致性，确认无遗留的旧规则表述（「必须首先通过 kflow-guide」「禁止直接调用阶段 Skill」「NEW CHANGE」）；验证方式：对 `skills/` 与 `docs/designs/` 全量检索上述表述，命中项均为合理保留（如变更历史记录）或已清除
