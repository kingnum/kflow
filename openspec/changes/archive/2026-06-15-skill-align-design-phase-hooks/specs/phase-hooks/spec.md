## MODIFIED Requirements

### Requirement: All phase Skills reference phase-hooks
All phase Skill SKILL.md files SHALL contain PRE_HOOK and POST_HOOK references to `kflow-shared/phase-hooks.md`. `kflow-design` SHALL be updated to include these references.

#### Scenario: kflow-design SKILL.md contains hook references
- **WHEN** `.claude/skills/kflow-design/SKILL.md` execution flow is read
- **THEN** it SHALL contain a PRE_HOOK step referencing `kflow-shared/phase-hooks.md` design PRE_HOOK
- **THEN** it SHALL contain a POST_HOOK step referencing `kflow-shared/phase-hooks.md` design POST_HOOK
