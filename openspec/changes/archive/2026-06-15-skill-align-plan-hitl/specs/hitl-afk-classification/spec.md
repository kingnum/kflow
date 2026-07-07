## MODIFIED Requirements

### Requirement: Plan phase annotates HITL decision points
`kflow-plan` SKILL.md SHALL include HITL decision point annotation rules: format (`[HITL D{n}]`), decision point checklist template, identification rules, and frontend subchange dependency annotation format.

#### Scenario: SKILL.md contains HITL annotation section
- **WHEN** `.claude/skills/kflow-plan/SKILL.md` is read
- **THEN** it SHALL contain a section defining HITL decision point annotation format and checklist template
