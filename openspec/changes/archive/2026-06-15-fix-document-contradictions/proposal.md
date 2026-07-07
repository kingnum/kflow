## Why

审查发现 3 处文档矛盾和 1 处内部重复：(1) 详细设计拆分阈值在 `02-directory-structure.md`（≤30 单文件）与 `kflow-design.md` + SKILL.md（≤20 单文件）矛盾；(2) `kflow-design.md` 设计文档中 SELFREV 执行流程图仍为被废除的「分工制」（Round 1-3 结构性/4-7 细节/8-10 边界），与 `07-agent-model.md` §16.3 已明确的「重复制」矛盾；(3) `04-gates-and-transitions.md` §6.6 和 §6.9 包含几乎完全相同的「编码阶段发现上游问题决策流程」。用户已确认阈值应为 20。

## What Changes

- `02-directory-structure.md` §2.4 阈值从 30 修改为 20
- `kflow-design.md` 设计文档执行流程图中 SELFREV 步骤从分工制描述改为重复制描述
- `04-gates-and-transitions.md` §6.9 删除（与 §6.6 重复）

## Capabilities

### New Capabilities

### Modified Capabilities
- `design-doc-directory`: 详细设计拆分阈值从 30 修改为 20
- `phase-self-review`: kflow-design.md 设计文档中 self-review 流程图更新为重复制模式描述
- `phase-boundary-enforcement`: 04-gates-and-transitions.md 删除 §6.9 重复段落

## Impact

- **核心机制文档**: `02-directory-structure.md`, `04-gates-and-transitions.md` 修改
- **Skill 设计文档**: `kflow-design.md` 修改
- 无运行时 SKILL.md 影响（实现已正确使用阈值 20 和重复制模式）
