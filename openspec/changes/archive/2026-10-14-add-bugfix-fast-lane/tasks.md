# Tasks

> **范围说明**：本任务清单仅含变更的实际交付工作。归档（`/opsx:archive`）、Git commit、版本自增、打包等元工作流任务由 CLAUDE.md 的「归档后规则」自动驱动，不列入本清单。
>
> **前置依赖**：本变更依赖 `streamline-design-flow` 已归档——快车道的「有界验证 + 报告完整 + 计数」口径复用该变更确立的单轮验证模型。任务 0.1 为硬前置校验。

## 0. 前置校验

- [x] 0.1 确认 `streamline-design-flow` 已归档：检查 `openspec/changes/archive/` 下存在该变更，且 `openspec/specs/convergence-driven-repetition/spec.md` 已不含见证轮四判据；验证方式：两条检查均通过后继续，否则停止并提示依赖未落地

## 1. 机制规范层（波次 1）

- [x] 1.1 更新 `docs/designs/core-mechanisms/03-status-and-tasks.md`：新增缺陷级状态文件与变更级状态文件的关系说明——缺陷级 `bugfix-status.md` 独立承载快车道缺陷的生命周期，不进入变更级阶段状态矩阵；验证方式：该文件内可检索到缺陷级状态文件的定义且明确其不参与门控

- [x] 1.2 更新 `docs/designs/core-mechanisms/04-gates-and-transitions.md`：说明快车道缺陷不进入阶段门控矩阵，以及审计对快车道产物的校验边界（校验产物完整性、不校验流程形态）；验证方式：该文件内可检索到快车道门控隔离的表述

- [x] 1.3 更新 `docs/designs/overview.md` 与 `docs/designs/index.md` 的核心设计决策表：新增「缺陷修复快车道」决策行（L4 独立生命周期、定向验证、快速收口）；验证方式：两个文件均含该决策行

- [x] 1.4 运行 `python scripts/validate-frontmatter.py` 与 `bash scripts/sync-references.sh`，确认机制规范层改动未引入 front matter 或引用一致性问题；验证方式：两条命令均以退出码 0 结束

## 2. Triage Skill（波次 2）

- [x] 2.1 更新 `skills/kflow-bug-triage/SKILL.md`：L4 路由由「调用 kflow-bug-fix」改为「进入缺陷修复快车道」——创建缺陷级状态文件、写入受影响项清单、路由输出声明快车道入口；验证方式：SKILL.md 的 ROUTE 步骤中 L4 分支输出含 `bugfix-status.md` 创建与受影响项清单

- [x] 2.2 更新 `skills/kflow-bug-triage/SKILL.md` 的输出产物章节：新增 L4 结论时创建 `bugfix-status.md` 的说明，并更新「Skill 与其他 Skill 的关系」中 L4 的输出目标；验证方式：SKILL.md 内 L4 输出目标不再表述为直接调用 bug-fix

- [x] 2.3 更新 `skills/kflow-bug-triage/references/` 下与路由、钩子、状态取值相关的分支文件：同步 L4 路由变更；验证方式：`references/` 内检索「L4」的落点描述与 SKILL.md 一致

- [x] 2.4 确认 `skills/kflow-bug-triage/SKILL.md` 中 L1/L2/L3 三路由的表述未被改动；验证方式：逐条比对三路由的 EXECUTION_MODE 声明与阶段回退动作与变更前一致

## 3. Bug-fix Skill（波次 2）

- [x] 3.1 更新 `skills/kflow-bug-fix/SKILL.md`：新增「快车道模式」分支——入口条件（无测试阶段上下文 + triage L4 路由）、状态写入位置（`bugfix-status.md`）、流程出口（进入定向验证而非返回测试阶段）；验证方式：SKILL.md 流程框图中新增快车道分支且出口明确

- [x] 3.2 更新 `skills/kflow-bug-fix/SKILL.md` 的门控与状态章节：快车道模式下不读取变更级 `.status.md` 的变更档位与阶段状态字段，轮次不写入变更级 `执行轮次`；验证方式：SKILL.md 内快车道模式的状态说明与变更级状态解耦

- [x] 3.3 更新 `skills/kflow-bug-fix/references/repetition.md`：新增快车道模式的重复制口径——复用既有三次尝试上限，不使用收敛驱动循环，出口为定向验证；验证方式：该文件内快车道章节不出现见证轮判据

- [x] 3.4 更新 `skills/kflow-bug-fix/references/gates.md` 与 `hooks.md`：新增快车道模式的门控与钩子分支（PRE_HOOK 不依赖服务、POST_HOOK 回写缺陷级状态文件）；验证方式：两个文件内均含快车道模式分支

- [x] 3.5 确认 `skills/kflow-bug-fix/SKILL.md` 中子变更级与变更级两种既有模式的流程、出口与门控未被改动；验证方式：逐条比对两模式的 REQA 返回动作与验证门控与变更前一致

## 4. 模板层（波次 3）

- [x] 4.1 新增 `docs/designs/templates/changes/{change}/bugfix-status.md` 缺陷级状态文件模板：含基本信息、分诊结论、受影响项清单、修复记录、定向验证、收口结论六个区；验证方式：模板文件含六个区且每区有字段说明与填写要求

- [x] 4.2 更新 `docs/designs/templates/changes/{change}/bugs/bugs-detail.md`（问题详情模板）：新增快车道入口标记位与收口状态字段；验证方式：模板含快车道入口标记且与 triage 输出产物清单一致

- [x] 4.3 更新 `docs/designs/templates/changes/{change}/bugs/bugs-index.md`（问题索引模板）：确认状态列可表达「已解决」并含快车道缺陷的区分标记；验证方式：模板中状态列取值与 `bug-registration` 的状态流转一致

- [x] 4.4 更新 `docs/designs/templates/index.md`：登记新增的 `bugfix-status.md` 模板；验证方式：索引文件中该模板条目存在

## 5. 设计文档同步与示例（波次 4）

- [x] 5.1 更新 `docs/designs/skills/kflow-bug-triage.md`：L4 路由分流、快车道入口声明、输出产物新增状态文件；验证方式：该文件内 L4 路由描述与 SKILL.md 一致

- [x] 5.2 更新 `docs/designs/skills/kflow-bug-fix.md`：快车道模式分支、无测试阶段上下文时的执行、流程出口扩展；验证方式：该文件内快车道模式描述与 SKILL.md 一致

- [x] 5.3 更新 `docs/designs/examples/subchange-status.md` 或新增缺陷级状态文件示例：展示 `bugfix-status.md` 的完整填写形态；验证方式：示例文件的区结构与模板一致

- [x] 5.4 更新 `README.md` 的版本更新说明条目，说明本变更范围（L4 缺陷快车道、定向验证、快速收口）；验证方式：README 中本次变更条目存在且描述上述三项

## 6. 集成验证

- [x] 6.1 运行 `bash scripts/sync-references.sh` 与 `python scripts/validate-frontmatter.py`，确认全部 skill 自包含且 front matter 合法；验证方式：两条命令以退出码 0 结束且无告警

- [x] 6.2 L1/L2/L3 路径回归校验：确认三条路由的阶段回退动作、`.status.md` 修改、路由输出声明与变更前完全一致；验证方式：逐条对照检查表无差异

- [x] 6.3 L4 快车道端到端走查：以「用户反馈一个实现层缺陷」为样例，核对分诊 L4 结论 → 创建 `bugfix-status.md` → 快车道模式修复 → 定向验证（仅受影响项）→ 快速收口 → `bugs/index.md` 状态更新 全链路可跑通；验证方式：走查记录中每步的输入产物、输出产物与判定依据均可对应到本次变更后的规范

- [x] 6.4 快车道边界校验：确认快车道修复过程中不触碰 `functional-designs/`、`detailed-design/`、`api-tests/`、`e2e-tests/`，且不修改变更级 `.status.md` 的阶段矩阵字段；验证方式：以 6.3 的走查样例核对上述目录与文件在快车道执行前后无变化

- [x] 6.5 分诊失效路径校验：构造「修复中发现影响面超出受影响项清单」的情形，确认系统判定分诊失效并退回 `kflow-bug-triage`；验证方式：走查记录中该路径被正确触发且未在快车道内擅自扩大验证范围

## 7. 设计文档 → SKILL.md 同步

- [x] 7.1 逐项核对 `docs/designs/skills/kflow-bug-triage.md`、`kflow-bug-fix.md` 与对应 `skills/kflow-*/SKILL.md` 的一致性：本次变更涉及的 L4 路由分流、快车道模式、状态文件写入、流程出口四处改动对应无遗漏；验证方式：逐项列出检查对照表并确认无未同步项

- [x] 7.2 检查改动后 skill 的自包含性：快车道相关规则（门控、钩子、重复制口径）位于各 skill 自身 `references/` 子目录，安装后零外部依赖；验证方式：`scripts/sync-references.sh` 无跨 skill 引用告警

- [x] 7.3 检查全部 SKILL.md 的 `version` 字段与仓库根 `VERSION` 一致（`scripts/sync-version.sh` 执行的准备条件）；验证方式：逐文件比对 version 字段值
