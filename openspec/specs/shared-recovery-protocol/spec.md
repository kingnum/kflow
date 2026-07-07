## ADDED Requirements

### Requirement: Shared recovery protocol definition file
The system SHALL provide `.claude/skills/kflow-shared/recovery-protocol.md` as the single source of truth for the checkpoint storage structure, 5-level recovery priority chain, and dispatch mapping table.

#### Scenario: New file creation
- **WHEN** the change is applied
- **THEN** `kflow-shared/recovery-protocol.md` SHALL exist containing: checkpoint file format, two-level storage (change-level + subchange-level), 5-level priority chain, checkpoint creation timing, expiry cleanup rules, kflow-resume workflow, dispatch mapping table (currently in `06-recovery.md` §12.2-12.3)

#### Scenario: Resume skill references shared file
- **WHEN** kflow-resume design doc describes recovery flow
- **THEN** it SHALL reference `kflow-shared/recovery-protocol.md` rather than inlining the full workflow

### Requirement: Core mechanism doc recovery section replaced
`06-recovery.md` §12.2-12.3 SHALL be replaced with a reference to `kflow-shared/recovery-protocol.md`.

#### Scenario: No duplicate recovery content
- **WHEN** `06-recovery.md` is read
- **THEN** it SHALL NOT contain the full priority chain or resume workflow — these SHALL only exist in `kflow-shared/recovery-protocol.md`
