## Context

`kflow-plan` 设计文档定义了完整的 HITL 子变更决策点标注机制，但 SKILL.md 实现中缺失。HITL 标记阻塞 plan 入口（`04-gates-and-transitions.md` §6.8），plan 阶段必须正确标注 HITL 决策点以便下游阶段感知。

## Goals / Non-Goals

**Goals:**
- SKILL.md 补齐 HITL 标注章节（格式、清单模板、识别规则）
- 补齐前端子变更依赖标注规则

**Non-Goals:**
- 不修改设计文档（已是权威来源）
- 不改变 HITL 语义

## Decisions

### D1: 从设计文档同步内容

从 `docs/designs/skills/kflow-plan.md` 同步以下章节到 SKILL.md：
- HITL 决策点标注格式（`[HITL D{n}]`）
- HITL 决策点清单表格模板
- 决策点任务识别规则
- 前端子变更依赖标注格式

### D2: 插入位置

在执行流程的步骤 4（TASKS 任务清单生成）之后添加 HITL 标注步骤。

## Risks / Trade-offs

无显著风险。
