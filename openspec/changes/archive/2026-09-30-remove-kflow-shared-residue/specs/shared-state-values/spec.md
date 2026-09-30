# Spec Delta

## REMOVED Requirements

### Requirement: Shared state values definition file

**Reason**: 该能力要求 `.claude/skills/kflow-shared/state-values.md` 作为状态值定义的统一权威文件，但 `kflow-shared/` 集中式目录已在 `2026-07-04-skill-self-contained-refactor` 中移除。状态值定义现分散存放于各 skill 的 `references/state-values.md`，由 `skill-self-contained` 定义的自包含结构承载。

**Migration**: 状态值定义改由各 skill 的 `references/state-values.md` 定义；跨阶段通用的状态值取值由 `03-status-and-tasks.md` 承载。

### Requirement: Core mechanism doc state values section replaced

**Reason**: 该需求要求核心机制文档的状态值章节替换为对 `kflow-shared/state-values.md` 的引用。目标文件已不存在，引用无法成立。

**Migration**: 核心机制文档的状态值章节改为一章内自述取值定义，并说明各 skill 的 `references/state-values.md` 为其阶段的落地副本。
