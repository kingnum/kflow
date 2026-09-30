# Spec Delta

## MODIFIED Requirements

### Requirement: Checkpoint storage and recovery protocol single source

The core definition of checkpoint storage and recovery priority chain SHALL reside in `skills/kflow-resume/references/recovery-protocol.md`. `06-recovery.md` §12.2-12.3 SHALL be replaced with references.

#### Scenario: Core mechanism doc recovery sections simplified

- **WHEN** `06-recovery.md` §12.2 is read after the change
- **THEN** it SHALL reference the per-skill recovery protocol file (`kflow-resume` 的 `references/recovery-protocol.md`) as the location of the full specification
- **THEN** the full priority chain and resume workflow SHALL NOT appear in `06-recovery.md`

#### Scenario: No reference to the removed centralized directory

- **WHEN** `06-recovery.md` is read
- **THEN** it SHALL NOT reference `.claude/skills/kflow-shared/recovery-protocol.md` or any other path under a `kflow-shared/` directory
- **AND** the referenced path SHALL resolve to an existing file in the repository
