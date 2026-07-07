## Why

当前 KFlow Skills 体系缺少三个关键防护机制：(1) 子变更级缺陷修复无尝试次数上限，可能导致无限自动循环；(2) 探索阶段的信息收集操作（WebFetch/WebSearch/图片查看）结果在上下文轮转后不可恢复；(3) 变更过程中的关键决策和错误无统一的结构化追踪入口。借鉴 planning-with-files 的核心理念，以零结构性成本的规则级改进填补这些空白。

## What Changes

- 在 `kflow-bug-fix` 子变更缺陷修复循环中增加 3 次自动修复尝试上限，第 3 次失败后自动升级用户
- 在 `kflow-explore` 中增加「两动作规则」：每 2 次信息收集操作后将发现写入产出文件
- 在变更级 `.status.md` 中增加「关键决策记录」表和增强「错误日志」表
- 在 `kflow-resume` 恢复输出中增加「五问题快速摘要」格式

## Capabilities

### New Capabilities

- `defect-strike-limit`: 子变更级缺陷修复三次尝试限制，与集成测试的「三回合架构评估」保持一致
- `explore-two-action-rule`: 探索阶段信息收集的两动作保存规则，防止非文本操作结果丢失
- `status-decision-error-tracking`: 变更级状态文件的决策记录和结构化错误日志扩展
- `resume-five-question-summary`: 中断恢复时的五问题快速摘要输出格式

### Modified Capabilities

- `defect-root-cause`: 在现有三分法分类基础上增加尝试次数上限和升级路由
- `two-level-checkpoint`: resume 恢复流程输出增加五问题摘要格式（不影响 checkpoint 存储逻辑）

## Impact

- `docs/designs/skills/kflow-bug-fix.md` — 增加修复尝试上限规则
- `docs/designs/skills/kflow-explore.md` — 增加两动作规则
- `docs/designs/core-mechanisms.md` — .status.md 格式扩展、缺陷修复循环增加上限
- `docs/designs/skills/kflow-resume.md` — 恢复输出增加五问题摘要
- `openspec/specs/defect-root-cause/spec.md` — 增加尝试上限 scenario
- `openspec/specs/two-level-checkpoint/spec.md` — 增加五问题摘要 scenario
