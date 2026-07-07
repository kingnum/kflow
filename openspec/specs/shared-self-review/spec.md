## ADDED Requirements

### Requirement: Shared self-review definition file
The system SHALL provide `.claude/skills/kflow-shared/self-review.md` as the single source of truth for 10-round self-review specifications, including workflow, phase-specific dimension tables, record storage structure, and report format.

#### Scenario: New file creation
- **WHEN** the change is applied
- **THEN** `kflow-shared/self-review.md` SHALL exist containing all content from `07-agent-model.md` §16 (workflow, 3-phase dimension tables, storage structure, report format, VERIFY subagent verification)

#### Scenario: Self-review references shared file
- **WHEN** explore/design/prototype Skill design docs describe self-review
- **THEN** they SHALL reference `kflow-shared/self-review.md` and only include phase-specific dimension tables

### Requirement: Core mechanism doc self-review section replaced
`07-agent-model.md` §16 SHALL retain only a brief overview and reference to `kflow-shared/self-review.md`.

#### Scenario: No duplicate self-review content
- **WHEN** `07-agent-model.md` is read
- **THEN** §16 SHALL NOT contain the full workflow diagram, storage structure, or report format — these SHALL only exist in `kflow-shared/self-review.md`
