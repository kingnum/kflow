## MODIFIED Requirements

### Requirement: Checkpoint storage and recovery protocol single source
The core definition of checkpoint storage and recovery priority chain SHALL reside in `kflow-shared/recovery-protocol.md`. `06-recovery.md` §12.2-12.3 SHALL be replaced with references.

#### Scenario: Core mechanism doc recovery sections simplified
- **WHEN** `06-recovery.md` §12.2 is read after the change
- **THEN** it SHALL contain a reference `> 完整规范参见 kflow-shared/recovery-protocol.md`
- **THEN** the full priority chain and resume workflow SHALL NOT appear in `06-recovery.md`
