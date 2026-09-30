# phase-self-review Specification

## Purpose

本能力定义设计类阶段自审工作流与报告的存放规则，规定自审规则位于各设计阶段 Skill 自身的 `references/self-review.md`，且各设计技能的自审内容保持一致。

## Requirements

### Requirement: Self-review workflow and reporting uses per-skill references
The specification of self-review SHALL reside in each design-phase skill's `references/self-review.md` (kflow-explore, kflow-prototype-design, kflow-design). No centralized `kflow-shared/self-review.md` SHALL exist.

#### Scenario: Design skill SKILL.md references local self-review
- **WHEN** `kflow-design/SKILL.md` constructs a self-review subagent prompt
- **THEN** it SHALL instruct loading `skills/kflow-design/references/self-review.md` (dev) or `.claude/skills/kflow-design/references/self-review.md` (consumer)

#### Scenario: Self-review content is identical across design skills
- **WHEN** comparing `references/self-review.md` across kflow-explore, kflow-prototype-design, and kflow-design
- **THEN** the content SHALL be identical (same self-review rules apply to all design phases)
