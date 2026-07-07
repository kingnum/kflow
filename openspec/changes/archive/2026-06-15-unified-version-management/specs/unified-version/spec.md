## MODIFIED Requirements

### Requirement: Single version source for all documents
All design documents, core mechanism documents, and SKILL.md files SHALL reference `VERSION` file as the single version source. Individual version numbers in file headers SHALL be replaced with "参见仓库根目录 `VERSION` 文件". SKILL.md frontmatter SHALL NOT contain `version:` field.

#### Scenario: Core mechanism doc header
- **WHEN** any core mechanism doc header is read
- **THEN** version line SHALL read "版本: 参见仓库根目录 `VERSION` 文件"

#### Scenario: Skill design doc header
- **WHEN** any skill design doc header is read
- **THEN** version line SHALL read "版本: 参见仓库根目录 `VERSION` 文件"

#### Scenario: v2.4.0 changelog note only in relevant file
- **WHEN** 01-project-types.md, 02-directory-structure.md, 03-status-and-tasks.md, 04-gates-and-transitions.md, 06-recovery.md, 08-governance.md headers are read
- **THEN** they SHALL NOT contain the v2.4.0 changelog note (only 07-agent-model.md retains it)
