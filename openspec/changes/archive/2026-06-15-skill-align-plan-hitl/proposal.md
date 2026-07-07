## Why

`kflow-plan` 的设计文档（`docs/designs/skills/kflow-plan.md`）包含完整的「HITL 子变更决策点标注」章节，定义了 HITL 决策点标注格式（`[HITL D{n}]`）、HITL 决策点清单表格模板、决策点任务识别规则。但 SKILL.md 实现中完全缺失此章节，导致 plan 阶段产出的 tasks.md 无法正确标注 HITL 决策点。

## What Changes

- `kflow-plan` SKILL.md 中添加 HITL 子变更决策点标注章节，从设计文档同步：
  - HITL 决策点标注格式（`[HITL D{n}]`）
  - HITL 决策点清单表格模板
  - 决策点任务识别规则
  - 前端子变更依赖标注规则

## Capabilities

### New Capabilities

### Modified Capabilities
- `hitl-afk-classification`: plan 阶段 SKILL.md 补齐 HITL 决策点标注能力

## Impact

- **SKILL.md**: `.claude/skills/kflow-plan/SKILL.md` 修改
- 设计文档不需要修改（已是权威来源）
- 影响 plan 阶段产出的 tasks.md 格式
