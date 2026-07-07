## Why

`kflow-code` 的设计文档包含两个重要章节未在 SKILL.md 实现中体现：(1) 「共享文件冲突预防」规则（4 条规则：识别共享文件、Agent 禁止操作、wait-for-all 模式、冲突回滚）；(2) 「前后端子变更文件隔离规则」（前端域/后端域目录范围定义、前端 FP>10 时的骨架+页面组策略）。这些规则对多子变更并行编码的正确性至关重要。

## What Changes

- `kflow-code` SKILL.md 中添加「共享文件冲突预防」章节
- `kflow-code` SKILL.md 中添加「前后端子变更文件隔离规则」章节
- 两个章节从设计文档 `docs/designs/skills/kflow-code.md` 同步

## Capabilities

### New Capabilities

### Modified Capabilities
- `cross-change-conflict`: kflow-code SKILL.md 补齐共享文件冲突预防规则
- `frontend-implementation-subchange`: kflow-code SKILL.md 补齐前后端文件隔离规则

## Impact

- **SKILL.md**: `.claude/skills/kflow-code/SKILL.md` 修改
- 设计文档不需要修改
- 影响编码阶段多子变更并行时的文件隔离和冲突预防行为
