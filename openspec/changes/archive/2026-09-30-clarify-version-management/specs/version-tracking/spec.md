# Spec Delta

## REMOVED Requirements

### Requirement: SKILL.md front matter includes version field

**Reason**: 该需求规定 SKILL.md front matter 须含 `version` 字段且与 `VERSION` 一致。要求本身与实现一致，但同一主题被拆到本能力与 `unified-version` 两处定义，导致 `unified-version` 演进为「SHALL 移除 version 字段」时无人发现两规格已相反。能力边界按同一规则不应分散承载——版本字段的存在性属版本管理规则，应由版本管理能力单独定义。

**Migration**: 并入 `unified-version` 的「Single version source for all documents」需求（Skill 级载体条款），并由新增的「SKILL.md 版本字段同步」需求承担同步与一致性场景。

### Requirement: sync-version.sh batch version synchronization

**Reason**: 同上的能力拆分问题。该需求定义 `scripts/sync-version.sh` 从 `VERSION` 读取版本并写入每个 `skills/kflow-*/SKILL.md`，属版本管理规则的同步环节。

**Migration**: 并入 `unified-version` 新增的「SKILL.md 版本字段同步」需求，脚本路径与三个场景（批量同步、已存在字段被覆盖、缺失字段被补入）一并迁移。

### Requirement: package-skills.sh validates version consistency

**Reason**: 同上的能力拆分问题。该需求定义打包前的版本一致性校验。它同时暴露了一个实现缺陷：`package-skills.sh` 的扫描根为 `.claude/skills`，与实现目录 `skills/` 不符，使该需求在一个空的 Skill 集合上校验通过——即需求形式上满足、实质从未生效。需求移入版本管理能力时须同时修正校验对象的来源。

**Migration**: 并入 `unified-version` 新增的「打包前版本一致性校验」需求，并新增「校验对象不得为空集」场景，使空扫描判定为失败而非通过。扫描根修正见 `skill-packaging` 的「打包范围与排除规则（自包含 Skill 目录）」需求。

### Requirement: Consumer version inspection

**Reason**: 同上的能力拆分问题。该需求定义消费方通过读取 SKILL.md 的 `version` 字段确定已安装版本，是 Skill 级版本载体的存在理由。

**Migration**: 并入 `unified-version` 新增的「消费方查看已安装版本」需求。
