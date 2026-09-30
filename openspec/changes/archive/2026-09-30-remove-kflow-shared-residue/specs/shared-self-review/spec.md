# Spec Delta

## REMOVED Requirements

### Requirement: Shared self-review definition file

**Reason**: 该能力要求 `.claude/skills/kflow-shared/self-review.md` 作为自审规范的唯一事实来源，但 `kflow-shared/` 集中式目录已在 `2026-07-04-skill-self-contained-refactor` 中移除。自审规范现存放于 `skills/kflow-explore`、`kflow-prototype-design`、`kflow-design` 各自的 `references/self-review.md`，且 `phase-self-review` 明确要求「No centralized kflow-shared/self-review.md SHALL exist」——本能力与该需求直接矛盾。

**Migration**: 自审规范改由三个设计类 skill 各自的 `references/self-review.md` 定义，三者内容一致性由 `phase-self-review` 的「Self-review content is identical across design skills」约束。

### Requirement: Core mechanism doc self-review section replaced

**Reason**: 该需求要求 `07-agent-model.md` §16 替换为对 `kflow-shared/self-review.md` 的引用。目标文件已不存在，引用无法成立。

**Migration**: `07-agent-model.md` §16 的引用改为指向三个设计类 skill 各自的 `references/self-review.md`。
