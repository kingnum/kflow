# Proposal: 前端实现集中化 + 阶段门控增强

## Why

当前 KFlow 体系存在四个结构性缺口：(1) 原型阶段产出 HTML 交互原型后，编码阶段缺少「原型到前端工程代码」的转译环节，前端实现的责任归属不清晰；(2) plan 阶段不区分后端/前端功能点，全部使用统一 TDD 模板，导致前端 UI 开发的任务粒度失配；(3) 归档阶段没有「禁止自动进入」的硬门控，存在审计通过后未经用户验证就进入归档的风险；(4) 阶段回退机制仅覆盖 design 和 explore 两种目标阶段，缺少 prototype-design 回退路径，且编码阶段发现上游问题时缺少标准化处理流程。

## What Changes

- **前端实现集中为独立子变更**：每个 Change 的前端实现统一由一个独立子变更负责，不再拆分到多个后端子变更中。前端子变更依赖 API 契约而非后端实现，可用 mock 并行启动
- **Plan 阶段区分后端/前端功能点**：后端 FP 沿用 TDD 模板，前端 FP 使用「原型转译」模板，归属到独立前端子变更
- **Code 阶段增加前端实现子流程**：在现有后端 TDD 循环基础上，新增「工程骨架搭建 → 逐页转译 → API 对接 → 状态覆盖」的前端实现流程
- **归档阶段禁止自动进入**：审计通过后必须用户显式确认才能进入归档，Archive 是唯一不允许自动流转的阶段
- **回退机制补全**：回退触发来源从 4 种扩展为 6 种（增加原型设计错误、功能设计调整），回退目标增加 prototype-design，编码阶段发现上游问题增加标准化 AskUserQuestion 决策流程

## Capabilities

### New Capabilities

- `frontend-implementation-subchange`: 前端实现 SHALL 集中在一个独立子变更中完成，包含原型转译流程（工程骨架 → 逐页转译 → API 对接 → 状态覆盖）。前端子变更依赖 API 契约（非后端实现），可用 mock 数据并行启动。前端 FP > 10 时允许拆分骨架子变更 + 串行页面组子变更
- `archive-manual-entry`: 归档阶段 SHALL NOT 被任何阶段自动触发。审计通过后 MUST 通过 AskUserQuestion 获取用户显式确认后方可进入归档阶段。Archive 是唯一禁止自动流转的阶段

### Modified Capabilities

- `change-rollback`: 回退触发来源新增 2 种（编码发现原型交互流程不合理 → 回退到 prototype-design；编码发现功能设计需调整 → 回退到 explore/design）。新增编码阶段发现上游问题的 AskUserQuestion 决策流程（确认回退 / 暂缓此 FP / 记录已知问题）。原型回退进入 prototype-design REVISION 模式
- `phase-boundary-enforcement`: 新增规则：归档阶段禁止自动进入，MUST 用户显式触发。新增前端子变更依赖规则：依赖 API 契约（design 阶段已定义）而非后端编码实现
- `prototype-to-code-consistency`: 从当前"约束注入"（PROTO_CONSTRAINTS 提示性约束）升级为前端子变更的「执行输入」——prototype/index.html、element-coverage-tree.md、design-tokens.css、design-system/MASTER.md 作为前端转译流程的必需输入

## Impact

- **受影响的 Skill 设计文档**: `kflow-plan.md`, `kflow-code.md`, `kflow-archive.md`, `kflow-prototype-design.md`
- **受影响的核心机制文档**: `04-gates-and-transitions.md`, `03-status-and-tasks.md`, `08-governance.md`
- **受影响的运行时 Skill**: `kflow-plan` (SKILL.md), `kflow-code` (SKILL.md), `kflow-archive` (SKILL.md)
- **受影响的模板**: 子变更 tasks.md 模板（新增前端 FP 任务模板）
- **无破坏性变更**: 现有后端 TDD 流程不受影响，仅在前端子变更中启用新流程
