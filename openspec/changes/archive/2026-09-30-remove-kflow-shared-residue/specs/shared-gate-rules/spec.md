# Spec Delta

## REMOVED Requirements

### Requirement: Shared gate rules definition file

**Reason**: 该能力要求 `.claude/skills/kflow-shared/gate-rules.md` 作为门控规则的统一权威文件，但 `kflow-shared/` 集中式目录已在 `2026-07-04-skill-self-contained-refactor` 中移除。门控规则现分散存放于各 skill 的 `references/gates.md`，由 `skill-self-contained` 定义的自包含结构承载。

**Migration**: 门控规则改由各 skill 的 `references/gates.md` 定义；跨阶段通用的门控原则由 `04-gates-and-transitions.md` 承载。

### Requirement: Core mechanism docs gate sections replaced

**Reason**: 该需求要求核心机制文档的门控章节替换为对 `kflow-shared/gate-rules.md` 的引用。目标文件已不存在，引用无法成立。

**Migration**: 核心机制文档的门控章节改为一章内自述门控原则，并对具体阶段门控引用各 skill 的 `references/gates.md`。

### Requirement: Internal duplication eliminated

**Reason**: 该需求的目标是消除核心机制文档与集中式文件之间的重复内容。集中式文件已不存在，重复的其中一端消失，需求失去对象。

**Migration**: 无。重复内容的另一端已由 `skill-self-contained` 的「references content is phase-specific」需求约束。
