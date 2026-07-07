## Why

§16（10轮自循环审查）已为创造性阶段建立了强制10轮审查机制，但 §15（Agent 迭代执行）定义的执行类阶段缺少强制轮次下限——Agent 自行判断"完成了"即可提前返回，无法保证执行质量。创造性阶段和执行类阶段应采用统一的10轮强制标准。

## What Changes

- 变更级和子变更级 .status.md `## 基本信息` 区均增加 `**执行轮次**: {N} / 10` 字段，Agent 每完成一轮更新当前值
- **BREAKING** Agent 迭代执行增加强制10轮下限：所有执行类阶段 Agent 须跑满10轮后方可返回，禁止提前终止
- §15.3 流程增加 INIT 步骤（主 Agent 在 DISPATCH 前写入初始轮次计数器）和 ACCEPT 轮次检查（轮次不足10/10则拒收）
- §15.6 Agent 完成判断增加"满10轮"条件，与原有产物合格条件并列
- §15.7 主 Agent 验收标准表增加轮次检查行
- 缺陷修复阶段的3次尝试上限与10轮迭代的层级关系澄清（上限约束单用例修复尝试次数，10轮约束整体迭代轮次，上下限独立）

## Capabilities

### New Capabilities
- `round-counter`: 执行轮次计数器机制——在变更级和子变更级 .status.md 中维护 `执行轮次: N/10` 字段，Agent 每完成一轮迭代递增，主 Agent 验收时以此为轮次门禁

### Modified Capabilities
- `agent-iteration-execution`: Agent 迭代执行从"收敛即停"改为"强制10轮"，流程增加 INIT 步骤（写入计数器）和轮次验收检查，Agent prompt 须包含轮次迭代指令
- `subchange-phase-unification`: 子变更 .status.md 模板在 `## 基本信息` 区增加 `**执行轮次**` 字段
- `defect-strike-limit`: 缺陷修复3次尝试上限与10轮迭代的层级关系——3次上限约束同一用例修复尝试次数（上限），10轮约束整体修复迭代轮次（下限），两者独立、不冲突

## Impact

- 受影响设计文档：`core-mechanisms.md` §3.1（变更级 .status.md 模板）、§3.2（子变更级 .status.md 模板）、§6.2（缺陷修复与10轮层级）、§15.3/§15.4/§15.6/§15.7/§15.9（Agent 迭代流程全链路）
- 受影响示例：`docs/designs/examples/change-status.md`（变更级示例）、`docs/designs/examples/subchange-status.md`（子变更级示例）
- 受影响 specs：`agent-iteration-execution`、`subchange-phase-unification`、`defect-strike-limit`
- 受影响 SKILL 设计文档：`kflow-plan.md`、`kflow-code.md`、`kflow-code-review.md`、`kflow-e2e-test.md`、`kflow-integration-test.md`、`kflow-bug-fix.md`（prompt 模板增加轮次迭代指令）
