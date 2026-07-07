## MODIFIED Requirements

### Requirement: Archive phase includes summary generation step
`kflow-archive` SHALL include a summary generation step after design merge.

#### Scenario: Archive SKILL.md updated
- **WHEN** `kflow-archive` SKILL.md execution flow is read
- **THEN** it SHALL contain a step for generating/updating `module-summary.md` after design merge
