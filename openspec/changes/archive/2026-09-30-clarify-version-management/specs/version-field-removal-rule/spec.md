# Spec Delta

## REMOVED Requirements

### Requirement: Auditor checks for version field in SKILL.md

**Reason**: 该需求要求 `kflow-skills-auditor` 检查 SKILL.md frontmatter 不含 `version:` 字段，发现时输出 WARN「版本号由 VERSION 文件统一管理，SKILL.md 不应包含独立版本号」。三点使其整体作废：

1. **与现行机制相反**：18 个 SKILL.md 均含 `version:` 字段，由 `scripts/sync-version.sh` 写入、`scripts/package-skills.sh` 校验、消费方 `grep '^version:'` 查看。按该需求执法，当前正确的仓库状态会被判为 18 处违规。
2. **无执法者**：`kflow-skills-auditor` 不在本仓库——`.claude/skills/` 下只有 `skill-creator` 与 `to-spec`，`skill-packaging` 的排除条款亦说明该 Skill 不随本仓库分发。需求无法被任何实现验证。
3. **与 `version-tracking` 直接冲突**：后者要求 SKILL.md 须含 `version` 字段，两者对同一字段给出相反要求。

该需求不包含任何可迁移的有效约束，不做并入。

**Migration**: 无。SKILL.md 的 `version:` 字段为受支持的载体，其存在性与一致性规则统一由 `unified-version` 定义（见「Single version source for all documents」的 Skill 级载体条款与「SKILL.md 版本字段同步」需求）。审计侧不再检查该字段；审计能力的实现文件 `skills/kflow-audit/` 中亦从未包含此项检查。
