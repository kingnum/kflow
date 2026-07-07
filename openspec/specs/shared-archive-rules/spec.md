## ADDED Requirements

### Requirement: Shared archive rules definition file
The system SHALL provide `.claude/skills/kflow-shared/archive-rules.md` as the single source of truth for archive preconditions, design merge workflow, and post-archive prohibitions.

#### Scenario: New file creation
- **WHEN** the change is applied
- **THEN** `kflow-shared/archive-rules.md` SHALL exist containing: archive checklist, design merge 7-step workflow, conflict handling rules, post-archive prohibitions, archive-after-forbidden-auto-flow rule (currently in `04-gates-and-transitions.md` §6.3-6.3.1, §6.4, §6.7)

#### Scenario: Archive skill references shared file
- **WHEN** kflow-archive design doc describes archive conditions
- **THEN** it SHALL reference `kflow-shared/archive-rules.md` rather than inlining the full conditions

### Requirement: Core mechanism doc archive sections replaced
`04-gates-and-transitions.md` §6.3, §6.3.1, §6.4, §6.7 SHALL be replaced with references to `kflow-shared/archive-rules.md`.

#### Scenario: No duplicate archive content
- **WHEN** `04-gates-and-transitions.md` is read
- **THEN** it SHALL NOT contain the full archive checklist or design merge workflow — these SHALL only exist in `kflow-shared/archive-rules.md`
