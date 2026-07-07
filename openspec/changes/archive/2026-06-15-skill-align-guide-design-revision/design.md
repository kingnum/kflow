## Context

`kflow-guide` SKILL.md 实现包含 DESIGN_REVISION 路由、Plan Mode 绕过等设计文档未记录的功能。需要反向同步设计文档。

## Goals / Non-Goals

**Goals:**
- 设计文档追平实现

**Non-Goals:**
- 不修改 SKILL.md（实现已是权威来源）
- 不改变运行时行为

## Decisions

### D1: 新增章节

设计文档 `docs/designs/skills/kflow-guide.md` 新增：
- DESIGN_REVISION 路由模式（关键词映射表 + 分流逻辑）
- 设计修订后处理流程（UPDATE_INDEX → UPDATE_STATUS → ASK_USER）
- Plan Mode 绕过规则（RESUME 路由优先级最高）
- 关键词映射表补充 DESIGN_REVISION 关键词

## Risks / Trade-offs

无风险。纯文档更新。
