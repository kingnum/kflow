# Proposal

## Why

当前 KFlow 中所有缺陷都被当作“变更”处理：用户说“修复某个 bug”时，guide 在没有活跃变更的情况下引导去 `kflow-explore` 新建功能缺陷变更；即使存在活跃变更，也常被引导新建变更。缺陷因此被功能变更的档位公式与完整阶段集合衡量，简单 bug 也会触发升档并走完设计、计划、编码、代码审查、测试、审计、归档的全流程。

已有的缺陷修复快车道（`bugfix-fast-lane`）本可承载 L4 实现缺陷，但它被“必须有活跃变更”和“必须经 triage”两个前提卡住，实际不可达。结果是：简单缺陷既没有走快车道，也没有避免变更开销。

本变更让 L4 简单缺陷默认进入快车道，并允许缺陷在不创建变更的情况下完成“分诊 → 修复 → 定向验证 → 快速收口”。

## What Changes

- `kflow-guide` 的修复意图不再依赖活跃变更，直接路由到 `kflow-bug-triage`；无可操作变更时不再把修复引导到 `kflow-explore` 建变更。
- `kflow-bug-triage` 解除“必须存在活跃变更”门控，新增缺陷工作区判定（项目级 / 变更级）与路径判定（快车道 / 创建变更）。
- 新增项目级缺陷工作区 `docs/bugs/`（`index.md` + 分页详情 + `fix/{BUG-ID}/`），用户反馈的缺陷默认登记于此；变更级 `bugs/` 保留给测试阶段自动发现（B 路径）。
- 活跃变更内发现的缺陷先判归属：由该变更引入则关联该变更，否则登记到项目级；两种情况下都不新建变更。
- 快车道入口改为：L4 + 不需要修改 L1/L2/L3 产物 + 不需要数据迁移/破坏性契约变更 + 用户确认。满足时默认快车道，不满足时才创建变更。
- 快车道状态文件支持项目级根 `docs/bugs/fix/{BUG-ID}/bugfix-status.md` 与既有变更级根；验证目标从“测试用例 ID”扩展为“已有测试 + 新增回归测试 + 手工验证步骤”。
- 归档门控读取项目级 `docs/bugs/index.md`，未关闭的 🔴 阻塞级缺陷阻断归档。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `devflow-guide`: 修复意图在无活跃变更时仍路由到 triage；不再把修复引导到 explore 创建变更；流程概览增加缺陷快车道路径。
- `bug-triage-skill`: 解除活跃变更门控；新增缺陷工作区判定、归属判定与快车道/变更路径判定；无活跃变更时使用产品级设计产物作为诊断证据。
- `bug-registration`: 新增项目级 `docs/bugs/` 工作区及其索引、分页、ID 命名与生命周期规则；明确项目级与变更级两种登记的适用场景。
- `triage-impact-assessment`: 影响范围评估在项目级与变更级两种工作区均可执行；受影响项清单作为快车道定向验证的唯一范围依据。
- `bugfix-fast-lane`: 入口不再要求活跃变更；状态文件与产物支持项目级根；验证目标扩展为测试用例、回归测试与手工步骤；多缺陷隔离扩展到项目级。
- `bug-fix-writeback`: 新增项目级 `docs/bugs/` 的回写路径与状态更新规则。
- `devflow-archive`: 归档门控读取项目级阻塞缺陷；未关闭的 🔴 阻塞级缺陷阻断归档。

## Impact

- 运行时 Skills: `kflow-guide`、`kflow-bug-triage`、`kflow-bug-fix`、`kflow-archive` 及其 `references/`。
- 模板: 新增项目级 bugs 模板（索引、分页详情、`fix/{BUG-ID}/bugfix-status.md`、`verify-report.md`）。
- 设计文档: `docs/designs/skills/kflow-guide.md`、`kflow-bug-triage.md`、`kflow-bug-fix.md`、`kflow-archive.md`；`core-mechanisms/02-directory-structure.md`、`03-status-and-tasks.md`。
- 状态与路径: 缺陷级状态文件路径由“变更级唯一”改为“项目级 / 变更级二选一”。
- 兼容性: 既有变更级 `bugs/` 与 `bugfix-status.md` 保持有效；不回填历史变更。
