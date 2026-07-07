## ADDED Requirements

### Requirement: Auditor checks for version field in SKILL.md
`kflow-skills-auditor` SHALL check that SKILL.md frontmatter does NOT contain a `version:` field. If found, output a WARN with message: "版本号由 VERSION 文件统一管理，SKILL.md 不应包含独立版本号".

#### Scenario: SKILL.md with version field triggers warning
- **WHEN** kflow-skills-auditor audits a SKILL.md containing `version: 1.2.0` in frontmatter
- **THEN** it SHALL output WARN: "版本号由 VERSION 文件统一管理，SKILL.md 不应包含独立版本号"

#### Scenario: SKILL.md without version field passes
- **WHEN** kflow-skills-auditor audits a SKILL.md without `version:` field
- **THEN** this check SHALL pass with no warning
