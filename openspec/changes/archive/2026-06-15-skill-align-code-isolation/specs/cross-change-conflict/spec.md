## MODIFIED Requirements

### Requirement: Code phase includes shared file conflict prevention
`kflow-code` SKILL.md SHALL include shared file conflict prevention rules (4 rules: identify shared files, agent prohibition, wait-for-all pattern, conflict rollback).

#### Scenario: SKILL.md contains conflict prevention section
- **WHEN** `.claude/skills/kflow-code/SKILL.md` is read
- **THEN** it SHALL contain a section on shared file conflict prevention with 4 rules

### Requirement: Code phase includes frontend-backend file isolation
`kflow-code` SKILL.md SHALL include frontend-backend file isolation rules (frontend domain directories, backend domain directories, FP>10 skeleton+page-group strategy).

#### Scenario: SKILL.md contains file isolation section
- **WHEN** `.claude/skills/kflow-code/SKILL.md` is read
- **THEN** it SHALL contain a section on frontend-backend file isolation with domain directory definitions
