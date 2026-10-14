# Proposal

## Why

正常变更执行过程中，用户会被反复弹回 `kflow-guide`，白跑一轮。实测触发点有四个：阶段中途说「继续」被拉去 guide；阶段跑完不直接衔接下一阶段；直接调用阶段 Skill 被规则拦下；阶段完成时被提示发送「继续 {change}」，而该词组被 guide 的最高优先级正则捕获，走进 7 步断点恢复流程。

根因是四个独立缺陷叠加：规则强制层（CLAUDE.md 要求每次用户变更都先经 guide）、自动触发层（guide description 的宽泛触发词）、有输入无衔接（阶段 COMPLETE 只改状态文件就停下）、推进接口撞恢复接口（同一个「继续」既是轻量推进又是重恢复，重的那套优先级更高）。

其中「推进接口撞恢复接口」还暴露了一处既有的 spec 与实现偏差：`intent-priority-rules` 已规定「继续类关键词 → 直接路由到活跃变更的当前阶段」，但实现中该词组被优先级 0 的 RESUME 正则先吃掉，永远走不到这条规则。

## What Changes

- **移除流程中回 guide 的强制**（**BREAKING**）：删除 CLAUDE.md 注入的「所有用户变更必须首先通过 `kflow-guide` 进行流程指引」与「禁止直接调用阶段 Skill 跳过 guide 指引」两条规则
- **新变更入口改由 `kflow-explore` 承接**（**BREAKING**）：变更类型分类、命名、档位初判、冲突预检均在该阶段完成，不再需要 guide 做创建前指引
- **新增阶段自动衔接**：阶段 Skill 的 COMPLETE 步骤完成后直接调度下一阶段，SHALL NOT 提示用户输入推进指令。复用 kflow-resume 既有的 DISPATCH 决策表，提升为跨 skill 通用规则
- **推进与恢复语义分离**（**BREAKING**）：「继续 {change}」为轻量推进（读状态后直接调度当前/下一阶段 Skill）；「恢复 {change}」/`resume` 为中断恢复（保留 7 步重流程）
- **`kflow-guide` 职责收缩**（**BREAKING**）：移除 NEW CHANGE 创建前指引、变更类型分类、变更名称建议三项能力（与 `kflow-explore` 完全重复），guide 保留状态查看路由、断点恢复路由、流程概览、设计修订分流
- **`kflow-guide` 触发面收敛**：description 移除「做、添加、实现、修复、搭建」等宽泛新工作意图触发词
- **存量项目需重跑 `/kflow-init`**：消费方 CLAUDE.md 中的旧规则文本不会自动更新，由 marker 版本判据在 re-init 时幂等替换

## Capabilities

### New Capabilities

- `phase-auto-transition`: 阶段完成后自动衔接下一阶段的规则——衔接决策表（按阶段状态分支）、停止条件（归档阶段、阻塞状态、人工门控）、与人工评审门控的共存方式

### Modified Capabilities

- `init-claude-md-injection`: 「变更流程强制规则」section 的规则集合变更——移除 guide 前置与阶段 Skill 禁用两条，新增阶段自动衔接约定，恢复入口触发词由「继续」改为「恢复」
- `devflow-guide`: 移除 `NEW CHANGE 创建前指引`、`变更类型分类`、`变更名称建议` 三条 requirement；`用户意图识别` 中 RESUME 相关 Scenario 的触发词范围收窄
- `intent-priority-rules`: 「继续」类关键词的语义明确为轻量推进（消除与 RESUME 正则的优先级冲突），并补充推进与恢复的分流判据
- `resume-plan-mode-bypass`: RESUME 触发词范围收窄为「恢复/resume + 变更名」；新增「继续 + 变更名」轻量推进路径同样绕过 Plan Mode 的约定

## Impact

**实现（Skill 定义）**

- `skills/kflow-init/SKILL.md` — Marker 2「变更流程强制规则」注入模板
- `skills/kflow-guide/SKILL.md` — description 触发词、PARSE 正则表、INTENT 关键词表与优先级规则、步骤 6 NEW CHANGE 指引（删除）
- `skills/kflow-resume/SKILL.md` — DISPATCH 决策表提升为通用规则后的定位调整、triggers 触发词
- `skills/kflow-resume/references/recovery-protocol.md` — 触发词引用更新
- 各阶段 Skill 的 COMPLETE 步骤 — `kflow-explore`、`kflow-prototype-design`、`kflow-design`、`kflow-plan`、`kflow-code`、`kflow-code-review`、`kflow-e2e-test`、`kflow-integration-test`、`kflow-audit`
- `skills/kflow-status/SKILL.md` — 结尾的用户引导措辞

**设计文档**

- `docs/designs/core-mechanisms/04-gates-and-transitions.md` — §6.1 正向流程新增阶段自动衔接规则（须与 §6.7「Archive 禁止自动流转」协调）
- `docs/designs/skills/kflow-init.md` — Marker 2 模板
- `docs/designs/skills/kflow-guide.md` — description、步骤 3、步骤 6、触发词
- `docs/designs/skills/kflow-resume.md`、`docs/designs/skills/index.md` — 路由表与触发词

**用户文档**

- `README.md` — 约 10 处（流程链路、Skill 职责表、触发词表、变更记录）

**消费方项目**

- CLAUDE.md「变更流程强制规则」section 需重跑 `kflow-init` 才会更新

**校验脚本**

- `scripts/validate-injection-scope.sh` — 确认规则文本变更后不产生误报
- `scripts/sync-references.sh` — 确认 `recovery-protocol.md` 改动后一致性校验仍通过
