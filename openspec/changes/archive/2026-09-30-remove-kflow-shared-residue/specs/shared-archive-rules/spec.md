# Spec Delta

## REMOVED Requirements

### Requirement: Shared archive rules definition file

**Reason**: 该能力要求 `.claude/skills/kflow-shared/archive-rules.md` 作为归档规则的唯一事实来源，但 `kflow-shared/` 集中式目录已在 `2026-07-04-skill-self-contained-refactor` 中移除。归档规则现存放于 `skills/kflow-archive/references/archive-rules.md`，由 `skill-self-contained` 定义的自包含结构承载。本能力与同一主题上的 `devflow-archive` 重复，且其描述的目录不存在。

**Migration**: 归档规则改由 `skills/kflow-archive/references/archive-rules.md` 定义；`04-gates-and-transitions.md` 的归档章节引用改为指向该 per-skill 文件（见 `remove-kflow-shared-residue` 对 `devflow-archive` 的修改）。

### Requirement: Core mechanism doc archive sections replaced

**Reason**: 该需求要求 `04-gates-and-transitions.md` 的归档章节替换为对 `kflow-shared/archive-rules.md` 的引用。目标文件已不存在，引用无法成立。

**Migration**: 同一需求改由 `devflow-archive` 承担，引用目标改为 per-skill 的 `kflow-archive/references/archive-rules.md`。
