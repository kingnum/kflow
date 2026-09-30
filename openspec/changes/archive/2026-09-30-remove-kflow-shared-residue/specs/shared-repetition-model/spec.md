# Spec Delta

## REMOVED Requirements

### Requirement: Shared repetition model definition file

**Reason**: 该能力要求 `.claude/skills/kflow-shared/repetition-model.md` 作为重复制执行规范的唯一事实来源，但 `kflow-shared/` 集中式目录已在 `2026-07-04-skill-self-contained-refactor` 中移除。重复制规范现分散存放于 8 个执行类 skill 各自的 `references/repetition.md`，且 `execution-repetition-mode` 明确要求「No centralized kflow-shared/repetition-model.md SHALL exist」——本能力与该需求直接矛盾。

**Migration**: 重复制规范改由各执行类 skill 的 `references/repetition.md` 定义，分发规则由 `skill-self-contained` 的「Shared file distribution by reference count」承载。

### Requirement: Flexible round decision logic

**Reason**: 与 `flexible-repetition-mode` 的「Flexible repetition round decision」重复定义同一规则，形成两处口径。集中式文件移除后，本处成为指向不存在位置的重述。

**Migration**: 轮次决策规则统一由 `flexible-repetition-mode` 承载（该能力经 `add-change-tier` 修改后改由变更档位驱动，见 `tier-driven-repetition`）。

### Requirement: Phase execution history tracking in shared model

**Reason**: 与 `flexible-repetition-mode` 的「Phase execution history tracking」重复定义同一规则。

**Migration**: 阶段执行历史追踪统一由 `flexible-repetition-mode` 承载。

### Requirement: Impact scope score reading mechanism

**Reason**: 与 `triage-impact-assessment` 及 `flexible-repetition-mode` 的分数读取规则重复，且集中式文件已不存在。

**Migration**: 影响范围分数的读取机制与映射统一由 `tier-driven-repetition` 承载（经 `add-change-tier` 引入）。

### Requirement: Core mechanism doc references shared file

**Reason**: 该需求要求 `07-agent-model.md` 引用集中式文件。目标文件已不存在。

**Migration**: `07-agent-model.md` §15 的引用改为指向各执行类 skill 的 `references/repetition.md`。

### Requirement: Skill design docs reference shared file

**Reason**: 该需求要求各 skill 设计文档引用集中式文件。目标文件已不存在。

**Migration**: 各 skill 设计文档的引用改为指向自身 `references/repetition.md`（`skill-self-contained` 已定义该结构）。
