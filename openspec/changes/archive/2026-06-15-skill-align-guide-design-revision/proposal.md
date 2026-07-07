## Why

`kflow-guide` 的 SKILL.md 实现包含多个设计文档中未记录的功能：(1) DESIGN_REVISION 路由模式（关键词匹配设计修订意图，分流到对应设计 Skill 的 REVISION 模式）；(2) 设计修订后处理流程（UPDATE_INDEX → UPDATE_STATUS → ASK_USER）；(3) Plan Mode 绕过规则（RESUME 路由匹配时禁止 Plan Mode）。设计文档落后于实现，存在文档与行为不一致的风险。

## What Changes

- `docs/designs/skills/kflow-guide.md` 设计文档中添加 DESIGN_REVISION 路由模式章节
- 设计文档中添加设计修订后处理流程
- 设计文档中添加 Plan Mode 绕过规则说明
- 设计文档关键词映射表补充 DESIGN_REVISION 相关关键词

## Capabilities

### New Capabilities

### Modified Capabilities
- `devflow-guide`: 设计文档追平实现的 DESIGN_REVISION 路由、Plan Mode 绕过、设计修订后处理功能

## Impact

- **设计文档**: `docs/designs/skills/kflow-guide.md` 修改
- SKILL.md 不需要修改（实现已是权威来源）
- 无运行时行为变更
